from __future__ import annotations

import logging
import tempfile
from pathlib import Path
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from fastapi.responses import FileResponse, Response

from .domain import (
    Actor,
    ActorType,
    ArenaPreviewRecord,
    ArenaRecipeCreate,
    ArenaRecipeRecord,
    ArtifactOrigin,
    ArtifactRecord,
    ArtifactType,
    AttemptRecord,
    AttemptRecordCreate,
    BenchmarkBindingCreate,
    BenchmarkBindingRecord,
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
    ChallengeStatusChange,
    ChatImportConfirmationResponse,
    ChatImportConfirmRequest,
    ChatImportPreviewRecord,
    ClaimAtomCreate,
    ClaimAtomRecord,
    ClaimRelationCreate,
    ClaimRelationRecord,
    CommandReceipt,
    ContinuationContractCreate,
    ContinuationContractRecord,
    CostVectorCreate,
    CostVectorRecord,
    DeadEndConstraintCreate,
    DeadEndConstraintRecord,
    EpistemicDeltaSummary,
    EventRecord,
    EvidenceCardCreate,
    EvidenceCardRecord,
    FormalCoverageBindingCreate,
    FormalCoverageBindingRecord,
    GenericEventCreate,
    GenericPluginRunRequest,
    HandoffArtifactCreate,
    HandoffArtifactRecord,
    HandoffDecisionCreate,
    HandoffPacketV2Create,
    HandoffPacketV2Record,
    HandoffReceipt,
    HistoricalSearchHit,
    HumanNoteCreate,
    ImportPreflightReport,
    IntegrityReport,
    InterpretationStatus,
    MicroFalsificationPlanCreate,
    MicroFalsificationPlanRecord,
    ModelSessionCreate,
    ModelSessionRecord,
    PluginHealthRecord,
    PluginInstallRequest,
    PluginManifestRecord,
    PluginRunRecord,
    ProjectCreate,
    ProjectManifest,
    ProjectPluginRecord,
    ProjectSummary,
    PythonPluginRunRequest,
    QuestionAgendaCreate,
    QuestionAgendaRecord,
    RepairLineageCreate,
    RepairLineageRecord,
    RepositorySnapshotCreate,
    RepositorySnapshotRecord,
    ResearchCheckpointCreate,
    ResearchCheckpointRecord,
    ResearchEpisodeDossierV2Create,
    ResearchEpisodeDossierV2Record,
    ResearchHierarchyNodeCreate,
    ResearchHierarchyNodeRecord,
    ResearchPacketRequest,
    ResearchPacketResponse,
    ResearchStateSnapshot,
    ResearchStateTransitionRecord,
    ReviewLineageCreate,
    ReviewLineageRecord,
    RouteCreate,
    RouteMergeRequest,
    RouteMergeResponse,
    RouteRecord,
    RouteSplitRequest,
    RouteSplitResponse,
    RouteStateChange,
    TransitionAcceptanceCreate,
    TransitionProposalCreate,
    TransitionProposalRecord,
    VerificationExecutionManifestCreate,
    VerificationExecutionManifestRecord,
    VerificationMutationSetCreate,
    VerificationMutationSetRecord,
)
from .event_store import EventStoreIntegrityError
from .service import ConflictError, NotFoundError, SchemaMathService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1")


def get_service() -> SchemaMathService:
    raise RuntimeError("service dependency was not configured")


def _translate_error(exc: Exception) -> HTTPException:
    if isinstance(exc, NotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    if isinstance(exc, ConflictError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    if isinstance(exc, EventStoreIntegrityError):
        logger.error("event store integrity failure", exc_info=exc)
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="event store integrity failure; the project is read-only until recovery",
        )
    if isinstance(exc, ValueError):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    logger.exception("internal error while handling request", exc_info=exc)
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error")


def _safe_content_disposition_filename(filename: str) -> str:
    """Strip characters that could inject or break the Content-Disposition header."""
    cleaned = Path(filename).name.replace("\r", "").replace("\n", "").replace('"', "")
    cleaned = "".join(ch for ch in cleaned if ch.isprintable())
    return cleaned[:200] or "artifact"


async def _spool_upload(file: UploadFile, maximum_bytes: int) -> Path:
    """Stream an upload to a temporary file without buffering it in RAM."""

    handle = tempfile.NamedTemporaryFile(suffix=".smath.zip", delete=False)
    path = Path(handle.name)
    total = 0
    try:
        with handle:
            while chunk := await file.read(1024 * 1024):
                total += len(chunk)
                if total > maximum_bytes:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="uploaded archive exceeds the configured import size limit",
                    )
                handle.write(chunk)
        return path
    except Exception:
        path.unlink(missing_ok=True)
        raise


@router.post("/projects", response_model=ProjectManifest, status_code=201)
def create_project(
    request: ProjectCreate, service: Annotated[SchemaMathService, Depends(get_service)]
) -> ProjectManifest:
    try:
        return service.create_project(request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects", response_model=list[ProjectSummary])
def list_projects(
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> list[ProjectSummary]:
    return service.list_projects()


@router.get("/projects/{project_id}", response_model=ProjectManifest)
def get_project(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> ProjectManifest:
    try:
        return service.get_project(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post("/projects/{project_id}/routes", response_model=RouteRecord, status_code=201)
def create_route(
    project_id: UUID,
    request: RouteCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> RouteRecord:
    try:
        return service.create_route(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/routes", response_model=list[RouteRecord])
def list_routes(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[RouteRecord]:
    try:
        return service.list_routes(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/routes/similar",
    response_model=list[HistoricalSearchHit],
)
def similar_routes(
    project_id: UUID,
    service: Annotated[SchemaMathService, Depends(get_service)],
    q: str = Query(min_length=1, max_length=1000),
    limit: int = Query(default=10, ge=1, le=50),
) -> list[HistoricalSearchHit]:
    """Return route-only retrieval hints; callers decide whether to reuse or fork."""
    try:
        hits = service.search_history(project_id, q, limit=max(limit * 4, 20))
        return [hit for hit in hits if hit.kind == "route"][:limit]
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/routes/{route_id}/split",
    response_model=RouteSplitResponse,
    status_code=201,
)
def split_route(
    project_id: UUID,
    route_id: UUID,
    request: RouteSplitRequest,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> RouteSplitResponse:
    try:
        return service.split_route(project_id, route_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/routes/merge",
    response_model=RouteMergeResponse,
    status_code=201,
)
def merge_routes(
    project_id: UUID,
    request: RouteMergeRequest,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> RouteMergeResponse:
    try:
        return service.merge_routes(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.patch("/projects/{project_id}/routes/{route_id}/state", response_model=RouteRecord)
def change_route_state(
    project_id: UUID,
    route_id: UUID,
    request: RouteStateChange,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> RouteRecord:
    try:
        return service.change_route_state(project_id, route_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post("/projects/{project_id}/branches", response_model=BranchRecord, status_code=201)
def create_branch(
    project_id: UUID,
    request: BranchCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> BranchRecord:
    try:
        return service.create_branch(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/branches", response_model=list[BranchRecord])
def list_branches(
    project_id: UUID,
    service: Annotated[SchemaMathService, Depends(get_service)],
    route_id: UUID | None = None,
) -> list[BranchRecord]:
    try:
        return service.list_branches(project_id, route_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.patch("/projects/{project_id}/branches/{branch_id}/state", response_model=BranchRecord)
def change_branch_state(
    project_id: UUID,
    branch_id: UUID,
    request: BranchStateChange,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> BranchRecord:
    try:
        return service.change_branch_state(project_id, branch_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post("/projects/{project_id}/challenges", response_model=ChallengeRecord, status_code=201)
def create_challenge(
    project_id: UUID,
    request: ChallengeCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ChallengeRecord:
    try:
        return service.create_challenge(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/challenges", response_model=list[ChallengeRecord])
def list_challenges(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[ChallengeRecord]:
    try:
        return service.list_challenges(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.patch(
    "/projects/{project_id}/challenges/{challenge_id}/status",
    response_model=ChallengeRecord,
)
def change_challenge_status(
    project_id: UUID,
    challenge_id: UUID,
    request: ChallengeStatusChange,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ChallengeRecord:
    try:
        return service.change_challenge_status(project_id, challenge_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/bridge-results",
    response_model=BridgeResultRecord,
    status_code=201,
)
def create_bridge_result(
    project_id: UUID,
    request: BridgeResultCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> BridgeResultRecord:
    try:
        return service.create_bridge_result(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/bridge-results", response_model=list[BridgeResultRecord])
def list_bridge_results(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[BridgeResultRecord]:
    try:
        return service.list_bridge_results(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/dead-ends",
    response_model=DeadEndConstraintRecord,
    status_code=201,
)
def create_dead_end(
    project_id: UUID,
    request: DeadEndConstraintCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> DeadEndConstraintRecord:
    try:
        return service.create_dead_end_constraint(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/dead-ends", response_model=list[DeadEndConstraintRecord])
def list_dead_ends(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[DeadEndConstraintRecord]:
    try:
        return service.list_dead_end_constraints(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/checkpoints",
    response_model=ResearchCheckpointRecord,
    status_code=201,
)
def create_checkpoint(
    project_id: UUID,
    request: ResearchCheckpointCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ResearchCheckpointRecord:
    try:
        return service.create_checkpoint(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/checkpoints", response_model=list[ResearchCheckpointRecord])
def list_checkpoints(
    project_id: UUID,
    service: Annotated[SchemaMathService, Depends(get_service)],
    limit: int | None = None,
) -> list[ResearchCheckpointRecord]:
    try:
        return service.list_checkpoints(project_id, limit)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post("/projects/{project_id}/notes", response_model=EventRecord, status_code=201)
def add_note(
    project_id: UUID,
    request: HumanNoteCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> EventRecord:
    try:
        return service.add_human_note(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post("/projects/{project_id}/events", response_model=EventRecord, status_code=201)
def append_event(
    project_id: UUID,
    request: GenericEventCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> EventRecord:
    try:
        return service.append_generic_event(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/events", response_model=list[EventRecord])
def list_events(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[EventRecord]:
    try:
        return service.list_events(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/command-receipts",
    response_model=list[CommandReceipt],
)
def list_command_receipts(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[CommandReceipt]:
    try:
        return service.list_command_receipts(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/transition-proposals",
    response_model=TransitionProposalRecord,
    status_code=201,
)
def create_transition_proposal(
    project_id: UUID,
    request: TransitionProposalCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> TransitionProposalRecord:
    try:
        return service.create_transition_proposal(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/transition-proposals",
    response_model=list[TransitionProposalRecord],
)
def list_transition_proposals(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[TransitionProposalRecord]:
    try:
        return service.list_transition_proposals(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/transition-proposals/{proposal_id}/accept",
    response_model=ResearchStateTransitionRecord,
    status_code=201,
)
def accept_transition_proposal(
    project_id: UUID,
    proposal_id: UUID,
    request: TransitionAcceptanceCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ResearchStateTransitionRecord:
    try:
        return service.accept_transition_proposal(project_id, proposal_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/research-state", response_model=ResearchStateSnapshot)
def get_research_state(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> ResearchStateSnapshot:
    try:
        return service.research_state(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/claim-atoms/proposals",
    response_model=TransitionProposalRecord,
    status_code=201,
)
def propose_claim_atom(
    project_id: UUID,
    request: ClaimAtomCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> TransitionProposalRecord:
    try:
        return service.propose_claim_atom(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/claim-atoms", response_model=list[ClaimAtomRecord])
def list_claim_atoms(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[ClaimAtomRecord]:
    try:
        return service.list_claim_atoms(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/claim-relations",
    response_model=ClaimRelationRecord,
    status_code=201,
)
def create_claim_relation(
    project_id: UUID,
    request: ClaimRelationCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ClaimRelationRecord:
    try:
        return service.create_claim_relation(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/claim-relations",
    response_model=list[ClaimRelationRecord],
)
def list_claim_relations(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[ClaimRelationRecord]:
    try:
        return service.list_claim_relations(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/review-lineage",
    response_model=ReviewLineageRecord,
    status_code=201,
)
def create_review_lineage(
    project_id: UUID,
    request: ReviewLineageCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ReviewLineageRecord:
    try:
        return service.create_review_lineage(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/review-lineage",
    response_model=list[ReviewLineageRecord],
)
def list_review_lineage(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[ReviewLineageRecord]:
    try:
        return service.list_review_lineage(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/evidence-cards",
    response_model=EvidenceCardRecord,
    status_code=201,
)
def create_evidence_card(
    project_id: UUID,
    request: EvidenceCardCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> EvidenceCardRecord:
    try:
        return service.create_evidence_card(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/evidence-cards",
    response_model=list[EvidenceCardRecord],
)
def list_evidence_cards(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[EvidenceCardRecord]:
    try:
        return service.list_evidence_cards(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/verification-manifests",
    response_model=VerificationExecutionManifestRecord,
    status_code=201,
)
def create_verification_manifest(
    project_id: UUID,
    request: VerificationExecutionManifestCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> VerificationExecutionManifestRecord:
    try:
        return service.create_verification_manifest(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/verification-manifests",
    response_model=list[VerificationExecutionManifestRecord],
)
def list_verification_manifests(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[VerificationExecutionManifestRecord]:
    try:
        return service.list_verification_manifests(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/verification-mutation-sets",
    response_model=VerificationMutationSetRecord,
    status_code=201,
)
def create_mutation_set(
    project_id: UUID,
    request: VerificationMutationSetCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> VerificationMutationSetRecord:
    try:
        return service.create_mutation_set(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/verification-mutation-sets",
    response_model=list[VerificationMutationSetRecord],
)
def list_mutation_sets(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[VerificationMutationSetRecord]:
    try:
        return service.list_mutation_sets(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/coverage-bindings",
    response_model=FormalCoverageBindingRecord,
    status_code=201,
)
def create_coverage_binding(
    project_id: UUID,
    request: FormalCoverageBindingCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> FormalCoverageBindingRecord:
    try:
        return service.create_coverage_binding(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/coverage-bindings",
    response_model=list[FormalCoverageBindingRecord],
)
def list_coverage_bindings(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[FormalCoverageBindingRecord]:
    try:
        return service.list_coverage_bindings(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/repository-snapshots",
    response_model=RepositorySnapshotRecord,
    status_code=201,
)
def create_repository_snapshot(
    project_id: UUID,
    request: RepositorySnapshotCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> RepositorySnapshotRecord:
    try:
        return service.create_repository_snapshot(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/repository-snapshots",
    response_model=list[RepositorySnapshotRecord],
)
def list_repository_snapshots(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[RepositorySnapshotRecord]:
    try:
        return service.list_repository_snapshots(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/repair-lineage",
    response_model=RepairLineageRecord,
    status_code=201,
)
def create_repair_lineage(
    project_id: UUID,
    request: RepairLineageCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> RepairLineageRecord:
    try:
        return service.create_repair_lineage(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/repair-lineage",
    response_model=list[RepairLineageRecord],
)
def list_repair_lineage(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[RepairLineageRecord]:
    try:
        return service.list_repair_lineage(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/hierarchy-nodes",
    response_model=ResearchHierarchyNodeRecord,
    status_code=201,
)
def create_hierarchy_node(
    project_id: UUID,
    request: ResearchHierarchyNodeCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ResearchHierarchyNodeRecord:
    try:
        return service.create_hierarchy_node(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/hierarchy-nodes",
    response_model=list[ResearchHierarchyNodeRecord],
)
def list_hierarchy_nodes(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[ResearchHierarchyNodeRecord]:
    try:
        return service.list_hierarchy_nodes(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/attempts",
    response_model=AttemptRecord,
    status_code=201,
)
def create_attempt_record(
    project_id: UUID,
    request: AttemptRecordCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> AttemptRecord:
    try:
        return service.create_attempt_record(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/attempts", response_model=list[AttemptRecord])
def list_attempt_records(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[AttemptRecord]:
    try:
        return service.list_attempt_records(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/cost-vectors",
    response_model=CostVectorRecord,
    status_code=201,
)
def create_cost_vector(
    project_id: UUID,
    request: CostVectorCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> CostVectorRecord:
    try:
        return service.create_cost_vector(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/cost-vectors", response_model=list[CostVectorRecord])
def list_cost_vectors(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[CostVectorRecord]:
    try:
        return service.list_cost_vectors(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/falsification-plans",
    response_model=MicroFalsificationPlanRecord,
    status_code=201,
)
def create_falsification_plan(
    project_id: UUID,
    request: MicroFalsificationPlanCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> MicroFalsificationPlanRecord:
    try:
        return service.create_falsification_plan(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/falsification-plans",
    response_model=list[MicroFalsificationPlanRecord],
)
def list_falsification_plans(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[MicroFalsificationPlanRecord]:
    try:
        return service.list_falsification_plans(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/benchmark-bindings",
    response_model=BenchmarkBindingRecord,
    status_code=201,
)
def create_benchmark_binding(
    project_id: UUID,
    request: BenchmarkBindingCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> BenchmarkBindingRecord:
    try:
        return service.create_benchmark_binding(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/benchmark-bindings",
    response_model=list[BenchmarkBindingRecord],
)
def list_benchmark_bindings(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[BenchmarkBindingRecord]:
    try:
        return service.list_benchmark_bindings(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/dossiers-v2",
    response_model=ResearchEpisodeDossierV2Record,
    status_code=201,
)
def create_dossier_v2(
    project_id: UUID,
    request: ResearchEpisodeDossierV2Create,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ResearchEpisodeDossierV2Record:
    try:
        return service.create_dossier_v2(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/dossiers-v2",
    response_model=list[ResearchEpisodeDossierV2Record],
)
def list_dossiers_v2(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[ResearchEpisodeDossierV2Record]:
    try:
        return service.list_dossiers_v2(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/question-agendas",
    response_model=QuestionAgendaRecord,
    status_code=201,
)
def create_question_agenda(
    project_id: UUID,
    request: QuestionAgendaCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> QuestionAgendaRecord:
    try:
        return service.create_question_agenda(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/question-agendas",
    response_model=list[QuestionAgendaRecord],
)
def list_question_agendas(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[QuestionAgendaRecord]:
    try:
        return service.list_question_agendas(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post("/projects/{project_id}/artifacts", response_model=ArtifactRecord, status_code=201)
async def add_artifact(
    project_id: UUID,
    service: Annotated[SchemaMathService, Depends(get_service)],
    file: UploadFile = File(...),
    artifact_type: ArtifactType = Form(ArtifactType.OTHER),
    origin: ArtifactOrigin = Form(ArtifactOrigin.IMPORT),
    interpretation_status: InterpretationStatus = Form(InterpretationStatus.RAW),
    actor_id: str = Form("local-researcher"),
    actor_display_name: str | None = Form(None),
    source_ref: str | None = Form(None),
) -> ArtifactRecord:
    try:
        content = await file.read(service.settings.maximum_upload_bytes + 1)
        return service.add_artifact(
            project_id=project_id,
            filename=file.filename or "artifact.bin",
            content=content,
            artifact_type=artifact_type,
            origin=origin,
            media_type=file.content_type,
            interpretation_status=interpretation_status,
            actor=Actor(
                type=ActorType.HUMAN,
                id=actor_id,
                display_name=actor_display_name,
            ),
            source_ref=source_ref,
        )
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/artifacts", response_model=list[ArtifactRecord])
def list_artifacts(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[ArtifactRecord]:
    try:
        return service.list_artifacts(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/artifacts/{artifact_id}/content")
def get_artifact_content(
    project_id: UUID,
    artifact_id: UUID,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> Response:
    try:
        artifact, content = service.artifact_bytes(project_id, artifact_id)
        safe_name = _safe_content_disposition_filename(artifact.original_filename)
        return Response(
            content=content,
            media_type=artifact.media_type,
            headers={"Content-Disposition": f'attachment; filename="{safe_name}"'},
        )
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/chat-imports/preview",
    response_model=ChatImportPreviewRecord,
    status_code=201,
)
@router.post(
    "/projects/{project_id}/chat-imports",
    response_model=ChatImportPreviewRecord,
    status_code=201,
)
async def create_chat_import(
    project_id: UUID,
    service: Annotated[SchemaMathService, Depends(get_service)],
    file: UploadFile = File(...),
    actor_id: str = Form("local-researcher"),
    actor_display_name: str | None = Form(None),
) -> ChatImportPreviewRecord:
    try:
        content = await file.read(service.settings.maximum_upload_bytes + 1)
        return service.create_chat_import_preview(
            project_id=project_id,
            filename=file.filename or "conversation.txt",
            media_type=file.content_type,
            content=content,
            actor=Actor(
                type=ActorType.HUMAN,
                id=actor_id,
                display_name=actor_display_name,
            ),
        )
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/chat-imports", response_model=list[ChatImportPreviewRecord])
def list_chat_imports(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[ChatImportPreviewRecord]:
    try:
        return service.list_chat_imports(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/chat-imports/{import_id}/confirm",
    response_model=ChatImportConfirmationResponse,
)
def confirm_chat_import(
    project_id: UUID,
    import_id: UUID,
    request: ChatImportConfirmRequest,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ChatImportConfirmationResponse:
    try:
        return service.confirm_chat_import(project_id, import_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/plugins", response_model=list[PluginManifestRecord])
def available_plugins(
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> list[PluginManifestRecord]:
    return service.available_plugins()


@router.get("/projects/{project_id}/plugins", response_model=list[ProjectPluginRecord])
def list_project_plugins(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[ProjectPluginRecord]:
    try:
        return service.list_project_plugins(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/plugins/{plugin_id}/install",
    response_model=ProjectPluginRecord,
    status_code=201,
)
def install_plugin(
    project_id: UUID,
    plugin_id: str,
    request: PluginInstallRequest,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ProjectPluginRecord:
    try:
        return service.install_plugin(project_id, plugin_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/plugins/{plugin_id}/health",
    response_model=PluginHealthRecord,
)
def check_plugin_health(
    project_id: UUID,
    plugin_id: str,
    request: Actor,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> PluginHealthRecord:
    try:
        return service.check_plugin_health(project_id, plugin_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/plugins/{plugin_id}/enable",
    response_model=ProjectPluginRecord,
)
def enable_plugin(
    project_id: UUID,
    plugin_id: str,
    request: Actor,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ProjectPluginRecord:
    try:
        return service.enable_plugin(project_id, plugin_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/plugins/{plugin_id}/uninstall",
    response_model=ProjectPluginRecord,
)
def uninstall_plugin(
    project_id: UUID,
    plugin_id: str,
    request: Actor,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ProjectPluginRecord:
    try:
        return service.uninstall_plugin(project_id, plugin_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/plugins/{plugin_id}/disable",
    response_model=ProjectPluginRecord,
)
def disable_plugin(
    project_id: UUID,
    plugin_id: str,
    request: Actor,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ProjectPluginRecord:
    try:
        return service.disable_plugin(project_id, plugin_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/plugin-runs/python",
    response_model=PluginRunRecord,
    status_code=201,
)
@router.post(
    "/projects/{project_id}/plugins/python.local/runs",
    response_model=PluginRunRecord,
    status_code=201,
)
def run_python_plugin(
    project_id: UUID,
    request: PythonPluginRunRequest,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> PluginRunRecord:
    try:
        return service.run_python_plugin(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/plugins/{plugin_id}/runs",
    response_model=PluginRunRecord,
    status_code=201,
)
def run_plugin(
    project_id: UUID,
    plugin_id: str,
    request: GenericPluginRunRequest,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> PluginRunRecord:
    try:
        return service.run_plugin(project_id, plugin_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/plugin-runs", response_model=list[PluginRunRecord])
def list_plugin_runs(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[PluginRunRecord]:
    try:
        return service.list_plugin_runs(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/sessions",
    response_model=ModelSessionRecord,
    status_code=201,
)
def create_model_session(
    project_id: UUID,
    request: ModelSessionCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ModelSessionRecord:
    try:
        return service.create_model_session(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/sessions", response_model=list[ModelSessionRecord])
def list_model_sessions(
    project_id: UUID,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> list[ModelSessionRecord]:
    try:
        return service.list_model_sessions(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/handoffs",
    response_model=HandoffArtifactRecord,
    status_code=201,
)
def create_handoff_artifact(
    project_id: UUID,
    request: HandoffArtifactCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> HandoffArtifactRecord:
    try:
        return service.create_handoff_artifact(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/handoffs", response_model=list[HandoffArtifactRecord])
def list_handoff_artifacts(
    project_id: UUID,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> list[HandoffArtifactRecord]:
    try:
        return service.list_handoff_artifacts(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/continuation-contracts",
    response_model=ContinuationContractRecord,
    status_code=201,
)
def create_continuation_contract(
    project_id: UUID,
    request: ContinuationContractCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ContinuationContractRecord:
    try:
        return service.create_continuation_contract(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/continuation-contracts",
    response_model=list[ContinuationContractRecord],
)
def list_continuation_contracts(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[ContinuationContractRecord]:
    try:
        return service.list_continuation_contracts(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/handoffs-v2",
    response_model=HandoffPacketV2Record,
    status_code=201,
)
def create_handoff_packet_v2(
    project_id: UUID,
    request: HandoffPacketV2Create,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> HandoffPacketV2Record:
    try:
        return service.create_handoff_packet_v2(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/handoffs-v2",
    response_model=list[HandoffPacketV2Record],
)
def list_handoff_packets_v2(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[HandoffPacketV2Record]:
    try:
        return service.list_handoff_packets_v2(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/handoffs-v2/{packet_id}/accept",
    response_model=HandoffReceipt,
    status_code=201,
)
def accept_handoff_packet_v2(
    project_id: UUID,
    packet_id: UUID,
    request: HandoffDecisionCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> HandoffReceipt:
    try:
        return service.accept_handoff_packet_v2(project_id, packet_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/handoff-receipts",
    response_model=list[HandoffReceipt],
)
def list_handoff_receipts(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> list[HandoffReceipt]:
    try:
        return service.list_handoff_receipts(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/arena-recipes",
    response_model=ArenaRecipeRecord,
    status_code=201,
)
def create_arena_recipe(
    project_id: UUID,
    request: ArenaRecipeCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ArenaRecipeRecord:
    try:
        return service.create_arena_recipe(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/arena-recipes", response_model=list[ArenaRecipeRecord])
def list_arena_recipes(
    project_id: UUID,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> list[ArenaRecipeRecord]:
    try:
        return service.list_arena_recipes(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/arena-recipes/{recipe_id}/preview",
    response_model=ArenaPreviewRecord,
)
def preview_arena_recipe(
    project_id: UUID,
    recipe_id: UUID,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ArenaPreviewRecord:
    try:
        return service.preview_arena_recipe(project_id, recipe_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/search", response_model=list[HistoricalSearchHit])
def search_history(
    project_id: UUID,
    service: Annotated[SchemaMathService, Depends(get_service)],
    q: str = Query(min_length=1, max_length=1000),
    limit: int = Query(default=50, ge=1, le=200),
) -> list[HistoricalSearchHit]:
    try:
        return service.search_history(project_id, q, limit=limit)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/epistemic-deltas",
    response_model=list[EpistemicDeltaSummary],
)
def epistemic_deltas(
    project_id: UUID,
    service: Annotated[SchemaMathService, Depends(get_service)],
    limit: int = Query(default=100, ge=1, le=1000),
) -> list[EpistemicDeltaSummary]:
    try:
        return service.epistemic_deltas(project_id, limit=limit)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post(
    "/projects/{project_id}/canvas/snapshots",
    response_model=CanvasSnapshotRecord,
    status_code=201,
)
def create_canvas_snapshot(
    project_id: UUID,
    request: CanvasSnapshotCreate,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> CanvasSnapshotRecord:
    try:
        return service.create_canvas_snapshot(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/canvas/snapshots",
    response_model=list[CanvasSnapshotRecord],
)
def list_canvas_snapshots(
    project_id: UUID,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> list[CanvasSnapshotRecord]:
    try:
        return service.list_canvas_snapshots(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get(
    "/projects/{project_id}/canvas/latest",
    response_model=CanvasSnapshotResponse | None,
)
def latest_canvas_snapshot(
    project_id: UUID,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> CanvasSnapshotResponse | None:
    try:
        return service.latest_canvas_snapshot(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post("/projects/{project_id}/research-packets", response_model=ResearchPacketResponse)
def build_research_packet(
    project_id: UUID,
    request: ResearchPacketRequest,
    service: Annotated[SchemaMathService, Depends(get_service)],
) -> ResearchPacketResponse:
    try:
        return service.build_research_packet(project_id, request)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/integrity", response_model=IntegrityReport)
def integrity_report(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> IntegrityReport:
    try:
        return service.integrity_report(project_id)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post("/projects/{project_id}/rebuild-projection")
def rebuild_projection(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> dict[str, int]:
    try:
        return {"events_replayed": service.rebuild_projection(project_id)}
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.get("/projects/{project_id}/export")
def export_project(
    project_id: UUID, service: Annotated[SchemaMathService, Depends(get_service)]
) -> FileResponse:
    try:
        path = service.export_project_zip(project_id)
        return FileResponse(path, media_type="application/zip", filename=path.name)
    except Exception as exc:
        raise _translate_error(exc) from exc


@router.post("/imports", response_model=ProjectManifest, status_code=201)
async def import_project(
    service: Annotated[SchemaMathService, Depends(get_service)],
    file: UploadFile = File(...),
) -> ProjectManifest:
    temporary_path: Path | None = None
    try:
        temporary_path = await _spool_upload(file, service.settings.maximum_import_bytes)
        return service.import_project_zip(temporary_path)
    except HTTPException:
        raise
    except Exception as exc:
        raise _translate_error(exc) from exc
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


@router.post("/imports/preflight", response_model=ImportPreflightReport)
async def preflight_project_import(
    service: Annotated[SchemaMathService, Depends(get_service)],
    file: UploadFile = File(...),
) -> ImportPreflightReport:
    temporary_path: Path | None = None
    try:
        temporary_path = await _spool_upload(file, service.settings.maximum_import_bytes)
        return service.preflight_project_zip(temporary_path)
    except HTTPException:
        raise
    except Exception as exc:
        raise _translate_error(exc) from exc
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
