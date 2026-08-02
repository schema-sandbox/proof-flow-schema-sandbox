"""
ProofFlow High-Level Python Developer SDK (proofflow)

Provides a 3-line, zero-friction developer experience for constructing sandboxes,
running life-cycle phases, and querying research event stores.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Sequence

from schemamath_api.sip import ComposedSandbox, SipModule, compose
from schemamath_api.sip import (
    createCampaign,
    createCapacity,
    createClaim,
    createFence,
    createFederation,
    createGate,
    createLedger,
    createPartition,
    createTelos,
    createTournament,
    createTrajectory,
    createVerifier,
)

logger = logging.getLogger(__name__)


@dataclass
class ProofFlowClient:
    """
    High-level ProofFlow Client SDK instance.
    """

    def compose_sandbox(
        self,
        modules: Sequence[SipModule] | None = None,
    ) -> ComposedSandbox:
        """Construct a ProofFlow sandbox instance."""
        if modules:
            return compose(*modules)

        # Default: Full 12-Module Sandbox
        return compose(
            createGate(input={"type": "object"}),
            createLedger(retention="90d"),
            createFence(fs=["/tmp"]),
            createPartition(mode="PROCESS"),
            createTelos(goal="Autonomous mathematical research"),
            createClaim(),
            createTrajectory(),
            createVerifier(),
            createFederation(),
            createCapacity(maxVerificationDebt=10),
            createCampaign(name="sdk_campaign"),
            createTournament(),
        )


def init() -> ProofFlowClient:
    """Initialize a ProofFlow Client SDK instance."""
    logger.info("ProofFlow SDK v5.0.0 initialized")
    return ProofFlowClient()
