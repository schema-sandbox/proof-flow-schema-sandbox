"""
Tests for @sip Governance Modules (G1: telos, G2: claim, G3: trajectory, G4: verifier)

Covers:
    - G1: @sip/telos non-goal drift detection and stagnation retry loop alerts
    - G2: @sip/claim state transitions, evidence maturity, and human-confirmation requirement for CERTIFIED
    - G3: @sip/trajectory logging, route supersession check, and failure assetization
    - G4: @sip/verifier custom verifiers and hardening checks
    - Multi-module Governance recipe composition (F1+F2+F3+G1+G2+G3+G4)
"""

from __future__ import annotations

import pytest
from schemamath_api.k0.decision import Decision
from schemamath_api.sip import (
    ClaimStatus,
    EvidenceMaturity,
    compose,
    createClaim,
    createFence,
    createGate,
    createLedger,
    createTelos,
    createTrajectory,
    createVerifier,
)


class TestSipTelosG1:
    def test_non_goal_drift_denied(self):
        telos = createTelos(
            goal="Analyze pricing",
            nonGoals=["Do not modify production database", "Do not send emails"],
        )
        sandbox = compose(telos)

        res = sandbox.run("modify_production_database_query")
        assert res.success is False
        assert "Goal drift detected" in res.abort_reason

    def test_stagnation_alert_on_consecutive_repeats(self):
        telos = createTelos(
            goal="Explore routes",
            stagnation={"maxEquivalentRetries": 3, "windowSteps": 10},
        )
        sandbox = compose(telos)

        # Run 2 identical calls -> allowed
        res1 = sandbox.run("same_action", input_data={"key": "val"})
        res2 = sandbox.run("same_action", input_data={"key": "val"})
        assert res1.success is True
        assert res2.success is True

        # 3rd identical call -> triggers REQUIRE_HUMAN / stagnation alert
        res3 = sandbox.run("same_action", input_data={"key": "val"})
        assert res3.final_decision.needs_human is True
        assert res3.final_decision.approval == Decision.REQUIRE_HUMAN


class TestSipClaimG2:
    def test_claim_certification_requires_human_confirmation(self):
        claim_mod = createClaim()
        claim = claim_mod.create_claim("Riemann Hypothesis candidate formulation")

        # Invalid transition to CERTIFIED without human confirmation
        with pytest.raises(ValueError, match="human_confirmed"):
            claim_mod.transition_claim(
                claim.claim_id,
                target_status=ClaimStatus.ACCEPTED,
                target_maturity=EvidenceMaturity.CERTIFIED,
                evidence_refs=["ev_1"],
                human_confirmed=False,
            )

        # Valid transition with human confirmation and evidence
        updated = claim_mod.transition_claim(
            claim.claim_id,
            target_status=ClaimStatus.ACCEPTED,
            target_maturity=EvidenceMaturity.CERTIFIED,
            evidence_refs=["ev_1"],
            human_confirmed=True,
        )
        assert updated.maturity == EvidenceMaturity.CERTIFIED
        assert updated.status == ClaimStatus.ACCEPTED


class TestSipTrajectoryG3:
    def test_trajectory_logging_and_failure_assetization(self):
        traj = createTrajectory()
        sandbox = compose(traj)

        res1 = sandbox.run("step1", input_data={"route_id": "r1", "is_failure": False})
        res2 = sandbox.run(
            "step2",
            input_data={"route_id": "r1", "is_failure": True, "failure_reason": "Zero division"},
        )

        assert res1.success is True
        assert res2.success is True

        assets = traj.inspect_failed_assets()
        assert len(assets) == 1
        assert assets[0]["asset"]["reason"] == "Zero division"


class TestSipVerifierG4:
    def test_verifier_unverified_without_expected_hash(self):
        verifier = createVerifier()
        sandbox = compose(verifier)

        # A target without an expected_hash cannot be claimed valid (no false success).
        res = sandbox.run("verify_op", input_data={"verification_target": {"data": 123}})
        assert res.success is False
        assert "unverified" in res.abort_reason

    def test_verifier_passes_on_matching_hash(self):
        verifier = createVerifier()
        sandbox = compose(verifier)
        import hashlib
        import json

        expected_hash = hashlib.sha256(
            json.dumps({"data": 123}, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        res = sandbox.run(
            "verify_op",
            input_data={
                "verification_target": {"data": 123, "expected_hash": expected_hash}
            },
        )
        assert res.success is True

    def test_verifier_fails_on_hash_mismatch(self):
        verifier = createVerifier()
        sandbox = compose(verifier)
        res = sandbox.run(
            "verify_op",
            input_data={
                "verification_target": {
                    "data": 123,
                    "expected_hash": "0" * 64,
                }
            },
        )
        assert res.success is False

    def test_verifier_fails_on_registered_strict_check(self):
        verifier = createVerifier()
        sandbox = compose(verifier)
        import hashlib
        import json

        from schemamath_api.sip.verifier import VerificationResult

        def failing_v(payload):
            return VerificationResult(valid=False, verifier_name="strict_v", details="Syntax error")

        verifier.register_verifier("strict_v", failing_v)

        # A hash-correct target passes the default check, so the registered
        # strict verifier is reached and correctly blocks the operation.
        expected_hash = hashlib.sha256(
            json.dumps({"data": 1}, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        res = sandbox.run(
            "verify_op",
            input_data={"verification_target": {"data": 1, "expected_hash": expected_hash}},
        )
        assert res.success is False
        assert "Verifier 'strict_v' failed" in res.abort_reason


class TestFullGovernanceRecipe:
    def test_full_7_module_governance_sandbox(self):
        sandbox = compose(
            createGate(input={"type": "object"}),
            createLedger(retention="90d"),
            createFence(fs=["*"], net=["*"], tools=["*"]),
            createTelos(goal="Prove conjecture", nonGoals=["Do not delete files"]),
            createClaim(),
            createTrajectory(),
            createVerifier(),
        )

        res = sandbox.run("governed_step", input_data={"query": "test"})
        assert res.success is True
        assert len(res.completed_phases) == 11
