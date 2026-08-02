"""
Tests for ProofFlow v19.0.0 (IpProofAttestor, RoyaltyAutoSettlement)

Covers:
    - IpProofAttestor (Algorithm IP registration & ZK novelty attestation)
    - RoyaltyAutoSettlement (Algorithm usage royalty payment settlement)
"""

from __future__ import annotations

import pytest

from schemamath_api.ip_attestation import IpProofAttestor, RoyaltyAutoSettlement


class TestIpProofAttestor:
    def test_register_algorithm_ip(self):
        attestor = IpProofAttestor()
        cert = attestor.register_algorithm_ip("algo_fft_v2", "researcher_alice", "def fft(x): return x")

        assert cert.algorithm_id == "algo_fft_v2"
        assert cert.owner_id == "researcher_alice"
        assert cert.zk_attestation_hash.startswith("zk_ip_")
        assert cert.patent_status == "REGISTERED"


class TestRoyaltyAutoSettlement:
    def test_settle_royalty(self):
        settlement = RoyaltyAutoSettlement()
        pmt = settlement.Settle_royalty("algo_fft_v2", "researcher_alice", "company_bob", 0.10)

        assert pmt.royalty_amount == 0.10
        assert pmt.status == "SETTLED"
