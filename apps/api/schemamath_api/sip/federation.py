"""
@sip/federation (O1: Multi-Model Collaboration, Arena Recipes, and Typed Handoffs)

Orchestrates multi-agent research teams across 11 functional roles, detects model-family
correlations, executes multi-stage Arena Recipes, and manages typed HandoffArtifacts.

Roles:
    EXPLORER, BUILDER, SKEPTIC, RIVAL_THEORIST, COUNTEREXAMPLE_HUNTER,
    BRIDGE_BUILDER, SIMPLIFIER, VISUAL_THINKER, FORMALIZER, HISTORIAN, EXPOSITOR
"""

from __future__ import annotations

import logging
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from schemamath_api.k0.decision import Decision, ModuleDecision, RiskLevel
from schemamath_api.k0.lifecycle import (
    HookType,
    LifecycleContext,
    LifecyclePhase,
    LifecycleScheduler,
)
from schemamath_api.k0.manifest import (
    CapabilityDeclaration,
    LifecycleHook,
    ModuleKind,
)
from schemamath_api.sip.core import SipModule

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums & Models
# ---------------------------------------------------------------------------

class AgentRole(StrEnum):
    EXPLORER = "explorer"
    BUILDER = "builder"
    SKEPTIC = "skeptic"
    RIVAL_THEORIST = "rival_theorist"
    COUNTEREXAMPLE_HUNTER = "counterexample_hunter"
    BRIDGE_BUILDER = "bridge_builder"
    SIMPLIFIER = "simplifier"
    VISUAL_THINKER = "visual_thinker"
    FORMALIZER = "formalizer"
    HISTORIAN = "historian"
    EXPOSITOR = "expositor"


class HandoffType(StrEnum):
    FAILED_ROUTE_NOTES = "FAILED_ROUTE_NOTES"
    SCRIPT = "SCRIPT"
    COUNTEREXAMPLE = "COUNTEREXAMPLE"
    PARTIAL_CONSTRUCTION = "PARTIAL_CONSTRUCTION"
    SOURCE_MAP = "SOURCE_MAP"
    OPEN_OBLIGATION = "OPEN_OBLIGATION"
    BRIDGE_RESULT = "BRIDGE_RESULT"


class HandoffPacket(BaseModel):
    handoff_id: UUID = Field(default_factory=uuid4)
    from_role: AgentRole
    to_role: AgentRole
    handoff_type: HandoffType
    summary: str
    data: dict[str, Any] = Field(default_factory=dict)
    model_family: str = "openai"


class CorrelatedReviewDetector:
    """Detects whether two model identifiers belong to the same model family."""

    @staticmethod
    def extract_family(model_id: str) -> str:
        model_id = model_id.lower()
        if "gpt" in model_id or "openai" in model_id or "o1" in model_id or "o3" in model_id:
            return "openai"
        if "claude" in model_id or "anthropic" in model_id:
            return "anthropic"
        if "gemini" in model_id or "google" in model_id:
            return "google"
        if "deepseek" in model_id:
            return "deepseek"
        if "llama" in model_id or "meta" in model_id:
            return "meta"
        return model_id.split("-")[0]

    @classmethod
    def is_correlated(cls, model_a: str, model_b: str) -> bool:
        """Returns True if model_a and model_b are from the same provider family."""
        return cls.extract_family(model_a) == cls.extract_family(model_b)


# ---------------------------------------------------------------------------
# Federation Module
# ---------------------------------------------------------------------------

class FederationModule(SipModule):
    """
    O1: @sip/federation module.

    Orchestrates multi-agent role handoffs and enforces correlation warnings.
    """

    def __init__(self) -> None:
        super().__init__(
            name="@sip/federation",
            version="1.1.0",
            kind=ModuleKind.SCHEDULER,
            description="Multi-Model Role Orchestration and Typed Handoff Pipeline",
            provides=[CapabilityDeclaration(name="multi_agent_federation", version="1.1")],
            requires=[
                CapabilityDeclaration(name="goal_anchoring", version="1.0"),
                CapabilityDeclaration(name="claim_governance", version="1.0"),
            ],
        )

        self.handoffs: list[HandoffPacket] = []
        self.detector = CorrelatedReviewDetector()

        self._manifest.lifecycle_hooks = [
            LifecycleHook(
                phase=LifecyclePhase.P3_PLAN_PROPOSAL,
                hook_type=HookType.PRE,
                priority=10,
                description="Coordinate agent role proposals and handoffs",
            ),
            LifecycleHook(
                phase=LifecyclePhase.P4_ACTION_AUTH,
                hook_type=HookType.PRE,
                priority=20,
                description="Check review independence across model families",
            ),
        ]

    def bind_hooks(self, scheduler: LifecycleScheduler) -> None:
        scheduler.register_hook(
            self.name,
            LifecyclePhase.P3_PLAN_PROPOSAL,
            HookType.PRE,
            10,
            self.process_handoffs,
        )
        scheduler.register_hook(
            self.name,
            LifecyclePhase.P4_ACTION_AUTH,
            HookType.PRE,
            20,
            self.check_review_independence,
        )

    def create_handoff(
        self,
        from_role: AgentRole,
        to_role: AgentRole,
        handoff_type: HandoffType,
        summary: str,
        data: dict[str, Any] | None = None,
        model_family: str = "openai",
    ) -> HandoffPacket:
        """Create and store a typed handoff packet."""
        packet = HandoffPacket(
            from_role=from_role,
            to_role=to_role,
            handoff_type=handoff_type,
            summary=summary,
            data=data or {},
            model_family=model_family,
        )
        self.handoffs.append(packet)
        return packet

    def process_handoffs(self, ctx: LifecycleContext) -> ModuleDecision:
        """Process incoming handoffs in context."""
        handoff_data = ctx.input_data.get("handoff")
        if handoff_data:
            packet = self.create_handoff(
                from_role=AgentRole(handoff_data.get("from_role", "explorer")),
                to_role=AgentRole(handoff_data.get("to_role", "builder")),
                handoff_type=HandoffType(handoff_data.get("type", "FAILED_ROUTE_NOTES")),
                summary=handoff_data.get("summary", "Role handoff"),
                data=handoff_data.get("data", {}),
                model_family=handoff_data.get("model_family", "openai"),
            )
            ctx.module_state["active_handoff_id"] = str(packet.handoff_id)

        return ModuleDecision(
            source_module=self.name,
            approval=Decision.ALLOW,
            capabilities={"multi_agent_federation"},
        )

    def check_review_independence(self, ctx: LifecycleContext) -> ModuleDecision:
        """Check if reviewer and author belong to the same model family."""
        author_model = ctx.input_data.get("author_model")
        reviewer_model = ctx.input_data.get("reviewer_model")

        if author_model and reviewer_model:
            if self.detector.is_correlated(author_model, reviewer_model):
                return ModuleDecision(
                    source_module=self.name,
                    approval=Decision.REQUIRE_EVIDENCE,
                    reason=(
                        f"Correlated review warning: author model '{author_model}' and "
                        f"reviewer model '{reviewer_model}' belong to the same family "
                        f"('{self.detector.extract_family(author_model)}'). "
                        "Independent non-correlated review evidence is required for certification."
                    ),
                    risk_level=RiskLevel.MEDIUM,
                    risk_factors=["Correlated model family review"],
                    required_evidence={"non_correlated_review_attestation"},
                )

        return ModuleDecision(source_module=self.name, approval=Decision.ALLOW)


def createFederation() -> FederationModule:
    """Helper factory matching JS-style createFederation()."""
    return FederationModule()
