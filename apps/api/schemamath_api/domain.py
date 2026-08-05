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

SCHEMA_VERSION = "0.6"
SUPPORTED_SCHEMA_VERSIONS = {"0.1", "0.2", "0.3", "0.4", "0.5", "0.6"}


class TraceDerivationClass(StrEnum):
    """Trace Derivation Classes (v0.13 §3): taxonomy of process transparency."""

    RAW_EVENT_STREAM = "RAW_EVENT_STREAM"
    REWRITTEN_LOG = "REWRITTEN_LOG"
    MODEL_RECONSTRUCTION = "MODEL_RECONSTRUCTION"
    HUMAN_SYNTHESIS = "HUMAN_SYNTHESIS"
    FINAL_ONLY_ARTIFACT = "FINAL_ONLY_ARTIFACT"


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


class ResearchPlane(StrEnum):
    """Independent v0.14 research-state coordinates."""

    OPERATIONAL = "operational"
    EPISTEMIC = "epistemic"
    CLAIM = "claim"
    ARTIFACT = "artifact"


class TransitionTriggerClass(StrEnum):
    OBSERVATION = "OBSERVATION"
    TOOL_RESULT = "TOOL_RESULT"
    MODEL_PROPOSAL = "MODEL_PROPOSAL"
    HUMAN_DECISION = "HUMAN_DECISION"
    EXACT_CHECK = "EXACT_CHECK"
    EXTERNAL_UPDATE = "EXTERNAL_UPDATE"
    PUBLIC_CORRECTION = "PUBLIC_CORRECTION"


class TransitionVisibility(StrEnum):
    DIRECT_OBSERVATION = "DIRECT_OBSERVATION"
    PUBLIC_TRACE_DERIVATION = "PUBLIC_TRACE_DERIVATION"
    AUTHOR_REPORTED = "AUTHOR_REPORTED"
    NOT_ESTABLISHED = "NOT_ESTABLISHED"


class TransitionProposalStatus(StrEnum):
    PROPOSED = "PROPOSED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class ContinuationDecision(StrEnum):
    RUN_NEXT = "RUN_NEXT"
    WAIT = "WAIT"
    REDIRECT = "REDIRECT"
    ASK_HUMAN = "ASK_HUMAN"
    STOP = "STOP"
    NO_CHANGE = "NO_CHANGE"


class ContinuationStatus(StrEnum):
    RECORDED = "RECORDED"
    REJECTED = "REJECTED"


class HandoffPacketStatus(StrEnum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class ClaimSourceClass(StrEnum):
    DIRECT_OBSERVATION = "DIRECT_OBSERVATION"
    TOOL_RESULT = "TOOL_RESULT"
    FORMAL_EXECUTION = "FORMAL_EXECUTION"
    AUTHOR_REPORTED = "AUTHOR_REPORTED"
    LEGACY = "LEGACY"
    UNKNOWN = "UNKNOWN"


class ClaimState(StrEnum):
    UNRESOLVED = "UNRESOLVED"
    CANDIDATE = "CANDIDATE"
    SUPPORTED = "SUPPORTED"
    REFUTED = "REFUTED"
    SUPERSEDED = "SUPERSEDED"


class ClaimRelationType(StrEnum):
    SUPPORTS = "SUPPORTS"
    REFUTES = "REFUTES"
    SUPERSEDES = "SUPERSEDES"
    DERIVED_FROM = "DERIVED_FROM"


class EvidenceDimensionStatus(StrEnum):
    UNKNOWN = "UNKNOWN"
    SUPPORTED = "SUPPORTED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class EvidenceDimensionName(StrEnum):
    PROVENANCE = "provenance"
    ARTIFACT_ACCESSIBILITY = "artifact_accessibility"
    DERIVATION_VALIDITY = "derivation_validity"
    INDEPENDENT_REPRODUCTION = "independent_reproduction"
    NEGATIVE_PRESSURE = "negative_pressure"
    AUDITABILITY = "auditability"


class VerificationExecutionStatus(StrEnum):
    CONFIGURED = "CONFIGURED"
    EXECUTED = "EXECUTED"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    UNAVAILABLE = "UNAVAILABLE"


class CoverageStatus(StrEnum):
    COVERED = "COVERED"
    PARTIAL = "PARTIAL"
    MISSING = "MISSING"
    UNKNOWN = "UNKNOWN"


class RepairLineageType(StrEnum):
    REPAIR = "REPAIR"
    REVERSION = "REVERSION"
    SUPERSESSION = "SUPERSESSION"
    FOLLOW_UP = "FOLLOW_UP"


class AttemptOutcome(StrEnum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    TIMED_OUT = "TIMED_OUT"
    DUPLICATE = "DUPLICATE"
    ROLLED_BACK = "ROLLED_BACK"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    REJECTED = "REJECTED"
    NO_CHANGE = "NO_CHANGE"


class DossierSourceClass(StrEnum):
    RAW_EVENT = "RAW_EVENT"
    TOOL_ARTIFACT = "TOOL_ARTIFACT"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    MODEL_REPORTED = "MODEL_REPORTED"
    LEGACY = "LEGACY"
    UNKNOWN = "UNKNOWN"


class HierarchyNodeType(StrEnum):
    EPISODE = "EPISODE"
    RESULT_FAMILY = "RESULT_FAMILY"
    DEPENDENCY_METHOD = "DEPENDENCY_METHOD"
    CLAIM_ATOM = "CLAIM_ATOM"
    FORMAL_TARGET_BUNDLE = "FORMAL_TARGET_BUNDLE"
    MANUSCRIPT_SECTION = "MANUSCRIPT_SECTION"
    SOURCE_FILE = "SOURCE_FILE"
    CHALLENGE_CONFIG = "CHALLENGE_CONFIG"


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

    @field_validator("initial_state")
    @classmethod
    def _initial_state_not_closed(cls, value: RouteState) -> RouteState:
        if value == RouteState.CERTIFIED_CLOSED:
            raise ValueError(
                "CERTIFIED_CLOSED cannot be an initial state; it requires "
                "human confirmation and closure evidence via a state transition"
            )
        return value


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

    @field_validator("initial_state")
    @classmethod
    def _initial_state_not_closed(cls, value: RouteState) -> RouteState:
        if value == RouteState.CERTIFIED_CLOSED:
            raise ValueError(
                "CERTIFIED_CLOSED cannot be an initial state; it requires "
                "human confirmation and closure evidence via a state transition"
            )
        return value


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

    @field_validator("initial_state")
    @classmethod
    def _initial_state_not_terminal(cls, value: BranchState) -> BranchState:
        if value == BranchState.COMPLETED:
            raise ValueError("COMPLETED cannot be an initial state")
        return value


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
    objections: list[str] = Field(default_factory=list)
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
    # Alpha.5 control-plane metadata. These remain optional so Alpha.1–Alpha.4
    # event lines can be read without rewriting historical JSONL.
    revision: int | None = Field(default=None, ge=1)
    batch_id: UUID | None = None
    idempotency_key: str | None = Field(default=None, max_length=240)
    command_id: str | None = Field(default=None, max_length=240)

    _schema_version = field_validator("schema_version")(_validate_schema_version)


class ResearchStateSnapshot(BaseModel):
    """Rebuildable four-plane state snapshot for the Alpha.5 transition kernel."""

    model_config = ConfigDict(extra="forbid")

    project_id: UUID
    revision: int = Field(default=0, ge=0)
    operational: dict[str, Any] = Field(default_factory=dict)
    epistemic: dict[str, Any] = Field(default_factory=dict)
    claim: dict[str, Any] = Field(default_factory=dict)
    artifact: dict[str, Any] = Field(default_factory=dict)
    as_of: datetime


class TransitionProposalCreate(BaseModel):
    """Observable state proposal; creating it does not change any plane."""

    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    trigger_class: TransitionTriggerClass
    trigger_evidence_refs: list[str] = Field(default_factory=list)
    accepted_delta: dict[str, dict[str, Any]] = Field(default_factory=dict)
    rejected_components: list[str] = Field(default_factory=list)
    next_obligation_refs: list[str] = Field(default_factory=list)
    handoff_refs: list[str] = Field(default_factory=list)
    visibility: TransitionVisibility = TransitionVisibility.NOT_ESTABLISHED
    proposal_actor: Actor

    @field_validator("accepted_delta")
    @classmethod
    def validate_plane_keys(cls, value: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
        allowed = {plane.value for plane in ResearchPlane}
        unknown = set(value) - allowed
        if unknown:
            raise ValueError(f"accepted_delta contains unknown research planes: {sorted(unknown)}")
        return value


class TransitionProposalRecord(TransitionProposalCreate):
    proposal_id: UUID
    project_id: UUID
    status: TransitionProposalStatus = TransitionProposalStatus.PROPOSED
    created_at: datetime


class TransitionAcceptanceCreate(BaseModel):
    """Human/mechanism acceptance of a previously proposed transition."""

    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    acceptance_actor: Actor
    acceptance_mechanism: str = Field(min_length=1, max_length=240)
    accepted: bool = True
    rejection_reason: str = Field(default="", max_length=4000)


class ResearchStateTransitionRecord(BaseModel):
    """Accepted or rejected transition with explicit M2 provenance."""

    model_config = ConfigDict(extra="forbid")

    transition_id: UUID
    proposal_id: UUID
    project_id: UUID
    from_revision: int = Field(ge=0)
    to_revision: int = Field(ge=0)
    trigger_class: TransitionTriggerClass
    trigger_evidence_refs: list[str] = Field(default_factory=list)
    proposal_actor: Actor
    acceptance_actor_or_mechanism_ref: str
    accepted_delta: dict[str, dict[str, Any]] = Field(default_factory=dict)
    rejected_components: list[str] = Field(default_factory=list)
    next_obligation_refs: list[str] = Field(default_factory=list)
    handoff_refs: list[str] = Field(default_factory=list)
    visibility: TransitionVisibility
    accepted: bool
    rejection_reason: str = ""
    idempotency_key: str
    accepted_at: datetime


class CommandReceipt(BaseModel):
    """Stable receipt returned by a command that touched the event stream."""

    model_config = ConfigDict(extra="forbid")

    command_id: UUID
    project_id: UUID
    operation: str
    accepted: bool
    idempotent_replay: bool = False
    from_revision: int = Field(ge=0)
    to_revision: int = Field(ge=0)
    event_ids: list[UUID] = Field(default_factory=list)
    batch_id: UUID | None = None
    projection_revision: int = Field(ge=0)
    error: str | None = None


class ContinuationContractCreate(BaseModel):
    """Typed end-of-episode instruction; it never hides an unrecorded action."""

    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    decision: ContinuationDecision
    scope: str = Field(min_length=1, max_length=4000)
    obligation_refs: list[str] = Field(default_factory=list)
    handoff_refs: list[str] = Field(default_factory=list)
    reason: str = Field(default="", max_length=4000)
    human_confirmed: bool = False
    actor: Actor

    @model_validator(mode="after")
    def require_human_for_run_next(self) -> ContinuationContractCreate:
        if self.decision is ContinuationDecision.RUN_NEXT and (
            self.actor.type is not ActorType.HUMAN or not self.human_confirmed
        ):
            raise ValueError("RUN_NEXT requires explicit human confirmation")
        return self


class ContinuationContractRecord(ContinuationContractCreate):
    contract_id: UUID
    project_id: UUID
    source_revision: int = Field(ge=0)
    status: ContinuationStatus = ContinuationStatus.RECORDED
    created_at: datetime


class HandoffPacketV2Create(BaseModel):
    """Evidence-oriented handoff packet; all claims remain source-referenced."""

    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    scope: str = Field(min_length=1, max_length=4000)
    tool_hashes: list[str] = Field(default_factory=list)
    fact_evidence_refs: list[str] = Field(default_factory=list)
    failure_evidence_refs: list[str] = Field(default_factory=list)
    revival_conditions: list[str] = Field(default_factory=list)
    obligation_refs: list[str] = Field(default_factory=list)
    next_receiver_refs: list[str] = Field(default_factory=list)
    source_session_ref: UUID | None = None
    actor: Actor


class HandoffPacketV2Record(HandoffPacketV2Create):
    packet_id: UUID
    project_id: UUID
    from_revision: int = Field(ge=0)
    packet_hash: str = Field(min_length=64, max_length=64)
    status: HandoffPacketStatus = HandoffPacketStatus.PENDING
    created_at: datetime


class HandoffDecisionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    accepted: bool
    reason: str = Field(default="", max_length=4000)
    acceptance_actor: Actor


class HandoffReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    receipt_id: UUID
    packet_id: UUID
    project_id: UUID
    accepted: bool
    reason: str = ""
    from_revision: int = Field(ge=0)
    to_revision: int = Field(ge=0)
    acceptance_actor: Actor
    accepted_at: datetime


class ClaimAtomCreate(BaseModel):
    """A source-addressed claim proposal; acceptance is performed by M1."""

    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    statement: str = Field(min_length=1, max_length=16000)
    source_refs: list[str] = Field(default_factory=list)
    source_class: ClaimSourceClass = ClaimSourceClass.UNKNOWN
    interpretation: str = Field(default="", max_length=16000)
    definitions: dict[str, str] = Field(default_factory=dict)
    quantifiers: list[str] = Field(default_factory=list)
    scope: dict[str, Any] = Field(default_factory=dict)
    relations: list[str] = Field(default_factory=list)
    open_obligation_refs: list[str] = Field(default_factory=list)
    actor: Actor


class ClaimAtomRecord(ClaimAtomCreate):
    claim_id: UUID
    project_id: UUID
    version: int = Field(default=1, ge=1)
    state: ClaimState = ClaimState.UNRESOLVED
    as_of: datetime


class ClaimRelationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    source_claim_id: UUID
    target_claim_id: UUID
    relation: ClaimRelationType
    evidence_refs: list[str] = Field(default_factory=list)
    actor: Actor


class ClaimRelationRecord(ClaimRelationCreate):
    relation_id: UUID
    project_id: UUID
    created_at: datetime


class EvidenceDimension(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_refs: list[str] = Field(default_factory=list)
    status: EvidenceDimensionStatus = EvidenceDimensionStatus.UNKNOWN
    evaluator_ref: str = ""
    note: str = Field(default="", max_length=4000)


class ReviewLineage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lineage_id: UUID
    reviewer_family: str = ""
    organization: str = ""
    editor: str = ""
    source_material_refs: list[str] = Field(default_factory=list)
    formatter: str = ""
    checker: str = ""
    scope: str = ""
    unchecked_items: list[str] = Field(default_factory=list)
    independence_group: str = ""
    correlation_flags: list[str] = Field(default_factory=list)


class ReviewLineageCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    reviewer_family: str = ""
    organization: str = ""
    editor: str = ""
    source_material_refs: list[str] = Field(default_factory=list)
    formatter: str = ""
    checker: str = ""
    scope: str = ""
    unchecked_items: list[str] = Field(default_factory=list)
    independence_group: str = ""
    correlation_flags: list[str] = Field(default_factory=list)
    actor: Actor


class EvidenceCardCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    claim_id: UUID
    dimensions: dict[EvidenceDimensionName, EvidenceDimension]
    review_lineage_ref: UUID | None = None
    actor: Actor

    @model_validator(mode="after")
    def require_all_dimensions(self) -> EvidenceCardCreate:
        missing = set(EvidenceDimensionName) - set(self.dimensions)
        if missing:
            raise ValueError(f"evidence card is missing dimensions: {sorted(item.value for item in missing)}")
        return self


class EvidenceCardRecord(EvidenceCardCreate):
    card_id: UUID
    project_id: UUID
    created_at: datetime


class ReviewLineageRecord(ReviewLineage):
    project_id: UUID
    created_at: datetime


class MutationObservation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mutation_id: str = Field(min_length=1, max_length=240)
    expected: str
    observed: str
    passed: bool
    note: str = ""


class VerificationExecutionManifestCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    command: list[str] = Field(min_length=1, max_length=64)
    working_directory: str = ""
    environment_fingerprint: dict[str, str] = Field(default_factory=dict)
    dependency_lock_refs: list[str] = Field(default_factory=list)
    exit_status: int | None = None
    stdout_artifact_ref: str | None = None
    stderr_artifact_ref: str | None = None
    verification_check_ids: list[str] = Field(default_factory=list)
    axiom_ceiling: list[str] = Field(default_factory=list)
    target_scope: str = ""
    timeout_seconds: int | None = Field(default=None, ge=1)
    status: VerificationExecutionStatus = VerificationExecutionStatus.CONFIGURED
    actor: Actor


class VerificationExecutionManifestRecord(VerificationExecutionManifestCreate):
    execution_id: UUID
    project_id: UUID
    executed_at: datetime
    manifest_sha256: str = Field(min_length=64, max_length=64)


class VerificationMutationSetCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    execution_id: UUID
    mutations: list[MutationObservation] = Field(min_length=1)
    actor: Actor


class VerificationMutationSetRecord(VerificationMutationSetCreate):
    mutation_set_id: UUID
    project_id: UUID
    created_at: datetime
    all_expected_failures: bool


class FormalCoverageBindingCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    challenge_id: str
    headline_statement_ref: str
    covered_declaration_refs: list[str] = Field(default_factory=list)
    missing_declaration_refs: list[str] = Field(default_factory=list)
    status: CoverageStatus = CoverageStatus.UNKNOWN
    actor: Actor


class FormalCoverageBindingRecord(FormalCoverageBindingCreate):
    binding_id: UUID
    project_id: UUID
    created_at: datetime


class RepositorySnapshotCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    repository_url: str = ""
    ref: str = ""
    commit: str = ""
    observed_at: datetime
    parent_commit: str | None = None
    diff_ref: str | None = None
    actor: Actor


class RepositorySnapshotRecord(RepositorySnapshotCreate):
    snapshot_id: UUID
    project_id: UUID
    created_at: datetime


class RepairLineageCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    repair_type: RepairLineageType
    input_refs: list[str] = Field(default_factory=list)
    output_refs: list[str] = Field(default_factory=list)
    affected_claim_refs: list[str] = Field(default_factory=list)
    downstream_reopen_obligations: list[str] = Field(default_factory=list)
    actor: Actor


class RepairLineageRecord(RepairLineageCreate):
    repair_id: UUID
    project_id: UUID
    created_at: datetime
    repair_sha256: str = Field(min_length=64, max_length=64)


class ResearchHierarchyNodeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    node_type: HierarchyNodeType
    label: str = Field(min_length=1, max_length=4000)
    parent_refs: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    payload: dict[str, Any] = Field(default_factory=dict)
    actor: Actor


class ResearchHierarchyNodeRecord(ResearchHierarchyNodeCreate):
    node_id: UUID
    project_id: UUID
    created_at: datetime


class AttemptRecordCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    target_ref: str
    method_ref: str = ""
    outcome: AttemptOutcome
    started_at: datetime
    completed_at: datetime | None = None
    input_refs: list[str] = Field(default_factory=list)
    output_refs: list[str] = Field(default_factory=list)
    failure_observations: list[str] = Field(default_factory=list)
    no_change_reason: str = ""
    actor: Actor


class AttemptRecord(AttemptRecordCreate):
    attempt_id: UUID
    project_id: UUID
    created_at: datetime


class CostVector(BaseModel):
    model_config = ConfigDict(extra="forbid")

    discovery: float = Field(default=0, ge=0)
    failed_attempts: float = Field(default=0, ge=0)
    human_selection: float = Field(default=0, ge=0)
    human_binding: float = Field(default=0, ge=0)
    human_review: float = Field(default=0, ge=0)
    compute: float = Field(default=0, ge=0)
    formalization: float = Field(default=0, ge=0)
    checking: float = Field(default=0, ge=0)
    independent_reproduction: float = Field(default=0, ge=0)
    infrastructure: float = Field(default=0, ge=0)


class CostVectorRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cost_id: UUID
    project_id: UUID
    scope_ref: str
    currency: str = "USD"
    vector: CostVector
    source_refs: list[str] = Field(default_factory=list)
    actor: Actor
    created_at: datetime


class CostVectorCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    scope_ref: str
    currency: str = "USD"
    vector: CostVector
    source_refs: list[str] = Field(default_factory=list)
    actor: Actor


class MicroFalsificationPlanCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    target_ref: str
    hypotheses: list[str] = Field(min_length=1)
    tests: list[str] = Field(min_length=1)
    stopping_conditions: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    actor: Actor


class MicroFalsificationPlanRecord(MicroFalsificationPlanCreate):
    plan_id: UUID
    project_id: UUID
    created_at: datetime


class BenchmarkBindingCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    benchmark_ref: str
    target_refs: list[str] = Field(default_factory=list)
    metric_definition: str
    baseline_ref: str = ""
    result_refs: list[str] = Field(default_factory=list)
    actor: Actor


class BenchmarkBindingRecord(BenchmarkBindingCreate):
    binding_id: UUID
    project_id: UUID
    created_at: datetime


DOSSIER_V2_FIELD_NAMES = (
    "episode_identity",
    "target_specification",
    "scope_and_definitions",
    "operational_configuration",
    "model_and_tool_identifiers",
    "input_provenance",
    "raw_event_coverage",
    "search_topology",
    "attempt_outcomes",
    "failure_observations",
    "negative_pressure",
    "claim_atoms",
    "claim_relations",
    "artifact_inventory",
    "verification_manifests",
    "formal_coverage",
    "axiom_ceiling",
    "kernel_execution",
    "independent_reproduction",
    "review_lineage",
    "repair_lineage",
    "continuation_contract",
    "handoff_receipts",
    "cost_vector",
    "micro_falsification",
    "benchmark_binding",
    "unresolved_obligations",
)


class DossierField(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: Any = None
    source_class: DossierSourceClass = DossierSourceClass.UNKNOWN
    source_refs: list[str] = Field(default_factory=list)


class ResearchEpisodeDossierV2Create(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    episode_ref: str
    fields: dict[str, DossierField]
    actor: Actor

    @model_validator(mode="after")
    def require_27_fields(self) -> ResearchEpisodeDossierV2Create:
        required = set(DOSSIER_V2_FIELD_NAMES)
        missing = required - set(self.fields)
        if missing:
            raise ValueError(f"dossier v2 is missing fields: {sorted(missing)}")
        return self


class ResearchEpisodeDossierV2Record(ResearchEpisodeDossierV2Create):
    dossier_id: UUID
    project_id: UUID
    dossier_sha256: str = Field(min_length=64, max_length=64)
    created_at: datetime


class QuestionAgendaCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=0)
    idempotency_key: str = Field(min_length=1, max_length=240)
    episode_ref: str
    target_specification: str
    questions: list[dict[str, Any]] = Field(default_factory=list)
    parent_child_edges: list[tuple[str, str]] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    actor: Actor


class QuestionAgendaRecord(QuestionAgendaCreate):
    agenda_id: UUID
    project_id: UUID
    coverage_score: float = Field(ge=0, le=1)
    created_at: datetime


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

    @field_validator("plugin_id", "version")
    @classmethod
    def _no_path_characters(cls, value: str) -> str:
        if not value or any(ch.isspace() or ord(ch) < 0x20 for ch in value):
            raise ValueError(f"must not contain whitespace or control characters: {value!r}")
        if value.startswith(".") or ".." in value or "/" in value or "\\" in value:
            raise ValueError(
                f"must not contain path separators or '..': {value!r}"
            )
        return value

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
