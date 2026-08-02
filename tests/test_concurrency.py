from __future__ import annotations

import threading
from uuid import UUID

from schemamath_api.domain import Actor, ActorType
from schemamath_api.event_store import EventStore


def test_concurrent_appends_preserve_hash_chain(tmp_path) -> None:
    store = EventStore(tmp_path / "events.jsonl")
    actor = Actor(type=ActorType.HUMAN, id="tester")
    barrier = threading.Barrier(8)

    def worker(worker_id: int) -> None:
        barrier.wait()
        for seq in range(25):
            store.append(
                project_id=UUID(int=1),
                event_type="CONCURRENT_TEST",
                actor=actor,
                payload={"worker": worker_id, "seq": seq},
            )

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    records = store.read_all()
    assert len(records) == 200
    event_ids = {record.event_id for record in records}
    assert len(event_ids) == 200
    valid, index, detail = store.verify_chain()
    assert valid is True, detail
    assert index is None


def test_service_concurrent_route_creates_are_consistent(service) -> None:
    from schemamath_api.domain import (
        ProblemContract,
        ProjectCreate,
        RouteCreate,
        RouteState,
    )

    project = service.create_project(
        ProjectCreate(
            title="concurrency",
            description="concurrency test",
            problem=ProblemContract(
                source_text="Concurrent writes must not corrupt the chain.",
                author_notes="No solution is required.",
            ),
        )
    )
    actor = Actor(type=ActorType.HUMAN, id="tester")
    barrier = threading.Barrier(8)

    def worker(worker_id: int) -> None:
        barrier.wait()
        for seq in range(10):
            service.create_route(
                project.project_id,
                RouteCreate(
                    title=f"route-{worker_id}-{seq}",
                    initial_state=RouteState.ACTIVE,
                    actor=actor,
                ),
            )

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    routes = service.list_routes(project.project_id)
    assert len(routes) == 80
    assert service.integrity_report(project.project_id).valid is True
