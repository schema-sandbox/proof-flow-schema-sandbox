from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest
from schemamath_api.domain import (
    Actor,
    ActorType,
    ArtifactOrigin,
    ArtifactType,
    HumanNoteCreate,
    InterpretationStatus,
    ProblemContract,
    ProjectCreate,
    ResearchPacketRequest,
    RouteCreate,
    RouteState,
    RouteStateChange,
)
from schemamath_api.projection import ProjectionStore
from schemamath_api.service import ConflictError, SchemaMathService


def make_project(service: SchemaMathService):
    return service.create_project(
        ProjectCreate(
            title="Test project",
            description="Event-store test",
            problem=ProblemContract(
                source_text="Determine whether the test statement is true.",
                author_notes="No solution is required.",
            ),
        )
    )


def test_project_route_event_chain_and_rebuild(service: SchemaMathService) -> None:
    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="First route", initial_state=RouteState.ACTIVE),
    )
    service.add_human_note(
        project.project_id,
        HumanNoteCreate(
            route_id=route.route_id,
            note_type="INTUITION",
            content="Try a parity invariant.",
        ),
    )
    changed = service.change_route_state(
        project.project_id,
        route.route_id,
        RouteStateChange(
            new_state=RouteState.DORMANT,
            reason="No progress yet; preserve for later.",
        ),
    )
    assert changed.state == RouteState.DORMANT

    report = service.integrity_report(project.project_id)
    assert report.valid is True
    assert report.event_count == 4

    database_path = service.project_dir(project.project_id) / "database" / "projections.sqlite3"
    database_path.unlink()
    replayed = service.rebuild_projection(project.project_id)
    assert replayed == 4
    routes = service.list_routes(project.project_id)
    assert routes[0].state == RouteState.DORMANT


def test_certified_close_requires_human_and_evidence(service: SchemaMathService) -> None:
    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="Closable route", initial_state=RouteState.ACTIVE),
    )
    with pytest.raises(ConflictError):
        service.change_route_state(
            project.project_id,
            route.route_id,
            RouteStateChange(
                new_state=RouteState.CERTIFIED_CLOSED,
                reason="A model says it is impossible.",
                actor=Actor(type=ActorType.MODEL, id="critic"),
            ),
        )

    closed = service.change_route_state(
        project.project_id,
        route.route_id,
        RouteStateChange(
            new_state=RouteState.CERTIFIED_CLOSED,
            reason="A finite exhaustive certificate was checked and accepted by the researcher.",
            evidence_refs=["artifact:certificate-1"],
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    assert closed.state == RouteState.CERTIFIED_CLOSED
    assert closed.closure_evidence_refs == ["artifact:certificate-1"]


def test_content_addressed_artifact_and_packet(service: SchemaMathService) -> None:
    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="Artifact route", initial_state=RouteState.ACTIVE),
    )
    content = b"candidate computation\n"
    artifact = service.add_artifact(
        project_id=project.project_id,
        filename="candidate.txt",
        content=content,
        artifact_type=ArtifactType.TEXT,
        origin=ArtifactOrigin.HUMAN,
        media_type="text/plain",
        interpretation_status=InterpretationStatus.RAW,
        actor=Actor(type=ActorType.HUMAN, id="researcher"),
    )
    stored = service.project_dir(project.project_id) / artifact.blob_relpath
    assert stored.read_bytes() == content

    packet = service.build_research_packet(
        project.project_id,
        ResearchPacketRequest(route_ids=[route.route_id]),
    )
    assert "Do not force a complete solution" in packet.markdown
    assert "Artifact route" in packet.markdown


def test_export_zip_contains_event_source(service: SchemaMathService) -> None:
    project = make_project(service)
    destination = service.export_project_zip(project.project_id)
    assert destination.exists()
    with zipfile.ZipFile(destination) as archive:
        names = set(archive.namelist())
    assert "project.json" in names
    assert "events/events.jsonl" in names


def test_branch_challenge_bridge_dead_end_checkpoint_and_rebuild(
    service: SchemaMathService,
) -> None:
    from schemamath_api.domain import (
        BranchCreate,
        BranchState,
        BranchStateChange,
        BridgeResultCreate,
        ChallengeCreate,
        ChallengeStatus,
        ChallengeStatusChange,
        ChallengeType,
        DeadEndConstraintCreate,
        DeadEndStrength,
        ResearchCheckpointCreate,
    )

    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="Generating-function route", initial_state=RouteState.ACTIVE),
    )
    branch = service.create_branch(
        project.project_id,
        BranchCreate(
            route_id=route.route_id,
            title="Small-parameter branch",
            description="Test n <= 30 before committing to the asymptotic route.",
            assumptions=["n is positive"],
            parameters={"n_max": 30},
            initial_state=BranchState.ACTIVE,
        ),
    )
    challenge = service.create_challenge(
        project.project_id,
        ChallengeCreate(
            route_id=route.route_id,
            branch_id=branch.branch_id,
            challenge_type=ChallengeType.BOUNDARY_CASE,
            statement="The claimed recurrence may fail at n=1.",
            test_plan="Enumerate n=1..30 exactly.",
        ),
    )
    assert challenge.status == ChallengeStatus.OPEN
    resolved = service.change_challenge_status(
        project.project_id,
        challenge.challenge_id,
        ChallengeStatusChange(
            new_status=ChallengeStatus.RESOLVED,
            resolution_summary="The n=1 case was separated and the recurrence was repaired.",
            evidence_refs=["artifact:table-1"],
        ),
    )
    assert resolved.status == ChallengeStatus.RESOLVED

    bridge = service.create_bridge_result(
        project.project_id,
        BridgeResultCreate(
            route_id=route.route_id,
            branch_id=branch.branch_id,
            title="Finite recurrence lemma",
            summary="A finite lemma survives even if the asymptotic route is replaced.",
            retained_value=["recurrence", "boundary classification"],
        ),
    )
    assert bridge.branch_id == branch.branch_id

    dead_end = service.create_dead_end_constraint(
        project.project_id,
        DeadEndConstraintCreate(
            title="Do not assume coefficient positivity",
            description="Repeated attempts used positivity that fails at n=7.",
            route_id=route.route_id,
            branch_id=branch.branch_id,
            applicability_scope=["this recurrence representation"],
            strength=DeadEndStrength.REPEATED,
            reopen_conditions=["a different normalization proves positivity"],
        ),
    )
    assert dead_end.strength == DeadEndStrength.REPEATED

    checkpoint = service.create_checkpoint(
        project.project_id,
        ResearchCheckpointCreate(
            current_target="Classify the valid recurrence range.",
            route_id=route.route_id,
            branch_id=branch.branch_id,
            intended_move="Separate boundary cases from the asymptotic step.",
            assumptions_used=["n >= 2"],
            observed_failure_or_gain="The n=1 obstruction is now explicit.",
            unresolved_obligations=["prove recurrence for all n >= 2"],
            next_route_suggestions=["formalize the recurrence", "search for a bijection"],
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    assert checkpoint.branch_id == branch.branch_id

    changed = service.change_branch_state(
        project.project_id,
        branch.branch_id,
        BranchStateChange(
            new_state=BranchState.BRIDGE_RESULT,
            reason="The branch produced a reusable finite lemma.",
        ),
    )
    assert changed.state == BranchState.BRIDGE_RESULT

    database_path = service.project_dir(project.project_id) / "database" / "projections.sqlite3"
    database_path.unlink()
    replayed = service.rebuild_projection(project.project_id)
    assert replayed >= 9
    assert service.list_branches(project.project_id)[0].state == BranchState.BRIDGE_RESULT
    assert service.list_challenges(project.project_id)[0].status == ChallengeStatus.RESOLVED
    assert service.list_bridge_results(project.project_id)[0].title == "Finite recurrence lemma"
    assert service.list_dead_end_constraints(project.project_id)[0].title.startswith("Do not")
    assert service.list_checkpoints(project.project_id)[0].current_target.startswith("Classify")


def test_chat_import_requires_human_confirmation(service: SchemaMathService) -> None:
    from schemamath_api.domain import (
        ChatImportConfirmRequest,
        ChatImportSelection,
        ImportDisposition,
    )

    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="Imported ideas", initial_state=RouteState.ACTIVE),
    )
    markdown = b"""# User\nCan this be attacked by parity?\n\n# Assistant\nAlternative approach: split into even and odd cases.\n\n# Assistant\nObjection: the odd case fails at n=3. Test n <= 20.\n"""
    preview = service.preview_chat_import(
        project_id=project.project_id,
        filename="conversation.md",
        content=markdown,
        media_type="text/markdown",
        actor=Actor(type=ActorType.HUMAN, id="researcher"),
    )
    assert len(preview.candidates) == 3
    assert service.list_branches(project.project_id) == []
    assert service.list_challenges(project.project_id) == []

    first_assistant = preview.candidates[1]
    second_assistant = preview.candidates[2]
    confirmation = service.confirm_chat_import(
        project.project_id,
        preview.import_id,
        ChatImportConfirmRequest(
            selections=[
                ChatImportSelection(
                    candidate_id=first_assistant.candidate_id,
                    disposition=ImportDisposition.NEW_BRANCH,
                    route_id=route.route_id,
                    title="Parity split",
                ),
                ChatImportSelection(
                    candidate_id=second_assistant.candidate_id,
                    disposition=ImportDisposition.CHALLENGE,
                    route_id=route.route_id,
                    structured_payload={"test_plan": "Enumerate n <= 20."},
                ),
            ],
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    assert confirmation.ignored_count == 0
    assert len(service.list_branches(project.project_id)) == 1
    assert len(service.list_challenges(project.project_id)) == 1
    imports = service.list_chat_imports(project.project_id)
    assert imports[0].confirmed_at is not None


def test_python_plugin_success_and_failure_are_recorded(service: SchemaMathService) -> None:
    from schemamath_api.domain import PythonPluginRunRequest

    project = make_project(service)
    service.enable_plugin(
        project.project_id,
        "python.local",
        Actor(type=ActorType.HUMAN, id="researcher"),
    )
    success = service.run_python_plugin(
        project.project_id,
        PythonPluginRunRequest(
            source_code=(
                "from pathlib import Path\n"
                "import os\n"
                "out = Path(os.environ['SCHEMAMATH_OUTPUT_DIR']) / 'result.txt'\n"
                "out.write_text('42', encoding='utf-8')\n"
                "print('experiment ok')\n"
            ),
            timeout_seconds=10,
        ),
    )
    assert success.status.value == "SUCCEEDED"
    assert success.exit_code == 0
    assert success.stdout_artifact_ref is not None
    assert success.produced_artifact_refs

    failed = service.run_python_plugin(
        project.project_id,
        PythonPluginRunRequest(
            source_code="raise RuntimeError('deliberate failure')\n",
            timeout_seconds=10,
        ),
    )
    assert failed.status.value == "FAILED"
    assert failed.exit_code != 0
    assert failed.stderr_artifact_ref is not None
    assert len(service.list_plugin_runs(project.project_id)) == 2
    event_types = [event.event_type for event in service.list_events(project.project_id)]
    assert event_types.count("PLUGIN_RUN_STARTED") == 2
    assert event_types.count("PLUGIN_RUN_COMPLETED") == 2
    assert service.integrity_report(project.project_id).valid is True


def test_route_split_and_merge_preserve_lineage(service: SchemaMathService) -> None:
    from schemamath_api.domain import (
        RouteMergeRequest,
        RouteSplitChild,
        RouteSplitRequest,
    )

    project = make_project(service)
    source = service.create_route(
        project.project_id,
        RouteCreate(
            title="Source route",
            description="A broad representation that should be decomposed.",
            initial_state=RouteState.ACTIVE,
        ),
    )
    split = service.split_route(
        project.project_id,
        source.route_id,
        RouteSplitRequest(
            children=[
                RouteSplitChild(title="Algebraic child", initial_state=RouteState.ACTIVE),
                RouteSplitChild(title="Combinatorial child", initial_state=RouteState.SEED),
            ],
            reason="The source route contains two genuinely different mechanisms.",
        ),
    )
    assert len(split.created_routes) == 2
    assert all(item.parent_route_id == source.route_id for item in split.created_routes)
    assert service._require_route(project.project_id, source.route_id).state == RouteState.ACTIVE

    merged = service.merge_routes(
        project.project_id,
        RouteMergeRequest(
            source_route_ids=[item.route_id for item in split.created_routes],
            title="Synthesis route",
            description="Combine the invariant from one child with the construction from the other.",
            reason="The two child routes supplied complementary components.",
        ),
    )
    assert merged.merged_route.state == RouteState.ACTIVE
    source_states = {
        service._require_route(project.project_id, item.route_id).state
        for item in split.created_routes
    }
    assert source_states == {RouteState.SUPERSEDED}
    event_types = [event.event_type for event in service.list_events(project.project_id)]
    assert "ROUTE_SPLIT" in event_types
    assert "ROUTES_MERGED" in event_types
    assert service.integrity_report(project.project_id).valid is True


def test_chat_import_model_cannot_confirm(service: SchemaMathService) -> None:
    from schemamath_api.domain import (
        ChatImportConfirmRequest,
        ChatImportSelection,
        ImportDisposition,
    )

    project = make_project(service)
    preview = service.preview_chat_import(
        project_id=project.project_id,
        filename="model-output.md",
        content=b"# Assistant\nA candidate route.",
        media_type="text/markdown",
        actor=Actor(type=ActorType.HUMAN, id="researcher"),
    )
    with pytest.raises(ConflictError):
        service.confirm_chat_import(
            project.project_id,
            preview.import_id,
            ChatImportConfirmRequest(
                selections=[
                    ChatImportSelection(
                        candidate_id=preview.candidates[0].candidate_id,
                        disposition=ImportDisposition.MODEL_NOTE,
                    )
                ],
                actor=Actor(type=ActorType.MODEL, id="self-confirming-model"),
            ),
        )


def test_export_import_retains_alpha2_objects_and_plugin_runs(
    service: SchemaMathService, tmp_path: Path
) -> None:
    from schemamath_api.config import Settings
    from schemamath_api.domain import (
        BranchCreate,
        BridgeResultCreate,
        ChallengeCreate,
        ChallengeType,
        DeadEndConstraintCreate,
        PythonPluginRunRequest,
        ResearchCheckpointCreate,
    )

    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="Portable route", initial_state=RouteState.ACTIVE),
    )
    branch = service.create_branch(
        project.project_id,
        BranchCreate(route_id=route.route_id, title="Portable branch"),
    )
    service.create_challenge(
        project.project_id,
        ChallengeCreate(
            route_id=route.route_id,
            branch_id=branch.branch_id,
            challenge_type=ChallengeType.OBJECTION,
            statement="Preserve this objection across export/import.",
        ),
    )
    service.create_bridge_result(
        project.project_id,
        BridgeResultCreate(
            route_id=route.route_id,
            branch_id=branch.branch_id,
            title="Portable bridge",
            summary="A bridge result that should survive replay.",
        ),
    )
    service.create_dead_end_constraint(
        project.project_id,
        DeadEndConstraintCreate(
            route_id=route.route_id,
            branch_id=branch.branch_id,
            title="Portable dead end",
            description="Do not repeat the naive reduction.",
        ),
    )
    service.create_checkpoint(
        project.project_id,
        ResearchCheckpointCreate(
            current_target="Portable checkpoint",
            route_id=route.route_id,
            branch_id=branch.branch_id,
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    service.enable_plugin(
        project.project_id,
        "python.local",
        Actor(type=ActorType.HUMAN, id="researcher"),
    )
    service.run_python_plugin(
        project.project_id,
        PythonPluginRunRequest(source_code="print('portable')", timeout_seconds=10),
    )
    archive = service.export_project_zip(project.project_id)

    imported_service = SchemaMathService(
        Settings.from_environment(tmp_path / "imported-workspaces", tmp_path / "imported-plugins")
    )
    imported = imported_service.import_project_zip(archive)
    assert imported.project_id == project.project_id
    assert imported_service.integrity_report(project.project_id).valid is True
    assert imported_service.list_branches(project.project_id)[0].title == "Portable branch"
    assert imported_service.list_challenges(project.project_id)[0].statement.startswith("Preserve")
    assert imported_service.list_bridge_results(project.project_id)[0].title == "Portable bridge"
    assert (
        imported_service.list_dead_end_constraints(project.project_id)[0].title
        == "Portable dead end"
    )
    assert (
        imported_service.list_checkpoints(project.project_id)[0].current_target
        == "Portable checkpoint"
    )
    assert imported_service.list_plugin_runs(project.project_id)[0].status.value == "SUCCEEDED"


def test_route_split_merge_preserves_source_history(service: SchemaMathService) -> None:
    from schemamath_api.domain import (
        RouteMergeRequest,
        RouteSplitChild,
        RouteSplitRequest,
    )

    project = make_project(service)
    source = service.create_route(
        project.project_id,
        RouteCreate(title="Ambiguous route", initial_state=RouteState.ACTIVE),
    )
    split = service.split_route(
        project.project_id,
        source.route_id,
        RouteSplitRequest(
            children=[
                RouteSplitChild(title="Algebraic child", initial_state=RouteState.ACTIVE),
                RouteSplitChild(title="Combinatorial child", initial_state=RouteState.ACTIVE),
            ],
            reason="The original route contains two genuinely different mechanisms.",
        ),
    )
    assert len(split.created_routes) == 2
    assert service._require_route(project.project_id, source.route_id).state == RouteState.ACTIVE

    merged = service.merge_routes(
        project.project_id,
        RouteMergeRequest(
            source_route_ids=[item.route_id for item in split.created_routes],
            title="Synthesis route",
            description="Use the invariant from one route inside the construction from the other.",
            reason="A bridge was found.",
            supersede_sources=True,
        ),
    )
    assert merged.merged_route.state == RouteState.ACTIVE
    routes = {route.route_id: route for route in service.list_routes(project.project_id)}
    for source_id in merged.source_route_ids:
        assert routes[source_id].state == RouteState.SUPERSEDED
    assert routes[source.route_id].state == RouteState.ACTIVE
    assert service.integrity_report(project.project_id).valid is True


def test_certified_dead_end_requires_human_evidence(service: SchemaMathService) -> None:
    from schemamath_api.domain import DeadEndConstraintCreate, DeadEndStrength

    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="Potential dead end", initial_state=RouteState.ACTIVE),
    )
    with pytest.raises(ConflictError):
        service.create_dead_end_constraint(
            project.project_id,
            DeadEndConstraintCreate(
                route_id=route.route_id,
                title="Premature closure",
                description="A model disliked the route.",
                strength=DeadEndStrength.CERTIFIED,
                actor=Actor(type=ActorType.MODEL, id="critic"),
            ),
        )
    certified = service.create_dead_end_constraint(
        project.project_id,
        DeadEndConstraintCreate(
            route_id=route.route_id,
            title="Bounded impossibility",
            description="A human accepted a finite exhaustive obstruction in the stated scope.",
            strength=DeadEndStrength.CERTIFIED,
            evidence_refs=["artifact:finite-certificate"],
            applicability_scope=["n <= 12"],
            reopen_conditions=["the scope is enlarged or the encoding changes"],
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    assert certified.strength == DeadEndStrength.CERTIFIED


def test_python_plugin_timeout_is_preserved(service: SchemaMathService) -> None:
    from schemamath_api.domain import PythonPluginRunRequest

    project = make_project(service)
    service.enable_plugin(
        project.project_id,
        "python.local",
        Actor(type=ActorType.HUMAN, id="researcher"),
    )
    timed_out = service.run_python_plugin(
        project.project_id,
        PythonPluginRunRequest(
            source_code="import time\ntime.sleep(5)\n",
            timeout_seconds=1,
        ),
    )
    assert timed_out.status.value == "TIMED_OUT"
    assert timed_out.error and "timeout" in timed_out.error
    assert timed_out.stdout_artifact_ref is not None
    assert timed_out.stderr_artifact_ref is not None
    assert service.integrity_report(project.project_id).valid is True


def test_chat_import_parses_html_and_json() -> None:
    from schemamath_api.chat_importer import parse_chat

    html = b"""<html><body><div data-message-author-role="user">Question</div><div data-message-author-role="assistant">Try parity.</div></body></html>"""
    parsed_html = parse_chat("chat.html", "text/html", html)
    assert parsed_html.messages == [("user", "Question"), ("assistant", "Try parity.")]

    json_payload = json.dumps(
        {"messages": [{"role": "user", "content": "Q"}, {"role": "assistant", "content": "A"}]}
    ).encode()
    parsed_json = parse_chat("chat.json", "application/json", json_payload)
    assert parsed_json.messages == [("user", "Q"), ("assistant", "A")]


def test_python_plugin_must_be_enabled(service: SchemaMathService) -> None:
    from schemamath_api.domain import PythonPluginRunRequest

    project = make_project(service)
    with pytest.raises(ConflictError):
        service.run_python_plugin(
            project.project_id,
            PythonPluginRunRequest(source_code="print('not enabled')", timeout_seconds=5),
        )


def test_import_rejects_path_traversal(service: SchemaMathService, tmp_path: Path) -> None:
    archive = tmp_path / "unsafe.smath.zip"
    with zipfile.ZipFile(archive, "w") as handle:
        handle.writestr("../escape.txt", "bad")
        handle.writestr("project.json", "{}")
    with pytest.raises(ConflictError):
        service.import_project_zip(archive)


def test_import_preflight_is_read_only_and_accepts_alpha2_package(
    service: SchemaMathService,
) -> None:
    archive = (
        Path(__file__).resolve().parents[1]
        / "examples"
        / "demo_open_research_project_alpha2.smath.zip"
    )
    report = service.preflight_project_zip(archive)
    assert report.can_import is True
    assert report.schema_version == "0.2"
    assert report.event_chain_valid is True
    assert report.event_count > 0
    assert report.missing_artifact_paths == []
    assert list(service.settings.workspace_root.iterdir()) == []


def test_import_preflight_reports_tampered_chain_and_unsafe_paths(
    service: SchemaMathService, tmp_path: Path
) -> None:
    source = (
        Path(__file__).resolve().parents[1]
        / "examples"
        / "demo_open_research_project_alpha2.smath.zip"
    )
    tampered = tmp_path / "tampered.smath.zip"
    with zipfile.ZipFile(source) as original, zipfile.ZipFile(tampered, "w") as replacement:
        for member in original.infolist():
            content = original.read(member.filename)
            if member.filename == "events/events.jsonl":
                lines = content.decode("utf-8").splitlines()
                event = json.loads(lines[0])
                event["event_type"] = "TAMPERED_EVENT"
                lines[0] = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
                content = ("\n".join(lines) + "\n").encode("utf-8")
            replacement.writestr(member, content)
    report = service.preflight_project_zip(tampered)
    assert report.can_import is False
    assert report.event_chain_valid is False
    assert "event hash chain is invalid" in report.errors

    unsafe = tmp_path / "unsafe-preflight.smath.zip"
    with zipfile.ZipFile(unsafe, "w") as archive:
        archive.writestr("../escape.txt", "bad")
        archive.writestr("project.json", "{}")
    unsafe_report = service.preflight_project_zip(unsafe)
    assert unsafe_report.can_import is False
    assert any("unsafe path" in error for error in unsafe_report.errors)


def test_corrupt_event_history_is_reported_by_integrity_check(service: SchemaMathService) -> None:
    project = make_project(service)
    event_path = service.project_dir(project.project_id) / "events" / "events.jsonl"
    records = event_path.read_text(encoding="utf-8").splitlines()
    record = json.loads(records[0])
    record["event_type"] = "TAMPERED_EVENT"
    records[0] = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
    event_path.write_text("\n".join(records) + "\n", encoding="utf-8")

    report = service.integrity_report(project.project_id)
    assert report.valid is False


def test_corrupt_event_tail_locks_project_against_new_writes(
    service: SchemaMathService,
) -> None:
    project = make_project(service)
    event_path = service.project_dir(project.project_id) / "events" / "events.jsonl"
    records = event_path.read_text(encoding="utf-8").splitlines()
    record = json.loads(records[-1])
    record["event_type"] = "TAMPERED_TAIL"
    records[-1] = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
    event_path.write_text("\n".join(records) + "\n", encoding="utf-8")

    report = service.integrity_report(project.project_id)
    assert report.valid is False
    with pytest.raises(ValueError, match="read-only until recovery"):
        service.create_route(
            project.project_id,
            RouteCreate(
                title="Must not append to a corrupt history", initial_state=RouteState.ACTIVE
            ),
        )


def test_projection_migrations_upgrade_legacy_database(tmp_path: Path) -> None:
    database_path = tmp_path / "legacy.sqlite3"
    import sqlite3

    with sqlite3.connect(database_path) as connection:
        connection.execute(
            "CREATE TABLE events (sequence INTEGER PRIMARY KEY, event_id TEXT NOT NULL, route_id TEXT)"
        )
        connection.execute(
            "CREATE TABLE project_plugins (plugin_id TEXT PRIMARY KEY, version TEXT, enabled INTEGER)"
        )
    projection = ProjectionStore(database_path)
    assert projection.schema_version() == ProjectionStore.CURRENT_SCHEMA_VERSION
    with projection.connect() as connection:
        event_columns = {row["name"] for row in connection.execute("PRAGMA table_info(events)")}
        plugin_columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(project_plugins)")
        }
    assert {"branch_id", "artifact_refs_json", "epistemic_delta_type"} <= event_columns
    assert "record_json" in plugin_columns
