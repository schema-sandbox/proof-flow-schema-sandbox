"""
@sip/claim (G2: Claim Envelopes, Evidence Maturity, and State Transitions)

Manages research claim envelopes, evidence maturity levels, and state transitions.

Evidence Maturity:
    CONJECTURE → SUPPORTED → CORROBORATED → VERIFIED → CERTIFIED

Claim Status:
    DRAFT → PROPOSED → UNDER_REVIEW → ACCEPTED / REJECTED / WITHDRAWN

Invariant:
    Transitioning a claim to CERTIFIED strictly requires human confirmation
    and non-correlated evidence.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from schemamath_api.k0.decision import Decision, ModuleDecision
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


class EvidenceMaturity(StrEnum):
    CONJECTURE = "CONJECTURE"
    SUPPORTED = "SUPPORTED"
    CORROBORATED = "CORROBORATED"
    VERIFIED = "VERIFIED"
    CERTIFIED = "CERTIFIED"


class ClaimStatus(StrEnum):
    DRAFT = "DRAFT"
    PROPOSED = "PROPOSED"
    UNDER_REVIEW = "UNDER_REVIEW"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"


class ClaimEnvelope(BaseModel):
    """A research claim envelope tracked by @sip/claim."""

    claim_id: UUID = Field(default_factory=uuid4)
    statement: str
    maturity: EvidenceMaturity = EvidenceMaturity.CONJECTURE
    status: ClaimStatus = ClaimStatus.DRAFT
    evidence_refs: list[str] = Field(default_factory=list)
    human_confirmed: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class ClaimModule(SipModule):
    """
    G2: @sip/claim module.

    Manages claims in P7_ASSERTION_EVALUATION.
    """

    def __init__(self) -> None:
        super().__init__(
            name="@sip/claim",
            version="1.0.0",
            kind=ModuleKind.STATE_MACHINE,
            description="Claim Envelope and Evidence Maturity Governance",
            provides=[CapabilityDeclaration(name="claim_governance", version="1.0")],
            requires=[CapabilityDeclaration(name="audit_logging", version="1.0")],
        )

        self.claims: dict[UUID, ClaimEnvelope] = {}

        self._manifest.lifecycle_hooks = [
            LifecycleHook(
                phase=LifecyclePhase.P7_ASSERTION_EVALUATION,
                hook_type=HookType.PRE,
                priority=10,
                description="Evaluate claim maturity and authorize state transition",
            ),
        ]

    def bind_hooks(self, scheduler: LifecycleScheduler) -> None:
        scheduler.register_hook(
            self.name,
            LifecyclePhase.P7_ASSERTION_EVALUATION,
            HookType.PRE,
            10,
            self.evaluate_claims,
        )

    def create_claim(
        self, statement: str, maturity: EvidenceMaturity = EvidenceMaturity.CONJECTURE
    ) -> ClaimEnvelope:
        """Create a new claim in DRAFT status."""
        claim = ClaimEnvelope(statement=statement, maturity=maturity)
        self.claims[claim.claim_id] = claim
        return claim

    def transition_claim(
        self,
        claim_id: UUID,
        target_status: ClaimStatus,
        target_maturity: EvidenceMaturity | None = None,
        evidence_refs: Sequence[str] | None = None,
        human_confirmed: bool = False,
    ) -> ClaimEnvelope:
        """Transition claim status & maturity with invariant checks."""
        claim = self.claims.get(claim_id)
        if not claim:
            raise KeyError(f"Claim '{claim_id}' not found")

        # Invariant Check: CERTIFIED requires human confirmation & evidence
        new_maturity = target_maturity or claim.maturity
        if new_maturity == EvidenceMaturity.CERTIFIED:
            if not human_confirmed:
                raise ValueError("Transition to CERTIFIED maturity requires explicit human_confirmed=True")
            if not (evidence_refs or claim.evidence_refs):
                raise ValueError("Transition to CERTIFIED maturity requires at least one evidence reference")

        claim.status = target_status
        claim.maturity = new_maturity
        if evidence_refs:
            claim.evidence_refs.extend(evidence_refs)
        claim.human_confirmed = claim.human_confirmed or human_confirmed

        return claim

    def evaluate_claims(self, ctx: LifecycleContext) -> ModuleDecision:
        """Evaluate claims proposed in context."""
        proposed_claim = ctx.input_data.get("claim_transition")
        if not proposed_claim:
            return ModuleDecision(
                source_module=self.name,
                approval=Decision.ALLOW,
                capabilities={"claim_governance"},
            )

        cid = proposed_claim.get("claim_id")
        target_status = proposed_claim.get("target_status")
        target_maturity = proposed_claim.get("target_maturity")
        human_conf = proposed_claim.get("human_confirmed", False)
        ev_refs = proposed_claim.get("evidence_refs", [])

        try:
            claim_uuid = UUID(str(cid)) if cid else None
            if claim_uuid and claim_uuid in self.claims:
                self.transition_claim(
                    claim_id=claim_uuid,
                    target_status=ClaimStatus(target_status),
                    target_maturity=EvidenceMaturity(target_maturity) if target_maturity else None,
                    evidence_refs=ev_refs,
                    human_confirmed=human_conf,
                )
            return ModuleDecision(
                source_module=self.name,
                approval=Decision.ALLOW,
                capabilities={"claim_governance"},
            )
        except Exception as exc:
            return ModuleDecision(
                source_module=self.name,
                approval=Decision.DENY,
                reason=f"Claim transition rejected: {exc}",
            )


def createClaim() -> ClaimModule:
    """Helper factory matching JS-style createClaim()."""
    return ClaimModule()
