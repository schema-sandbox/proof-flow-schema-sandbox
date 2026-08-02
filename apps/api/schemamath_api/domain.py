from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    field_validator,
    model_validator,
)

SCHEMA_VERSION = "0.4"
SUPPORTED_SCHEMA_VERSIONS = {"0.1", "0.2", "0.3", "0.4"}


def utc_now() -> datetime:
    return datetime.now(UTC)


def _validate_schema_version(value: str) -> str:
    if value not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValueError(
            f"unsupported schema version {value!r}; "
            f"supported versions: {sorted(SUPPORTED_SCHEMA_VERSIONS)}"
        )
    return value


class ActorType(StrEnum):
    HUMAN = "human"
    MODEL = "model"
    TOOL = "tool"
    RUNTIME = "runtime"


class RouteState(StrEnum):
    SEED = "SEED"
    ACTIVE = "ACTIVE"
    CHALLENGED = "CHALLENGED"
    CONDITIONAL = "CONDITIONAL"
    DORMANT = "DORMANT"
    REVIVED = "REVIVED"
    BRIDGE_RESULT = "BRIDGE_RESULT"
    SUPERSEDED = "SUPERSEDED"
    CERTIFIED_CLOSED = "CERTIFIED_CLOSED"


class BranchState(StrEnum):
    SEED = "SEED"
    ACTIVE = "ACTIVE"
    CHALLENGED = "CHALLENGED"
    DORMANT = "DORMANT"
    REVIVED = "REVIVED"
    BRIDGE_RESULT = "BRIDGE_RESULT"
    SUPERSEDED = "SUPERSEDED"
    COMPLETED = "COMPLETED"


class ChallengeType(StrEnum):
    OBJECTION = "OBJECTION"
    COUNTEREXAMPLE_SEARCH = "COUNTEREXAMPLE_SEARCH"
    SOURCE_CHECK = "SOURCE_CHECK"
    QUANTIFIER_CHECK = "QUANTIFIER_CHECK"
    FORMALIZATION_TEST = "FORMALIZATION_TEST"
    COMPUTATIONAL_TEST = "COMPUTATIONAL_TEST"
    BOUNDARY_CASE = "BOUNDARY_CASE"
    OTHER = "OTHER"


class ChallengeStatus(StrEnum):
    OPEN = "OPEN"
    TESTING = "TESTING"
    RESOLVED = "RESOLVED"
    DEFERRED = "DEFERRED"
    WITHDRAWN = "WITHDRAWN"


class BridgeResultStatus(StrEnum):
    ACTIVE = "ACTIVE"
    REUSED = "REUSED"
    SUPERSEDED = "SUPERSEDED"


class DeadEndStrength(StrEnum):
    OBSERVED = "OBSERVED"
    REPEATED = "REPEATED"
    CERTIFIED = "CERTIFIED"


class CheckpointConfidence(StrEnum):
    UNSPECIFIED = "UNSPECIFIED"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ImportFormat(StrEnum):
    MARKDOWN = "MARKDOWN"
    HTML = "HTML"
    JSON = "JSON"
    PLAIN_TEXT = "PLAIN_TEXT"


class ImportDisposition(StrEnum):
    MODEL_NOTE = "MODEL_NOTE"
    RESEARCH_CHECKPOINT = "RESEARCH_CHECKPOINT"
    CHALLENGE = "CHALLENGE"
    BRIDGE_RESULT = "BRIDGE_RESULT"
    NEW_BRANCH = "NEW_BRANCH"
    IGNORE = "IGNORE"


class PluginRunStatus(StrEnum):
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    CANCELLED = "CANCELLED"


class EpistemicDeltaType(StrEnum):
    TARGET_CLARIFIED = "TARGET_CLARIFIED"
    ASSUMPTION_CHANGED = "ASSUMPTION_CHANGED"
    ROUTE_CREATED = "ROUTE_CREATED"
    ROUTE_OBSTRUCTED = "ROUTE_OBSTRUCTED"
    ROUTE_REVIVED = "ROUTE_REVIVED"
    COUNTEREXAMPLE_FOUND = "COUNTEREXAMPLE_FOUND"
    BRIDGE_RESULT_CREATED = "BRIDGE_RESULT_CREATED"
    TOOL_EVIDENCE_ADDED = "TOOL_EVIDENCE_ADDED"
    HANDOFF_REUSED = "HANDOFF_REUSED"
    VISUAL_PATTERN_NOTED = "VISUAL_PATTERN_NOTED"
    HUMAN_INTERVENTION = "HUMAN_INTERVENTION"
    SESSION_RECORDED = "SESSION_RECORDED"
    NO_STATE_CHANGE = "NO_STATE_CHANGE"


class PluginCategory(StrEnum):
    COMPUTE = "COMPUTE"
    SEARCH = "SEARCH"
    FORMALIZE = "FORMALIZE"
    VISUALIZE = "VISUALIZE"
    VIDEO = "VIDEO"
    IMPORTER = "IMPORTER"
    EXPORTER = "EXPORTER"


class PluginRunnerType(StrEnum):
    PYTHON = "python"
    LOCAL_COMMAND = "local_command"
    OCI = "oci"


class PluginLifecycleStatus(StrEnum):
    DISCOVERED = "DISCOVERED"
    INSPECTED = "INSPECTED"
    INSTALLED = "INSTALLED"
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"
    ENABLED_FOR_PROJECT = "ENABLED_FOR_PROJECT"
    DISABLED = "DISABLED"
    UNINSTALLED = "UNINSTALLED"


class ConnectorType(StrEnum):
    MANUAL_CHATGPT = "manual_chatgpt"
    OPENAI_API = "openai_api"
    IMPORTED_TRANSCRIPT = "imported_transcript"
    TOOL_SESSION = "tool_session"
    FUTURE_PLUGIN = "future_plugin"


class SessionCompleteness(StrEnum):
    COMPLETE_VISIBLE = "COMPLETE_VISIBLE"
    PARTIAL_VISIBLE = "PARTIAL_VISIBLE"
    AUTHOR_ATTESTED = "AUTHOR_ATTESTED"
    UNKNOWN = "UNKNOWN"


class ArenaRole(StrEnum):
    EXPLORER = "explorer"
    BUILDER = "builder"
    RIVAL_THEORIST = "rival_theorist"
    COUNTEREXAMPLE_HUNTER = "counterexample_hunter"
    SKEPTIC = "skeptic"
    BRIDGE_BUILDER = "bridge_builder"
    SIMPLIFIER = "simplifier"
    VISUAL_THINKER = "visual_thinker"
    FORMALIZER = "formalizer"
    HISTORIAN = "historian"
    EXPOSITOR = "expositor"


class ArenaComputeMode(StrEnum):
    CONSERVATIVE = "conservative"
    MANUAL_PARALLEL = "manual_parallel"
    CUSTOM = "custom"


class HandoffArtifactType(StrEnum):
    FAILED_ROUTE_NOTES = "FAILED_ROUTE_NOTES"
    SCRIPT = "SCRIPT"
    COUNTEREXAMPLE = "COUNTEREXAMPLE"
    PARTIAL_CONSTRUCTION = "PARTIAL_CONSTRUCTION"
    SOURCE_MAP = "SOURCE_MAP"
    OPEN_OBLIGATION = "OPEN_OBLIGATION"
    BRIDGE_RESULT = "BRIDGE_RESULT"


class VisualMappingStatus(StrEnum):
    CONFIRMED = "CONFIRMED"
    PARTIAL = "PARTIAL"
    AMBIGUOUS = "AMBIGUOUS"
    UNMAPPED = "UNMAPPED"


class ProjectStatus(StrEnum):
    UNRESOLVED = "UNRESOLVED"
    CLARIFIED = "CLARIFIED"
    REFORMULATED = "REFORMULATED"
    PARTIAL_RESULT = "PARTIAL_RESULT"
    BRIDGE_RESULT = "BRIDGE_RESULT"
    ROUTE_OBSTRUCTION = "ROUTE_OBSTRUCTION"
    COMPUTATIONAL_PATTERN = "COMPUTATIONAL_PATTERN"
    COUNTEREXAMPLE_CANDIDATE = "COUNTEREXAMPLE_CANDIDATE"
    CANDIDATE_PROOF = "CANDIDATE_PROOF"
    FORMAL_TARGET_ENCODED = "FORMAL_TARGET_ENCODED"
    KERNEL_ACCEPTED = "KERNEL_ACCEPTED"
    HUMAN_REVIEWED = "HUMAN_REVIEWED"
    INDEPENDENTLY_RE_DERIVED = "INDEPENDENTLY_RE_DERIVED"
    WITHDRAWN = "WITHDRAWN"


class ArtifactType(StrEnum):
    TEXT = "TEXT"
    FORMULA = "FORMULA"
    IMAGE = "IMAGE"
    HAND_DRAWING = "HAND_DRAWING"
    VIDEO = "VIDEO"
    CODE = "CODE"
    TABLE = "TABLE"
    GRAPH = "GRAPH"
    PROOF_SOURCE = "PROOF_SOURCE"
    PROOF_BUILD_LOG = "PROOF_BUILD_LOG"
    COUNTEREXAMPLE = "COUNTEREXAMPLE"
    DATASET = "DATASET"
    EXECUTION_LOG = "EXECUTION_LOG"
    CHAT_TRANSCRIPT = "CHAT_TRANSCRIPT"
    CHECKPOINT = "CHECKPOINT"
    OTHER = "OTHER"


class ArtifactOrigin(StrEnum):
    HUMAN = "HUMAN"
    MODEL = "MODEL"
    PLUGIN = "PLUGIN"
    IMPORT = "IMPORT"
    DERIVED = "DERIVED"


class InterpretationStatus(StrEnum):
    RAW = "RAW"
    ANNOTATED = "ANNOTATED"
    INTERPRETED = "INTERPRETED"
    STRUCTURED = "STRUCTURED"
    PARTIAL = "PARTIAL"
    AMBIGUOUS = "AMBIGUOUS"
    UNMAPPED = "UNMAPPED"


class Actor(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: ActorType
    id: str = Field(min_length=1, max_length=160)
    display_name: str | None = Field(default=None, max_length=240)


class ProblemContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_text: str = Field(min_length=1)
    source_uri: HttpUrl | None = None
    source_version: str | None = Field(default=None, max_length=160)
    author_notes: str = ""
    definitions: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)


class ProjectCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=240)
    description: str = Field(default="", max_length=4000)
    problem: ProblemContract
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class ProjectManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str = SCHEMA_VERSION
    project_id: UUID
    title: str
    description: str = ""
    created_at: datetime
    updated_at: datetime
    original_problem: ProblemContract
    current_goal_id: UUID
    project_status: list[ProjectStatus] = Field(default_factory=lambda: [ProjectStatus.UNRESOLVED])
    event_stream: str = "events/events.jsonl"
    artifact_store: str = "blobs/sha256"
    plugins_lock: str = "plugins/plugins.lock.json"

    _schema_version = field_validator("schema_version")(_validate_schema_version)


class ProjectSummary(BaseModel):
    project_id: UUID
    title: str
    description: str
    updated_at: datetime
    project_status: list[ProjectStatus]


class RouteCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=240)
    description: str = Field(default="", max_length=8000)
    parent_route_id: UUID | None = None
    initial_state: RouteState = RouteState.SEED
    revival_conditions: list[str] = Field(default_factory=list)
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class RouteRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    route_id: UUID
    project_id: UUID
    parent_route_id: UUID | None = None
    title: str
    description: str = ""
    state: RouteState
    objections: list[str] = Field(default_factory=list)
    revival_conditions: list[str] = Field(default_factory=list)
    closure_evidence_refs: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class RouteStateChange(BaseModel):
    model_config = ConfigDict(extra="forbid")

    new_state: RouteState
    reason: str = Field(min_length=1, max_length=8000)
    evidence_refs: list[str] = Field(default_factory=list)
    human_confirmed: bool = False
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class RouteSplitChild(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=240)
    description: str = Field(default="", max_length=8000)
    initial_state: RouteState = RouteState.SEED
    revival_conditions: list[str] = Field(default_factory=list)


class RouteSplitRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    children: list[RouteSplitChild] = Field(min_length=2, max_length=20)
    reason: str = Field(min_length=1, max_length=8000)
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class RouteSplitResponse(BaseModel):
    source_route_id: UUID
    created_routes: list[RouteRecord]
    event_id: UUID


class RouteMergeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_route_ids: list[UUID] = Field(min_length=2, max_length=20)
    title: str = Field(min_length=1, max_length=240)
    description: str = Field(default="", max_length=8000)
    reason: str = Field(min_length=1, max_length=8000)
    supersede_sources: bool = True
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))

    @field_validator("source_route_ids")
    @classmethod
    def source_ids_are_unique(cls, value: list[UUID]) -> list[UUID]:
        if len(set(value)) != len(value):
            raise ValueError("source_route_ids must be unique")
        return value


class RouteMergeResponse(BaseModel):
    merged_route: RouteRecord
    source_route_ids: list[UUID]
    event_id: UUID


class BranchCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    route_id: UUID
    title: str = Field(min_length=1, max_length=240)
    description: str = Field(default="", max_length=8000)
    parent_branch_id: UUID | None = None
    assumptions: list[str] = Field(default_factory=list)
    parameters: dict[str, Any] = Field(default_factory=dict)
    initial_state: BranchState = BranchState.SEED
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class BranchRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    branch_id: UUID
    project_id: UUID
    route_id: UUID
    parent_branch_id: UUID | None = None
    title: str
    description: str = ""
    assumptions: list[str] = Field(default_factory=list)
    parameters: dict[str, Any] = Field(default_factory=dict)
    state: BranchState
    created_at: datetime
    updated_at: datetime


class BranchStateChange(BaseModel):
    model_config = ConfigDict(extra="forbid")

    new_state: BranchState
    reason: str = Field(min_length=1, max_length=8000)
    evidence_refs: list[str] = Field(default_factory=list)
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class ChallengeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    route_id: UUID | None = None
    branch_id: UUID | None = None
    challenge_type: ChallengeType = ChallengeType.OBJECTION
    statement: str = Field(min_length=1, max_length=16000)
    test_plan: str = Field(default="", max_length=16000)
    evidence_refs: list[str] = Field(default_factory=list)
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))

    @model_validator(mode="after")
    def target_required(self) -> ChallengeCreate:
        if self.route_id is None and self.branch_id is None:
            raise ValueError("a challenge must target a route or branch")
        return self


class ChallengeRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    challenge_id: UUID
    project_id: UUID
    route_id: UUID | None = None
    branch_id: UUID | None = None
    challenge_type: ChallengeType
    status: ChallengeStatus
    statement: str
    test_plan: str = ""
    evidence_refs: list[str] = Field(default_factory=list)
    resolution_summary: str = ""
    created_at: datetime
    updated_at: datetime


class ChallengeStatusChange(BaseModel):
    model_config = ConfigDict(extra="forbid")

    new_status: ChallengeStatus
    resolution_summary: str = Field(default="", max_length=16000)
    evidence_refs: list[str] = Field(default_factory=list)
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class BridgeResultCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    route_id: UUID
    branch_id: UUID | None = None
    title: str = Field(min_length=1, max_length=240)
    summary: str = Field(min_length=1, max_length=16000)
    enabled_route_ids: list[UUID] = Field(default_factory=list)
    artifact_refs: list[str] = Field(default_factory=list)
    retained_value: list[str] = Field(default_factory=list)
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class BridgeResultRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bridge_result_id: UUID
    project_id: UUID
    route_id: UUID
    branch_id: UUID | None = None
    title: str
    summary: str
    enabled_route_ids: list[UUID] = Field(default_factory=list)
    artifact_refs: list[str] = Field(default_factory=list)
    retained_value: list[str] = Field(default_factory=list)
    status: BridgeResultStatus = BridgeResultStatus.ACTIVE
    created_at: datetime
    updated_at: datetime


class DeadEndConstraintCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=240)
    description: str = Field(min_length=1, max_length=16000)
    route_id: UUID | None = None
    branch_id: UUID | None = None
    applicability_scope: list[str] = Field(default_factory=list)
    prior_attempt_refs: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    strength: DeadEndStrength = DeadEndStrength.OBSERVED
    reopen_conditions: list[str] = Field(default_factory=list)
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class DeadEndConstraintRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dead_end_id: UUID
    project_id: UUID
    route_id: UUID | None = None
    branch_id: UUID | None = None
    title: str
    description: str
    applicability_scope: list[str] = Field(default_factory=list)
    prior_attempt_refs: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    strength: DeadEndStrength
    reopen_conditions: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class ResearchCheckpointCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    current_target: str = Field(min_length=1, max_length=16000)
    route_id: UUID | None = None
    branch_id: UUID | None = None
    intended_move: str = Field(default="", max_length=16000)
    assumptions_used: list[str] = Field(default_factory=list)
    expected_result: str = Field(default="", max_length=16000)
    produced_artifact_refs: list[str] = Field(default_factory=list)
    observed_failure_or_gain: str = Field(default="", max_length=16000)
    confidence: CheckpointConfidence = CheckpointConfidence.UNSPECIFIED
    unresolved_obligations: list[str] = Field(default_factory=list)
    next_route_suggestions: list[str] = Field(default_factory=list)
    source_session_ref: str | None = Field(default=None, max_length=1000)
    actor: Actor


class ResearchCheckpointRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    checkpoint_id: UUID
    project_id: UUID
    current_target: str
    route_id: UUID | None = None
    branch_id: UUID | None = None
    intended_move: str = ""
    assumptions_used: list[str] = Field(default_factory=list)
    expected_result: str = ""
    produced_artifact_refs: list[str] = Field(default_factory=list)
    observed_failure_or_gain: str = ""
    confidence: CheckpointConfidence
    unresolved_obligations: list[str] = Field(default_factory=list)
    next_route_suggestions: list[str] = Field(default_factory=list)
    source_session_ref: str | None = None
    actor: Actor
    created_at: datetime


class HumanNoteCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    content: str = Field(min_length=1)
    route_id: UUID | None = None
    branch_id: UUID | None = None
    note_type: Literal[
        "INTUITION",
        "DEFINITION",
        "COUNTEREXAMPLE",
        "ROUTE_PRIORITY",
        "VISUAL_ANNOTATION",
        "SOURCE",
        "SIMPLIFICATION_GOAL",
        "FREEZE",
        "REVIVE",
        "MERGE",
        "REDIRECT",
        "GENERAL",
    ] = "GENERAL"
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class GenericEventCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_type: str = Field(min_length=3, max_length=120)
    actor: Actor
    route_id: UUID | None = None
    branch_id: UUID | None = None
    artifact_refs: list[str] = Field(default_factory=list)
    caused_by: list[str] = Field(default_factory=list)
    epistemic_delta: str | None = None
    epistemic_delta_type: EpistemicDeltaType | None = None
    payload: dict[str, Any] = Field(default_factory=dict)

    @field_validator("event_type")
    @classmethod
    def normalize_event_type(cls, value: str) -> str:
        return value.strip().upper().replace(" ", "_")


class EventRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    schema_version: str = SCHEMA_VERSION
    event_id: UUID
    event_type: str
    project_id: UUID
    timestamp: datetime
    actor: Actor
    caused_by: list[str] = Field(default_factory=list)
    route_id: UUID | None = None
    branch_id: UUID | None = None
    artifact_refs: list[str] = Field(default_factory=list)
    payload: dict[str, Any] = Field(default_factory=dict)
    epistemic_delta: str | None = None
    epistemic_delta_type: EpistemicDeltaType | None = None
    previous_event_hash: str | None = None
    event_hash: str

    _schema_version = field_validator("schema_version")(_validate_schema_version)


class ArtifactRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: UUID
    project_id: UUID
    artifact_type: ArtifactType
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    media_type: str
    size_bytes: int = Field(ge=0)
    origin: ArtifactOrigin
    original_filename: str
    blob_relpath: str
    source_ref: str | None = None
    interpretation_status: InterpretationStatus = InterpretationStatus.RAW
    created_at: datetime


class ResearchPacketRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    route_ids: list[UUID] = Field(default_factory=list)
    include_recent_events: int = Field(default=30, ge=0, le=500)
    include_checkpoints: int = Field(default=8, ge=0, le=100)
    purpose: str = Field(default="Continue open mathematical exploration")
    special_instructions: str = ""


class ResearchPacketResponse(BaseModel):
    generated_at: datetime
    markdown: str


class IntegrityReport(BaseModel):
    project_id: UUID
    event_count: int
    valid: bool
    projection_schema_version: int = Field(default=0, ge=0)
    first_invalid_index: int | None = None
    error: str | None = None


class ImportPreflightReport(BaseModel):
    """Read-only compatibility and safety diagnosis for a .smath archive."""

    archive_name: str
    archive_bytes: int = Field(ge=0)
    file_count: int = Field(ge=0)
    compressed_bytes: int = Field(ge=0)
    uncompressed_bytes: int = Field(ge=0)
    schema_version: str | None = None
    project_id: UUID | None = None
    event_count: int = Field(default=0, ge=0)
    event_chain_valid: bool | None = None
    first_invalid_event_index: int | None = None
    event_chain_error: str | None = None
    missing_artifact_paths: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    can_import: bool


class ChatMessageCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_id: UUID
    sequence: int = Field(ge=0)
    role: Literal["user", "assistant", "system", "tool", "unknown"]
    content: str = Field(min_length=1)
    suggested_disposition: ImportDisposition = ImportDisposition.MODEL_NOTE


class ChatImportPreviewRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    import_id: UUID
    project_id: UUID
    artifact_id: UUID
    source_filename: str
    import_format: ImportFormat
    parser_name: str
    candidates: list[ChatMessageCandidate]
    created_at: datetime
    confirmed_at: datetime | None = None


class ChatImportSelection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_id: UUID
    disposition: ImportDisposition
    route_id: UUID | None = None
    branch_id: UUID | None = None
    title: str | None = Field(default=None, max_length=240)
    content_override: str | None = None
    structured_payload: dict[str, Any] = Field(default_factory=dict)


class ChatImportConfirmRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    selections: list[ChatImportSelection]
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class ChatImportConfirmationResponse(BaseModel):
    import_id: UUID
    created_event_ids: list[UUID] = Field(default_factory=list)
    created_object_refs: list[str] = Field(default_factory=list)
    ignored_count: int = 0


class PluginPermissions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    network: bool = False
    filesystem_read: list[str] = Field(default_factory=lambda: ["project_inputs"])
    filesystem_write: list[str] = Field(default_factory=lambda: ["run_workspace"])
    environment_variables: list[str] = Field(default_factory=list)
    subprocess: bool = True


class PluginResources(BaseModel):
    model_config = ConfigDict(extra="forbid")

    max_cpu_seconds: int = Field(default=60, ge=1, le=3600)
    max_memory_mb: int = Field(default=1024, ge=64, le=65536)
    max_output_mb: int = Field(default=10, ge=1, le=4096)
    timeout_seconds: int = Field(default=20, ge=1, le=3600)


class PluginInstallSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["bundled", "local_command", "python_venv", "oci_container"] = "bundled"
    package: str | None = None
    image: str | None = None
    dependency_lock: list[str] = Field(default_factory=list)
    allow_network_install: bool = False


class PluginManifestRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str = SCHEMA_VERSION
    plugin_id: str = Field(min_length=3, max_length=160)
    version: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=240)
    description: str = Field(default="", max_length=4000)
    category: PluginCategory = PluginCategory.COMPUTE
    runner_type: PluginRunnerType = PluginRunnerType.PYTHON
    capabilities: list[str] = Field(default_factory=list)
    install: PluginInstallSpec = Field(default_factory=PluginInstallSpec)
    entrypoint: list[str] = Field(default_factory=list)
    healthcheck: list[str] = Field(default_factory=list)
    permissions: PluginPermissions = Field(default_factory=PluginPermissions)
    resources: PluginResources = Field(default_factory=PluginResources)
    isolation_level: Literal["process-only", "container", "external"] = "process-only"
    default_timeout_seconds: int = Field(default=20, ge=1, le=300)
    maximum_timeout_seconds: int = Field(default=60, ge=1, le=600)
    enabled_by_default: bool = False

    _schema_version = field_validator("schema_version")(_validate_schema_version)


class ProjectPluginRecord(BaseModel):
    plugin_id: str
    version: str
    enabled: bool
    lifecycle_status: PluginLifecycleStatus = PluginLifecycleStatus.DISCOVERED
    installed_at: datetime | None = None
    enabled_at: datetime | None = None
    last_healthcheck_at: datetime | None = None
    health_message: str = ""


class PluginInstallRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_version: str | None = None
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class PluginHealthRecord(BaseModel):
    plugin_id: str
    version: str
    healthy: bool
    checked_at: datetime
    message: str
    runner_type: PluginRunnerType


class GenericPluginRunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    input_text: str = Field(min_length=1, max_length=2_000_000)
    input_filename: str = Field(default="input.txt", min_length=1, max_length=240)
    arguments: list[str] = Field(default_factory=list, max_length=32)
    timeout_seconds: int = Field(default=20, ge=1, le=600)
    route_id: UUID | None = None
    branch_id: UUID | None = None
    input_artifact_ids: list[UUID] = Field(default_factory=list, max_length=32)
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class PythonPluginRunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_code: str = Field(min_length=1, max_length=500_000)
    stdin: str = Field(default="", max_length=2_000_000)
    arguments: list[str] = Field(default_factory=list, max_length=32)
    timeout_seconds: int = Field(default=20, ge=1, le=60)
    route_id: UUID | None = None
    branch_id: UUID | None = None
    input_artifact_ids: list[UUID] = Field(default_factory=list, max_length=32)
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class PluginRunRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: UUID
    project_id: UUID
    plugin_id: str
    plugin_version: str
    route_id: UUID | None = None
    branch_id: UUID | None = None
    status: PluginRunStatus
    command: list[str]
    runtime_version: str
    isolation_level: str
    timeout_seconds: int
    exit_code: int | None = None
    source_artifact_ref: str
    input_artifact_refs: list[str] = Field(default_factory=list)
    stdout_artifact_ref: str | None = None
    stderr_artifact_ref: str | None = None
    produced_artifact_refs: list[str] = Field(default_factory=list)
    output_truncated: bool = False
    started_at: datetime
    completed_at: datetime
    error: str | None = None


class ModelSessionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    connector_type: ConnectorType
    display_label: str = Field(min_length=1, max_length=240)
    reported_model: str = Field(default="", max_length=240)
    model_family: str = Field(default="", max_length=240)
    role: ArenaRole | None = None
    context_packet_refs: list[str] = Field(default_factory=list)
    output_artifact_refs: list[str] = Field(default_factory=list)
    completeness: SessionCompleteness = SessionCompleteness.UNKNOWN
    route_id: UUID | None = None
    branch_id: UUID | None = None
    notes: str = Field(default="", max_length=16000)
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class ModelSessionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: UUID
    project_id: UUID
    connector_type: ConnectorType
    display_label: str
    reported_model: str = ""
    model_family: str = ""
    role: ArenaRole | None = None
    context_packet_refs: list[str] = Field(default_factory=list)
    output_artifact_refs: list[str] = Field(default_factory=list)
    completeness: SessionCompleteness
    route_id: UUID | None = None
    branch_id: UUID | None = None
    notes: str = ""
    created_at: datetime


class HandoffArtifactCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    producing_session_ref: UUID
    receiving_session_refs: list[UUID] = Field(default_factory=list)
    artifact_type: HandoffArtifactType
    established_facts: list[str] = Field(default_factory=list)
    rejected_directions: list[str] = Field(default_factory=list)
    unresolved_items: list[str] = Field(default_factory=list)
    artifact_refs: list[str] = Field(default_factory=list)
    receiving_impact: str = Field(default="", max_length=16000)
    route_id: UUID | None = None
    branch_id: UUID | None = None
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class HandoffArtifactRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    handoff_id: UUID
    project_id: UUID
    producing_session_ref: UUID
    receiving_session_refs: list[UUID] = Field(default_factory=list)
    artifact_type: HandoffArtifactType
    established_facts: list[str] = Field(default_factory=list)
    rejected_directions: list[str] = Field(default_factory=list)
    unresolved_items: list[str] = Field(default_factory=list)
    artifact_refs: list[str] = Field(default_factory=list)
    receiving_impact: str = ""
    route_id: UUID | None = None
    branch_id: UUID | None = None
    created_at: datetime


class ArenaStage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stage_id: str = Field(min_length=1, max_length=160)
    role: ArenaRole
    connector_id: str | None = Field(default=None, max_length=240)
    input_selection: list[str] = Field(default_factory=list)
    output_kind: str = Field(default="research_checkpoint", max_length=240)
    human_gate_after: bool = True


class ArenaRecipeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=240)
    description: str = Field(default="", max_length=4000)
    compute_mode: ArenaComputeMode = ArenaComputeMode.CONSERVATIVE
    parallel_workers: int = Field(default=0, ge=0, le=16)
    stages: list[ArenaStage] = Field(min_length=1, max_length=32)
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class ArenaRecipeRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    recipe_id: UUID
    project_id: UUID
    name: str
    description: str = ""
    compute_mode: ArenaComputeMode
    parallel_workers: int = 0
    stages: list[ArenaStage]
    created_at: datetime


class ArenaPreviewRecord(BaseModel):
    recipe: ArenaRecipeRecord
    requires_human_confirmation: bool
    correlated_review_warnings: list[str] = Field(default_factory=list)
    execution_started: bool = False
    note: str = "Preview only. ProofFlow does not use role voting to determine mathematical truth."


class HistoricalSearchHit(BaseModel):
    kind: Literal[
        "route", "challenge", "bridge_result", "dead_end", "checkpoint", "handoff", "event"
    ]
    object_id: str
    title: str
    excerpt: str
    route_id: UUID | None = None
    branch_id: UUID | None = None
    created_at: datetime
    score: float = Field(ge=0)
    reopen_conditions: list[str] = Field(default_factory=list)


class EpistemicDeltaSummary(BaseModel):
    event_id: UUID
    event_type: str
    delta_type: EpistemicDeltaType
    description: str
    timestamp: datetime
    route_id: UUID | None = None
    branch_id: UUID | None = None


class CanvasSnapshotCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scene: dict[str, Any]
    author_description: str = Field(default="", max_length=16000)
    machine_interpretation: str = Field(default="", max_length=16000)
    mapping_status: VisualMappingStatus = VisualMappingStatus.UNMAPPED
    element_links: dict[str, str] = Field(default_factory=dict)
    actor: Actor = Field(default_factory=lambda: Actor(type=ActorType.HUMAN, id="local-researcher"))


class CanvasSnapshotRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    visual_id: UUID
    project_id: UUID
    original_artifact_ref: str
    author_description: str = ""
    machine_interpretation: str = ""
    machine_interpretation_ref: str | None = None
    mapping_status: VisualMappingStatus
    element_links: dict[str, str] = Field(default_factory=dict)
    created_at: datetime
    confirmed_by: str | None = None


class CanvasSnapshotResponse(BaseModel):
    visual_artifact: CanvasSnapshotRecord
    scene: dict[str, Any]


def new_uuid() -> UUID:
    return uuid4()
