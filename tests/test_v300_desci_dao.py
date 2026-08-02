"""
Tests for ProofFlow v30.0 (Autonomous DeSci Research DAO & Automated Bounty Settlement Engine)

Covers:
    - ResearchProposalDAO (Proposal token voting & quorum validation)
    - BountyEscrowSmartContract (Escrow bounty payout execution)
    - ReputationScoringSystem (Author reputation score computation)
"""

from __future__ import annotations

import pytest

from schemamath_api.desci_dao_engine import (
    BountyEscrowSmartContract,
    ReputationScoringSystem,
    ResearchProposalDAO,
)


class TestDesciDaoEngine:
    def test_proposal_voting_and_escrow(self):
        dao = ResearchProposalDAO()
        vote_res = dao.cast_vote("prop_201", yes_weight=800.0, no_weight=300.0, quorum_threshold=1000.0)
        assert vote_res.passed is True
        assert vote_res.quorum_reached is True

        escrow = BountyEscrowSmartContract()
        payout = escrow.execute_payout("bounty_501", "researcher_carol", 500.0)
        assert payout.status == "PAID"
        assert payout.payout_amount == 500.0

        rep = ReputationScoringSystem()
        score = rep.compute_reputation(verified_proofs=5, citations=12)
        assert score == 80.0
