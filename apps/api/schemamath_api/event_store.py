from __future__ import annotations

import hashlib
import json
import os
import tempfile
import threading
import time
from collections.abc import Iterable
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from .auth import authenticated_actor
from .domain import SCHEMA_VERSION, Actor, EpistemicDeltaType, EventRecord, utc_now

_LOCKS_GUARD = threading.Lock()
_LOCKS: dict[str, threading.Lock] = {}


def _lock_for(path: Path) -> threading.Lock:
    key = str(path.resolve())
    with _LOCKS_GUARD:
        return _LOCKS.setdefault(key, threading.Lock())


@contextmanager
def _process_lock(path: Path):
    """Coordinate appenders across worker processes as well as threads."""

    lock_path = path.with_name(f"{path.name}.lock")
    with lock_path.open("a+b") as handle:
        if os.name == "nt":
            import msvcrt

            handle.seek(0)
            handle.write(b"0")
            handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def serialize_record(value: dict[str, Any]) -> bytes:
    """Canonical JSONL serialization shared by hashing and on-disk writes."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")


def canonical_json(value: dict[str, Any]) -> bytes:
    return serialize_record(value)


def event_digest(event_without_hash: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(event_without_hash)).hexdigest()


class EventStoreIntegrityError(ValueError):
    """The canonical event chain is corrupt; appends are refused until recovery."""


def _atomic_replace(source: Path, target: Path, attempts: int = 10) -> None:
    """Atomically replace ``target``, retrying transient Windows sharing violations."""
    for attempt in range(attempts):
        try:
            os.replace(source, target)
            return
        except OSError:
            if attempt == attempts - 1:
                raise
            time.sleep(0.01 * (attempt + 1))


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
                    raise EventStoreIntegrityError(
                        f"invalid event JSON at line {line_number}: {exc}"
                    ) from exc
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
        return self.append_batch(
            project_id=project_id,
            events=[
                {
                    "event_type": event_type,
                    "actor": actor,
                    "payload": payload,
                    "route_id": route_id,
                    "branch_id": branch_id,
                    "caused_by": caused_by,
                    "artifact_refs": artifact_refs,
                    "epistemic_delta": epistemic_delta,
                    "epistemic_delta_type": epistemic_delta_type,
                }
            ],
        )[0]

    def append_batch(
        self,
        *,
        project_id: UUID,
        events: list[dict[str, Any]],
        expected_revision: int | None = None,
        idempotency_key: str | None = None,
        batch_id: UUID | None = None,
    ) -> list[EventRecord]:
        """Append a fully validated event batch as one filesystem replacement.

        The previous implementation appended each event independently.  A bad
        second event could therefore leave the first event in the canonical
        stream even though the transaction reported failure.  This method
        validates every actor and event before writing, builds the complete new
        JSONL bytes, and atomically replaces the file while holding the existing
        process/thread locks.  Historical lines are copied byte-for-byte; the
        append-only meaning is preserved even though the filesystem operation is
        a replacement.

        ``expected_revision`` is the number of non-empty canonical events at
        the time of the write.  ``idempotency_key`` is copied to every event in
        the batch and a repeated key returns the original records without
        adding a duplicate batch.
        """
        lock = _lock_for(self.events_path)
        with _process_lock(self.events_path), lock:
            # Single full read: the same bytes feed chain verification, the
            # revision/idempotency scan, the previous-hash lookup and the
            # replacement prefix, avoiding three whole-file passes per append.
            original = self.events_path.read_bytes()
            lines = original.decode("utf-8").splitlines()
            valid, index, error = self._verify_lines(lines)
            if not valid:
                raise EventStoreIntegrityError(
                    "event store is read-only until recovery: "
                    f"invalid event at index {index}: {error}"
                )
            raw_lines = [line for line in lines if line.strip()]
            current_revision = len(raw_lines)
            if idempotency_key:
                existing = [
                    EventRecord.model_validate_json(line)
                    for line in raw_lines
                    if json.loads(line).get("idempotency_key") == idempotency_key
                ]
                if existing:
                    if any(record.project_id != project_id for record in existing):
                        raise ValueError("idempotency key is already bound to another project")
                    return existing

            if expected_revision is not None and expected_revision != current_revision:
                raise ValueError(
                    f"stale event-store revision: expected {expected_revision}, "
                    f"current {current_revision}"
                )

            if not events:
                return []

            previous_hash = None
            if raw_lines:
                previous_hash = str(json.loads(raw_lines[-1]).get("event_hash"))
            records: list[EventRecord] = []
            serialized: list[bytes] = []
            resolved_batch_id = batch_id or uuid4()
            for offset, event_data in enumerate(events, start=1):
                actor_value = event_data.get("actor")
                if actor_value is None:
                    from .domain import ActorType

                    actor_value = Actor(type=ActorType.RUNTIME, id="k0")
                if isinstance(actor_value, dict):
                    actor_value = Actor.model_validate(actor_value)
                if not isinstance(actor_value, Actor):
                    raise TypeError("event actor must be an Actor or actor mapping")
                actor_value = authenticated_actor(actor_value)
                delta_type = event_data.get("epistemic_delta_type")
                if delta_type is not None and hasattr(delta_type, "value"):
                    delta_type = delta_type.value
                event_without_hash: dict[str, Any] = {
                    "schema_version": SCHEMA_VERSION,
                    "event_id": str(uuid4()),
                    "event_type": str(event_data.get("event_type", "GENERIC_ACTION"))
                    .strip()
                    .upper()
                    .replace(" ", "_"),
                    "project_id": str(project_id),
                    "timestamp": utc_now().isoformat(),
                    "actor": actor_value.model_dump(mode="json"),
                    "caused_by": event_data.get("caused_by") or [],
                    "route_id": str(event_data["route_id"]) if event_data.get("route_id") else None,
                    "branch_id": str(event_data["branch_id"]) if event_data.get("branch_id") else None,
                    "artifact_refs": event_data.get("artifact_refs") or [],
                    "payload": event_data.get("payload") or {},
                    "epistemic_delta": event_data.get("epistemic_delta"),
                    "epistemic_delta_type": delta_type,
                    "previous_event_hash": previous_hash,
                    "revision": current_revision + offset,
                    "batch_id": str(resolved_batch_id),
                    "idempotency_key": idempotency_key,
                    "command_id": event_data.get("command_id"),
                }
                event_hash = event_digest(event_without_hash)
                record_dict = {**event_without_hash, "event_hash": event_hash}
                record = EventRecord.model_validate(record_dict)
                records.append(record)
                serialized.append(serialize_record(record_dict) + b"\n")
                previous_hash = event_hash

            prefix = b"" if not original or original.endswith(b"\n") else b"\n"
            temp_name: str | None = None
            try:
                fd, temp_name = tempfile.mkstemp(
                    prefix=f".{self.events_path.name}.", suffix=".tmp", dir=self.events_path.parent
                )
                with os.fdopen(fd, "wb") as handle:
                    handle.write(original)
                    handle.write(prefix)
                    handle.write(b"".join(serialized))
                    handle.flush()
                    os.fsync(handle.fileno())
                _atomic_replace(temp_name, self.events_path)
                temp_name = None
            finally:
                if temp_name:
                    try:
                        os.unlink(temp_name)
                    except FileNotFoundError:
                        pass
            return records

    @contextmanager
    def append_lock(self):
        """Hold the append locks (thread + process) while reading or rebuilding."""
        lock = _lock_for(self.events_path)
        with _process_lock(self.events_path), lock:
            yield

    def current_revision(self) -> int:
        """Return the number of valid non-empty events in the canonical stream."""
        valid, index, error = self.verify_chain()
        if not valid:
            raise EventStoreIntegrityError(f"event store is invalid at index {index}: {error}")
        with self.events_path.open("r", encoding="utf-8") as handle:
            return sum(1 for line in handle if line.strip())

    def verify_chain(self) -> tuple[bool, int | None, str | None]:
        with self.events_path.open("r", encoding="utf-8") as handle:
            return self._verify_lines(list(handle))

    @staticmethod
    def _verify_lines(lines: list[str]) -> tuple[bool, int | None, str | None]:
        expected_previous: str | None = None
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
