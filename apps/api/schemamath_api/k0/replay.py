"""
K0 Trust Kernel — Event Replay Engine

The ReplayEngine is responsible for replaying the canonical SHA-256 chained
JSONL event stream to rebuild SQLite projections or custom module state graphs.

Core Principles:
    1. Single Source of Truth: The event log is the sole canonical truth; all module
       state graphs are rebuildable CQRS projections.
    2. Monotonic & Deterministic: Replaying the same event log from the same offset
       always yields the exact same state graph.
    3. Event Chain Integrity: Before replaying, the engine verifies the SHA-256
       hash chain. If corrupted, it refuses to replay past the broken link.
    4. Flexible Projection Registration: Custom projection handlers can be registered
       to build specialized views (e.g., SQLite DB, graph analytics, audit logs).
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

from schemamath_api.domain import EventRecord
from schemamath_api.event_store import EventStore

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Protocols & Types
# ---------------------------------------------------------------------------

class ProjectionHandler(Protocol):
    """Protocol for projection handlers registered with the ReplayEngine."""

    def __call__(self, event: EventRecord, index: int) -> None: ...


ProgressCallback = Callable[[int, int], None]  # (current_index, total_events)


@dataclass(frozen=True)
class ReplayResult:
    """Outcome of a replay run."""

    success: bool
    events_processed: int
    start_offset: int
    end_offset: int
    chain_valid: bool
    duration_ms: float
    error: str | None = None


# ---------------------------------------------------------------------------
# Replay Engine
# ---------------------------------------------------------------------------

class ReplayEngine:
    """
    Engine for replaying event logs to rebuild projections.
    """

    def __init__(self, event_store: EventStore | None = None) -> None:
        self._event_store = event_store
        self._handlers: list[ProjectionHandler] = []

    def set_event_store(self, event_store: EventStore) -> None:
        """Set or update the active EventStore."""
        self._event_store = event_store

    def register_handler(self, handler: ProjectionHandler) -> None:
        """Register a projection handler to receive events during replay."""
        self._handlers.append(handler)

    def replay(
        self,
        event_store: EventStore | None = None,
        from_offset: int = 0,
        limit: int | None = None,
        progress_callback: ProgressCallback | None = None,
        verify_chain_first: bool = True,
    ) -> ReplayResult:
        """
        Replay events starting from `from_offset`.

        Args:
            event_store: EventStore instance (uses self._event_store if None).
            from_offset: Index of first event to replay (0-based).
            limit: Maximum number of events to replay (None for all).
            progress_callback: Optional callback receiving (current_idx, total_events).
            verify_chain_first: Whether to verify SHA-256 event chain before replaying.

        Returns:
            ReplayResult containing statistics and outcome.
        """
        store = event_store or self._event_store
        if not store:
            raise ValueError("No EventStore provided to ReplayEngine")

        start_time = time.perf_counter()

        # Phase 1: Chain Integrity Check
        chain_valid = True
        if verify_chain_first:
            valid, bad_idx, err_msg = store.verify_chain()
            if not valid:
                chain_valid = False
                logger.error("Event chain integrity check failed at index %s: %s", bad_idx, err_msg)
                elapsed = (time.perf_counter() - start_time) * 1000
                return ReplayResult(
                    success=False,
                    events_processed=0,
                    start_offset=from_offset,
                    end_offset=from_offset,
                    chain_valid=False,
                    duration_ms=elapsed,
                    error=f"Corrupted SHA-256 event chain at index {bad_idx}: {err_msg}",
                )

        # Phase 2: Read Events
        all_events = store.read_all()
        total_count = len(all_events)

        if from_offset < 0 or from_offset > total_count:
            elapsed = (time.perf_counter() - start_time) * 1000
            return ReplayResult(
                success=False,
                events_processed=0,
                start_offset=from_offset,
                end_offset=from_offset,
                chain_valid=chain_valid,
                duration_ms=elapsed,
                error=f"Invalid offset {from_offset} (total events: {total_count})",
            )

        events_to_replay = all_events[from_offset:]
        if limit is not None and limit > 0:
            events_to_replay = events_to_replay[:limit]

        processed_count = 0
        current_idx = from_offset

        try:
            for event in events_to_replay:
                for handler in self._handlers:
                    handler(event, current_idx)

                processed_count += 1
                current_idx += 1

                if progress_callback:
                    progress_callback(current_idx, total_count)

            elapsed = (time.perf_counter() - start_time) * 1000
            return ReplayResult(
                success=True,
                events_processed=processed_count,
                start_offset=from_offset,
                end_offset=current_idx,
                chain_valid=chain_valid,
                duration_ms=elapsed,
            )

        except Exception as exc:
            logger.error("Error during event replay at index %d: %s", current_idx, exc)
            elapsed = (time.perf_counter() - start_time) * 1000
            return ReplayResult(
                success=False,
                events_processed=processed_count,
                start_offset=from_offset,
                end_offset=current_idx,
                chain_valid=chain_valid,
                duration_ms=elapsed,
                error=f"Replay failed at event index {current_idx}: {exc}",
            )
