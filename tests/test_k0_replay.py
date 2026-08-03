"""
Tests for K0 Trust Kernel — Replay Engine

Covers:
    - Offset-based replay of event logs
    - Projection handler dispatching
    - Chain integrity check refusal on corrupt chain
    - Limit and offset bounds checks
    - Progress callback notification
"""

from __future__ import annotations

from uuid import uuid4

import pytest
from schemamath_api.domain import Actor, ActorType, EventRecord
from schemamath_api.event_store import EventStore
from schemamath_api.k0.replay import ReplayEngine


@pytest.fixture
def temp_event_store(tmp_path):
    events_file = tmp_path / "events.jsonl"
    store = EventStore(events_file)
    project_id = uuid4()

    # Append 5 events
    for i in range(5):
        store.append(
            project_id=project_id,
            event_type=f"EVENT_{i}",
            actor=Actor(type=ActorType.HUMAN, id="user1"),
            payload={"index": i},
        )

    return store, events_file


class TestReplayEngine:
    def test_full_replay(self, temp_event_store):
        store, _ = temp_event_store
        engine = ReplayEngine(store)

        replayed_events: list[EventRecord] = []

        def handler(event: EventRecord, idx: int):
            replayed_events.append(event)

        engine.register_handler(handler)
        res = engine.replay()

        assert res.success is True
        assert res.events_processed == 5
        assert res.start_offset == 0
        assert res.end_offset == 5
        assert len(replayed_events) == 5
        assert replayed_events[0].event_type == "EVENT_0"
        assert replayed_events[4].event_type == "EVENT_4"

    def test_offset_and_limit_replay(self, temp_event_store):
        store, _ = temp_event_store
        engine = ReplayEngine(store)

        replayed_events: list[EventRecord] = []

        def handler(event: EventRecord, idx: int):
            replayed_events.append(event)

        engine.register_handler(handler)
        res = engine.replay(from_offset=2, limit=2)

        assert res.success is True
        assert res.events_processed == 2
        assert res.start_offset == 2
        assert res.end_offset == 4
        assert len(replayed_events) == 2
        assert replayed_events[0].event_type == "EVENT_2"
        assert replayed_events[1].event_type == "EVENT_3"

    def test_progress_callback(self, temp_event_store):
        store, _ = temp_event_store
        engine = ReplayEngine(store)

        progress_calls: list[tuple[int, int]] = []

        def cb(curr: int, total: int):
            progress_calls.append((curr, total))

        res = engine.replay(progress_callback=cb)

        assert res.success is True
        assert len(progress_calls) == 5
        assert progress_calls[-1] == (5, 5)

    def test_corrupt_chain_rejection(self, temp_event_store):
        store, events_file = temp_event_store

        # Tamper with file
        lines = events_file.read_text(encoding="utf-8").splitlines()
        lines[2] = lines[2].replace("EVENT_2", "TAMPERED_EVENT")
        events_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

        engine = ReplayEngine(store)
        res = engine.replay(verify_chain_first=True)

        assert res.success is False
        assert res.chain_valid is False
        assert "Corrupted SHA-256 event chain" in res.error
