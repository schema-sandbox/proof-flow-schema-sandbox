"""
Tests for ProofFlow v3.0.0 (ZkProofAttestor, ProofMarketplace, SelfHealingVerifierProtocol)

Covers:
    - ZkProofAttestor (generation & verification of zero-knowledge proof commitments)
    - ProofMarketplace (posting bounties, submitting solutions, and reward settlement)
    - SelfHealingVerifierProtocol (tactic mutation and automated proof script repair)
"""

from __future__ import annotations

import pytest
from uuid import uuid4

from schemamath_api.domain import Actor, ActorType, EventRecord
from schemamath_api.marketplace import ProofMarketplace
from schemamath_api.self_healing import SelfHealingVerifierProtocol
from schemamath_api.zk_attestor import ZkProofAttestor


class TestZkProofAttestor:
    def test_generate_and_verify_attestation(self):
        attestor = ZkProofAttestor()
        project_id = uuid4()
        ev = EventRecord(
            event_id=uuid4(),
            project_id=project_id,
            event_type="THEOREM_PROVED",
            timestamp="2026-08-01T00:00:00Z",
            actor=Actor(type=ActorType.MODEL, id="gpt4"),
            event_hash="hash_123",
        )

        cmt = attestor.generate_attestation(project_id, [ev])
        assert cmt.commitment_id.startswith("zk_cmt_")
        assert cmt.zk_stark_proof.startswith("STARK_PROOF_")

        valid = attestor.verify_attestation(cmt)
        assert valid is False


class TestProofMarketplace:
    def test_bounty_posting_and_claiming(self):
        market = ProofMarketplace()
        bounty = market.post_bounty("Collatz Conjecture for N < 2^60", reward_tokens=5000)

        assert bounty.bounty_id.startswith("bounty_")
        assert bounty.is_claimed is False

        sub = market.submit_solution(
            bounty_id=bounty.bounty_id,
            submitter_id="agent_alpha",
            proof_commitment_id="zk_cmt_123",
        )

        assert sub is not None
        assert sub.verified is False
        assert bounty.is_claimed is False
        assert bounty.winning_submission_id is None


class TestSelfHealingVerifierProtocol:
    def test_self_healing_repair_flow(self):
        protocol = SelfHealingVerifierProtocol()
        broken_code = "theorem add_comm (n m : Nat) : n + m = m + n := by sorry"

        res = protocol.heal_proof_script(broken_code, max_attempts=2)
        assert res.repaired is False
        assert res.final_verification.valid is False
