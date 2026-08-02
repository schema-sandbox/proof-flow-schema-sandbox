"""
K0 Trust Kernel — Decision Algebra

The decision algebra defines how multiple module decisions are merged
into a single K0 verdict.  This replaces ad-hoc if/else chains with
a formal, auditable composition model.

Composition rules (from V34 specification):
    - Capability Range  → Intersection (Cap₁ ∩ Cap₂)
    - Risk Level        → Maximum (max(Riskᵢ))
    - Required Evidence → Union (∪ Reqᵢ)
    - Assertion Ceiling → Minimum (min(Ceilingᵢ))
    - Approval Priority → DENY > REQUIRE_HUMAN > DEFER > REQUIRE_EVIDENCE > ALLOW

Design principle:
    When modules disagree, the system errs on the side of caution.
    A single DENY overrides any number of ALLOWs.
"""

from __future__ import annotations

from enum import IntEnum, StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Core Decision Type
# ---------------------------------------------------------------------------

class Decision(StrEnum):
    """
    A module's verdict on whether an operation should proceed.

    Ordered by increasing restrictiveness.  When merging decisions
    from multiple modules, the most restrictive decision wins.
    """

    ALLOW = "allow"
    """Operation is permitted unconditionally."""

    REQUIRE_EVIDENCE = "require_evidence"
    """Operation is permitted only if specified evidence is provided."""

    DEFER = "defer"
    """Module abstains; let other modules or the default policy decide."""

    REQUIRE_HUMAN = "require_human"
    """Operation requires explicit human confirmation before proceeding."""

    DENY = "deny"
    """Operation is forbidden.  No override possible except by K0 admin."""


# Priority mapping: higher number = more restrictive = wins in merge
_DECISION_PRIORITY: dict[Decision, int] = {
    Decision.ALLOW: 0,
    Decision.REQUIRE_EVIDENCE: 1,
    Decision.DEFER: 2,
    Decision.REQUIRE_HUMAN: 3,
    Decision.DENY: 4,
}


def decision_priority(d: Decision) -> int:
    """Return the priority rank of a decision (higher = more restrictive)."""
    return _DECISION_PRIORITY[d]


def more_restrictive(a: Decision, b: Decision) -> Decision:
    """Return the more restrictive of two decisions."""
    return a if _DECISION_PRIORITY[a] >= _DECISION_PRIORITY[b] else b


# ---------------------------------------------------------------------------
# Risk Level
# ---------------------------------------------------------------------------

class RiskLevel(IntEnum):
    """
    Discrete risk levels for operations.

    Used in composition algebra: merged risk = max(all risk levels).
    """

    NONE = 0
    LOW = 25
    MEDIUM = 50
    HIGH = 75
    CRITICAL = 100


# ---------------------------------------------------------------------------
# Decision Context (single module's output)
# ---------------------------------------------------------------------------

class ModuleDecision(BaseModel):
    """
    A single module's decision about an operation.

    This is what a module produces when its lifecycle hook runs.
    The DecisionMerger aggregates these into a final K0 verdict.
    """

    # Which module produced this decision
    source_module: str = Field(
        ...,
        description="Name of the module that produced this decision",
    )

    # The verdict
    approval: Decision = Field(
        default=Decision.DEFER,
        description="The module's verdict on the operation",
    )
    reason: str = Field(
        default="",
        max_length=1024,
        description="Human-readable explanation for the decision",
    )

    # Capability range contributed by this module
    capabilities: set[str] = Field(
        default_factory=set,
        description="Capabilities this module grants for this operation",
    )

    # Risk assessment
    risk_level: RiskLevel = Field(
        default=RiskLevel.NONE,
        description="Risk level assessed by this module",
    )
    risk_factors: list[str] = Field(
        default_factory=list,
        description="Specific risk factors identified",
    )

    # Evidence requirements
    required_evidence: set[str] = Field(
        default_factory=set,
        description="Evidence that must be present for this operation",
    )

    # Assertion ceiling (how confident can downstream claims be)
    assertion_ceiling: int = Field(
        default=100,
        ge=0,
        le=100,
        description="Maximum confidence level (0-100) for downstream assertions",
    )

    # Optional structured payload
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Module-specific metadata attached to the decision",
    )

    model_config = ConfigDict(frozen=True)


# ---------------------------------------------------------------------------
# Merged Decision (K0 kernel output)
# ---------------------------------------------------------------------------

class MergedDecision(BaseModel):
    """
    The K0 kernel's final verdict after merging all module decisions.

    This is the authoritative output of the decision algebra.
    """

    # Final verdict
    approval: Decision = Field(
        ...,
        description="Final merged approval decision",
    )

    # Composition results
    effective_capabilities: set[str] = Field(
        default_factory=set,
        description="Intersection of all module capabilities",
    )
    effective_risk: RiskLevel = Field(
        default=RiskLevel.NONE,
        description="Maximum risk level across all modules",
    )
    all_required_evidence: set[str] = Field(
        default_factory=set,
        description="Union of all evidence requirements",
    )
    assertion_ceiling: int = Field(
        default=100,
        ge=0,
        le=100,
        description="Minimum assertion ceiling across all modules",
    )

    # Audit trail
    contributing_decisions: list[ModuleDecision] = Field(
        default_factory=list,
        description="All individual module decisions that were merged",
    )
    all_risk_factors: list[str] = Field(
        default_factory=list,
        description="Aggregated risk factors from all modules",
    )
    denial_reasons: list[str] = Field(
        default_factory=list,
        description="Reasons from modules that voted DENY or REQUIRE_HUMAN",
    )

    @property
    def is_approved(self) -> bool:
        """Whether the operation is approved (ALLOW or REQUIRE_EVIDENCE with evidence available)."""
        return self.approval == Decision.ALLOW

    @property
    def needs_evidence(self) -> bool:
        """Whether additional evidence is needed."""
        return self.approval == Decision.REQUIRE_EVIDENCE or bool(
            self.all_required_evidence
        )

    @property
    def needs_human(self) -> bool:
        """Whether human intervention is required."""
        return self.approval == Decision.REQUIRE_HUMAN

    @property
    def is_denied(self) -> bool:
        """Whether the operation is denied."""
        return self.approval == Decision.DENY


# ---------------------------------------------------------------------------
# Decision Merger
# ---------------------------------------------------------------------------

class DecisionMerger:
    """
    Merges multiple module decisions using K0 composition algebra.

    Composition rules:
        1. Approval:           Most restrictive wins (DENY > REQUIRE_HUMAN > DEFER > REQUIRE_EVIDENCE > ALLOW)
        2. Capability Range:   Intersection of all module capabilities
        3. Risk Level:         Maximum across all modules
        4. Required Evidence:  Union of all evidence requirements
        5. Assertion Ceiling:  Minimum across all modules

    If no decisions are provided, the default is DENY (fail-closed).
    """

    def __init__(self, *, default_on_empty: Decision = Decision.DENY) -> None:
        """
        Args:
            default_on_empty: Decision to use when no modules provide input.
                              Defaults to DENY (fail-closed principle).
        """
        self._default_on_empty = default_on_empty

    def merge(self, decisions: list[ModuleDecision]) -> MergedDecision:
        """
        Merge a list of module decisions into a single K0 verdict.

        Args:
            decisions: Individual module decisions to merge.

        Returns:
            MergedDecision with the composed result.
        """
        if not decisions:
            return MergedDecision(
                approval=self._default_on_empty,
                denial_reasons=[
                    f"No modules provided a decision; defaulting to {self._default_on_empty.value}"
                ],
            )

        # --- 1. Approval: most restrictive wins ---
        final_approval = Decision.ALLOW
        for d in decisions:
            if d.approval == Decision.DEFER:
                continue  # DEFER doesn't influence the final decision
            final_approval = more_restrictive(final_approval, d.approval)

        # If all decisions are DEFER, use default
        non_defer = [d for d in decisions if d.approval != Decision.DEFER]
        if not non_defer:
            final_approval = self._default_on_empty

        # --- 2. Capability Range: intersection ---
        cap_sets = [d.capabilities for d in decisions if d.capabilities]
        if cap_sets:
            effective_caps = cap_sets[0]
            for cs in cap_sets[1:]:
                effective_caps = effective_caps & cs
        else:
            effective_caps = set()

        # --- 3. Risk Level: maximum ---
        effective_risk = RiskLevel(max(d.risk_level for d in decisions))

        # --- 4. Required Evidence: union ---
        all_evidence: set[str] = set()
        for d in decisions:
            all_evidence |= d.required_evidence

        # --- 5. Assertion Ceiling: minimum ---
        assertion_ceiling = min(d.assertion_ceiling for d in decisions)

        # --- Audit trail ---
        all_risk_factors: list[str] = []
        denial_reasons: list[str] = []
        for d in decisions:
            all_risk_factors.extend(d.risk_factors)
            if d.approval in (Decision.DENY, Decision.REQUIRE_HUMAN) and d.reason:
                denial_reasons.append(f"[{d.source_module}] {d.reason}")

        return MergedDecision(
            approval=final_approval,
            effective_capabilities=effective_caps,
            effective_risk=effective_risk,
            all_required_evidence=all_evidence,
            assertion_ceiling=assertion_ceiling,
            contributing_decisions=list(decisions),
            all_risk_factors=all_risk_factors,
            denial_reasons=denial_reasons,
        )

    def merge_approvals_only(self, decisions: list[ModuleDecision]) -> Decision:
        """
        Quick merge that only considers the approval field.

        Useful when you only need the go/no-go answer without
        the full composition algebra.
        """
        if not decisions:
            return self._default_on_empty

        result = Decision.ALLOW
        for d in decisions:
            if d.approval == Decision.DEFER:
                continue
            result = more_restrictive(result, d.approval)

        non_defer = [d for d in decisions if d.approval != Decision.DEFER]
        if not non_defer:
            return self._default_on_empty

        return result
