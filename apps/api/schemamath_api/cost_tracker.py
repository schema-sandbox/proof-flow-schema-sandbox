"""
Discovery Cost & Lifecycle Cost Tracker (v50.0)

Distinguishes the two cost dimensions emphasized in v0.13 §7:
- Discovery-Token Cost: raw inference token consumption (API billing)
- Lifecycle Cost: includes failed attempts, human curation, formalization, review

Integrates with HumanLaborTracker (v44.0) for L0-L2 labor attribution.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class TokenCostEntry:
    model_id: str
    phase: str  # e.g., "search", "formalization", "repair", "verification"
    input_tokens: int
    output_tokens: int
    cost_usd: float


@dataclass
class HumanCostEntry:
    contributor: str
    labor_tier: str  # L0, L1, L2
    hours: float
    activity: str  # e.g., "target_selection", "formalization", "review", "manuscript"


@dataclass
class CostReport:
    episode_id: str
    discovery_token_cost_usd: float
    lifecycle_cost_usd: float
    token_entries: list[TokenCostEntry]
    human_entries: list[HumanCostEntry]
    cost_ratio: float
    by_model: dict[str, float]
    by_phase: dict[str, float]
    total_tokens: int
    total_human_hours: float

    @property
    def is_cost_compressed(self) -> bool:
        """Flag if reported discovery cost is <10% of lifecycle cost (H6 hazard)."""
        return self.cost_ratio < 0.1 if self.lifecycle_cost_usd > 0 else False


class CostTracker:
    """Tracks and reports discovery-token cost vs lifecycle cost."""

    def __init__(self) -> None:
        self._token_entries: list[TokenCostEntry] = []
        self._human_entries: list[HumanCostEntry] = []

    def record_token_cost(
        self,
        model_id: str,
        phase: str,
        input_tokens: int,
        output_tokens: int,
        cost_usd: float,
    ) -> TokenCostEntry:
        entry = TokenCostEntry(
            model_id=model_id,
            phase=phase,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost_usd,
        )
        self._token_entries.append(entry)
        return entry

    def record_human_cost(
        self,
        contributor: str,
        labor_tier: str,
        hours: float,
        activity: str,
    ) -> HumanCostEntry:
        entry = HumanCostEntry(
            contributor=contributor,
            labor_tier=labor_tier,
            hours=hours,
            activity=activity,
        )
        self._human_entries.append(entry)
        return entry

    def generate_report(self, episode_id: str, hourly_rate_usd: float = 100.0) -> CostReport:
        discovery_cost = sum(e.cost_usd for e in self._token_entries)
        human_hours = sum(e.hours for e in self._human_entries)
        human_cost = human_hours * hourly_rate_usd
        lifecycle_cost = discovery_cost + human_cost

        by_model: dict[str, float] = {}
        for e in self._token_entries:
            by_model[e.model_id] = by_model.get(e.model_id, 0.0) + e.cost_usd

        by_phase: dict[str, float] = {}
        for e in self._token_entries:
            by_phase[e.phase] = by_phase.get(e.phase, 0.0) + e.cost_usd
        for e in self._human_entries:
            by_phase[e.activity] = by_phase.get(e.activity, 0.0) + (e.hours * hourly_rate_usd)

        total_tokens = sum(e.input_tokens + e.output_tokens for e in self._token_entries)
        ratio = discovery_cost / lifecycle_cost if lifecycle_cost > 0 else 0.0

        report = CostReport(
            episode_id=episode_id,
            discovery_token_cost_usd=discovery_cost,
            lifecycle_cost_usd=lifecycle_cost,
            token_entries=list(self._token_entries),
            human_entries=list(self._human_entries),
            cost_ratio=ratio,
            by_model=by_model,
            by_phase=by_phase,
            total_tokens=total_tokens,
            total_human_hours=human_hours,
        )
        logger.info(
            "Cost report '%s': discovery=$%.2f, lifecycle=$%.2f, ratio=%.1f%%",
            episode_id,
            discovery_cost,
            lifecycle_cost,
            ratio * 100,
        )
        return report

    def reset(self) -> None:
        self._token_entries.clear()
        self._human_entries.clear()
