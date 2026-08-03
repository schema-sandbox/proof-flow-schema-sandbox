"""
DeSci Governance & Staking Token Manager (DesciGovernanceToken)

Manages ProofFlow Research (PFR) token balances, compute node staking deposits,
and slashing mechanisms for malicious or failing research nodes.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TokenAccount:
    node_id: str
    balance: float = 1000.0
    staked_amount: float = 0.0


class DesciGovernanceToken:
    """
    Token and staking ledger for ProofFlow DeSci DAO network.
    """

    def __init__(self) -> None:
        self.accounts: dict[str, TokenAccount] = {}

    def get_or_create_account(self, node_id: str) -> TokenAccount:
        """Get or initialize a node's token account."""
        if node_id not in self.accounts:
            self.accounts[node_id] = TokenAccount(node_id=node_id)
        return self.accounts[node_id]

    def stake(self, node_id: str, amount: float) -> bool:
        """Stake a specified amount of tokens."""
        acc = self.get_or_create_account(node_id)
        if acc.balance < amount:
            logger.warning("Node '%s' insufficient balance to stake %.2f", node_id, amount)
            return False

        acc.balance -= amount
        acc.staked_amount += amount
        logger.info("Node '%s' staked %.2f PFR tokens", node_id, amount)
        return True

    def slash(self, node_id: str, penalty_amount: float, reason: str = "Collusion") -> float:
        """Slash (confiscate) staked tokens from a malicious node."""
        acc = self.get_or_create_account(node_id)
        slashed = min(acc.staked_amount, penalty_amount)
        acc.staked_amount -= slashed
        logger.warning("Node '%s' slashed %.2f PFR tokens. Reason: %s", node_id, slashed, reason)
        return slashed
