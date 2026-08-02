"""
Autonomous Grant & Bounty Auto-Distributor (AutonomousGrantDistributor)

Automatically evaluates research breakthrough novelty scores and disburses grant funds
to verified authors and theorem contributors.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from schemamath_api.desci_token import DesciGovernanceToken

logger = logging.getLogger(__name__)


@dataclass
class GrantPayout:
    recipient_id: str
    amount: float
    breakthrough_score: float
    status: str = "DISBURSED"


class AutonomousGrantDistributor:
    """
    Auto-distributes grants based on theorem novelty and verification debt scores.
    """

    def __init__(self, token_manager: DesciGovernanceToken) -> None:
        self.token_manager = token_manager
        self.payout_history: list[GrantPayout] = []

    def evaluate_and_disburse(self, recipient_id: str, novelty_score: float) -> GrantPayout | None:
        """Disburse research grant proportional to theorem novelty score."""
        if novelty_score < 0.5:
            logger.info("Novelty score %.2f below grant threshold 0.50", novelty_score)
            return None

        payout_amount = round(novelty_score * 1000.0, 2)
        acc = self.token_manager.get_or_create_account(recipient_id)
        acc.balance += payout_amount

        payout = GrantPayout(
            recipient_id=recipient_id,
            amount=payout_amount,
            breakthrough_score=novelty_score,
        )
        self.payout_history.append(payout)
        logger.info("Disbursed grant %.2f PFR to recipient '%s'", payout_amount, recipient_id)
        return payout
