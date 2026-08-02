"""
Tests for ProofFlow v8.0.0 (DesciGovernanceToken, PeerReviewStaking, AutonomousGrantDistributor)

Covers:
    - DesciGovernanceToken (staking, balance updates, slashing penalties)
    - PeerReviewStaking (peer review collateral deposit & collusion penalties)
    - AutonomousGrantDistributor (automated grant disbursement based on novelty score)
"""

from __future__ import annotations

import pytest

from schemamath_api.desci_token import DesciGovernanceToken
from schemamath_api.grant_distributor import AutonomousGrantDistributor
from schemamath_api.peer_review_staking import PeerReviewStaking


class TestDesciGovernanceToken:
    def test_staking_and_slashing(self):
        token_mgr = DesciGovernanceToken()
        acc = token_mgr.get_or_create_account("node_1")
        assert acc.balance == 1000.0

        staked = token_mgr.stake("node_1", 300.0)
        assert staked is True
        assert acc.balance == 700.0
        assert acc.staked_amount == 300.0

        slashed = token_mgr.slash("node_1", 100.0, reason="Test slash")
        assert slashed == 100.0
        assert acc.staked_amount == 200.0


class TestPeerReviewStaking:
    def test_submit_review_and_penalize_collusion(self):
        token_mgr = DesciGovernanceToken()
        review_staking = PeerReviewStaking(token_mgr)

        ok = review_staking.submit_review(
            reviewer_id="reviewer_1",
            paper_id="paper_101",
            approval=True,
            deposit=150.0,
        )
        assert ok is True
        acc = token_mgr.get_or_create_account("reviewer_1")
        assert acc.staked_amount == 150.0

        slashed = review_staking.penalize_collusion("reviewer_1", "paper_101")
        assert slashed == 100.0
        assert acc.staked_amount == 50.0


class TestAutonomousGrantDistributor:
    def test_evaluate_and_disburse(self):
        token_mgr = DesciGovernanceToken()
        distributor = AutonomousGrantDistributor(token_mgr)

        # Low score: no grant
        payout1 = distributor.evaluate_and_disburse("author_1", novelty_score=0.4)
        assert payout1 is None

        # High score: grant disbursed
        payout2 = distributor.evaluate_and_disburse("author_1", novelty_score=0.85)
        assert payout2 is not None
        assert payout2.amount == 850.0
        assert payout2.status == "DISBURSED"

        acc = token_mgr.get_or_create_account("author_1")
        assert acc.balance == 1850.0  # 1000 initial + 850 grant
