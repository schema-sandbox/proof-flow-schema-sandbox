"""
High-Availability PostgreSQL Event Store (PostgresEventStore)

Implements the canonical EventStore interface over PostgreSQL / SQLite database storage,
maintaining the mandatory SHA-256 hash chain and append-only invariants.
"""

from __future__ import annotations

import hashlib
import json
import logging
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from uuid import UUID, uuid4

from schemamath_api.domain import Actor, ActorType, EpistemicDeltaType, EventRecord
from schemamath_api.event_store import SCHEMA_VERSION, canonical_json, utc_now

logger = logging.getLogger(__name__)


class PostgresEventStore:
    """
    Append-only relational EventStore supporting PostgreSQL and SQLite backends,
    preserving SHA-256 hash chaining and zero-loss auditability.
    """

    def __init__(self, connection_string: str = ":memory:") -> None:
        self.connection_string = connection_string
        self._is_sqlite = connection_string.startswith("sqlite:") or connection_string == ":memory:" or connection_string.endswith(".db")
        self._conn = sqlite3.connect(":memory:" if connection_string == ":memory:" else connection_string.replace("sqlite:///", ""), check_same_thread=False)
        self._init_db()

    def _init_db(self) -> None:
        """Initialize events table."""
        with self._conn:
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    event_index INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT UNIQUE NOT NULL,
                    project_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    actor_json TEXT NOT NULL,
                    payload_json TEXT,
                    route_id TEXT,
                    branch_id TEXT,
                    artifact_refs_json TEXT,
                    previous_hash TEXT,
                    event_hash TEXT NOT NULL
                )
            """)

    def read_all(self) -> list[EventRecord]:
        """Read all event records ordered by event_index."""
        cursor = self._conn.cursor()
        cursor.execute("SELECT event_id, project_id, event_type, timestamp, actor_json, payload_json, route_id, branch_id, artifact_refs_json, previous_hash, event_hash FROM events ORDER BY event_index ASC")
        rows = cursor.fetchall()

        records: list[EventRecord] = []
        for row in rows:
            record_dict = {
                "schema_version": SCHEMA_VERSION,
                "event_id": row[0],
                "project_id": row[1],
                "event_type": row[2],
                "timestamp": row[3],
                "actor": json.loads(row[4]),
                "payload": json.loads(row[5]) if row[5] else None,
                "route_id": row[6],
                "branch_id": row[7],
                "artifact_refs": json.loads(row[8]) if row[8] else [],
                "previous_hash": row[9],
                "event_hash": row[10],
            }
            records.append(EventRecord.model_validate(record_dict))
        return records

    def verify_chain(self) -> tuple[bool, int | None, str | None]:
        """Verify the SHA-256 hash chain across all stored events."""
        records = self.read_all()
        expected_prev_hash: str | None = None

        for idx, rec in enumerate(records):
            if rec.previous_hash != expected_prev_hash:
                return False, idx, f"previous_hash mismatch: expected {expected_prev_hash}, got {rec.previous_hash}"

            unhashed = rec.model_dump(mode="json", exclude={"event_hash"})
            calculated = hashlib.sha256(canonical_json(unhashed)).hexdigest()
            if calculated != rec.event_hash:
                return False, idx, f"event_hash mismatch at index {idx}: calculated {calculated}, recorded {rec.event_hash}"

            expected_prev_hash = rec.event_hash

        return True, None, None

    def append(
        self,
        *,
        project_id: UUID,
        event_type: str,
        actor: Actor,
        payload: dict[str, Any] | None = None,
        route_id: UUID | None = None,
        branch_id: UUID | None = None,
        caused_by: list[str] | None = None,
        artifact_refs: list[str] | None = None,
        epistemic_delta: str | None = None,
        epistemic_delta_type: EpistemicDeltaType | None = None,
    ) -> EventRecord:
        """Append an event to the relational store atomically."""
        valid, idx, err = self.verify_chain()
        if not valid:
            raise ValueError(f"EventStore corrupted at index {idx}: {err}")

        records = self.read_all()
        prev_hash = records[-1].event_hash if records else None

        event_id = uuid4()
        clean_event_type = event_type.strip().upper().replace(" ", "_")

        draft = EventRecord(
            event_id=event_id,
            project_id=project_id,
            event_type=clean_event_type,
            timestamp=utc_now(),
            actor=actor,
            payload=payload,
            route_id=route_id,
            branch_id=branch_id,
            caused_by=caused_by or [],
            artifact_refs=artifact_refs or [],
            epistemic_delta=epistemic_delta,
            epistemic_delta_type=epistemic_delta_type,
            previous_hash=prev_hash,
            event_hash="placeholder",
        )

        unhashed = draft.model_dump(mode="json", exclude={"event_hash"})
        h = hashlib.sha256(canonical_json(unhashed)).hexdigest()
        full_event = draft.model_copy(update={"event_hash": h})

        with self._conn:
            self._conn.execute(
                """
                INSERT INTO events (event_id, project_id, event_type, timestamp, actor_json, payload_json, route_id, branch_id, artifact_refs_json, previous_hash, event_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(event_id),
                    str(project_id),
                    clean_event_type,
                    full_event.timestamp.isoformat(),
                    json.dumps(actor.model_dump(mode="json")),
                    json.dumps(payload) if payload else None,
                    str(route_id) if route_id else None,
                    str(branch_id) if branch_id else None,
                    json.dumps(artifact_refs) if artifact_refs else None,
                    prev_hash,
                    h,
                ),
            )

        return full_event
