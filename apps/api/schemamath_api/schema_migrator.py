"""
Schema Migrator — v0.1 through v0.6 (Alpha.5)

Provides automatic migration of event records and domain objects from schema
version 0.1 through 0.6, with backward-compatible reading of older formats.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .event_store import event_digest, serialize_record

logger = logging.getLogger(__name__)

MIGRATION_PAIRS: list[tuple[str, str]] = [
    ("0.1", "0.2"),
    ("0.2", "0.3"),
    ("0.3", "0.4"),
    ("0.4", "0.5"),
    ("0.5", "0.6"),
]

V05_NEW_FIELDS: dict[str, Any] = {
    "trace_class": "FINAL_ONLY_ARTIFACT",
    "artifact_correlations": [],
    "cost_boundary": None,
}

V06_NEW_FIELDS: dict[str, Any] = {
    "revision": None,
    "batch_id": None,
    "idempotency_key": None,
    "command_id": None,
}


@dataclass
class MigrationResult:
    source_version: str
    target_version: str
    records_migrated: int
    records_skipped: int
    errors: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return len(self.errors) == 0


class SchemaMigrator:
    """Migrates event records across schema versions."""

    def migrate_record(self, record: dict[str, Any], target_version: str = "0.5") -> dict[str, Any]:
        """Migrate a single record dict to the target schema version."""
        current = record.get("schema_version", "0.1")
        if current == target_version:
            return record

        migrated = dict(record)
        version_chain = self._build_chain(current, target_version)

        for from_v, to_v in version_chain:
            migrated = self._apply_step(migrated, from_v, to_v)

        return migrated

    def migrate_records(
        self, records: list[dict[str, Any]], target_version: str = "0.5"
    ) -> MigrationResult:
        """Migrate a batch of records, collecting errors."""
        migrated_count = 0
        skipped_count = 0
        errors: list[str] = []

        for i, rec in enumerate(records):
            current = rec.get("schema_version", "0.1")
            if current == target_version:
                skipped_count += 1
                continue
            try:
                records[i] = self.migrate_record(rec, target_version)
                migrated_count += 1
            except ValueError as exc:
                errors.append(f"record {i}: {exc}")

        source_versions = {r.get("schema_version", "0.1") for r in records}
        source_v = min(source_versions) if source_versions else "0.1"

        return MigrationResult(
            source_version=source_v,
            target_version=target_version,
            records_migrated=migrated_count,
            records_skipped=skipped_count,
            errors=errors,
        )

    def migrate_jsonl_file(
        self, source_path: Path, target_path: Path | None = None, target_version: str = "0.5"
    ) -> MigrationResult:
        """Migrate an entire JSONL event file in place or to a new path."""
        if target_path is None:
            target_path = source_path

        records: list[dict[str, Any]] = []
        with source_path.open("r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    records.append(json.loads(stripped))

        result = self.migrate_records(records, target_version)

        if result.success:
            # Rebuild the SHA-256 chain so the migrated file passes
            # EventStore.verify_chain (field additions invalidate old hashes).
            previous: str | None = None
            for rec in records:
                without_hash = dict(rec)
                without_hash.pop("event_hash", None)
                rec["previous_event_hash"] = previous
                rec["event_hash"] = event_digest(without_hash)
                previous = rec["event_hash"]
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with target_path.open("wb") as f:
                for rec in records:
                    f.write(serialize_record(rec) + b"\n")
            logger.info(
                "Migrated %d records from %s to %s (skipped %d)",
                result.records_migrated,
                result.source_version,
                result.target_version,
                result.records_skipped,
            )

        return result

    def _build_chain(self, from_v: str, to_v: str) -> list[tuple[str, str]]:
        """Build the migration chain between two versions."""
        chain: list[tuple[str, str]] = []
        current = from_v
        for src, dst in MIGRATION_PAIRS:
            if src == current:
                chain.append((src, dst))
                current = dst
                if current == to_v:
                    return chain
        if current != to_v:
            raise ValueError(f"No migration path from {from_v} to {to_v}")
        return chain

    def _apply_step(self, record: dict[str, Any], from_v: str, to_v: str) -> dict[str, Any]:
        """Apply a single migration step."""
        migrated = dict(record)
        migrated["schema_version"] = to_v

        if from_v == "0.4" and to_v == "0.5":
            for key, default in V05_NEW_FIELDS.items():
                if key not in migrated:
                    payload = migrated.get("payload", {})
                    if isinstance(payload, dict) and key not in payload:
                        payload[key] = default
                        migrated["payload"] = payload

        if from_v == "0.5" and to_v == "0.6":
            for key, default in V06_NEW_FIELDS.items():
                migrated.setdefault(key, default)
            # Adding the control-plane fields changes the record content, so any
            # existing event_hash must be recomputed over the new bytes to stay
            # consistent with EventStore.verify_chain.
            if "event_hash" in migrated:
                without_hash = dict(migrated)
                without_hash.pop("event_hash", None)
                migrated["event_hash"] = event_digest(without_hash)

        return migrated
