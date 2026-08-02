from __future__ import annotations

import hashlib
import json
import os
import threading
from collections.abc import Iterable
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from .domain import SCHEMA_VERSION, Actor, EpistemicDeltaType, EventRecord, utc_now

_LOCKS_GUARD = threading.Lock()
_LOCKS: dict[str, threading.Lock] = {}


def _lock_for(path: Path) -> threading.Lock:
    key = str(path.resolve())
    with _LOCKS_GUARD:
        return _LOCKS.setdefault(key, threading.Lock())


def canonical_json(value: dict[str, Any]) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")


def event_digest(event_without_hash: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(event_without_hash)).hexdigest()


class EventStore:
    """Append-only JSONL event store with a simple SHA-256 hash chain."""

    def __init__(self, events_path: Path) -> None:
        self.events_path = events_path
        self.events_path.parent.mkdir(parents=True, exist_ok=True)
        self.events_path.touch(exist_ok=True)

    def read_all(self) -> list[EventRecord]:
        records: list[EventRecord] = []
        with self.events_path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    records.append(EventRecord.model_validate_json(stripped))
                except Exception as exc:  # pragma: no cover - defensive context
                    raise ValueError(f"invalid event JSON at line {line_number}: {exc}") from exc
        return records

    def iter_raw(self) -> Iterable[dict[str, Any]]:
        with self.events_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    yield json.loads(line)

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
        lock = _lock_for(self.events_path)
        with lock:
            valid, index, error = self.verify_chain()
            if not valid:
                detail = error or "unknown event-chain error"
                raise ValueError(
                    "event store is read-only until recovery: "
                    f"invalid event at index {index}: {detail}"
                )
            previous_hash = self._last_hash_unlocked()
            event_without_hash: dict[str, Any] = {
                "schema_version": SCHEMA_VERSION,
                "event_id": str(uuid4()),
                "event_type": event_type.strip().upper().replace(" ", "_"),
                "project_id": str(project_id),
                "timestamp": utc_now().isoformat(),
                "actor": actor.model_dump(mode="json"),
                "caused_by": caused_by or [],
                "route_id": str(route_id) if route_id else None,
                "branch_id": str(branch_id) if branch_id else None,
                "artifact_refs": artifact_refs or [],
                "payload": payload or {},
                "epistemic_delta": epistemic_delta,
                "epistemic_delta_type": (
                    epistemic_delta_type.value if epistemic_delta_type else None
                ),
                "previous_event_hash": previous_hash,
            }
            event_hash = event_digest(event_without_hash)
            record_dict = {**event_without_hash, "event_hash": event_hash}
            record = EventRecord.model_validate(record_dict)

            with self.events_path.open("a", encoding="utf-8") as handle:
                handle.write(
                    json.dumps(
                        record_dict, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                    )
                    + "\n"
                )
                handle.flush()
                os.fsync(handle.fileno())
            return record

    def _last_hash_unlocked(self) -> str | None:
        last: dict[str, Any] | None = None
        for raw in self.iter_raw():
            last = raw
        return None if last is None else str(last.get("event_hash"))

    def verify_chain(self) -> tuple[bool, int | None, str | None]:
        expected_previous: str | None = None
        with self.events_path.open("r", encoding="utf-8") as handle:
            lines = list(handle)
        for index, line in enumerate(lines):
            if not line.strip():
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                return False, index, f"invalid JSON: {exc.msg}"
            actual_previous = raw.get("previous_event_hash")
            if actual_previous != expected_previous:
                return (
                    False,
                    index,
                    f"previous hash mismatch: expected {expected_previous}, got {actual_previous}",
                )
            actual_hash = raw.get("event_hash")
            without_hash = dict(raw)
            without_hash.pop("event_hash", None)
            expected_hash = event_digest(without_hash)
            if actual_hash != expected_hash:
                return (
                    False,
                    index,
                    f"event hash mismatch: expected {expected_hash}, got {actual_hash}",
                )
            expected_previous = str(actual_hash)
        return True, None, None
