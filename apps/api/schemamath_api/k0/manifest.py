"""
K0 Trust Kernel — Module Manifest

Every module that participates in the K0 lifecycle must declare a manifest
specifying its identity, capabilities, requirements, lifecycle hooks,
security privileges, failure semantics, and guarantees.

The manifest serves as the single source of truth for what a module is,
what it can do, what it needs, and how it behaves under failure.

Design principles:
    - Modules cannot silently expand external privileges (Monotonic Consequences)
    - Only K0 executes side-effects; modules propose, K0 commits
    - Failure defaults to FAIL_CLOSED unless explicitly declared otherwise
    - Every module must declare what it does NOT guarantee
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, model_validator


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class ModuleKind(StrEnum):
    """
    Kind of module, determining its role in the K0 lifecycle.

    Only K0 itself may perform side-effects.  All other module kinds
    operate through proposals that K0 arbitrates and commits.
    """

    OBSERVER = "observer"
    """Read-only monitoring — no state mutation, no decisions."""

    GATE = "gate"
    """Pre/post validation gate — may ALLOW, DENY, or REQUIRE_EVIDENCE."""

    STATE_MACHINE = "state_machine"
    """Manages internal state transitions with declared transition rules."""

    TRANSFORMER = "transformer"
    """Pure data transformation — no side-effects, deterministic output."""

    VERIFIER = "verifier"
    """Verification and validation — checks claims against evidence."""

    ROUTER = "router"
    """Decision routing — directs flow based on context and policy."""

    SCHEDULER = "scheduler"
    """Lifecycle and task scheduling — proposes execution ordering."""

    ADAPTER = "adapter"
    """External system integration — bridges to tools, models, or services."""


class FailureSemantics(StrEnum):
    """
    How the module behaves when it encounters an error.

    The K0 kernel uses this declaration to determine system-level behavior
    when a module fails.  FAIL_CLOSED is the safest default.
    """

    FAIL_CLOSED = "fail_closed"
    """Block execution entirely.  No operation proceeds past this module."""

    DEFER = "defer"
    """Pass the decision to the next module in the chain."""

    DEGRADE = "degrade"
    """Continue with explicitly reduced capability.  Must declare what degrades."""

    REQUIRE_HUMAN = "require_human"
    """Halt execution and require human intervention before proceeding."""


class CriticalityLevel(StrEnum):
    """How critical this module is to system operation."""

    REQUIRED = "required"
    """System cannot operate without this module."""

    RECOMMENDED = "recommended"
    """System works but with reduced guarantees when this module is absent."""

    OPTIONAL = "optional"
    """Nice to have.  No impact on core guarantees if missing."""


class LifecyclePhase(StrEnum):
    """
    Fixed lifecycle phases P0–P10.

    Instead of arbitrary compose() middleware chains where safety depends
    on loading order, execution follows these fixed phases.  Modules
    register hooks into specific phases; K0 schedules them in order.
    """

    P0_LOAD_ATTEST = "P0_LOAD_ATTEST"
    """Load module, verify integrity, attest identity."""

    P1_INPUT_NORMALIZATION = "P1_INPUT_NORMALIZATION"
    """Normalize and validate incoming data."""

    P2_GOAL_BINDING = "P2_GOAL_BINDING"
    """Bind operation to declared goals; detect drift."""

    P3_PLAN_PROPOSAL = "P3_PLAN_PROPOSAL"
    """Propose execution plan; modules contribute sub-plans."""

    P4_ACTION_AUTH = "P4_ACTION_AUTH"
    """Authorize proposed actions against capability grants."""

    P5_EXECUTION = "P5_EXECUTION"
    """Execute authorized actions (only K0 performs side-effects)."""

    P6_ARTIFACT_RECORDING = "P6_ARTIFACT_RECORDING"
    """Record artifacts produced during execution."""

    P7_ASSERTION_EVALUATION = "P7_ASSERTION_EVALUATION"
    """Evaluate assertions and claims against evidence."""

    P8_RELEASE_AUTH = "P8_RELEASE_AUTH"
    """Authorize release of results to external consumers."""

    P9_ATOMIC_COMMIT = "P9_ATOMIC_COMMIT"
    """Atomically commit all state changes to the event journal."""

    P10_TEARDOWN_COMPACT = "P10_TEARDOWN_COMPACT"
    """Teardown temporary resources; compact if needed."""


class HookType(StrEnum):
    """When within a phase a hook runs."""

    PRE = "pre"
    """Runs before the phase's core logic."""

    POST = "post"
    """Runs after the phase's core logic."""


# ---------------------------------------------------------------------------
# Nested Models
# ---------------------------------------------------------------------------

class CapabilityDeclaration(BaseModel):
    """
    A capability that a module provides or requires.

    Capabilities are the currency of module composition.  The K0 kernel
    uses capability declarations to resolve dependencies and detect
    conflicts during registration.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="Capability identifier, e.g. 'schema_validation', 'audit_logging'",
    )
    version: str = Field(
        default="1.0",
        pattern=r"^\d+\.\d+",
        description="Capability version (semver major.minor at minimum)",
    )
    description: str = Field(
        default="",
        max_length=512,
        description="Human-readable description of the capability",
    )

    def __hash__(self) -> int:
        return hash((self.name, self.version))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CapabilityDeclaration):
            return NotImplemented
        return self.name == other.name and self.version == other.version


class SecurityPrivilege(BaseModel):
    """
    Security privilege required by a module.

    Modules must declare all privileges they need upfront.  K0 will
    refuse to load a module that requests undeclared privileges at
    runtime (Monotonic Consequences).
    """

    resource: str = Field(
        ...,
        description="Resource type: 'fs', 'net', 'tool', 'event_store', 'projection', 'plugin'",
    )
    access: str = Field(
        ...,
        description="Access level: 'read', 'write', 'execute'",
    )
    scope: str = Field(
        default="*",
        description="Scope restriction, e.g. '/workspace/blobs' or 'api.openai.com'",
    )
    justification: str = Field(
        default="",
        max_length=512,
        description="Why this privilege is needed (for audit trail)",
    )

    @field_validator("resource")
    @classmethod
    def _validate_resource(cls, v: str) -> str:
        allowed = {"fs", "net", "tool", "event_store", "projection", "plugin", "env"}
        if v not in allowed:
            msg = f"Unknown resource type '{v}'. Allowed: {sorted(allowed)}"
            raise ValueError(msg)
        return v

    @field_validator("access")
    @classmethod
    def _validate_access(cls, v: str) -> str:
        allowed = {"read", "write", "execute"}
        if v not in allowed:
            msg = f"Unknown access level '{v}'. Allowed: {sorted(allowed)}"
            raise ValueError(msg)
        return v


class LifecycleHook(BaseModel):
    """
    Declaration of which lifecycle phase a module hooks into.

    A module may register multiple hooks across different phases.
    Within a single phase, hooks are ordered by priority (lower = earlier).
    """

    phase: LifecyclePhase = Field(
        ...,
        description="Which lifecycle phase this hook targets",
    )
    hook_type: HookType = Field(
        ...,
        description="Whether this runs before or after the phase core logic",
    )
    priority: int = Field(
        default=100,
        ge=0,
        le=1000,
        description="Execution priority within phase (lower = earlier, default 100)",
    )
    description: str = Field(
        default="",
        max_length=512,
        description="What this hook does",
    )

    def __hash__(self) -> int:
        return hash((self.phase, self.hook_type, self.priority))


class DegradationSpec(BaseModel):
    """
    When failure_semantics is DEGRADE, this describes what degrades.
    """

    affected_capabilities: list[str] = Field(
        default_factory=list,
        description="Capabilities that are reduced or lost during degradation",
    )
    fallback_behavior: str = Field(
        default="",
        max_length=512,
        description="Human-readable description of degraded behavior",
    )
    max_degradation_duration_seconds: int | None = Field(
        default=None,
        ge=0,
        description="Maximum time in degraded state before escalating to FAIL_CLOSED",
    )


# ---------------------------------------------------------------------------
# Main Manifest Model
# ---------------------------------------------------------------------------

class ModuleManifest(BaseModel):
    """
    K0 Trust Kernel Module Manifest.

    Every module that participates in the K0 lifecycle must declare
    a manifest specifying its capabilities, requirements, lifecycle
    hooks, security privileges, and failure semantics.

    Design invariants:
        1. A module MUST declare all capabilities it provides.
        2. A module MUST declare all capabilities it requires.
        3. A module MUST declare all lifecycle phases it hooks into.
        4. A module MUST declare all security privileges it needs.
        5. A module MUST declare its failure semantics.
        6. A module SHOULD declare non-guarantees to set expectations.
        7. DEGRADE failure semantics MUST include a degradation_spec.
    """

    # --- Identity -----------------------------------------------------------

    module_id: UUID = Field(
        default_factory=uuid4,
        description="Unique identifier for this module instance",
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=128,
        pattern=r"^[a-zA-Z@][a-zA-Z0-9_\-/\.]*$",
        description="Module name, e.g. '@sip/contract' or 'python.local'",
    )
    version: str = Field(
        ...,
        pattern=r"^\d+\.\d+\.\d+",
        description="Semantic version string",
    )
    description: str = Field(
        default="",
        max_length=1024,
        description="Human-readable module description",
    )
    author: str = Field(default="", max_length=256)
    license: str = Field(default="", max_length=64)

    # --- Classification -----------------------------------------------------

    kind: ModuleKind = Field(
        ...,
        description="Module kind, determining its role in the K0 lifecycle",
    )
    criticality: CriticalityLevel = Field(
        default=CriticalityLevel.OPTIONAL,
        description="How critical this module is to system operation",
    )

    # --- Capabilities -------------------------------------------------------

    provides: list[CapabilityDeclaration] = Field(
        default_factory=list,
        description="Capabilities this module provides to others",
    )
    requires: list[CapabilityDeclaration] = Field(
        default_factory=list,
        description="Capabilities this module requires from others",
    )

    # --- Lifecycle ----------------------------------------------------------

    lifecycle_hooks: list[LifecycleHook] = Field(
        default_factory=list,
        description="Lifecycle phases this module participates in",
    )

    # --- Security -----------------------------------------------------------

    privileges: list[SecurityPrivilege] = Field(
        default_factory=list,
        description="Security privileges required by this module",
    )

    # --- Failure behavior ---------------------------------------------------

    failure_semantics: FailureSemantics = Field(
        default=FailureSemantics.FAIL_CLOSED,
        description="How the module behaves on error",
    )
    degradation_spec: DegradationSpec | None = Field(
        default=None,
        description="Required when failure_semantics is DEGRADE",
    )

    # --- Guarantees ---------------------------------------------------------

    guarantees: list[str] = Field(
        default_factory=list,
        description="What this module guarantees when functioning correctly",
    )
    non_guarantees: list[str] = Field(
        default_factory=list,
        description="What this module explicitly does NOT guarantee",
    )

    # --- Metadata -----------------------------------------------------------

    schema_version: str = Field(
        default="1.0",
        description="Manifest schema version for forward compatibility",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Freeform tags for categorization and discovery",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Extension metadata for domain-specific needs",
    )

    # --- Validators ---------------------------------------------------------

    @model_validator(mode="after")
    def _validate_degradation_spec(self) -> ModuleManifest:
        """DEGRADE failure semantics must include a degradation spec."""
        if self.failure_semantics == FailureSemantics.DEGRADE:
            if self.degradation_spec is None:
                msg = (
                    "failure_semantics is DEGRADE but no degradation_spec provided. "
                    "You must declare what degrades and how."
                )
                raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _validate_provides_not_empty_for_non_observer(self) -> ModuleManifest:
        """Non-OBSERVER modules should provide at least one capability."""
        if self.kind != ModuleKind.OBSERVER and not self.provides:
            msg = (
                f"Module kind '{self.kind}' should provide at least one capability. "
                "Only OBSERVER modules may provide nothing."
            )
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _validate_no_duplicate_hooks(self) -> ModuleManifest:
        """No duplicate phase+hook_type combinations at the same priority."""
        seen: set[tuple[str, str, int]] = set()
        for hook in self.lifecycle_hooks:
            key = (hook.phase, hook.hook_type, hook.priority)
            if key in seen:
                msg = (
                    f"Duplicate lifecycle hook: phase={hook.phase}, "
                    f"type={hook.hook_type}, priority={hook.priority}"
                )
                raise ValueError(msg)
            seen.add(key)
        return self

    # --- Utility methods ----------------------------------------------------

    def provides_capability(self, name: str) -> bool:
        """Check if this module provides a named capability."""
        return any(cap.name == name for cap in self.provides)

    def requires_capability(self, name: str) -> bool:
        """Check if this module requires a named capability."""
        return any(cap.name == name for cap in self.requires)

    def hooks_into_phase(self, phase: LifecyclePhase) -> bool:
        """Check if this module has any hooks in the given phase."""
        return any(hook.phase == phase for hook in self.lifecycle_hooks)

    def provided_capability_names(self) -> set[str]:
        """Return the set of capability names this module provides."""
        return {cap.name for cap in self.provides}

    def required_capability_names(self) -> set[str]:
        """Return the set of capability names this module requires."""
        return {cap.name for cap in self.requires}
