from __future__ import annotations

import hashlib
import json
import mimetypes
import os
import shutil
import stat
import tempfile
import threading
import time
import zipfile
from difflib import SequenceMatcher
from pathlib import Path
from uuid import UUID, uuid4

from .chat_importer import parse_chat, to_candidates
from .config import Settings
from .domain import (
    SCHEMA_VERSION,
    Actor,
    ActorType,
    ArenaPreviewRecord,
    ArenaRecipeCreate,
    ArenaRecipeRecord,
    ArtifactOrigin,
    ArtifactRecord,
    ArtifactType,
    BranchCreate,
    BranchRecord,
    BranchStateChange,
    BridgeResultCreate,
    BridgeResultRecord,
    CanvasSnapshotCreate,
    CanvasSnapshotRecord,
    CanvasSnapshotResponse,
    ChallengeCreate,
    ChallengeRecord,
    ChallengeStatus,
    ChallengeStatusChange,
    ChatImportConfirmationResponse,
    ChatImportConfirmRequest,
    ChatImportPreviewRecord,
    DeadEndConstraintCreate,
    DeadEndConstraintRecord,
    EpistemicDeltaSummary,
    EpistemicDeltaType,
    EventRecord,
    GenericEventCreate,
    GenericPluginRunRequest,
    HandoffArtifactCreate,
    HandoffArtifactRecord,
    HistoricalSearchHit,
    HumanNoteCreate,
    ImportDisposition,
    ImportPreflightReport,
    IntegrityReport,
    InterpretationStatus,
    ModelSessionCreate,
    ModelSessionRecord,
    PluginHealthRecord,
    PluginInstallRequest,
    PluginLifecycleStatus,
    PluginManifestRecord,
    PluginRunRecord,
    ProjectCreate,
    ProjectManifest,
    ProjectPluginRecord,
    ProjectStatus,
    ProjectSummary,
    PythonPluginRunRequest,
    ResearchCheckpointCreate,
    ResearchCheckpointRecord,
    ResearchPacketRequest,
    ResearchPacketResponse,
    RouteCreate,
    RouteMergeRequest,
    RouteMergeResponse,
    RouteRecord,
    RouteSplitRequest,
    RouteSplitResponse,
    RouteState,
    RouteStateChange,
    VisualMappingStatus,
    utc_now,
)
from .event_store import EventStore
from .plugin_host import PluginHost
from .plugin_runner import PythonPluginRunner
from .projection import ProjectionStore
from .transitions import (
    InvalidTransition,
    validate_branch_transition,
    validate_challenge_transition,
    validate_route_transition,
)


class NotFoundError(LookupError):
    pass


class ConflictError(ValueError):
    pass


_MANIFEST_LOCKS_GUARD = threading.Lock()
_MANIFEST_LOCKS: dict[str, threading.Lock] = {}


def _manifest_lock(path: Path) -> threading.Lock:
    key = str(path.resolve())
    with _MANIFEST_LOCKS_GUARD:
        return _MANIFEST_LOCKS.setdefault(key, threading.Lock())


def _replace_with_retry(source: Path, target: Path, attempts: int = 10) -> None:
    """Atomically replace ``target``, retrying transient Windows sharing violations."""
    for attempt in range(attempts):
        try:
            os.replace(source, target)
            return
        except OSError:
            if attempt == attempts - 1:
                raise
            time.sleep(0.01 * (attempt + 1))


# Event types that are emitted exclusively by dedicated service methods (which
# enforce transitions, evidence, and actor rules). The generic event endpoint
# must never accept them, otherwise a caller could forge internal
# state-machine transitions, for example ``ROUTE_STATE_CHANGED`` with
# ``new_state=CERTIFIED_CLOSED`` and empty closure evidence.
RESERVED_EVENT_TYPES = frozenset(
    {
        "PROJECT_CREATED",
        "ROUTE_CREATED",
        "ROUTE_SPLIT",
        "ROUTES_MERGED",
        "ROUTE_STATE_CHANGED",
        "BRANCH_CREATED",
        "BRANCH_STATE_CHANGED",
        "CHALLENGE_CREATED",
        "CHALLENGE_STATUS_CHANGED",
        "BRIDGE_RESULT_CREATED",
        "DEAD_END_CONSTRAINT_CREATED",
        "RESEARCH_CHECKPOINT_CREATED",
        "ARTIFACT_ADDED",
        "OBJECTION_ADDED",
        "HUMAN_INTERVENTION_ADDED",
        "CHAT_IMPORT_PREVIEW_CREATED",
        "MODEL_NOTE_IMPORTED",
        "CHAT_IMPORT_CONFIRMED",
        "PLUGIN_INSTALLED",
        "PLUGIN_HEALTH_CHECKED",
        "PLUGIN_ENABLED",
        "PLUGIN_DISABLED",
        "PLUGIN_UNINSTALLED",
        "PLUGIN_RUN_STARTED",
        "PLUGIN_RUN_COMPLETED",
        "MODEL_SESSION_CREATED",
        "HANDOFF_CREATED",
        "ARENA_RECIPE_CREATED",
        "VISUAL_CANVAS_SNAPSHOT_CREATED",
    }
)


class SchemaMathService:
    MAX_IMPORT_MEMBERS = 10_000
    MAX_IMPORT_UNCOMPRESSED_BYTES = 250 * 1024 * 1024
    MAX_IMPORT_MANIFEST_BYTES = 4 * 1024 * 1024

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.settings.workspace_root.mkdir(parents=True, exist_ok=True)
        self.repository_root = Path(__file__).resolve().parents[3]

    def project_dir(self, project_id: UUID) -> Path:
        return self.settings.workspace_root / f"{project_id}.smath"

    def _manifest_path(self, project_id: UUID) -> Path:
        return self.project_dir(project_id) / "project.json"

    def _event_store(self, project_id: UUID) -> EventStore:
        return EventStore(self.project_dir(project_id) / "events" / "events.jsonl")

    def _projection(self, project_id: UUID) -> ProjectionStore:
        return ProjectionStore(self.project_dir(project_id) / "database" / "projections.sqlite3")

    # ------------------------------------------------------------------
    # Projects
    # ------------------------------------------------------------------

    def create_project(self, request: ProjectCreate) -> ProjectManifest:
        project_id = uuid4()
        goal_id = uuid4()
        project_dir = self.project_dir(project_id)
        if project_dir.exists():
            raise ConflictError(f"project {project_id} already exists")

        for relative in (
            "events",
            "database",
            "blobs/sha256",
            "canvas",
            "views",
            "plugins",
            "runs",
            "snapshots",
            "exports",
            "imports",
        ):
            (project_dir / relative).mkdir(parents=True, exist_ok=True)

        now = utc_now()
        manifest = ProjectManifest(
            schema_version=SCHEMA_VERSION,
            project_id=project_id,
            title=request.title,
            description=request.description,
            created_at=now,
            updated_at=now,
            original_problem=request.problem,
            current_goal_id=goal_id,
            project_status=[ProjectStatus.UNRESOLVED],
        )
        self._write_manifest(manifest)
        self._write_plugins_lock(project_id, [])
        (project_dir / "views" / "routes.json").write_text(
            json.dumps({"schema_version": SCHEMA_VERSION, "routes": []}, indent=2),
            encoding="utf-8",
        )
        (project_dir / "canvas" / "main.excalidraw").write_text(
            json.dumps(
                {
                    "type": "excalidraw",
                    "version": 2,
                    "source": "https://schemamath.org",
                    "elements": [],
                    "appState": {},
                    "files": {},
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="PROJECT_CREATED",
            actor=request.actor,
            payload={
                "project": manifest.model_dump(mode="json"),
                "goal_id": str(goal_id),
            },
            epistemic_delta="A new unresolved research space was created.",
        )
        self._projection(project_id).apply(event)
        return manifest

    def list_projects(self) -> list[ProjectSummary]:
        summaries: list[ProjectSummary] = []
        for path in sorted(self.settings.workspace_root.glob("*.smath/project.json")):
            try:
                manifest = ProjectManifest.model_validate_json(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            summaries.append(
                ProjectSummary(
                    project_id=manifest.project_id,
                    title=manifest.title,
                    description=manifest.description,
                    updated_at=manifest.updated_at,
                    project_status=manifest.project_status,
                )
            )
        return sorted(summaries, key=lambda item: item.updated_at, reverse=True)

    def get_project(self, project_id: UUID) -> ProjectManifest:
        path = self._manifest_path(project_id)
        if not path.exists():
            raise NotFoundError(f"project {project_id} not found")
        return ProjectManifest.model_validate_json(path.read_text(encoding="utf-8"))

    # ------------------------------------------------------------------
    # Routes and branches
    # ------------------------------------------------------------------

    def create_route(self, project_id: UUID, request: RouteCreate) -> RouteRecord:
        self.get_project(project_id)
        if request.parent_route_id is not None:
            self._require_route(project_id, request.parent_route_id)
        now = utc_now()
        route = RouteRecord(
            route_id=uuid4(),
            project_id=project_id,
            parent_route_id=request.parent_route_id,
            title=request.title,
            description=request.description,
            state=request.initial_state,
            objections=[],
            revival_conditions=request.revival_conditions,
            closure_evidence_refs=[],
            created_at=now,
            updated_at=now,
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="ROUTE_CREATED",
            actor=request.actor,
            route_id=route.route_id,
            payload={"route": route.model_dump(mode="json")},
            epistemic_delta=f"A new route '{route.title}' entered the research space.",
        )
        self._projection(project_id).apply(event)
        self._touch_manifest(project_id)
        return route

    def list_routes(self, project_id: UUID) -> list[RouteRecord]:
        self.get_project(project_id)
        return self._projection(project_id).list_routes()

    def split_route(
        self, project_id: UUID, route_id: UUID, request: RouteSplitRequest
    ) -> RouteSplitResponse:
        """Create child routes without deleting or implicitly rejecting the source route."""
        source = self._require_route(project_id, route_id)
        created: list[RouteRecord] = []
        for child in request.children:
            route = self.create_route(
                project_id,
                RouteCreate(
                    title=child.title,
                    description=child.description,
                    parent_route_id=source.route_id,
                    initial_state=child.initial_state,
                    revival_conditions=child.revival_conditions,
                    actor=request.actor,
                ),
            )
            created.append(route)
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="ROUTE_SPLIT",
            actor=request.actor,
            route_id=source.route_id,
            payload={
                "source_route_id": str(source.route_id),
                "created_route_ids": [str(item.route_id) for item in created],
                "reason": request.reason,
            },
            epistemic_delta=(
                f"Route '{source.title}' was split into {len(created)} explicit child routes "
                "without closing the source route."
            ),
        )
        self._projection(project_id).apply(event)
        self._touch_manifest(project_id)
        return RouteSplitResponse(
            source_route_id=source.route_id,
            created_routes=created,
            event_id=event.event_id,
        )

    def merge_routes(self, project_id: UUID, request: RouteMergeRequest) -> RouteMergeResponse:
        """Create a synthesis route and optionally supersede its source routes."""
        sources = [
            self._require_route(project_id, route_id) for route_id in request.source_route_ids
        ]
        if request.supersede_sources:
            for source in sources:
                if source.state == RouteState.SUPERSEDED:
                    continue
                transition = RouteStateChange(
                    new_state=RouteState.SUPERSEDED,
                    reason=f"Merged into synthesis route '{request.title}': {request.reason}",
                    actor=request.actor,
                )
                try:
                    validate_route_transition(source.state, transition)
                except InvalidTransition as exc:
                    raise ConflictError(
                        f"route {source.route_id} cannot be superseded from {source.state.value}: {exc}"
                    ) from exc

        merged = self.create_route(
            project_id,
            RouteCreate(
                title=request.title,
                description=request.description,
                initial_state=RouteState.ACTIVE,
                actor=request.actor,
            ),
        )
        if request.supersede_sources:
            for source in sources:
                if source.state == RouteState.SUPERSEDED:
                    continue
                self.change_route_state(
                    project_id,
                    source.route_id,
                    RouteStateChange(
                        new_state=RouteState.SUPERSEDED,
                        reason=f"Merged into route {merged.route_id}: {request.reason}",
                        actor=request.actor,
                    ),
                )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="ROUTES_MERGED",
            actor=request.actor,
            route_id=merged.route_id,
            payload={
                "source_route_ids": [str(item.route_id) for item in sources],
                "merged_route_id": str(merged.route_id),
                "reason": request.reason,
                "supersede_sources": request.supersede_sources,
            },
            epistemic_delta=(
                f"{len(sources)} routes were synthesized into '{merged.title}'. "
                "The source routes remain in the event history."
            ),
        )
        self._projection(project_id).apply(event)
        self._touch_manifest(project_id)
        return RouteMergeResponse(
            merged_route=merged,
            source_route_ids=[item.route_id for item in sources],
            event_id=event.event_id,
        )

    def change_route_state(
        self, project_id: UUID, route_id: UUID, request: RouteStateChange
    ) -> RouteRecord:
        route = self._require_route(project_id, route_id)
        try:
            validate_route_transition(route.state, request)
        except InvalidTransition as exc:
            raise ConflictError(str(exc)) from exc
        closure_evidence = (
            request.evidence_refs
            if request.new_state.value == "CERTIFIED_CLOSED"
            else route.closure_evidence_refs
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="ROUTE_STATE_CHANGED",
            actor=request.actor,
            route_id=route_id,
            artifact_refs=request.evidence_refs,
            payload={
                "previous_state": route.state.value,
                "new_state": request.new_state.value,
                "reason": request.reason,
                "human_confirmed": request.human_confirmed,
                "closure_evidence_refs": closure_evidence,
            },
            epistemic_delta=(
                f"Route state changed from {route.state.value} to "
                f"{request.new_state.value}: {request.reason}"
            ),
        )
        projection = self._projection(project_id)
        projection.apply(event)
        self._touch_manifest(project_id)
        updated = projection.get_route(str(route_id))
        assert updated is not None
        return updated

    def create_branch(self, project_id: UUID, request: BranchCreate) -> BranchRecord:
        self._require_route(project_id, request.route_id)
        if request.parent_branch_id is not None:
            parent = self._require_branch(project_id, request.parent_branch_id)
            if parent.route_id != request.route_id:
                raise ConflictError("parent branch belongs to a different route")
        now = utc_now()
        branch = BranchRecord(
            branch_id=uuid4(),
            project_id=project_id,
            route_id=request.route_id,
            parent_branch_id=request.parent_branch_id,
            title=request.title,
            description=request.description,
            assumptions=request.assumptions,
            parameters=request.parameters,
            state=request.initial_state,
            created_at=now,
            updated_at=now,
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="BRANCH_CREATED",
            actor=request.actor,
            route_id=request.route_id,
            branch_id=branch.branch_id,
            payload={"branch": branch.model_dump(mode="json")},
            epistemic_delta=f"A concrete branch '{branch.title}' was created.",
        )
        self._projection(project_id).apply(event)
        self._touch_manifest(project_id)
        return branch

    def list_branches(self, project_id: UUID, route_id: UUID | None = None) -> list[BranchRecord]:
        self.get_project(project_id)
        if route_id is not None:
            self._require_route(project_id, route_id)
        return self._projection(project_id).list_branches(str(route_id) if route_id else None)

    def change_branch_state(
        self, project_id: UUID, branch_id: UUID, request: BranchStateChange
    ) -> BranchRecord:
        branch = self._require_branch(project_id, branch_id)
        try:
            validate_branch_transition(branch.state, request)
        except InvalidTransition as exc:
            raise ConflictError(str(exc)) from exc
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="BRANCH_STATE_CHANGED",
            actor=request.actor,
            route_id=branch.route_id,
            branch_id=branch_id,
            artifact_refs=request.evidence_refs,
            payload={
                "previous_state": branch.state.value,
                "new_state": request.new_state.value,
                "reason": request.reason,
                "evidence_refs": request.evidence_refs,
            },
            epistemic_delta=(
                f"Branch state changed from {branch.state.value} to "
                f"{request.new_state.value}: {request.reason}"
            ),
        )
        projection = self._projection(project_id)
        projection.apply(event)
        self._touch_manifest(project_id)
        updated = projection.get_branch(str(branch_id))
        assert updated is not None
        return updated

    # ------------------------------------------------------------------
    # Challenges, bridge results, dead ends, checkpoints
    # ------------------------------------------------------------------

    def create_challenge(self, project_id: UUID, request: ChallengeCreate) -> ChallengeRecord:
        route_id, branch_id = self._normalize_target(
            project_id, request.route_id, request.branch_id
        )
        now = utc_now()
        challenge = ChallengeRecord(
            challenge_id=uuid4(),
            project_id=project_id,
            route_id=route_id,
            branch_id=branch_id,
            challenge_type=request.challenge_type,
            status=ChallengeStatus.OPEN,
            statement=request.statement,
            test_plan=request.test_plan,
            evidence_refs=request.evidence_refs,
            resolution_summary="",
            created_at=now,
            updated_at=now,
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="CHALLENGE_CREATED",
            actor=request.actor,
            route_id=route_id,
            branch_id=branch_id,
            artifact_refs=request.evidence_refs,
            payload={"challenge": challenge.model_dump(mode="json")},
            epistemic_delta=f"A challenge was raised: {request.statement}",
        )
        self._projection(project_id).apply(event)
        self._touch_manifest(project_id)
        return challenge

    def list_challenges(self, project_id: UUID) -> list[ChallengeRecord]:
        self.get_project(project_id)
        return self._projection(project_id).list_challenges()

    def change_challenge_status(
        self, project_id: UUID, challenge_id: UUID, request: ChallengeStatusChange
    ) -> ChallengeRecord:
        challenge = self._projection(project_id).get_challenge(str(challenge_id))
        if challenge is None:
            raise NotFoundError(f"challenge {challenge_id} not found")
        try:
            validate_challenge_transition(challenge.status, request)
        except InvalidTransition as exc:
            raise ConflictError(str(exc)) from exc
        combined_evidence = list(dict.fromkeys([*challenge.evidence_refs, *request.evidence_refs]))
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="CHALLENGE_STATUS_CHANGED",
            actor=request.actor,
            route_id=challenge.route_id,
            branch_id=challenge.branch_id,
            artifact_refs=request.evidence_refs,
            payload={
                "challenge_id": str(challenge_id),
                "previous_status": challenge.status.value,
                "new_status": request.new_status.value,
                "resolution_summary": request.resolution_summary,
                "evidence_refs": combined_evidence,
            },
            epistemic_delta=(
                f"Challenge changed from {challenge.status.value} to {request.new_status.value}."
            ),
        )
        projection = self._projection(project_id)
        projection.apply(event)
        self._touch_manifest(project_id)
        updated = projection.get_challenge(str(challenge_id))
        assert updated is not None
        return updated

    def create_bridge_result(
        self, project_id: UUID, request: BridgeResultCreate
    ) -> BridgeResultRecord:
        self._validate_route_branch(project_id, request.route_id, request.branch_id)
        for route_id in request.enabled_route_ids:
            self._require_route(project_id, route_id)
        now = utc_now()
        record = BridgeResultRecord(
            bridge_result_id=uuid4(),
            project_id=project_id,
            route_id=request.route_id,
            branch_id=request.branch_id,
            title=request.title,
            summary=request.summary,
            enabled_route_ids=request.enabled_route_ids,
            artifact_refs=request.artifact_refs,
            retained_value=request.retained_value,
            created_at=now,
            updated_at=now,
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="BRIDGE_RESULT_CREATED",
            actor=request.actor,
            route_id=request.route_id,
            branch_id=request.branch_id,
            artifact_refs=request.artifact_refs,
            payload={"bridge_result": record.model_dump(mode="json")},
            epistemic_delta=f"Bridge result preserved: {request.title}",
        )
        self._projection(project_id).apply(event)
        self._touch_manifest(project_id)
        return record

    def list_bridge_results(self, project_id: UUID) -> list[BridgeResultRecord]:
        self.get_project(project_id)
        return self._projection(project_id).list_bridge_results()

    def create_dead_end_constraint(
        self, project_id: UUID, request: DeadEndConstraintCreate
    ) -> DeadEndConstraintRecord:
        route_id, branch_id = self._normalize_optional_target(
            project_id, request.route_id, request.branch_id
        )
        if request.strength.value == "CERTIFIED":
            if request.actor.type != ActorType.HUMAN:
                raise ConflictError("CERTIFIED dead-end constraints require a human actor")
            if not request.evidence_refs:
                raise ConflictError("CERTIFIED dead-end constraints require evidence")
        now = utc_now()
        record = DeadEndConstraintRecord(
            dead_end_id=uuid4(),
            project_id=project_id,
            route_id=route_id,
            branch_id=branch_id,
            title=request.title,
            description=request.description,
            applicability_scope=request.applicability_scope,
            prior_attempt_refs=request.prior_attempt_refs,
            evidence_refs=request.evidence_refs,
            strength=request.strength,
            reopen_conditions=request.reopen_conditions,
            created_at=now,
            updated_at=now,
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="DEAD_END_CONSTRAINT_CREATED",
            actor=request.actor,
            route_id=route_id,
            branch_id=branch_id,
            artifact_refs=request.evidence_refs,
            payload={"dead_end": record.model_dump(mode="json")},
            epistemic_delta=(
                f"A known dead-end constraint was recorded without deleting the route: "
                f"{request.title}"
            ),
        )
        self._projection(project_id).apply(event)
        self._touch_manifest(project_id)
        return record

    def list_dead_end_constraints(self, project_id: UUID) -> list[DeadEndConstraintRecord]:
        self.get_project(project_id)
        return self._projection(project_id).list_dead_ends()

    def create_checkpoint(
        self, project_id: UUID, request: ResearchCheckpointCreate
    ) -> ResearchCheckpointRecord:
        route_id, branch_id = self._normalize_optional_target(
            project_id, request.route_id, request.branch_id
        )
        checkpoint = ResearchCheckpointRecord(
            checkpoint_id=uuid4(),
            project_id=project_id,
            current_target=request.current_target,
            route_id=route_id,
            branch_id=branch_id,
            intended_move=request.intended_move,
            assumptions_used=request.assumptions_used,
            expected_result=request.expected_result,
            produced_artifact_refs=request.produced_artifact_refs,
            observed_failure_or_gain=request.observed_failure_or_gain,
            confidence=request.confidence,
            unresolved_obligations=request.unresolved_obligations,
            next_route_suggestions=request.next_route_suggestions,
            source_session_ref=request.source_session_ref,
            actor=request.actor,
            created_at=utc_now(),
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="RESEARCH_CHECKPOINT_CREATED",
            actor=request.actor,
            route_id=route_id,
            branch_id=branch_id,
            artifact_refs=request.produced_artifact_refs,
            payload={"checkpoint": checkpoint.model_dump(mode="json")},
            epistemic_delta=(
                request.observed_failure_or_gain or "A structured research checkpoint was recorded."
            ),
        )
        self._projection(project_id).apply(event)
        self._touch_manifest(project_id)
        return checkpoint

    def list_checkpoints(
        self, project_id: UUID, limit: int | None = None
    ) -> list[ResearchCheckpointRecord]:
        self.get_project(project_id)
        return self._projection(project_id).list_checkpoints(limit)

    # ------------------------------------------------------------------
    # Notes, generic events, artifacts
    # ------------------------------------------------------------------

    def add_human_note(self, project_id: UUID, request: HumanNoteCreate) -> EventRecord:
        route_id, branch_id = self._normalize_optional_target(
            project_id, request.route_id, request.branch_id
        )
        event_type = (
            "OBJECTION_ADDED"
            if request.note_type in {"COUNTEREXAMPLE", "FREEZE"}
            else "HUMAN_INTERVENTION_ADDED"
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type=event_type,
            actor=request.actor,
            route_id=route_id,
            branch_id=branch_id,
            payload={"note_type": request.note_type, "content": request.content},
            epistemic_delta=f"Human {request.note_type.lower()} note added.",
        )
        self._projection(project_id).apply(event)
        self._touch_manifest(project_id)
        return event

    def append_generic_event(self, project_id: UUID, request: GenericEventCreate) -> EventRecord:
        if request.event_type in RESERVED_EVENT_TYPES:
            raise ValueError(
                f"event type {request.event_type} is managed by a dedicated endpoint "
                "and cannot be submitted as a generic event"
            )
        route_id, branch_id = self._normalize_optional_target(
            project_id, request.route_id, request.branch_id
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type=request.event_type,
            actor=request.actor,
            payload=request.payload,
            route_id=route_id,
            branch_id=branch_id,
            caused_by=request.caused_by,
            artifact_refs=request.artifact_refs,
            epistemic_delta=request.epistemic_delta,
            epistemic_delta_type=request.epistemic_delta_type,
        )
        self._projection(project_id).apply(event)
        self._touch_manifest(project_id)
        return event

    def list_events(self, project_id: UUID) -> list[EventRecord]:
        self.get_project(project_id)
        return self._event_store(project_id).read_all()

    def add_artifact(
        self,
        *,
        project_id: UUID,
        filename: str,
        content: bytes,
        artifact_type: ArtifactType,
        origin: ArtifactOrigin,
        media_type: str | None,
        interpretation_status: InterpretationStatus,
        actor: Actor,
        source_ref: str | None = None,
    ) -> ArtifactRecord:
        self.get_project(project_id)
        if len(content) > self.settings.maximum_upload_bytes:
            raise ConflictError(
                f"artifact exceeds maximum upload size ({self.settings.maximum_upload_bytes} bytes)"
            )
        sha256 = hashlib.sha256(content).hexdigest()
        blob_relpath = f"blobs/sha256/{sha256[:2]}/{sha256}"
        blob_path = self.project_dir(project_id) / blob_relpath
        blob_path.parent.mkdir(parents=True, exist_ok=True)
        if not blob_path.exists():
            blob_path.write_bytes(content)
        artifact = ArtifactRecord(
            artifact_id=uuid4(),
            project_id=project_id,
            artifact_type=artifact_type,
            sha256=sha256,
            media_type=media_type
            or mimetypes.guess_type(filename)[0]
            or "application/octet-stream",
            size_bytes=len(content),
            origin=origin,
            original_filename=Path(filename).name,
            blob_relpath=blob_relpath,
            source_ref=source_ref,
            interpretation_status=interpretation_status,
            created_at=utc_now(),
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="ARTIFACT_ADDED",
            actor=actor,
            artifact_refs=[str(artifact.artifact_id)],
            payload={"artifact": artifact.model_dump(mode="json")},
            epistemic_delta=f"Artifact '{artifact.original_filename}' was preserved.",
        )
        self._projection(project_id).apply(event)
        self._touch_manifest(project_id)
        return artifact

    def list_artifacts(self, project_id: UUID) -> list[ArtifactRecord]:
        self.get_project(project_id)
        return self._projection(project_id).list_artifacts()

    def artifact_bytes(self, project_id: UUID, artifact_id: UUID) -> tuple[ArtifactRecord, bytes]:
        artifact = self._require_artifact(project_id, artifact_id)
        path = self.project_dir(project_id) / artifact.blob_relpath
        if not path.exists():
            raise NotFoundError(f"artifact blob for {artifact_id} is missing")
        return artifact, path.read_bytes()

    # ------------------------------------------------------------------
    # ChatGPT companion import
    # ------------------------------------------------------------------

    def create_chat_import_preview(
        self,
        *,
        project_id: UUID,
        filename: str,
        media_type: str | None,
        content: bytes,
        actor: Actor,
    ) -> ChatImportPreviewRecord:
        self.get_project(project_id)
        if len(content.decode("utf-8", errors="replace")) > self.settings.maximum_chat_import_chars:
            raise ConflictError("chat import exceeds configured character limit")
        artifact = self.add_artifact(
            project_id=project_id,
            filename=filename,
            content=content,
            artifact_type=ArtifactType.CHAT_TRANSCRIPT,
            origin=ArtifactOrigin.IMPORT,
            media_type=media_type,
            interpretation_status=InterpretationStatus.RAW,
            actor=actor,
            source_ref="chat-import-raw",
        )
        parsed = parse_chat(filename, media_type, content)
        preview = ChatImportPreviewRecord(
            import_id=uuid4(),
            project_id=project_id,
            artifact_id=artifact.artifact_id,
            source_filename=filename,
            import_format=parsed.import_format,
            parser_name=parsed.parser_name,
            candidates=to_candidates(parsed.messages),
            created_at=utc_now(),
            confirmed_at=None,
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="CHAT_IMPORT_PREVIEW_CREATED",
            actor=actor,
            artifact_refs=[str(artifact.artifact_id)],
            payload={"preview": preview.model_dump(mode="json")},
            epistemic_delta=(
                "A model conversation was preserved and parsed into candidates. "
                "No candidate entered the research graph without human confirmation."
            ),
        )
        self._projection(project_id).apply(event)
        self._touch_manifest(project_id)
        return preview

    # Compatibility name used by early alpha clients and tests.
    def preview_chat_import(
        self,
        *,
        project_id: UUID,
        filename: str,
        content: bytes,
        media_type: str | None,
        actor: Actor,
    ) -> ChatImportPreviewRecord:
        return self.create_chat_import_preview(
            project_id=project_id,
            filename=filename,
            media_type=media_type,
            content=content,
            actor=actor,
        )

    def list_chat_imports(self, project_id: UUID) -> list[ChatImportPreviewRecord]:
        self.get_project(project_id)
        return self._projection(project_id).list_chat_imports()

    def confirm_chat_import(
        self,
        project_id: UUID,
        import_id: UUID,
        request: ChatImportConfirmRequest,
    ) -> ChatImportConfirmationResponse:
        if request.actor.type != ActorType.HUMAN:
            raise ConflictError("chat import confirmation requires a human actor")
        preview = self._projection(project_id).get_chat_import(str(import_id))
        if preview is None:
            raise NotFoundError(f"chat import {import_id} not found")
        if preview.confirmed_at is not None:
            raise ConflictError("chat import has already been confirmed")
        candidate_map = {item.candidate_id: item for item in preview.candidates}
        created_event_ids: list[UUID] = []
        created_object_refs: list[str] = []
        ignored_count = 0
        for selection in request.selections:
            candidate = candidate_map.get(selection.candidate_id)
            if candidate is None:
                raise ConflictError(
                    f"candidate {selection.candidate_id} does not belong to import {import_id}"
                )
            content = (selection.content_override or candidate.content).strip()
            if selection.disposition == ImportDisposition.IGNORE:
                ignored_count += 1
                continue
            if selection.disposition == ImportDisposition.MODEL_NOTE:
                event = self._event_store(project_id).append(
                    project_id=project_id,
                    event_type="MODEL_NOTE_IMPORTED",
                    actor=request.actor,
                    route_id=selection.route_id,
                    branch_id=selection.branch_id,
                    caused_by=[str(import_id), str(selection.candidate_id)],
                    epistemic_delta=(
                        "A human accepted imported model text as a visible research note."
                    ),
                    payload={
                        "title": selection.title,
                        "content": content,
                        "source_artifact_id": str(preview.artifact_id),
                    },
                )
                self._projection(project_id).apply(event)
                created_event_ids.append(event.event_id)
                created_object_refs.append(f"event:{event.event_id}")
            elif selection.disposition == ImportDisposition.RESEARCH_CHECKPOINT:
                payload = selection.structured_payload
                checkpoint = self.create_checkpoint(
                    project_id,
                    ResearchCheckpointCreate(
                        current_target=str(payload.get("current_target") or content[:4000]),
                        route_id=selection.route_id,
                        branch_id=selection.branch_id,
                        intended_move=str(payload.get("intended_move") or ""),
                        assumptions_used=[str(x) for x in payload.get("assumptions_used", [])],
                        expected_result=str(payload.get("expected_result") or ""),
                        produced_artifact_refs=[
                            str(x) for x in payload.get("produced_artifact_refs", [])
                        ],
                        observed_failure_or_gain=str(
                            payload.get("observed_failure_or_gain") or content
                        ),
                        confidence=payload.get("confidence", "UNSPECIFIED"),
                        unresolved_obligations=[
                            str(x) for x in payload.get("unresolved_obligations", [])
                        ],
                        next_route_suggestions=[
                            str(x) for x in payload.get("next_route_suggestions", [])
                        ],
                        source_session_ref=f"chat-import:{import_id}:{selection.candidate_id}",
                        actor=request.actor,
                    ),
                )
                created_object_refs.append(f"checkpoint:{checkpoint.checkpoint_id}")
            elif selection.disposition == ImportDisposition.CHALLENGE:
                challenge = self.create_challenge(
                    project_id,
                    ChallengeCreate(
                        route_id=selection.route_id,
                        branch_id=selection.branch_id,
                        challenge_type=selection.structured_payload.get(
                            "challenge_type", "OBJECTION"
                        ),
                        statement=content,
                        test_plan=str(selection.structured_payload.get("test_plan") or ""),
                        evidence_refs=[str(preview.artifact_id)],
                        actor=request.actor,
                    ),
                )
                created_object_refs.append(f"challenge:{challenge.challenge_id}")
            elif selection.disposition == ImportDisposition.BRIDGE_RESULT:
                if selection.route_id is None:
                    raise ConflictError("a bridge result requires route_id")
                bridge = self.create_bridge_result(
                    project_id,
                    BridgeResultCreate(
                        route_id=selection.route_id,
                        branch_id=selection.branch_id,
                        title=selection.title or "Imported bridge result",
                        summary=content,
                        enabled_route_ids=[
                            UUID(str(x))
                            for x in selection.structured_payload.get("enabled_route_ids", [])
                        ],
                        artifact_refs=[str(preview.artifact_id)],
                        retained_value=[
                            str(x) for x in selection.structured_payload.get("retained_value", [])
                        ],
                        actor=request.actor,
                    ),
                )
                created_object_refs.append(f"bridge:{bridge.bridge_result_id}")
            elif selection.disposition == ImportDisposition.NEW_BRANCH:
                if selection.route_id is None:
                    raise ConflictError("a new branch requires route_id")
                branch = self.create_branch(
                    project_id,
                    BranchCreate(
                        route_id=selection.route_id,
                        parent_branch_id=selection.branch_id,
                        title=selection.title or "Imported branch",
                        description=content,
                        assumptions=[
                            str(x) for x in selection.structured_payload.get("assumptions", [])
                        ],
                        parameters=dict(selection.structured_payload.get("parameters", {})),
                        actor=request.actor,
                    ),
                )
                created_object_refs.append(f"branch:{branch.branch_id}")
        confirmation_event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="CHAT_IMPORT_CONFIRMED",
            actor=request.actor,
            artifact_refs=[str(preview.artifact_id)],
            caused_by=[str(import_id)],
            payload={
                "import_id": str(import_id),
                "created_object_refs": created_object_refs,
                "ignored_count": ignored_count,
            },
            epistemic_delta=(
                "A human confirmed selected imported conversation fragments. "
                "Unselected text remains preserved only in the raw transcript artifact."
            ),
        )
        self._projection(project_id).apply(confirmation_event)
        created_event_ids.append(confirmation_event.event_id)
        self._touch_manifest(project_id)
        return ChatImportConfirmationResponse(
            import_id=import_id,
            created_event_ids=created_event_ids,
            created_object_refs=created_object_refs,
            ignored_count=ignored_count,
        )

    # ------------------------------------------------------------------
    # Optional plugin registry and Python runner
    # ------------------------------------------------------------------

    def available_plugins(self) -> list[PluginManifestRecord]:
        return self._plugin_host().available_manifests()

    def health_available_plugins(self) -> list[PluginHealthRecord]:
        host = self._plugin_host()
        return [host.healthcheck(manifest) for manifest in host.available_manifests()]

    def install_plugin(
        self, project_id: UUID, plugin_id: str, request: PluginInstallRequest
    ) -> ProjectPluginRecord:
        self.get_project(project_id)
        if request.actor.type != ActorType.HUMAN:
            raise ConflictError("plugin installation requires a human actor")
        manifest = self._require_plugin_manifest(plugin_id)
        if not self.settings.allow_local_plugins and manifest.runner_type.value in {
            "python",
            "local_command",
        }:
            raise ConflictError(
                "local process plugins are disabled by deployment policy; use a digest-pinned OCI runner"
            )
        if request.expected_version and request.expected_version != manifest.version:
            raise ConflictError(
                f"requested {request.expected_version}, available version is {manifest.version}"
            )
        self._plugin_host().install_manifest(manifest)
        now = utc_now()
        record = ProjectPluginRecord(
            plugin_id=manifest.plugin_id,
            version=manifest.version,
            enabled=False,
            lifecycle_status=PluginLifecycleStatus.INSTALLED,
            installed_at=now,
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="PLUGIN_INSTALLED",
            actor=request.actor,
            payload={
                "plugin": record.model_dump(mode="json"),
                "manifest": manifest.model_dump(mode="json"),
            },
            epistemic_delta=f"Plugin {plugin_id}@{manifest.version} was installed.",
            epistemic_delta_type=EpistemicDeltaType.NO_STATE_CHANGE,
        )
        projection = self._projection(project_id)
        projection.apply(event)
        self._write_plugins_lock(project_id, projection.list_project_plugins())
        self._touch_manifest(project_id)
        return record

    def check_plugin_health(
        self, project_id: UUID, plugin_id: str, actor: Actor
    ) -> PluginHealthRecord:
        self.get_project(project_id)
        manifest = self._require_plugin_manifest(plugin_id)
        current = self._projection(project_id).get_project_plugin(plugin_id)
        if current is None:
            raise ConflictError("plugin must be installed before its health check")
        health = self._plugin_host().healthcheck(manifest)
        updated = current.model_copy(
            update={
                "lifecycle_status": (
                    PluginLifecycleStatus.HEALTHY
                    if health.healthy
                    else PluginLifecycleStatus.UNHEALTHY
                ),
                "last_healthcheck_at": health.checked_at,
                "health_message": health.message,
            }
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="PLUGIN_HEALTH_CHECKED",
            actor=actor,
            payload={
                "plugin": updated.model_dump(mode="json"),
                "health": health.model_dump(mode="json"),
            },
            epistemic_delta=f"Plugin {plugin_id} health was checked.",
            epistemic_delta_type=EpistemicDeltaType.NO_STATE_CHANGE,
        )
        projection = self._projection(project_id)
        projection.apply(event)
        self._write_plugins_lock(project_id, projection.list_project_plugins())
        return health

    def enable_plugin(self, project_id: UUID, plugin_id: str, actor: Actor) -> ProjectPluginRecord:
        self.get_project(project_id)
        if actor.type != ActorType.HUMAN:
            raise ConflictError("plugin enablement requires a human actor")
        manifest = self._require_plugin_manifest(plugin_id)
        if not self.settings.allow_local_plugins and manifest.runner_type.value in {
            "python",
            "local_command",
        }:
            raise ConflictError(
                "local process plugins are disabled by deployment policy; use a digest-pinned OCI runner"
            )
        current = self._projection(project_id).get_project_plugin(plugin_id)
        if current is None or current.lifecycle_status == PluginLifecycleStatus.UNINSTALLED:
            self.install_plugin(
                project_id,
                plugin_id,
                PluginInstallRequest(expected_version=manifest.version, actor=actor),
            )
        if plugin_id == "python.local":
            runner = self._python_runner()
            runner.ensure_environment()
        health = self.check_plugin_health(project_id, plugin_id, actor)
        if not health.healthy:
            raise ConflictError(f"plugin is not healthy: {health.message}")
        current = self._projection(project_id).get_project_plugin(plugin_id)
        assert current is not None
        record = ProjectPluginRecord(
            plugin_id=manifest.plugin_id,
            version=manifest.version,
            enabled=True,
            lifecycle_status=PluginLifecycleStatus.ENABLED_FOR_PROJECT,
            installed_at=current.installed_at,
            enabled_at=utc_now(),
            last_healthcheck_at=health.checked_at,
            health_message=health.message,
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="PLUGIN_ENABLED",
            actor=actor,
            payload={
                "plugin": record.model_dump(mode="json"),
                "manifest": manifest.model_dump(mode="json"),
            },
            epistemic_delta=f"Optional plugin {plugin_id} was enabled for this project.",
            epistemic_delta_type=EpistemicDeltaType.NO_STATE_CHANGE,
        )
        projection = self._projection(project_id)
        projection.apply(event)
        self._write_plugins_lock(project_id, projection.list_project_plugins())
        self._touch_manifest(project_id)
        return record

    def disable_plugin(self, project_id: UUID, plugin_id: str, actor: Actor) -> ProjectPluginRecord:
        plugin = self._projection(project_id).get_project_plugin(plugin_id)
        if plugin is None:
            raise NotFoundError(f"project plugin {plugin_id} not found")
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="PLUGIN_DISABLED",
            actor=actor,
            payload={
                "plugin_id": plugin_id,
                "plugin": plugin.model_copy(
                    update={
                        "enabled": False,
                        "lifecycle_status": PluginLifecycleStatus.DISABLED,
                    }
                ).model_dump(mode="json"),
            },
            epistemic_delta=f"Optional plugin {plugin_id} was disabled for this project.",
            epistemic_delta_type=EpistemicDeltaType.NO_STATE_CHANGE,
        )
        projection = self._projection(project_id)
        projection.apply(event)
        self._write_plugins_lock(project_id, projection.list_project_plugins())
        self._touch_manifest(project_id)
        updated = projection.get_project_plugin(plugin_id)
        assert updated is not None
        return updated

    def uninstall_plugin(
        self, project_id: UUID, plugin_id: str, actor: Actor
    ) -> ProjectPluginRecord:
        if actor.type != ActorType.HUMAN:
            raise ConflictError("plugin uninstall requires a human actor")
        current = self._projection(project_id).get_project_plugin(plugin_id)
        if current is None:
            raise NotFoundError(f"project plugin {plugin_id} not found")
        if current.enabled:
            raise ConflictError("disable the plugin before uninstalling it")
        updated = current.model_copy(
            update={
                "enabled": False,
                "lifecycle_status": PluginLifecycleStatus.UNINSTALLED,
            }
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="PLUGIN_UNINSTALLED",
            actor=actor,
            payload={"plugin": updated.model_dump(mode="json")},
            epistemic_delta=(
                f"Plugin {plugin_id} was removed from the project lock. "
                "Historical runs and artifacts remain immutable."
            ),
            epistemic_delta_type=EpistemicDeltaType.NO_STATE_CHANGE,
        )
        projection = self._projection(project_id)
        projection.apply(event)
        self._write_plugins_lock(project_id, projection.list_project_plugins())
        self._touch_manifest(project_id)
        return updated

    def list_project_plugins(self, project_id: UUID) -> list[ProjectPluginRecord]:
        self.get_project(project_id)
        return self._projection(project_id).list_project_plugins()

    def run_python_plugin(
        self, project_id: UUID, request: PythonPluginRunRequest
    ) -> PluginRunRecord:
        self.get_project(project_id)
        if not self.settings.allow_local_plugins:
            raise ConflictError("python.local is disabled by deployment policy")
        plugin = self._projection(project_id).get_project_plugin("python.local")
        if plugin is None or not plugin.enabled:
            raise ConflictError("python.local must be enabled before running it")
        route_id, branch_id = self._normalize_optional_target(
            project_id, request.route_id, request.branch_id
        )
        input_files: list[tuple[str, bytes]] = []
        input_refs: list[str] = []
        for artifact_id in request.input_artifact_ids:
            artifact, content = self.artifact_bytes(project_id, artifact_id)
            input_files.append((f"{artifact_id}-{artifact.original_filename}", content))
            input_refs.append(str(artifact_id))

        run_id = uuid4()
        run_dir = self.project_dir(project_id) / "runs" / str(run_id)
        source_artifact = self.add_artifact(
            project_id=project_id,
            filename=f"python-run-{run_id}.py",
            content=request.source_code.encode("utf-8"),
            artifact_type=ArtifactType.CODE,
            origin=ArtifactOrigin.HUMAN,
            media_type="text/x-python",
            interpretation_status=InterpretationStatus.RAW,
            actor=request.actor,
            source_ref=f"plugin-run:{run_id}:source",
        )
        runner = self._python_runner()
        started_at = utc_now()
        started_event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="PLUGIN_RUN_STARTED",
            actor=request.actor,
            route_id=route_id,
            branch_id=branch_id,
            artifact_refs=[str(source_artifact.artifact_id), *input_refs],
            payload={
                "run_id": str(run_id),
                "plugin_id": "python.local",
                "plugin_version": runner.plugin_version,
                "timeout_seconds": request.timeout_seconds,
                "source_artifact_ref": str(source_artifact.artifact_id),
                "input_artifact_refs": input_refs,
            },
            epistemic_delta=(
                "A local Python experiment started. This event records intent and "
                "inputs even if the host process ends before a completion event."
            ),
        )
        self._projection(project_id).apply(started_event)
        outcome = runner.execute(
            project_id=project_id,
            run_id=run_id,
            run_dir=run_dir,
            source_code=request.source_code,
            stdin_text=request.stdin,
            arguments=request.arguments,
            timeout_seconds=request.timeout_seconds,
            input_files=input_files,
        )
        tool_actor = Actor(
            type=ActorType.TOOL,
            id="python.local",
            display_name="Local Python Experiment Runner",
        )
        stdout_artifact = self.add_artifact(
            project_id=project_id,
            filename=f"python-run-{run_id}.stdout.log",
            content=outcome.stdout_path.read_bytes() if outcome.stdout_path.exists() else b"",
            artifact_type=ArtifactType.EXECUTION_LOG,
            origin=ArtifactOrigin.PLUGIN,
            media_type="text/plain",
            interpretation_status=InterpretationStatus.RAW,
            actor=tool_actor,
            source_ref=f"plugin-run:{run_id}:stdout",
        )
        stderr_artifact = self.add_artifact(
            project_id=project_id,
            filename=f"python-run-{run_id}.stderr.log",
            content=outcome.stderr_path.read_bytes() if outcome.stderr_path.exists() else b"",
            artifact_type=ArtifactType.EXECUTION_LOG,
            origin=ArtifactOrigin.PLUGIN,
            media_type="text/plain",
            interpretation_status=InterpretationStatus.RAW,
            actor=tool_actor,
            source_ref=f"plugin-run:{run_id}:stderr",
        )
        produced_refs: list[str] = []
        for path in outcome.output_files:
            artifact = self.add_artifact(
                project_id=project_id,
                filename=path.name,
                content=path.read_bytes(),
                artifact_type=ArtifactType.OTHER,
                origin=ArtifactOrigin.PLUGIN,
                media_type=mimetypes.guess_type(path.name)[0],
                interpretation_status=InterpretationStatus.RAW,
                actor=tool_actor,
                source_ref=f"plugin-run:{run_id}:output:{path.name}",
            )
            produced_refs.append(str(artifact.artifact_id))
        completed_at = utc_now()
        record = PluginRunRecord(
            run_id=run_id,
            project_id=project_id,
            plugin_id="python.local",
            plugin_version=runner.plugin_version,
            route_id=route_id,
            branch_id=branch_id,
            status=outcome.status,
            command=outcome.command,
            runtime_version=outcome.runtime_version,
            isolation_level=runner.isolation_level,
            timeout_seconds=request.timeout_seconds,
            exit_code=outcome.exit_code,
            source_artifact_ref=str(source_artifact.artifact_id),
            input_artifact_refs=input_refs,
            stdout_artifact_ref=str(stdout_artifact.artifact_id),
            stderr_artifact_ref=str(stderr_artifact.artifact_id),
            produced_artifact_refs=produced_refs,
            output_truncated=outcome.output_truncated,
            started_at=started_at,
            completed_at=completed_at,
            error=outcome.error,
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="PLUGIN_RUN_COMPLETED",
            actor=tool_actor,
            route_id=route_id,
            branch_id=branch_id,
            artifact_refs=[
                str(source_artifact.artifact_id),
                str(stdout_artifact.artifact_id),
                str(stderr_artifact.artifact_id),
                *produced_refs,
            ],
            payload={"plugin_run": record.model_dump(mode="json")},
            epistemic_delta=(
                f"python.local run ended as {record.status.value}. "
                "Successful and failed runs are both retained as experiment evidence."
            ),
        )
        self._projection(project_id).apply(event)
        self._touch_manifest(project_id)
        return record

    def list_plugin_runs(self, project_id: UUID) -> list[PluginRunRecord]:
        self.get_project(project_id)
        return self._projection(project_id).list_plugin_runs()

    def run_plugin(
        self, project_id: UUID, plugin_id: str, request: GenericPluginRunRequest
    ) -> PluginRunRecord:
        self.get_project(project_id)
        manifest = self._require_plugin_manifest(plugin_id)
        if not self.settings.allow_local_plugins and manifest.runner_type.value in {
            "python",
            "local_command",
        }:
            raise ConflictError("local process plugins are disabled by deployment policy")
        if manifest.runner_type.value == "python":
            raise ConflictError(
                "python.local keeps its backward-compatible structured run endpoint"
            )
        project_plugin = self._projection(project_id).get_project_plugin(plugin_id)
        if project_plugin is None or not project_plugin.enabled:
            raise ConflictError(f"{plugin_id} must be enabled before running it")
        route_id, branch_id = self._normalize_optional_target(
            project_id, request.route_id, request.branch_id
        )
        input_refs: list[str] = []
        for artifact_id in request.input_artifact_ids:
            self._require_artifact(project_id, artifact_id)
            input_refs.append(str(artifact_id))

        run_id = uuid4()
        run_dir = self.project_dir(project_id) / "runs" / str(run_id)
        source_artifact = self.add_artifact(
            project_id=project_id,
            filename=request.input_filename,
            content=request.input_text.encode("utf-8"),
            artifact_type=ArtifactType.TEXT,
            origin=ArtifactOrigin.HUMAN,
            media_type=mimetypes.guess_type(request.input_filename)[0] or "text/plain",
            interpretation_status=InterpretationStatus.RAW,
            actor=request.actor,
            source_ref=f"plugin-run:{run_id}:input",
        )
        started_at = utc_now()
        started_event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="PLUGIN_RUN_STARTED",
            actor=request.actor,
            route_id=route_id,
            branch_id=branch_id,
            artifact_refs=[str(source_artifact.artifact_id), *input_refs],
            payload={
                "run_id": str(run_id),
                "plugin_id": plugin_id,
                "plugin_version": manifest.version,
                "timeout_seconds": request.timeout_seconds,
            },
            epistemic_delta=f"A {plugin_id} experiment started.",
            epistemic_delta_type=EpistemicDeltaType.NO_STATE_CHANGE,
        )
        self._projection(project_id).apply(started_event)
        outcome = self._plugin_host().execute(
            manifest=manifest,
            run_dir=run_dir,
            input_filename=request.input_filename,
            input_bytes=request.input_text.encode("utf-8"),
            arguments=request.arguments,
            timeout_seconds=request.timeout_seconds,
        )
        tool_actor = Actor(
            type=ActorType.TOOL,
            id=plugin_id,
            display_name=manifest.name,
        )
        stdout_artifact = self.add_artifact(
            project_id=project_id,
            filename=f"{plugin_id}-{run_id}.stdout.log",
            content=(outcome.stdout_path.read_bytes() if outcome.stdout_path.exists() else b""),
            artifact_type=ArtifactType.EXECUTION_LOG,
            origin=ArtifactOrigin.PLUGIN,
            media_type="text/plain",
            interpretation_status=InterpretationStatus.RAW,
            actor=tool_actor,
            source_ref=f"plugin-run:{run_id}:stdout",
        )
        stderr_artifact = self.add_artifact(
            project_id=project_id,
            filename=f"{plugin_id}-{run_id}.stderr.log",
            content=(outcome.stderr_path.read_bytes() if outcome.stderr_path.exists() else b""),
            artifact_type=ArtifactType.EXECUTION_LOG,
            origin=ArtifactOrigin.PLUGIN,
            media_type="text/plain",
            interpretation_status=InterpretationStatus.RAW,
            actor=tool_actor,
            source_ref=f"plugin-run:{run_id}:stderr",
        )
        produced_refs: list[str] = []
        for path in outcome.output_files:
            media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            artifact = self.add_artifact(
                project_id=project_id,
                filename=path.name,
                content=path.read_bytes(),
                artifact_type=(
                    ArtifactType.GRAPH if media_type == "image/svg+xml" else ArtifactType.OTHER
                ),
                origin=ArtifactOrigin.PLUGIN,
                media_type=media_type,
                interpretation_status=InterpretationStatus.RAW,
                actor=tool_actor,
                source_ref=f"plugin-run:{run_id}:output:{path.name}",
            )
            produced_refs.append(str(artifact.artifact_id))
        record = PluginRunRecord(
            run_id=run_id,
            project_id=project_id,
            plugin_id=plugin_id,
            plugin_version=manifest.version,
            route_id=route_id,
            branch_id=branch_id,
            status=outcome.status,
            command=outcome.command,
            runtime_version=outcome.runtime_version,
            isolation_level=manifest.isolation_level,
            timeout_seconds=request.timeout_seconds,
            exit_code=outcome.exit_code,
            source_artifact_ref=str(source_artifact.artifact_id),
            input_artifact_refs=input_refs,
            stdout_artifact_ref=str(stdout_artifact.artifact_id),
            stderr_artifact_ref=str(stderr_artifact.artifact_id),
            produced_artifact_refs=produced_refs,
            output_truncated=outcome.output_truncated,
            started_at=started_at,
            completed_at=utc_now(),
            error=outcome.error,
        )
        completed_event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="PLUGIN_RUN_COMPLETED",
            actor=tool_actor,
            route_id=route_id,
            branch_id=branch_id,
            artifact_refs=[
                str(source_artifact.artifact_id),
                str(stdout_artifact.artifact_id),
                str(stderr_artifact.artifact_id),
                *produced_refs,
            ],
            payload={"plugin_run": record.model_dump(mode="json")},
            epistemic_delta=(
                f"{plugin_id} ended as {record.status.value}; all observable output "
                "was retained without a mathematical-success claim."
            ),
            epistemic_delta_type=(
                EpistemicDeltaType.TOOL_EVIDENCE_ADDED
                if produced_refs
                else EpistemicDeltaType.NO_STATE_CHANGE
            ),
        )
        self._projection(project_id).apply(completed_event)
        self._touch_manifest(project_id)
        return record

    # ------------------------------------------------------------------
    # Model sessions, handoffs and arena recipes
    # ------------------------------------------------------------------

    def create_model_session(
        self, project_id: UUID, request: ModelSessionCreate
    ) -> ModelSessionRecord:
        route_id, branch_id = self._normalize_optional_target(
            project_id, request.route_id, request.branch_id
        )
        record = ModelSessionRecord(
            session_id=uuid4(),
            project_id=project_id,
            connector_type=request.connector_type,
            display_label=request.display_label,
            reported_model=request.reported_model,
            model_family=request.model_family,
            role=request.role,
            context_packet_refs=request.context_packet_refs,
            output_artifact_refs=request.output_artifact_refs,
            completeness=request.completeness,
            route_id=route_id,
            branch_id=branch_id,
            notes=request.notes,
            created_at=utc_now(),
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="MODEL_SESSION_CREATED",
            actor=request.actor,
            route_id=route_id,
            branch_id=branch_id,
            artifact_refs=request.output_artifact_refs,
            payload={"model_session": record.model_dump(mode="json")},
            epistemic_delta=(
                "A visible model or tool session was recorded. The record does not "
                "claim access to hidden model reasoning."
            ),
            epistemic_delta_type=EpistemicDeltaType.SESSION_RECORDED,
        )
        self._projection(project_id).apply(event)
        self._touch_manifest(project_id)
        return record

    def list_model_sessions(self, project_id: UUID) -> list[ModelSessionRecord]:
        self.get_project(project_id)
        return self._projection(project_id).list_model_sessions()

    def create_handoff_artifact(
        self, project_id: UUID, request: HandoffArtifactCreate
    ) -> HandoffArtifactRecord:
        projection = self._projection(project_id)
        if projection.get_model_session(str(request.producing_session_ref)) is None:
            raise NotFoundError("producing model session not found")
        for session_id in request.receiving_session_refs:
            if projection.get_model_session(str(session_id)) is None:
                raise NotFoundError(f"receiving model session {session_id} not found")
        route_id, branch_id = self._normalize_optional_target(
            project_id, request.route_id, request.branch_id
        )
        record = HandoffArtifactRecord(
            handoff_id=uuid4(),
            project_id=project_id,
            producing_session_ref=request.producing_session_ref,
            receiving_session_refs=request.receiving_session_refs,
            artifact_type=request.artifact_type,
            established_facts=request.established_facts,
            rejected_directions=request.rejected_directions,
            unresolved_items=request.unresolved_items,
            artifact_refs=request.artifact_refs,
            receiving_impact=request.receiving_impact,
            route_id=route_id,
            branch_id=branch_id,
            created_at=utc_now(),
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="HANDOFF_CREATED",
            actor=request.actor,
            route_id=route_id,
            branch_id=branch_id,
            artifact_refs=request.artifact_refs,
            payload={"handoff": record.model_dump(mode="json")},
            epistemic_delta=(
                "A cross-session handoff preserved established facts, rejected "
                "directions and unresolved obligations without promoting them to proof."
            ),
            epistemic_delta_type=EpistemicDeltaType.HANDOFF_REUSED,
        )
        projection.apply(event)
        self._touch_manifest(project_id)
        return record

    def list_handoff_artifacts(self, project_id: UUID) -> list[HandoffArtifactRecord]:
        self.get_project(project_id)
        return self._projection(project_id).list_handoff_artifacts()

    def create_arena_recipe(
        self, project_id: UUID, request: ArenaRecipeCreate
    ) -> ArenaRecipeRecord:
        self.get_project(project_id)
        if request.parallel_workers > 0 and request.actor.type != ActorType.HUMAN:
            raise ConflictError("parallel arena capacity requires human confirmation")
        if request.compute_mode.value == "conservative" and request.parallel_workers != 0:
            raise ConflictError("conservative arena recipes must default to zero workers")
        record = ArenaRecipeRecord(
            recipe_id=uuid4(),
            project_id=project_id,
            name=request.name,
            description=request.description,
            compute_mode=request.compute_mode,
            parallel_workers=request.parallel_workers,
            stages=request.stages,
            created_at=utc_now(),
        )
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="ARENA_RECIPE_CREATED",
            actor=request.actor,
            payload={"arena_recipe": record.model_dump(mode="json")},
            epistemic_delta=(
                "An arena recipe was saved for preview. No sessions were started and "
                "role agreement does not determine mathematical status."
            ),
            epistemic_delta_type=EpistemicDeltaType.NO_STATE_CHANGE,
        )
        self._projection(project_id).apply(event)
        self._touch_manifest(project_id)
        return record

    def list_arena_recipes(self, project_id: UUID) -> list[ArenaRecipeRecord]:
        self.get_project(project_id)
        return self._projection(project_id).list_arena_recipes()

    def preview_arena_recipe(self, project_id: UUID, recipe_id: UUID) -> ArenaPreviewRecord:
        projection = self._projection(project_id)
        recipe = projection.get_arena_recipe(str(recipe_id))
        if recipe is None:
            raise NotFoundError(f"arena recipe {recipe_id} not found")
        session_by_id = {
            str(session.session_id): session for session in projection.list_model_sessions()
        }
        family_stages: dict[str, list[str]] = {}
        for stage in recipe.stages:
            session = session_by_id.get(stage.connector_id or "")
            if session and session.model_family:
                family_stages.setdefault(session.model_family, []).append(stage.stage_id)
        warnings = [
            (
                f"Stages {', '.join(stage_ids)} use the same reported model family "
                f"'{family}' and are correlated reviews, not independent verification."
            )
            for family, stage_ids in family_stages.items()
            if len(stage_ids) > 1
        ]
        return ArenaPreviewRecord(
            recipe=recipe,
            requires_human_confirmation=(
                recipe.parallel_workers > 0
                or any(not stage.human_gate_after for stage in recipe.stages)
            ),
            correlated_review_warnings=warnings,
        )

    # ------------------------------------------------------------------
    # Epistemic deltas, historical retrieval and immutable visual snapshots
    # ------------------------------------------------------------------

    def epistemic_deltas(
        self, project_id: UUID, *, limit: int = 100
    ) -> list[EpistemicDeltaSummary]:
        events = self.list_events(project_id)
        summaries: list[EpistemicDeltaSummary] = []
        for event in events:
            delta_type = event.epistemic_delta_type or self._infer_delta_type(event.event_type)
            if delta_type == EpistemicDeltaType.NO_STATE_CHANGE:
                continue
            summaries.append(
                EpistemicDeltaSummary(
                    event_id=event.event_id,
                    event_type=event.event_type,
                    delta_type=delta_type,
                    description=event.epistemic_delta or event.event_type,
                    timestamp=event.timestamp,
                    route_id=event.route_id,
                    branch_id=event.branch_id,
                )
            )
        return summaries[-limit:]

    def search_history(
        self, project_id: UUID, query: str, *, limit: int = 50
    ) -> list[HistoricalSearchHit]:
        self.get_project(project_id)
        normalized = " ".join(query.casefold().split())
        if not normalized:
            return []
        projection = self._projection(project_id)
        hits: list[HistoricalSearchHit] = []

        def add_hit(
            *,
            kind: str,
            object_id: str,
            title: str,
            body: str,
            created_at,
            route_id=None,
            branch_id=None,
            reopen_conditions: list[str] | None = None,
        ) -> None:
            haystack = f"{title}\n{body}".casefold()
            ratio = SequenceMatcher(None, normalized, haystack[:2000]).ratio()
            occurrences = haystack.count(normalized)
            token_matches = sum(1 for token in normalized.split() if token in haystack)
            score = occurrences * 4.0 + token_matches + ratio
            if score <= ratio and ratio < 0.18:
                return
            hits.append(
                HistoricalSearchHit(
                    kind=kind,
                    object_id=object_id,
                    title=title,
                    excerpt=body[:600],
                    route_id=route_id,
                    branch_id=branch_id,
                    created_at=created_at,
                    score=round(score, 4),
                    reopen_conditions=reopen_conditions or [],
                )
            )

        for route in projection.list_routes():
            add_hit(
                kind="route",
                object_id=str(route.route_id),
                title=route.title,
                body="\n".join(
                    [
                        route.description,
                        *route.objections,
                        *route.revival_conditions,
                    ]
                ),
                route_id=route.route_id,
                created_at=route.created_at,
                reopen_conditions=route.revival_conditions,
            )
        for challenge in projection.list_challenges():
            add_hit(
                kind="challenge",
                object_id=str(challenge.challenge_id),
                title=challenge.challenge_type.value,
                body=f"{challenge.statement}\n{challenge.test_plan}\n{challenge.resolution_summary}",
                route_id=challenge.route_id,
                branch_id=challenge.branch_id,
                created_at=challenge.created_at,
            )
        for bridge in projection.list_bridge_results():
            add_hit(
                kind="bridge_result",
                object_id=str(bridge.bridge_result_id),
                title=bridge.title,
                body=f"{bridge.summary}\n" + "\n".join(bridge.retained_value),
                route_id=bridge.route_id,
                branch_id=bridge.branch_id,
                created_at=bridge.created_at,
            )
        for dead_end in projection.list_dead_end_constraints():
            add_hit(
                kind="dead_end",
                object_id=str(dead_end.dead_end_id),
                title=dead_end.title,
                body="\n".join(
                    [
                        dead_end.description,
                        *dead_end.applicability_scope,
                        *dead_end.reopen_conditions,
                    ]
                ),
                route_id=dead_end.route_id,
                branch_id=dead_end.branch_id,
                created_at=dead_end.created_at,
                reopen_conditions=dead_end.reopen_conditions,
            )
        for handoff in projection.list_handoff_artifacts():
            add_hit(
                kind="handoff",
                object_id=str(handoff.handoff_id),
                title=handoff.artifact_type.value,
                body="\n".join(
                    [
                        *handoff.established_facts,
                        *handoff.rejected_directions,
                        *handoff.unresolved_items,
                        handoff.receiving_impact,
                    ]
                ),
                route_id=handoff.route_id,
                branch_id=handoff.branch_id,
                created_at=handoff.created_at,
            )
        return sorted(hits, key=lambda item: (item.score, item.created_at), reverse=True)[:limit]

    def create_canvas_snapshot(
        self, project_id: UUID, request: CanvasSnapshotCreate
    ) -> CanvasSnapshotRecord:
        self.get_project(project_id)
        if (
            request.mapping_status == VisualMappingStatus.CONFIRMED
            and request.actor.type != ActorType.HUMAN
        ):
            raise ConflictError("only a human actor may confirm a visual mapping")
        visual_id = uuid4()
        scene_bytes = json.dumps(request.scene, ensure_ascii=False, sort_keys=True).encode("utf-8")
        scene_artifact = self.add_artifact(
            project_id=project_id,
            filename=f"canvas-{visual_id}.excalidraw",
            content=scene_bytes,
            artifact_type=ArtifactType.HAND_DRAWING,
            origin=(
                ArtifactOrigin.HUMAN
                if request.actor.type == ActorType.HUMAN
                else ArtifactOrigin.MODEL
            ),
            media_type="application/vnd.excalidraw+json",
            interpretation_status=InterpretationStatus.RAW,
            actor=request.actor,
            source_ref=f"visual:{visual_id}:original",
        )
        interpretation_ref: str | None = None
        if request.machine_interpretation:
            interpretation = self.add_artifact(
                project_id=project_id,
                filename=f"canvas-{visual_id}-machine-interpretation.txt",
                content=request.machine_interpretation.encode("utf-8"),
                artifact_type=ArtifactType.TEXT,
                origin=ArtifactOrigin.DERIVED,
                media_type="text/plain",
                interpretation_status=InterpretationStatus.INTERPRETED,
                actor=request.actor,
                source_ref=f"visual:{visual_id}:machine-interpretation",
            )
            interpretation_ref = str(interpretation.artifact_id)
        record = CanvasSnapshotRecord(
            visual_id=visual_id,
            project_id=project_id,
            original_artifact_ref=str(scene_artifact.artifact_id),
            author_description=request.author_description,
            machine_interpretation=request.machine_interpretation,
            machine_interpretation_ref=interpretation_ref,
            mapping_status=request.mapping_status,
            element_links=request.element_links,
            created_at=utc_now(),
            confirmed_by=(
                request.actor.id
                if request.mapping_status == VisualMappingStatus.CONFIRMED
                else None
            ),
        )
        artifact_refs = [str(scene_artifact.artifact_id)]
        if interpretation_ref:
            artifact_refs.append(interpretation_ref)
        event = self._event_store(project_id).append(
            project_id=project_id,
            event_type="VISUAL_CANVAS_SNAPSHOT_CREATED",
            actor=request.actor,
            artifact_refs=artifact_refs,
            payload={"visual_artifact": record.model_dump(mode="json")},
            epistemic_delta=(
                "An immutable free-canvas snapshot was saved. Author description, "
                "machine interpretation and structured links remain distinct."
            ),
            epistemic_delta_type=EpistemicDeltaType.VISUAL_PATTERN_NOTED,
        )
        self._projection(project_id).apply(event)
        self._touch_manifest(project_id)
        return record

    def list_canvas_snapshots(self, project_id: UUID) -> list[CanvasSnapshotRecord]:
        self.get_project(project_id)
        return self._projection(project_id).list_visual_artifacts()

    def latest_canvas_snapshot(self, project_id: UUID) -> CanvasSnapshotResponse | None:
        snapshots = self.list_canvas_snapshots(project_id)
        if not snapshots:
            return None
        record = snapshots[-1]
        artifact, content = self.artifact_bytes(project_id, UUID(record.original_artifact_ref))
        del artifact
        return CanvasSnapshotResponse(
            visual_artifact=record,
            scene=json.loads(content.decode("utf-8")),
        )

    # ------------------------------------------------------------------
    # Research packet, integrity and portability
    # ------------------------------------------------------------------

    def build_research_packet(
        self, project_id: UUID, request: ResearchPacketRequest
    ) -> ResearchPacketResponse:
        project = self.get_project(project_id)
        routes = self.list_routes(project_id)
        selected_ids = set(request.route_ids)
        selected_routes = (
            [route for route in routes if route.route_id in selected_ids]
            if selected_ids
            else routes
        )
        branches = self.list_branches(project_id)
        challenges = self.list_challenges(project_id)
        bridges = self.list_bridge_results(project_id)
        dead_ends = self.list_dead_end_constraints(project_id)
        checkpoints = self.list_checkpoints(project_id)
        events = self.list_events(project_id)
        recent_events = (
            events[-request.include_recent_events :] if request.include_recent_events else []
        )
        recent_checkpoints = (
            checkpoints[-request.include_checkpoints :] if request.include_checkpoints else []
        )

        lines: list[str] = [
            f"# ProofFlow Research Packet: {project.title}",
            "",
            f"Generated: {utc_now().isoformat()}",
            "",
            "## Purpose",
            request.purpose,
            "",
            "## Original Problem (immutable source record)",
            project.original_problem.source_text,
        ]
        if project.original_problem.source_uri:
            lines.extend(["", f"Source: {project.original_problem.source_uri}"])
        if project.original_problem.author_notes:
            lines.extend(["", "### Researcher Notes", project.original_problem.author_notes])
        if project.original_problem.definitions:
            lines.extend(
                ["", "### Definitions", *[f"- {x}" for x in project.original_problem.definitions]]
            )
        if project.original_problem.assumptions:
            lines.extend(
                ["", "### Assumptions", *[f"- {x}" for x in project.original_problem.assumptions]]
            )

        lines.extend(["", "## Open Challenges"])
        open_challenges = [
            item
            for item in challenges
            if item.status
            in {ChallengeStatus.OPEN, ChallengeStatus.TESTING, ChallengeStatus.DEFERRED}
        ]
        if not open_challenges:
            lines.append("- No open challenges are currently recorded.")
        else:
            for challenge in open_challenges:
                target = f" route={challenge.route_id}" if challenge.route_id else ""
                if challenge.branch_id:
                    target += f" branch={challenge.branch_id}"
                lines.append(
                    f"- [{challenge.status.value}]{target} {challenge.statement}"
                    + (f" Test: {challenge.test_plan}" if challenge.test_plan else "")
                )

        lines.extend(["", "## Research Routes"])
        if not selected_routes:
            lines.append("- No routes have been created yet.")
        for route in selected_routes:
            lines.extend(
                [
                    "",
                    f"### {route.title} [{route.state.value}]",
                    route.description or "(No route description.)",
                ]
            )
            route_branches = [item for item in branches if item.route_id == route.route_id]
            if route_branches:
                lines.append("\nBranches:")
                for branch in route_branches:
                    lines.append(
                        f"- {branch.title} [{branch.state.value}]: "
                        f"{branch.description or '(no description)'}"
                    )
            route_challenges = [item for item in challenges if item.route_id == route.route_id]
            if route_challenges:
                lines.append("\nChallenges:")
                for challenge in route_challenges:
                    lines.append(
                        f"- [{challenge.status.value}] {challenge.statement}"
                        + (f" Test: {challenge.test_plan}" if challenge.test_plan else "")
                    )
            route_dead_ends = [item for item in dead_ends if item.route_id == route.route_id]
            if route_dead_ends:
                lines.append("\nKnown dead ends (deprioritization, not automatic deletion):")
                for item in route_dead_ends:
                    reopen = "; ".join(item.reopen_conditions) or "new evidence"
                    lines.append(
                        f"- [{item.strength.value}] {item.title}: {item.description}; "
                        f"reopen on {reopen}"
                    )

        if bridges:
            lines.extend(["", "## Bridge Results"])
            for item in bridges:
                lines.append(f"- {item.title}: {item.summary}")

        if recent_checkpoints:
            lines.extend(["", "## Structured Research Checkpoints"])
            for checkpoint in recent_checkpoints:
                lines.extend(
                    [
                        "",
                        f"### {checkpoint.created_at.isoformat()}",
                        f"Target: {checkpoint.current_target}",
                        f"Intended move: {checkpoint.intended_move or '(not stated)'}",
                        f"Expected result: {checkpoint.expected_result or '(not stated)'}",
                        f"Observed failure/gain: {checkpoint.observed_failure_or_gain or '(not stated)'}",
                        f"Confidence: {checkpoint.confidence.value}",
                    ]
                )
                if checkpoint.unresolved_obligations:
                    lines.extend(
                        [
                            "Unresolved obligations:",
                            *[f"- {x}" for x in checkpoint.unresolved_obligations],
                        ]
                    )

        lines.extend(["", "## Recent Observable Research Events"])
        if not recent_events:
            lines.append("- No recent events.")
        for event in recent_events:
            delta = event.epistemic_delta or event.event_type
            route_suffix = f" route={event.route_id}" if event.route_id else ""
            branch_suffix = f" branch={event.branch_id}" if event.branch_id else ""
            lines.append(
                f"- {event.timestamp.isoformat()} | {event.actor.type.value}:{event.actor.id}"
                f" | {event.event_type}{route_suffix}{branch_suffix} | {delta}"
            )

        lines.extend(
            [
                "",
                "## Working Constitution",
                "- Do not force a complete solution.",
                "- Raise objections freely, but do not close a route without strong evidence.",
                "- Distinguish a conjecture, candidate argument, finite test, formal target, and reviewed result.",
                "- Preserve failed routes, bridge results, and open obligations.",
                "- State what changed in the research state, not merely what was written.",
            ]
        )
        if request.special_instructions:
            lines.extend(["", "## Researcher Instructions", request.special_instructions])
        lines.extend(
            [
                "",
                "## Requested Output Format",
                "Return a visible research checkpoint with:",
                "1. current target and route;",
                "2. assumptions used;",
                "3. proposed move;",
                "4. produced artifact or obstruction;",
                "5. unresolved obligations;",
                "6. next non-equivalent routes.",
            ]
        )
        return ResearchPacketResponse(generated_at=utc_now(), markdown="\n".join(lines))

    def integrity_report(self, project_id: UUID) -> IntegrityReport:
        self.get_project(project_id)
        store = self._event_store(project_id)
        valid, index, error = store.verify_chain()
        return IntegrityReport(
            project_id=project_id,
            event_count=len(store.read_all()),
            valid=valid,
            projection_schema_version=self._projection(project_id).schema_version(),
            first_invalid_index=index,
            error=error,
        )

    def rebuild_projection(self, project_id: UUID) -> int:
        self.get_project(project_id)
        projection = self._projection(project_id)
        projection.reset()
        events = self._event_store(project_id).read_all()
        for event in events:
            projection.apply(event)
        return len(events)

    def export_project_zip(self, project_id: UUID) -> Path:
        project = self.get_project(project_id)
        export_dir = self.project_dir(project_id) / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        destination = export_dir / f"{project.project_id}.smath.zip"
        excluded_tops = {"database", "runs", "exports"}
        with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in self.project_dir(project_id).rglob("*"):
                if not path.is_file() or path == destination:
                    continue
                relative = path.relative_to(self.project_dir(project_id))
                if relative.parts and relative.parts[0] in excluded_tops:
                    continue
                archive.write(path, relative)
        return destination

    def preflight_project_zip(self, archive_path: Path) -> ImportPreflightReport:
        """Inspect an archive without touching the workspace or importing it.

        The report makes compatibility, chain-integrity and missing-artifact
        failures observable before an operator elects to import a project.
        """
        archive_name = archive_path.name
        archive_bytes = archive_path.stat().st_size if archive_path.exists() else 0
        errors: list[str] = []
        warnings: list[str] = []
        missing_artifact_paths: list[str] = []
        file_count = compressed_bytes = uncompressed_bytes = event_count = 0
        schema_version: str | None = None
        project_id: UUID | None = None
        event_chain_valid: bool | None = None
        first_invalid_event_index: int | None = None
        event_chain_error: str | None = None

        if not archive_path.is_file():
            errors.append("archive does not exist or is not a file")
        elif archive_bytes > self.settings.maximum_import_bytes:
            errors.append("archive exceeds configured import size limit")

        if not errors:
            try:
                with zipfile.ZipFile(archive_path, "r") as archive:
                    members = [member for member in archive.infolist() if not member.is_dir()]
                    file_count = len(members)
                    compressed_bytes = sum(member.compress_size for member in members)
                    uncompressed_bytes = sum(member.file_size for member in members)
                    if file_count > self.MAX_IMPORT_MEMBERS:
                        errors.append("archive contains too many files")
                    if uncompressed_bytes > self.MAX_IMPORT_UNCOMPRESSED_BYTES:
                        errors.append("archive exceeds uncompressed size limit")

                    member_names: set[str] = set()
                    for member in members:
                        normalized = member.filename.replace("\\", "/")
                        parts = tuple(part for part in normalized.split("/") if part)
                        mode = member.external_attr >> 16
                        if (
                            normalized.startswith("/")
                            or ":" in normalized
                            or ".." in parts
                            or stat.S_ISLNK(mode)
                        ):
                            errors.append(f"archive contains unsafe path: {member.filename}")
                        if normalized in member_names:
                            errors.append(f"archive contains duplicate path: {normalized}")
                        member_names.add(normalized)

                    if "project.json" not in member_names:
                        errors.append("archive is missing project.json")
                    if errors:
                        return ImportPreflightReport(
                            archive_name=archive_name,
                            archive_bytes=archive_bytes,
                            file_count=file_count,
                            compressed_bytes=compressed_bytes,
                            uncompressed_bytes=uncompressed_bytes,
                            missing_artifact_paths=missing_artifact_paths,
                            warnings=warnings,
                            errors=errors,
                            can_import=False,
                        )

                    manifest_member = archive.getinfo("project.json")
                    if manifest_member.file_size > self.MAX_IMPORT_MANIFEST_BYTES:
                        errors.append("project manifest exceeds the configured size limit")
                        return ImportPreflightReport(
                            archive_name=archive_name,
                            archive_bytes=archive_bytes,
                            file_count=file_count,
                            compressed_bytes=compressed_bytes,
                            uncompressed_bytes=uncompressed_bytes,
                            missing_artifact_paths=missing_artifact_paths,
                            warnings=warnings,
                            errors=errors,
                            can_import=False,
                        )

                    try:
                        manifest = ProjectManifest.model_validate_json(
                            archive.read("project.json").decode("utf-8")
                        )
                    except Exception as exc:
                        errors.append(f"invalid project manifest: {exc}")
                        manifest = None

                    if manifest is not None:
                        schema_version = manifest.schema_version
                        project_id = manifest.project_id
                        event_stream = manifest.event_stream.replace("\\", "/")
                        if event_stream not in member_names:
                            errors.append(f"archive is missing event stream: {event_stream}")
                        else:
                            with tempfile.TemporaryDirectory(
                                prefix="proofflow-preflight-"
                            ) as temp_dir:
                                events_path = Path(temp_dir) / "events.jsonl"
                                with archive.open(event_stream, "r") as source, events_path.open(
                                    "wb"
                                ) as target:
                                    shutil.copyfileobj(source, target, length=1024 * 1024)
                                store = EventStore(events_path)
                                try:
                                    events = store.read_all()
                                    event_count = len(events)
                                    for event in events:
                                        if event.project_id != manifest.project_id:
                                            errors.append(
                                                "event project_id does not match project manifest"
                                            )
                                            break
                                        if event.event_type == "ARTIFACT_ADDED":
                                            artifact = ArtifactRecord.model_validate(
                                                event.payload["artifact"]
                                            )
                                            if artifact.blob_relpath not in member_names:
                                                missing_artifact_paths.append(artifact.blob_relpath)
                                    (
                                        event_chain_valid,
                                        first_invalid_event_index,
                                        event_chain_error,
                                    ) = store.verify_chain()
                                    if not event_chain_valid:
                                        errors.append("event hash chain is invalid")
                                except Exception as exc:
                                    errors.append(f"invalid event stream: {exc}")
                        if manifest.schema_version != SCHEMA_VERSION:
                            warnings.append(
                                f"archive schema {manifest.schema_version} will be projected by {SCHEMA_VERSION}"
                            )
            except (OSError, zipfile.BadZipFile) as exc:
                errors.append(f"cannot read archive: {exc}")

        if missing_artifact_paths:
            errors.append("archive is missing content-addressed artifact blobs")
        return ImportPreflightReport(
            archive_name=archive_name,
            archive_bytes=archive_bytes,
            file_count=file_count,
            compressed_bytes=compressed_bytes,
            uncompressed_bytes=uncompressed_bytes,
            schema_version=schema_version,
            project_id=project_id,
            event_count=event_count,
            event_chain_valid=event_chain_valid,
            first_invalid_event_index=first_invalid_event_index,
            event_chain_error=event_chain_error,
            missing_artifact_paths=missing_artifact_paths,
            warnings=warnings,
            errors=errors,
            can_import=not errors,
        )

    def import_project_zip(self, archive_path: Path) -> ProjectManifest:
        preflight = self.preflight_project_zip(archive_path)
        if not preflight.can_import:
            detail = "; ".join(preflight.errors)
            raise ConflictError(f"archive preflight failed: {detail}")
        with tempfile.TemporaryDirectory(prefix="schemamath-import-") as temp_dir:
            temp_path = Path(temp_dir)
            with zipfile.ZipFile(archive_path, "r") as archive:
                for member in archive.infolist():
                    target = (temp_path / member.filename).resolve()
                    if not target.is_relative_to(temp_path.resolve()):
                        raise ConflictError("archive contains an unsafe path")
                archive.extractall(temp_path)
            manifest_path = temp_path / "project.json"
            if not manifest_path.exists():
                raise ConflictError("archive is missing project.json")
            manifest = ProjectManifest.model_validate_json(
                manifest_path.read_text(encoding="utf-8")
            )
            destination = self.project_dir(manifest.project_id)
            if destination.exists():
                raise ConflictError(f"project {manifest.project_id} already exists")
            staging = self.settings.workspace_root / (
                f".{manifest.project_id}.smath.importing-{uuid4().hex}"
            )
            try:
                shutil.copytree(temp_path, staging)
                projection = ProjectionStore(staging / "database" / "projections.sqlite3")
                projection.reset()
                events = EventStore(staging / "events" / "events.jsonl").read_all()
                for event in events:
                    projection.apply(event)
                staging.replace(destination)
            finally:
                if staging.exists():
                    shutil.rmtree(staging, ignore_errors=True)
            return manifest

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _infer_delta_type(event_type: str) -> EpistemicDeltaType:
        mapping = {
            "ROUTE_CREATED": EpistemicDeltaType.ROUTE_CREATED,
            "ROUTE_SPLIT": EpistemicDeltaType.ROUTE_CREATED,
            "ROUTE_MERGED": EpistemicDeltaType.ROUTE_CREATED,
            "ROUTE_REVIVED": EpistemicDeltaType.ROUTE_REVIVED,
            "BRIDGE_RESULT_CREATED": EpistemicDeltaType.BRIDGE_RESULT_CREATED,
            "DEAD_END_CONSTRAINT_CREATED": EpistemicDeltaType.ROUTE_OBSTRUCTED,
            "CHALLENGE_CREATED": EpistemicDeltaType.ROUTE_OBSTRUCTED,
            "HUMAN_INTERVENTION_ADDED": EpistemicDeltaType.HUMAN_INTERVENTION,
            "OBJECTION_ADDED": EpistemicDeltaType.HUMAN_INTERVENTION,
            "PLUGIN_RUN_COMPLETED": EpistemicDeltaType.TOOL_EVIDENCE_ADDED,
            "HANDOFF_CREATED": EpistemicDeltaType.HANDOFF_REUSED,
            "MODEL_SESSION_CREATED": EpistemicDeltaType.SESSION_RECORDED,
            "VISUAL_CANVAS_SNAPSHOT_CREATED": EpistemicDeltaType.VISUAL_PATTERN_NOTED,
        }
        return mapping.get(event_type, EpistemicDeltaType.NO_STATE_CHANGE)

    def _require_route(self, project_id: UUID, route_id: UUID) -> RouteRecord:
        self.get_project(project_id)
        route = self._projection(project_id).get_route(str(route_id))
        if route is None:
            raise NotFoundError(f"route {route_id} not found")
        return route

    def _require_branch(self, project_id: UUID, branch_id: UUID) -> BranchRecord:
        self.get_project(project_id)
        branch = self._projection(project_id).get_branch(str(branch_id))
        if branch is None:
            raise NotFoundError(f"branch {branch_id} not found")
        return branch

    def _validate_route_branch(
        self, project_id: UUID, route_id: UUID, branch_id: UUID | None
    ) -> None:
        self._require_route(project_id, route_id)
        if branch_id is not None:
            branch = self._require_branch(project_id, branch_id)
            if branch.route_id != route_id:
                raise ConflictError("branch belongs to a different route")

    def _normalize_target(
        self, project_id: UUID, route_id: UUID | None, branch_id: UUID | None
    ) -> tuple[UUID, UUID | None]:
        if branch_id is not None:
            branch = self._require_branch(project_id, branch_id)
            if route_id is not None and branch.route_id != route_id:
                raise ConflictError("branch belongs to a different route")
            return branch.route_id, branch_id
        if route_id is None:
            raise ConflictError("this object requires a route or branch target")
        self._require_route(project_id, route_id)
        return route_id, None

    def _normalize_optional_target(
        self, project_id: UUID, route_id: UUID | None, branch_id: UUID | None
    ) -> tuple[UUID | None, UUID | None]:
        self.get_project(project_id)
        if branch_id is not None:
            branch = self._require_branch(project_id, branch_id)
            if route_id is not None and branch.route_id != route_id:
                raise ConflictError("branch belongs to a different route")
            return branch.route_id, branch_id
        if route_id is not None:
            self._require_route(project_id, route_id)
        return route_id, None

    def _require_artifact(self, project_id: UUID, artifact_id: UUID) -> ArtifactRecord:
        artifact = self._projection(project_id).get_artifact(str(artifact_id))
        if artifact is None:
            raise NotFoundError(f"artifact {artifact_id} not found")
        return artifact

    def _require_plugin_manifest(self, plugin_id: str) -> PluginManifestRecord:
        for manifest in self.available_plugins():
            if manifest.plugin_id == plugin_id:
                return manifest
        raise NotFoundError(f"plugin {plugin_id} not found")

    def _python_runner(self) -> PythonPluginRunner:
        return PythonPluginRunner(
            plugin_root=self.settings.plugin_root,
            maximum_output_bytes=self.settings.maximum_plugin_output_bytes,
            maximum_output_files=self.settings.maximum_plugin_output_files,
        )

    def _plugin_host(self) -> PluginHost:
        return PluginHost(
            repository_root=self.repository_root,
            plugin_root=self.settings.plugin_root,
            maximum_output_bytes=self.settings.maximum_plugin_output_bytes,
            maximum_output_files=self.settings.maximum_plugin_output_files,
        )

    def _write_plugins_lock(self, project_id: UUID, plugins: list[ProjectPluginRecord]) -> None:
        path = self.project_dir(project_id) / "plugins" / "plugins.lock.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": SCHEMA_VERSION,
            "plugins": [item.model_dump(mode="json") for item in plugins],
        }
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _write_manifest(self, manifest: ProjectManifest) -> None:
        path = self._manifest_path(manifest.project_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        with _manifest_lock(path):
            temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
            temporary.write_text(
                manifest.model_dump_json(indent=2, exclude_none=False), encoding="utf-8"
            )
            _replace_with_retry(temporary, path)

    def _touch_manifest(self, project_id: UUID) -> None:
        manifest = self.get_project(project_id)
        updated = manifest.model_copy(update={"updated_at": utc_now()})
        self._write_manifest(updated)
