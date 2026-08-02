"""
Visible Human Labor & Attribution Tracker (v44.0)

Tracks visible human labor lower-bound tiers (L0, L1, L2, L?) for target selection,
curation, proof repair, formalization, and manuscript maturation, preventing unearned "fully autonomous" claims.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class HumanLaborRecord:
    episode_id: str
    labor_tier: str  # L0, L1, L2, L?
    curation_hours: float
    proof_repair_hours: float
    formalization_hours: float
    manuscript_hours: float
    total_human_hours: float
    attribution_statement: str


class HumanLaborTracker:
    """
    Tracks and discloses visible human labor bounds across research episodes.
    """

    def record_labor(
        self,
        episode_id: str,
        curation_hours: float = 0.0,
        repair_hours: float = 0.0,
        formalization_hours: float = 0.0,
        manuscript_hours: float = 0.0,
    ) -> HumanLaborRecord:
        total = curation_hours + repair_hours + formalization_hours + manuscript_hours

        if total == 0:
            tier = "L0"  # Minimal intervention
        elif total < 10.0:
            tier = "L1"  # Bounded curation / single-researcher cleanup
        else:
            tier = "L2"  # Multi-day sustained team reconstruction & maturation

        statement = f"Episode '{episode_id}' human labor tier {tier} ({total:.1f} total hours)."
        logger.info("Recorded human labor for '%s': tier=%s (total=%.1fh)", episode_id, tier, total)
        return HumanLaborRecord(
            episode_id=episode_id,
            labor_tier=tier,
            curation_hours=curation_hours,
            proof_repair_hours=repair_hours,
            formalization_hours=formalization_hours,
            manuscript_hours=manuscript_hours,
            total_human_hours=total,
            attribution_statement=statement,
        )
