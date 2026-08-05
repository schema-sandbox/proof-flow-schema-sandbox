from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient
from schemamath_api.main import create_app


def test_api_vertical_slice(tmp_path: Path) -> None:
    app = create_app(tmp_path / "workspaces", tmp_path / "plugins")
    client = TestClient(app)

    response = client.post(
        "/api/v1/projects",
        json={
            "title": "API project",
            "description": "test",
            "problem": {
                "source_text": "Investigate a statement without forcing closure.",
                "author_notes": "",
                "definitions": [],
                "assumptions": [],
            },
            "actor": {"type": "human", "id": "tester"},
        },
    )
    assert response.status_code == 201, response.text
    project_id = response.json()["project_id"]

    response = client.post(
        f"/api/v1/projects/{project_id}/routes",
        json={
            "title": "Search route",
            "description": "Look for small counterexamples.",
            "initial_state": "ACTIVE",
            "revival_conditions": [],
            "actor": {"type": "human", "id": "tester"},
        },
    )
    assert response.status_code == 201, response.text
    route_id = response.json()["route_id"]

    response = client.post(
        f"/api/v1/projects/{project_id}/notes",
        json={
            "content": "Keep the route even if the first search fails.",
            "route_id": route_id,
            "note_type": "INTUITION",
            "actor": {"type": "human", "id": "tester"},
        },
    )
    assert response.status_code == 201, response.text

    response = client.post(
        f"/api/v1/projects/{project_id}/research-packets",
        json={"route_ids": [route_id], "include_recent_events": 20},
    )
    assert response.status_code == 200
    assert "Search route" in response.json()["markdown"]

    response = client.get(f"/api/v1/projects/{project_id}/integrity")
    assert response.status_code == 200
    assert response.json()["valid"] is True


def test_alpha5_research_state_transition_api(tmp_path: Path) -> None:
    app = create_app(tmp_path / "workspaces", tmp_path / "plugins")
    client = TestClient(app)
    project = client.post(
        "/api/v1/projects",
        json={
            "title": "Transition API project",
            "problem": {"source_text": "Track a proposed state change."},
            "actor": {"type": "human", "id": "tester"},
        },
    )
    assert project.status_code == 201, project.text
    project_id = project.json()["project_id"]

    proposal = client.post(
        f"/api/v1/projects/{project_id}/transition-proposals",
        json={
            "expected_revision": 1,
            "idempotency_key": "api-proposal-1",
            "trigger_class": "OBSERVATION",
            "trigger_evidence_refs": ["artifact:obs-1"],
            "accepted_delta": {"epistemic": {"support": "weak"}},
            "visibility": "DIRECT_OBSERVATION",
            "proposal_actor": {"type": "human", "id": "tester"},
        },
    )
    assert proposal.status_code == 201, proposal.text
    proposal_id = proposal.json()["proposal_id"]

    listed = client.get(f"/api/v1/projects/{project_id}/transition-proposals")
    assert listed.status_code == 200
    assert listed.json()[0]["status"] == "PROPOSED"

    accepted = client.post(
        f"/api/v1/projects/{project_id}/transition-proposals/{proposal_id}/accept",
        json={
            "expected_revision": 2,
            "idempotency_key": "api-accept-1",
            "acceptance_actor": {"type": "human", "id": "reviewer"},
            "acceptance_mechanism": "manual-review",
            "accepted": True,
        },
    )
    assert accepted.status_code == 201, accepted.text
    assert accepted.json()["accepted"] is True

    state = client.get(f"/api/v1/projects/{project_id}/research-state")
    assert state.status_code == 200
    assert state.json()["revision"] == 3
    assert state.json()["epistemic"]["support"] == "weak"


def test_alpha5_continuation_and_handoff_v2_api(tmp_path: Path) -> None:
    app = create_app(tmp_path / "workspaces", tmp_path / "plugins")
    client = TestClient(app)
    project = client.post(
        "/api/v1/projects",
        json={
            "title": "Typed handoff API project",
            "problem": {"source_text": "Keep a typed continuation receipt."},
            "actor": {"type": "human", "id": "tester"},
        },
    )
    assert project.status_code == 201, project.text
    project_id = project.json()["project_id"]

    continuation = client.post(
        f"/api/v1/projects/{project_id}/continuation-contracts",
        json={
            "expected_revision": 1,
            "idempotency_key": "api-continuation-1",
            "decision": "NO_CHANGE",
            "scope": "retain route",
            "actor": {"type": "human", "id": "tester"},
        },
    )
    assert continuation.status_code == 201, continuation.text

    packet = client.post(
        f"/api/v1/projects/{project_id}/handoffs-v2",
        json={
            "expected_revision": 2,
            "idempotency_key": "api-handoff-1",
            "scope": "route packet",
            "tool_hashes": ["sha256:tool"],
            "fact_evidence_refs": ["artifact:fact"],
            "failure_evidence_refs": ["artifact:failure"],
            "actor": {"type": "human", "id": "tester"},
        },
    )
    assert packet.status_code == 201, packet.text
    packet_id = packet.json()["packet_id"]

    receipt = client.post(
        f"/api/v1/projects/{project_id}/handoffs-v2/{packet_id}/accept",
        json={
            "expected_revision": 3,
            "idempotency_key": "api-handoff-receipt-1",
            "accepted": True,
            "acceptance_actor": {"type": "human", "id": "receiver"},
        },
    )
    assert receipt.status_code == 201, receipt.text
    assert receipt.json()["accepted"] is True


def test_alpha2_api_objects_chat_import_and_python_plugin(tmp_path: Path) -> None:
    app = create_app(tmp_path / "workspaces", tmp_path / "plugins")
    client = TestClient(app)
    project = client.post(
        "/api/v1/projects",
        json={
            "title": "Alpha.2 project",
            "problem": {"source_text": "Explore without forcing closure."},
            "actor": {"type": "human", "id": "tester"},
        },
    )
    assert project.status_code == 201, project.text
    project_id = project.json()["project_id"]
    route = client.post(
        f"/api/v1/projects/{project_id}/routes",
        json={
            "title": "Main route",
            "initial_state": "ACTIVE",
            "actor": {"type": "human", "id": "tester"},
        },
    )
    assert route.status_code == 201, route.text
    route_id = route.json()["route_id"]

    branch = client.post(
        f"/api/v1/projects/{project_id}/branches",
        json={
            "route_id": route_id,
            "title": "Concrete branch",
            "initial_state": "ACTIVE",
            "actor": {"type": "human", "id": "tester"},
        },
    )
    assert branch.status_code == 201, branch.text
    branch_id = branch.json()["branch_id"]

    challenge = client.post(
        f"/api/v1/projects/{project_id}/challenges",
        json={
            "route_id": route_id,
            "branch_id": branch_id,
            "challenge_type": "COUNTEREXAMPLE_SEARCH",
            "statement": "Search small cases.",
            "actor": {"type": "human", "id": "tester"},
        },
    )
    assert challenge.status_code == 201, challenge.text

    preview = client.post(
        f"/api/v1/projects/{project_id}/chat-imports/preview",
        files={"file": ("chat.md", b"# Assistant\nNew route: try parity.", "text/markdown")},
        data={"actor_id": "tester"},
    )
    assert preview.status_code == 201, preview.text
    preview_json = preview.json()
    candidate_id = preview_json["candidates"][0]["candidate_id"]
    import_id = preview_json["import_id"]
    confirmation = client.post(
        f"/api/v1/projects/{project_id}/chat-imports/{import_id}/confirm",
        json={
            "selections": [
                {
                    "candidate_id": candidate_id,
                    "disposition": "MODEL_NOTE",
                    "route_id": route_id,
                    "branch_id": branch_id,
                }
            ],
            "actor": {"type": "human", "id": "tester"},
        },
    )
    assert confirmation.status_code == 200, confirmation.text

    enabled = client.post(
        f"/api/v1/projects/{project_id}/plugins/python.local/enable",
        json={"type": "human", "id": "tester"},
    )
    assert enabled.status_code == 200, enabled.text
    run = client.post(
        f"/api/v1/projects/{project_id}/plugin-runs/python",
        json={
            "source_code": "print(6 * 7)",
            "timeout_seconds": 10,
            "route_id": route_id,
            "branch_id": branch_id,
            "actor": {"type": "human", "id": "tester"},
        },
    )
    assert run.status_code == 201, run.text
    assert run.json()["status"] == "SUCCEEDED"

    packet = client.post(
        f"/api/v1/projects/{project_id}/research-packets",
        json={"include_recent_events": 50, "include_checkpoints": 5},
    )
    assert packet.status_code == 200
    assert "Open Challenges" in packet.json()["markdown"]
    assert "Concrete branch" in packet.json()["markdown"]


def test_route_split_and_merge_api(tmp_path: Path) -> None:
    app = create_app(tmp_path / "workspaces")
    client = TestClient(app)
    project = client.post(
        "/api/v1/projects",
        json={
            "title": "Route operations",
            "problem": {"source_text": "Explore two representations."},
            "actor": {"type": "human", "id": "tester"},
        },
    )
    project_id = project.json()["project_id"]
    source = client.post(
        f"/api/v1/projects/{project_id}/routes",
        json={
            "title": "Broad route",
            "initial_state": "ACTIVE",
            "actor": {"type": "human", "id": "tester"},
        },
    )
    source_id = source.json()["route_id"]
    split = client.post(
        f"/api/v1/projects/{project_id}/routes/{source_id}/split",
        json={
            "children": [
                {"title": "Route A", "initial_state": "ACTIVE"},
                {"title": "Route B", "initial_state": "SEED"},
            ],
            "reason": "Separate mechanisms.",
            "actor": {"type": "human", "id": "tester"},
        },
    )
    assert split.status_code == 201, split.text
    child_ids = [item["route_id"] for item in split.json()["created_routes"]]
    merged = client.post(
        f"/api/v1/projects/{project_id}/routes/merge",
        json={
            "source_route_ids": child_ids,
            "title": "Merged insight",
            "reason": "Combine complementary insights.",
            "actor": {"type": "human", "id": "tester"},
        },
    )
    assert merged.status_code == 201, merged.text
    assert merged.json()["merged_route"]["state"] == "ACTIVE"


def test_dead_end_api_uses_stable_dead_ends_path(tmp_path: Path) -> None:
    app = create_app(tmp_path / "workspaces", tmp_path / "plugins")
    client = TestClient(app)
    project = client.post(
        "/api/v1/projects",
        json={
            "title": "Dead-end API",
            "problem": {"source_text": "Record a bounded obstruction."},
            "actor": {"type": "human", "id": "tester"},
        },
    )
    project_id = project.json()["project_id"]
    route = client.post(
        f"/api/v1/projects/{project_id}/routes",
        json={
            "title": "Naive route",
            "initial_state": "ACTIVE",
            "actor": {"type": "human", "id": "tester"},
        },
    )
    route_id = route.json()["route_id"]
    created = client.post(
        f"/api/v1/projects/{project_id}/dead-ends",
        json={
            "route_id": route_id,
            "title": "Known obstruction",
            "description": "The representation fails at n=7.",
            "strength": "OBSERVED",
            "reopen_conditions": ["change the normalization"],
            "actor": {"type": "human", "id": "tester"},
        },
    )
    assert created.status_code == 201, created.text
    listed = client.get(f"/api/v1/projects/{project_id}/dead-ends")
    assert listed.status_code == 200
    assert listed.json()[0]["title"] == "Known obstruction"


def test_import_preflight_api_does_not_create_project(tmp_path: Path) -> None:
    app = create_app(tmp_path / "workspaces", tmp_path / "plugins")
    archive = (
        Path(__file__).resolve().parents[1]
        / "examples"
        / "demo_open_research_project_alpha2.smath.zip"
    )
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/imports/preflight",
            files={
                "file": (
                    archive.name,
                    archive.read_bytes(),
                    "application/zip",
                )
            },
        )
    assert response.status_code == 200, response.text
    assert response.json()["can_import"] is True
    assert list((tmp_path / "workspaces").iterdir()) == []


def test_generic_event_api_rejects_internal_state_machine_events(tmp_path: Path) -> None:
    app = create_app(tmp_path / "workspaces", tmp_path / "plugins")
    client = TestClient(app)
    project = client.post(
        "/api/v1/projects",
        json={
            "title": "Guarded project",
            "description": "test",
            "problem": {"source_text": "Test statement.", "author_notes": ""},
            "actor": {"type": "human", "id": "tester"},
        },
    ).json()
    project_id = project["project_id"]
    route = client.post(
        f"/api/v1/projects/{project_id}/routes",
        json={
            "title": "Target",
            "initial_state": "ACTIVE",
            "actor": {"type": "human", "id": "tester"},
        },
    ).json()

    response = client.post(
        f"/api/v1/projects/{project_id}/events",
        json={
            "event_type": "ROUTE_STATE_CHANGED",
            "actor": {"type": "model", "id": "forger"},
            "route_id": route["route_id"],
            "payload": {"new_state": "CERTIFIED_CLOSED", "closure_evidence_refs": []},
        },
    )
    assert response.status_code == 400, response.text

    routes = client.get(f"/api/v1/projects/{project_id}/routes").json()
    assert routes[0]["state"] == "ACTIVE"

    annotation = client.post(
        f"/api/v1/projects/{project_id}/events",
        json={
            "event_type": "EXPERIMENT_NOTE",
            "actor": {"type": "human", "id": "tester"},
            "payload": {"label": "observation"},
        },
    )
    assert annotation.status_code == 201, annotation.text


def test_corrupt_event_chain_returns_500_not_400(tmp_path: Path) -> None:
    import json

    app = create_app(tmp_path / "workspaces", tmp_path / "plugins")
    client = TestClient(app)

    project_id = client.post(
        "/api/v1/projects",
        json={
            "title": "Integrity project",
            "description": "test",
            "problem": {
                "source_text": "Verify chain corruption is reported as 500.",
                "author_notes": "",
                "definitions": [],
                "assumptions": [],
            },
            "actor": {"type": "human", "id": "tester"},
        },
    ).json()["project_id"]

    event_path = (
        tmp_path / "workspaces" / f"{project_id}.smath" / "events" / "events.jsonl"
    )
    records = event_path.read_text(encoding="utf-8").splitlines()
    record = json.loads(records[0])
    record["event_type"] = "TAMPERED_EVENT"
    records[0] = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
    event_path.write_text("\n".join(records) + "\n", encoding="utf-8")

    response = client.post(
        f"/api/v1/projects/{project_id}/events",
        json={
            "event_type": "EXPERIMENT_NOTE",
            "actor": {"type": "human", "id": "tester"},
            "payload": {"label": "must be refused"},
        },
    )
    assert response.status_code == 500, response.text
    assert "integrity" in response.json()["detail"]
