"""
Campaign Auditor — 6 Single-Campaign Audit Hazards (v47.0)

Detects the six audit hazards identified in v0.13 §6 for large-scale
single-campaign releases (e.g., OpenAI Astra C17):

1. Result-Family Counting Inflation
2. Cross-Result Dependence Masking
3. Retrospective Trace Coherence Gap
4. Correlated Artifact Triangulation Failure
5. Trusted-Challenge Definition Laundering
6. Discovery Cost Compression
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CampaignHazard:
    hazard_id: str
    hazard_name: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    description: str


@dataclass
class CampaignAuditReport:
    campaign_id: str
    result_family_count: int
    hazards_detected: list[CampaignHazard]
    hazard_count: int
    is_clean: bool


class CampaignAuditor:
    """
    Audits large-scale mathematical discovery campaigns for the 6 hazards
    defined in From_Prompt_to_Proof v0.13 §6.
    """

    def audit_campaign(
        self,
        campaign_id: str,
        result_families: list[str],
        shared_dependencies: list[tuple[str, str]] | None = None,
        trace_derivation_class: str = "RAW_EVENT_STREAM",
        artifact_producers: list[str] | None = None,
        challenge_definitions_audited: bool = True,
        reported_discovery_cost: float | None = None,
        estimated_lifecycle_cost: float | None = None,
    ) -> CampaignAuditReport:
        hazards: list[CampaignHazard] = []

        # H1: Result-Family Counting Inflation
        unique_families = set(result_families)
        if len(result_families) > len(unique_families):
            hazards.append(CampaignHazard(
                hazard_id="H1_RESULT_FAMILY_COUNTING",
                hazard_name="Result-Family Counting Inflation",
                severity="MEDIUM",
                description=f"Claimed {len(result_families)} results but only {len(unique_families)} are unique",
            ))

        # H2: Cross-Result Dependence Masking
        deps = shared_dependencies or []
        if len(deps) > 0:
            dep_ratio = len(deps) / max(len(unique_families), 1)
            if dep_ratio > 0.5:
                hazards.append(CampaignHazard(
                    hazard_id="H2_CROSS_RESULT_DEPENDENCE",
                    hazard_name="Cross-Result Dependence Masking",
                    severity="HIGH",
                    description=f"Dependency ratio {dep_ratio:.1%} exceeds 50% threshold",
                ))

        # H3: Retrospective Trace Coherence Gap
        if trace_derivation_class in ("MODEL_RECONSTRUCTION", "HUMAN_SYNTHESIS"):
            hazards.append(CampaignHazard(
                hazard_id="H3_TRACE_COHERENCE_GAP",
                hazard_name="Retrospective Trace Coherence Gap",
                severity="MEDIUM",
                description=f"Trace class '{trace_derivation_class}' lacks raw event verification",
            ))

        # H4: Correlated Artifact Triangulation Failure
        producers = artifact_producers or []
        unique_producers = set(producers)
        if len(unique_producers) == 1 and len(producers) > 1:
            hazards.append(CampaignHazard(
                hazard_id="H4_ARTIFACT_TRIANGULATION",
                hazard_name="Correlated Artifact Triangulation Failure",
                severity="HIGH",
                description=f"All {len(producers)} artifacts produced by single source: {unique_producers.pop()}",
            ))

        # H5: Trusted-Challenge Definition Laundering
        if not challenge_definitions_audited:
            hazards.append(CampaignHazard(
                hazard_id="H5_CHALLENGE_LAUNDERING",
                hazard_name="Trusted-Challenge Definition Laundering",
                severity="CRITICAL",
                description="Challenge definitions not independently audited for definition holes",
            ))

        # H6: Discovery Cost Compression
        if reported_discovery_cost is not None and estimated_lifecycle_cost is not None:
            if estimated_lifecycle_cost > 0 and reported_discovery_cost / estimated_lifecycle_cost < 0.1:
                hazards.append(CampaignHazard(
                    hazard_id="H6_COST_COMPRESSION",
                    hazard_name="Discovery Cost Compression",
                    severity="MEDIUM",
                    description=(
                        f"Reported discovery cost ${reported_discovery_cost:,.0f} is "
                        f"<10% of estimated lifecycle cost ${estimated_lifecycle_cost:,.0f}"
                    ),
                ))

        is_clean = len(hazards) == 0
        logger.info(
            "Campaign audit '%s': %d result families, %d hazards detected (clean=%s)",
            campaign_id,
            len(unique_families),
            len(hazards),
            is_clean,
        )
        return CampaignAuditReport(
            campaign_id=campaign_id,
            result_family_count=len(unique_families),
            hazards_detected=hazards,
            hazard_count=len(hazards),
            is_clean=is_clean,
        )
