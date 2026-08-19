from __future__ import annotations

from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from schemamath_api.domain import (
    Actor,
    ActorType,
    ArenaRecipeCreate,
    ArenaRole,
    ArenaStage,
    CanvasSnapshotCreate,
    ConnectorType,
    GenericPluginRunRequest,
    HandoffArtifactCreate,
    HandoffArtifactType,
    ModelSessionCreate,
    PluginInstallRequest,
    PluginLifecycleStatus,
    PluginRunStatus,
    ProblemContract,
    ProjectCreate,
    RouteCreate,
    RouteState,
    SessionCompleteness,
    VisualMappingStatus,
)
from schemamath_api.main import create_app
from schemamath_api.service import ConflictError, SchemaMathService

HUMAN = Actor(type=ActorType.HUMAN, id="alpha3-researcher")


def make_project(service: SchemaMathService):
    return service.create_project(
        ProjectCreate(
            title="ProofFlow Alpha.3 test",
            problem=ProblemContract(
                source_text="Explore a difficult statement without promising closure."
            ),
            actor=HUMAN,
        )
    )


def test_alpha3_model_handoff_arena_search_and_rebuild(
    service: SchemaMathService,
) -> None:
    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(
            title="Spectral obstruction route",
            description="Investigate a historical obstruction and its revival condition.",
            initial_state=RouteState.DORMANT,
            revival_conditions=["A sharper eigenvalue estimate becomes available."],
            actor=HUMAN,
        ),
    )
    explorer = service.create_model_session(
        project.project_id,
        ModelSessionCreate(
            connector_type=ConnectorType.MANUAL_CHATGPT,
            display_label="Explorer transcript",
            reported_model="Example Pro",
            model_family="example-family",
            role=ArenaRole.EXPLORER,
            completeness=SessionCompleteness.PARTIAL_VISIBLE,
            route_id=route.route_id,
            actor=HUMAN,
        ),
    )
    skeptic = service.create_model_session(
        project.project_id,
        ModelSessionCreate(
            connector_type=ConnectorType.IMPORTED_TRANSCRIPT,
            display_label="Skeptic transcript",
            reported_model="Example Pro",
            model_family="example-family",
            role=ArenaRole.SKEPTIC,
            completeness=SessionCompleteness.COMPLETE_VISIBLE,
            route_id=route.route_id,
            actor=HUMAN,
        ),
    )
    handoff = service.create_handoff_artifact(
        project.project_id,
        HandoffArtifactCreate(
            producing_session_ref=explorer.session_id,
            receiving_session_refs=[skeptic.session_id],
            artifact_type=HandoffArtifactType.FAILED_ROUTE_NOTES,
            rejected_directions=["The naive spectral bound loses the required factor."],
            unresolved_items=["Can interlacing recover the missing factor?"],
            receiving_impact="The skeptic reused the failure boundary.",
            route_id=route.route_id,
            actor=HUMAN,
        ),
    )
    recipe = service.create_arena_recipe(
        project.project_id,
        ArenaRecipeCreate(
            name="Explorer and skeptic",
            stages=[
                ArenaStage(
                    stage_id="explore",
                    role=ArenaRole.EXPLORER,
                    connector_id=str(explorer.session_id),
                    input_selection=[str(route.route_id)],
                    human_gate_after=True,
                ),
                ArenaStage(
                    stage_id="skeptic",
                    role=ArenaRole.SKEPTIC,
                    connector_id=str(skeptic.session_id),
                    input_selection=[str(handoff.handoff_id)],
                    human_gate_after=True,
                ),
            ],
            actor=HUMAN,
        ),
    )

    preview = service.preview_arena_recipe(project.project_id, recipe.recipe_id)
    assert preview.execution_started is False
    assert preview.correlated_review_warnings
    hits = service.search_history(project.project_id, "spectral missing factor")
    assert {hit.kind for hit in hits} >= {"route", "handoff"}
    deltas = service.epistemic_deltas(project.project_id)
    assert any(delta.delta_type.value == "HANDOFF_REUSED" for delta in deltas)

    before = service.integrity_report(project.project_id)
    assert before.valid
    assert service.rebuild_projection(project.project_id) == before.event_count
    assert len(service.list_model_sessions(project.project_id)) == 2
    assert len(service.list_handoff_artifacts(project.project_id)) == 1
    assert len(service.list_arena_recipes(project.project_id)) == 1


def test_canvas_snapshots_are_content_addressed_and_human_confirmed(
    service: SchemaMathService,
) -> None:
    project = make_project(service)
    first = service.create_canvas_snapshot(
        project.project_id,
        CanvasSnapshotCreate(
            scene={"type": "excalidraw", "version": 2, "elements": [{"id": "a"}]},
            author_description="Original sketch.",
            machine_interpretation="Possible route relation.",
            element_links={"a": "route:future"},
            actor=HUMAN,
        ),
    )
    second = service.create_canvas_snapshot(
        project.project_id,
        CanvasSnapshotCreate(
            scene={
                "type": "excalidraw",
                "version": 2,
                "elements": [{"id": "a"}, {"id": "b"}],
            },
            author_description="Researcher-added element.",
            mapping_status=VisualMappingStatus.CONFIRMED,
            actor=HUMAN,
        ),
    )
    assert first.original_artifact_ref != second.original_artifact_ref
    _, first_bytes = service.artifact_bytes(project.project_id, UUID(first.original_artifact_ref))
    assert b'"id": "a"' in first_bytes
    assert b'"id": "b"' not in first_bytes
    latest = service.latest_canvas_snapshot(project.project_id)
    assert latest is not None
    assert latest.visual_artifact.confirmed_by == HUMAN.id
    assert len(latest.scene["elements"]) == 2

    with pytest.raises(ConflictError):
        service.create_canvas_snapshot(
            project.project_id,
            CanvasSnapshotCreate(
                scene={"type": "excalidraw", "elements": []},
                mapping_status=VisualMappingStatus.CONFIRMED,
                actor=Actor(type=ActorType.MODEL, id="model-a"),
            ),
        )


def test_general_plugin_lifecycle_keeps_version_lock(
    service: SchemaMathService,
) -> None:
    project = make_project(service)
    installed = service.install_plugin(
        project.project_id,
        "python.local",
        PluginInstallRequest(expected_version="0.1.0", actor=HUMAN),
    )
    assert installed.lifecycle_status == PluginLifecycleStatus.INSTALLED
    health = service.check_plugin_health(project.project_id, "python.local", HUMAN)
    assert health.healthy
    enabled = service.enable_plugin(project.project_id, "python.local", HUMAN)
    assert enabled.lifecycle_status == PluginLifecycleStatus.ENABLED_FOR_PROJECT
    disabled = service.disable_plugin(project.project_id, "python.local", HUMAN)
    assert disabled.lifecycle_status == PluginLifecycleStatus.DISABLED
    uninstalled = service.uninstall_plugin(project.project_id, "python.local", HUMAN)
    assert uninstalled.lifecycle_status == PluginLifecycleStatus.UNINSTALLED

    lock_text = (
        service.project_dir(project.project_id) / "plugins" / "plugins.lock.json"
    ).read_text(encoding="utf-8")
    assert '"version": "0.1.0"' in lock_text
    assert "UNINSTALLED" in lock_text


def test_alpha2_package_remains_importable(service: SchemaMathService) -> None:
    archive = (
        Path(__file__).resolve().parents[1]
        / "examples"
        / "demo_open_research_project_alpha2.smath.zip"
    )
    manifest = service.import_project_zip(archive)
    assert manifest.schema_version == "0.2"
    assert service.integrity_report(manifest.project_id).valid
    assert service.list_routes(manifest.project_id)


def test_graphviz_plugin_health_is_truthful_and_runs_only_when_available(
    service: SchemaMathService,
) -> None:
    project = make_project(service)
    installed = service.install_plugin(
        project.project_id,
        "graphviz.local",
        PluginInstallRequest(expected_version="1.0.0", actor=HUMAN),
    )
    assert installed.lifecycle_status == PluginLifecycleStatus.INSTALLED
    health = service.check_plugin_health(project.project_id, "graphviz.local", HUMAN)
    if not health.healthy:
        with pytest.raises(ConflictError):
            service.enable_plugin(project.project_id, "graphviz.local", HUMAN)
    else:
        service.enable_plugin(project.project_id, "graphviz.local", HUMAN)
        run = service.run_plugin(
            project.project_id,
            "graphviz.local",
            GenericPluginRunRequest(
                input_text="digraph proof_flow { conjecture -> unresolved; }",
                input_filename="route.dot",
                actor=HUMAN,
            ),
        )
        assert run.status == PluginRunStatus.SUCCEEDED
        assert run.produced_artifact_refs
    assert service.integrity_report(project.project_id).valid


def test_production_app_mount_and_alpha4_openapi(tmp_path: Path) -> None:
    app = create_app(tmp_path / "workspaces", tmp_path / "plugins")
    with TestClient(app) as client:
        root = client.get("/", follow_redirects=False)
        assert root.status_code in {302, 307}
        assert root.headers["location"] == "/prototype/"
        page = client.get("/app/")
        assert page.status_code == 200
        assert "ProofFlow Schema Sandbox" in page.text
        openapi = client.get("/openapi.json").json()
        assert openapi["info"]["version"] == "0.1.0-alpha.6"
        assert "/api/v1/projects/{project_id}/epistemic-deltas" in openapi["paths"]
        assert "/api/v1/projects/{project_id}/routes/similar" in openapi["paths"]


def test_import_archive_rejects_tampered_blob_sha256(service: SchemaMathService, tmp_path: Path) -> None:
    import zipfile
    project = make_project(service)
    from schemamath_api.domain import ArtifactOrigin, ArtifactType, InterpretationStatus
    artifact = service.add_artifact(
        project_id=project.project_id,
        filename="evidence.txt",
        content=b"authentic research data",
        artifact_type=ArtifactType.TEXT,
        origin=ArtifactOrigin.HUMAN,
        media_type="text/plain",
        interpretation_status=InterpretationStatus.RAW,
        actor=HUMAN,
    )
    assert artifact.sha256

    exported_zip = service.export_project_zip(project.project_id)

    # Create a tampered copy of the zip archive where the blob content is altered
    tampered_zip = tmp_path / "tampered.smath.zip"
    with zipfile.ZipFile(exported_zip, "r") as src, zipfile.ZipFile(tampered_zip, "w") as dst:
        for item in src.infolist():
            content = src.read(item.filename)
            if item.filename == artifact.blob_relpath:
                content = b"maliciously tampered content"
            dst.writestr(item, content)

    # Preflight must detect SHA-256 mismatch
    preflight = service.preflight_project_zip(tampered_zip)
    assert not preflight.can_import
    assert any("SHA-256 mismatch" in err or "size mismatch" in err for err in preflight.errors)

    # Direct import must raise ConflictError
    with pytest.raises(ConflictError, match="archive preflight failed"):
        service.import_project_zip(tampered_zip)


def test_integrity_report_and_artifact_bytes_detect_disk_blob_tampering(
    service: SchemaMathService,
) -> None:
    project = make_project(service)
    from schemamath_api.domain import ArtifactOrigin, ArtifactType, InterpretationStatus

    artifact = service.add_artifact(
        project_id=project.project_id,
        filename="notes.txt",
        content=b"pristine research notes",
        artifact_type=ArtifactType.TEXT,
        origin=ArtifactOrigin.HUMAN,
        media_type="text/plain",
        interpretation_status=InterpretationStatus.RAW,
        actor=HUMAN,
    )

    # Initial integrity report must be valid
    report = service.integrity_report(project.project_id)
    assert report.valid is True

    # Reading artifact bytes succeeds
    art_rec, data = service.artifact_bytes(project.project_id, artifact.artifact_id)
    assert data == b"pristine research notes"

    # Now tamper with the blob file directly on disk
    blob_on_disk = service.project_dir(project.project_id) / artifact.blob_relpath
    assert blob_on_disk.is_file()
    blob_on_disk.write_bytes(b"tampered notes content on disk")

    # Integrity report must now flag the project as invalid
    report_tampered = service.integrity_report(project.project_id)
    assert report_tampered.valid is False
    assert "blob SHA-256 mismatch" in (report_tampered.error or "")

    # Reading artifact bytes directly must now fail with ConflictError
    with pytest.raises(ConflictError, match="artifact blob SHA-256 mismatch"):
        service.artifact_bytes(project.project_id, artifact.artifact_id)


