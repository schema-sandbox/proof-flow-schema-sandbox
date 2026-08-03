"""
18-Point Research Episode Dossier Generator (v48.0)

Automatically generates dossiers conforming to the 18-item Research Episode
Dossier standard defined in From_Prompt_to_Proof v0.13 §9.
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class EvidenceCardScores:
    """Six-dimensional evidence card (v0.12 §2)."""
    process_provenance: int  # 0-5
    artifact_availability: int  # 0-5
    deterministic_verification: int  # 0-5
    independent_review: int  # 0-5
    novelty_prior_art: int  # 0-5
    autonomy_attribution: int  # 0-5

    @property
    def total(self) -> int:
        return sum([
            self.process_provenance,
            self.artifact_availability,
            self.deterministic_verification,
            self.independent_review,
            self.novelty_prior_art,
            self.autonomy_attribution,
        ])


@dataclass
class CostBoundary:
    """Discovery-token cost vs lifecycle cost (v0.13 §7)."""
    discovery_token_cost_usd: float
    lifecycle_cost_usd: float
    cost_ratio: float = 0.0

    def __post_init__(self) -> None:
        if self.lifecycle_cost_usd > 0:
            self.cost_ratio = self.discovery_token_cost_usd / self.lifecycle_cost_usd


@dataclass
class ResearchEpisodeDossier:
    """18-point Research Episode Dossier (v0.13 §9)."""
    # 1. Episode ID & timestamp
    episode_id: str
    timestamp: str
    # 2. Target specification
    target_specification: str
    # 3. Model identifiers & versions
    model_identifiers: list[str]
    # 4. Operational configuration (O1-O4)
    operational_config: str
    # 5. Search topology
    search_topology: str
    # 6. Trajectory state snapshot
    trajectory_state: dict[str, Any]
    # 7. Falsification record
    falsification_record: list[str]
    # 8. Repair lineage
    repair_lineage: list[str]
    # 9. Verification method & kernel identity
    verification_method: str
    kernel_identity: str
    # 10. Axiom ceiling declaration
    axiom_ceiling: list[str]
    # 11. Human labor tier (L0-L2)
    human_labor_tier: str
    # 12. Evidence tier (E0-E5)
    evidence_tier: str
    # 13. Six-dimensional evidence card
    evidence_card: EvidenceCardScores
    # 14. Trace derivation class
    trace_derivation_class: str
    # 15. Artifact correlation disclosure
    artifact_correlations: list[str]
    # 16. Trusted challenge boundary
    trusted_challenge_boundary: str
    # 17. Cost boundary
    cost_boundary: CostBoundary | None
    # 18. Benchmark completeness statement
    benchmark_completeness: str

    # Computed
    dossier_sha256: str = ""

    def __post_init__(self) -> None:
        content = json.dumps(self.to_dict(), sort_keys=True, default=str)
        self.dossier_sha256 = hashlib.sha256(content.encode()).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "timestamp": self.timestamp,
            "target_specification": self.target_specification,
            "model_identifiers": self.model_identifiers,
            "operational_config": self.operational_config,
            "search_topology": self.search_topology,
            "trajectory_state": self.trajectory_state,
            "falsification_record": self.falsification_record,
            "repair_lineage": self.repair_lineage,
            "verification_method": self.verification_method,
            "kernel_identity": self.kernel_identity,
            "axiom_ceiling": self.axiom_ceiling,
            "human_labor_tier": self.human_labor_tier,
            "evidence_tier": self.evidence_tier,
            "evidence_card": {
                "process_provenance": self.evidence_card.process_provenance,
                "artifact_availability": self.evidence_card.artifact_availability,
                "deterministic_verification": self.evidence_card.deterministic_verification,
                "independent_review": self.evidence_card.independent_review,
                "novelty_prior_art": self.evidence_card.novelty_prior_art,
                "autonomy_attribution": self.evidence_card.autonomy_attribution,
                "total": self.evidence_card.total,
            },
            "trace_derivation_class": self.trace_derivation_class,
            "artifact_correlations": self.artifact_correlations,
            "trusted_challenge_boundary": self.trusted_challenge_boundary,
            "cost_boundary": {
                "discovery_token_cost_usd": self.cost_boundary.discovery_token_cost_usd,
                "lifecycle_cost_usd": self.cost_boundary.lifecycle_cost_usd,
                "cost_ratio": self.cost_boundary.cost_ratio,
            } if self.cost_boundary else None,
            "benchmark_completeness": self.benchmark_completeness,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2, default=str)

    def to_markdown(self) -> str:
        lines = [
            f"# Research Episode Dossier: {self.episode_id}",
            "",
            f"**Generated**: {self.timestamp}",
            f"**SHA-256**: `{self.dossier_sha256[:16]}...`",
            "",
            "## 1. Episode Identification",
            f"- **ID**: {self.episode_id}",
            f"- **Timestamp**: {self.timestamp}",
            "",
            "## 2. Target Specification",
            f"{self.target_specification}",
            "",
            "## 3. Model Identifiers",
            *[f"- {m}" for m in self.model_identifiers],
            "",
            f"## 4. Operational Configuration: {self.operational_config}",
            "",
            f"## 5. Search Topology: {self.search_topology}",
            "",
            "## 6. Trajectory State",
            f"- Failed routes: {len(self.trajectory_state.get('failed_routes', []))}",
            f"- Open obligations: {len(self.trajectory_state.get('open_obligations', []))}",
            f"- Negative knowledge entries: {len(self.trajectory_state.get('negative_knowledge', []))}",
            "",
            "## 7. Falsification Record",
            *([f"- {f}" for f in self.falsification_record] if self.falsification_record else ["- None recorded"]),
            "",
            "## 8. Repair Lineage",
            *([f"- {r}" for r in self.repair_lineage] if self.repair_lineage else ["- No repairs"]),
            "",
            "## 9. Verification",
            f"- **Method**: {self.verification_method}",
            f"- **Kernel**: {self.kernel_identity}",
            "",
            "## 10. Axiom Ceiling",
            *[f"- `{a}`" for a in self.axiom_ceiling],
            "",
            f"## 11. Human Labor Tier: {self.human_labor_tier}",
            "",
            f"## 12. Evidence Tier: {self.evidence_tier}",
            "",
            "## 13. Six-Dimensional Evidence Card",
            "| Dimension | Score |",
            "|:---|:---:|",
            f"| Process Provenance | {self.evidence_card.process_provenance}/5 |",
            f"| Artifact Availability | {self.evidence_card.artifact_availability}/5 |",
            f"| Deterministic Verification | {self.evidence_card.deterministic_verification}/5 |",
            f"| Independent Review | {self.evidence_card.independent_review}/5 |",
            f"| Novelty & Prior Art | {self.evidence_card.novelty_prior_art}/5 |",
            f"| Autonomy & Attribution | {self.evidence_card.autonomy_attribution}/5 |",
            f"| **Total** | **{self.evidence_card.total}/30** |",
            "",
            f"## 14. Trace Derivation Class: {self.trace_derivation_class}",
            "",
            "## 15. Artifact Correlations",
            *([f"- {c}" for c in self.artifact_correlations] if self.artifact_correlations else ["- Independent sources"]),
            "",
            "## 16. Trusted Challenge Boundary",
            f"{self.trusted_challenge_boundary}",
            "",
            "## 17. Cost Boundary",
        ]
        if self.cost_boundary:
            lines.extend([
                f"- Discovery-token cost: ${self.cost_boundary.discovery_token_cost_usd:,.2f}",
                f"- Lifecycle cost: ${self.cost_boundary.lifecycle_cost_usd:,.2f}",
                f"- Ratio: {self.cost_boundary.cost_ratio:.1%}",
            ])
        else:
            lines.append("- Not reported")
        lines.extend([
            "",
            "## 18. Benchmark Completeness",
            f"{self.benchmark_completeness}",
        ])
        return "\n".join(lines)


class DossierGenerator:
    """Generates 18-point Research Episode Dossiers from workflow data."""

    def generate(
        self,
        episode_id: str,
        target_specification: str,
        model_identifiers: list[str],
        operational_config: str = "O1",
        search_topology: str = "sequential",
        trajectory_state: dict[str, Any] | None = None,
        falsification_record: list[str] | None = None,
        repair_lineage: list[str] | None = None,
        verification_method: str = "none",
        kernel_identity: str = "none",
        axiom_ceiling: list[str] | None = None,
        human_labor_tier: str = "L?",
        evidence_tier: str = "E0",
        evidence_card: EvidenceCardScores | None = None,
        trace_derivation_class: str = "FINAL_ONLY_ARTIFACT",
        artifact_correlations: list[str] | None = None,
        trusted_challenge_boundary: str = "not applicable",
        cost_boundary: CostBoundary | None = None,
        benchmark_completeness: str = "not assessed",
    ) -> ResearchEpisodeDossier:
        if evidence_card is None:
            evidence_card = EvidenceCardScores(0, 0, 0, 0, 0, 0)

        dossier = ResearchEpisodeDossier(
            episode_id=episode_id,
            timestamp=datetime.now(UTC).isoformat(),
            target_specification=target_specification,
            model_identifiers=model_identifiers,
            operational_config=operational_config,
            search_topology=search_topology,
            trajectory_state=trajectory_state or {},
            falsification_record=falsification_record or [],
            repair_lineage=repair_lineage or [],
            verification_method=verification_method,
            kernel_identity=kernel_identity,
            axiom_ceiling=axiom_ceiling or [],
            human_labor_tier=human_labor_tier,
            evidence_tier=evidence_tier,
            evidence_card=evidence_card,
            trace_derivation_class=trace_derivation_class,
            artifact_correlations=artifact_correlations or [],
            trusted_challenge_boundary=trusted_challenge_boundary,
            cost_boundary=cost_boundary,
            benchmark_completeness=benchmark_completeness,
        )
        logger.info("Generated dossier '%s' with evidence tier %s", episode_id, evidence_tier)
        return dossier
