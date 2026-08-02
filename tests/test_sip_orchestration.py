"""
Tests for @sip Orchestration Modules (O1: federation, O2: capacity, O3: campaign, O4: tournament)

Covers:
    - O1: @sip/federation roles, correlated review detection, and typed handoffs
    - O2: @sip/capacity lease management and verification debt limits
    - O3: @sip/campaign token budget accounting and target deduplication
    - O4: @sip/schema-tournament proposal evaluation and framework overthrow
    - Full 12-Module All-Layer Sandbox composition (F1-F4 + G1-G4 + O1-O4)
"""

from __future__ import annotations

import pytest

from schemamath_api.k0.decision import Decision
from schemamath_api.sip import (
    AgentRole,
    CorrelatedReviewDetector,
    HandoffType,
    compose,
    createCampaign,
    createCapacity,
    createClaim,
    createFence,
    createFederation,
    createGate,
    createLedger,
    createPartition,
    createTelos,
    createTournament,
    createTrajectory,
    createVerifier,
)


class TestSipFederationO1:
    def test_correlated_review_detector(self):
        assert CorrelatedReviewDetector.is_correlated("openai/gpt-4o", "openai/gpt-4-turbo") is True
        assert CorrelatedReviewDetector.is_correlated("openai/gpt-4o", "anthropic/claude-3-5-sonnet") is False

    def test_correlated_review_triggers_evidence_requirement(self):
        fed = createFederation()
        sandbox = compose(fed)

        res = sandbox.run("review_step", input_data={
            "author_model": "gpt-4o",
            "reviewer_model": "gpt-4-turbo",
        })

        assert res.final_decision.needs_evidence is True
        ev_decision = next(d for d in res.final_decision.contributing_decisions if d.approval == Decision.REQUIRE_EVIDENCE)
        assert "Correlated review warning" in ev_decision.reason


class TestSipCapacityO2:
    def test_verification_debt_suspends_new_moves(self):
        cap = createCapacity(maxVerificationDebt=3)
        sandbox = compose(cap)

        res = sandbox.run("explore", input_data={"unverified_claim_count": 5})
        assert res.success is False
        assert "Verification debt exceeded limit" in res.abort_reason


class TestSipCampaignO3:
    def test_campaign_token_budget_exhaustion(self):
        camp = createCampaign(name="test_c", maxTokens=500)
        sandbox = compose(camp)

        # Spend 300 tokens in 2 runs, 3rd run exceeds budget
        res1 = sandbox.run("task1", input_data={"tokens_used": 300})
        res2 = sandbox.run("task2", input_data={"tokens_used": 300})
        res3 = sandbox.run("task3", input_data={"tokens_used": 100})

        assert res1.success is True
        assert res2.success is True
        assert res3.success is False
        assert "token budget exhausted" in res3.abort_reason


class TestSipTournamentO4:
    def test_framework_overthrow_event(self):
        tourn = createTournament()
        tourn.submit_proposal("p1", "Classical Set Theory", {"type": "set"}, author="builder")
        tourn.submit_proposal("p2", "Homotopy Type Theory", {"type": "hott"}, author="rival_theorist")

        sandbox = compose(tourn)

        # Evaluate p2 with high score delta
        res = sandbox.run("evaluate", input_data={
            "tournament_proposal_id": "p2",
            "evaluation_score_delta": 10.0,
        })

        assert res.success is True
        assert tourn.leading_proposal_id == "p2"


class TestFull12ModuleSandbox:
    def test_all_12_modules_composed_successfully(self, tmp_path):
        workspace = tmp_path / "sandbox"
        workspace.mkdir()

        sandbox = compose(
            createGate(input={"type": "object"}),
            createLedger(retention="90d"),
            createFence(fs=[str(workspace)]),
            createPartition(mode="PROCESS"),
            createTelos(goal="Solve Goldbach Conjecture"),
            createClaim(),
            createTrajectory(),
            createVerifier(),
            createFederation(),
            createCapacity(maxVerificationDebt=10),
            createCampaign(name="goldbach_campaign"),
            createTournament(),
        )

        res = sandbox.run("grand_unified_step", input_data={"requested_fs": str(workspace / "data.json")})
        assert res.success is True
        assert len(res.completed_phases) == 11
