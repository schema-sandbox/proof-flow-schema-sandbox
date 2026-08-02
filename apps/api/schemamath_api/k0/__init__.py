"""
K0 Trust Kernel — ProofFlow Schema Sandbox

The K0 Trust Kernel is the non-bypassable minimal execution kernel
that enforces system invariants: identity, capability grants, lifecycle
scheduling, decision algebra, canonical event journal, artifact
identity/lineage, and transactional side-effect commits.

Modules:
    manifest    — ModuleManifest declaration and validation
    registry    — Manifest registry with conflict detection
    decision    — Decision algebra and merger
    lifecycle   — Fixed-phase lifecycle scheduler (P0–P10)
    transaction — Transactional side-effect executor
    replay      — Event replay engine
"""

from __future__ import annotations

__all__ = [
    # manifest
    "ModuleManifest",
    "ModuleKind",
    "FailureSemantics",
    "CriticalityLevel",
    "LifecyclePhase",
    "HookType",
    "CapabilityDeclaration",
    "SecurityPrivilege",
    "LifecycleHook",
    "DegradationSpec",
    # registry
    "ManifestRegistry",
    # decision
    "Decision",
    "ModuleDecision",
    "MergedDecision",
    "DecisionMerger",
    "RiskLevel",
    # lifecycle
    "LifecycleScheduler",
    "LifecycleContext",
    "LifecycleResult",
    # transaction
    "Transaction",
    "ProposedArtifact",
    "TransactionResult",
    "TransactionExecutor",
    # replay
    "ReplayEngine",
    "ReplayResult",
]

from schemamath_api.k0.decision import (
    Decision,
    DecisionMerger,
    MergedDecision,
    ModuleDecision,
    RiskLevel,
)
from schemamath_api.k0.lifecycle import (
    LifecycleContext,
    LifecycleResult,
    LifecycleScheduler,
)
from schemamath_api.k0.manifest import (
    CapabilityDeclaration,
    CriticalityLevel,
    DegradationSpec,
    FailureSemantics,
    HookType,
    LifecycleHook,
    LifecyclePhase,
    ModuleKind,
    ModuleManifest,
    SecurityPrivilege,
)
from schemamath_api.k0.registry import ManifestRegistry
from schemamath_api.k0.replay import (
    ReplayEngine,
    ReplayResult,
)
from schemamath_api.k0.transaction import (
    ProposedArtifact,
    Transaction,
    TransactionExecutor,
    TransactionResult,
)
