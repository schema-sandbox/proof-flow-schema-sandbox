"""
@sip Modular Sandbox System (Foundation, Governance, and Orchestration)

Modules:
    F1: @sip/contract          — Input/Output JSON Schema constraints
    F2: @sip/evidence          — Audit log & evidence ledger
    F3: @sip/permission        — Scope & permission fences
    F4: @sip/partition         — Workspace isolation
    G1: @sip/telos             — Goal anchoring & stagnation alerts
    G2: @sip/claim             — Claim envelopes & evidence maturity
    G3: @sip/trajectory        — Trajectory recording & failure assetization
    G4: @sip/verifier          — Verifier adapters & hardening checks
    O1: @sip/federation        — Multi-model roles & Arena recipes
    O2: @sip/capacity          — Compute leases & verification debt
    O3: @sip/campaign          — Campaign accounting & deduplication
    O4: @sip/schema-tournament — Competitive schema framework tournaments
"""

from __future__ import annotations

__all__ = [
    "SipModule",
    "ComposedSandbox",
    "compose",
    # F1
    "ContractModule",
    "createGate",
    # F2
    "EvidenceModule",
    "createLedger",
    # F3
    "PermissionModule",
    "createFence",
    # F4
    "PartitionModule",
    "createPartition",
    "IsolationMode",
    # G1
    "TelosModule",
    "createTelos",
    # G2
    "ClaimModule",
    "createClaim",
    "ClaimEnvelope",
    "ClaimStatus",
    "EvidenceMaturity",
    # G3
    "TrajectoryModule",
    "createTrajectory",
    # G4
    "VerifierModule",
    "createVerifier",
    # O1
    "FederationModule",
    "createFederation",
    "AgentRole",
    "HandoffType",
    "HandoffPacket",
    "CorrelatedReviewDetector",
    # O2
    "CapacityModule",
    "createCapacity",
    "ComputeLease",
    # O3
    "CampaignModule",
    "createCampaign",
    # O4
    "TournamentModule",
    "createTournament",
    "SchemaProposal",
]

from schemamath_api.sip.campaign import CampaignModule, createCampaign
from schemamath_api.sip.capacity import CapacityModule, ComputeLease, createCapacity
from schemamath_api.sip.claim import (
    ClaimEnvelope,
    ClaimModule,
    ClaimStatus,
    EvidenceMaturity,
    createClaim,
)
from schemamath_api.sip.contract import ContractModule, createGate
from schemamath_api.sip.core import ComposedSandbox, SipModule, compose
from schemamath_api.sip.evidence import EvidenceModule, createLedger
from schemamath_api.sip.federation import (
    AgentRole,
    CorrelatedReviewDetector,
    FederationModule,
    HandoffPacket,
    HandoffType,
    createFederation,
)
from schemamath_api.sip.partition import IsolationMode, PartitionModule, createPartition
from schemamath_api.sip.permission import PermissionModule, createFence
from schemamath_api.sip.telos import TelosModule, createTelos
from schemamath_api.sip.tournament import SchemaProposal, TournamentModule, createTournament
from schemamath_api.sip.trajectory import TrajectoryModule, createTrajectory
from schemamath_api.sip.verifier import VerifierModule, createVerifier
