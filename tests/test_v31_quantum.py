"""
Tests for ProofFlow v3.1.0 (DilithiumProofAttestor, CopilotWorkspaceServer, CounterexampleFuzzer)

Covers:
    - DilithiumProofAttestor (post-quantum ML-DSA signature generation and verification)
    - CopilotWorkspaceServer (IDE session management and tactic hint generation)
    - CounterexampleFuzzer (property fuzzing and counterexample discovery)
"""

from __future__ import annotations

import pytest
from uuid import uuid4

from schemamath_api.copilot_server import CopilotWorkspaceServer
from schemamath_api.dilithium_attestor import DilithiumProofAttestor
from schemamath_api.domain import Actor, ActorType, EventRecord
from schemamath_api.fuzzer import CounterexampleFuzzer


class TestDilithiumProofAttestor:
    def test_post_quantum_signature_signing_and_verification(self):
        attestor = DilithiumProofAttestor()
        ev = EventRecord(
            event_id=uuid4(),
            project_id=uuid4(),
            event_type="AXIOM_ADDED",
            timestamp="2026-08-01T00:00:00Z",
            actor=Actor(type=ActorType.HUMAN, id="user1"),
            event_hash="hash_pqc_1",
        )

        attestation = attestor.sign_events([ev])
        assert attestation.attestation_id.startswith("pqc_att_")
        assert attestation.dilithium_signature.startswith("DILITHIUM_ML_DSA_SIG_")
        assert attestation.quantum_resistant is True

        valid = attestor.verify_quantum_signature(attestation)
        assert valid is True


class TestCopilotWorkspaceServer:
    def test_copilot_session_and_tactic_completion(self):
        server = CopilotWorkspaceServer()
        session_id = server.create_session("vscode_ext")

        assert session_id.startswith("session_")
        hints = server.request_tactic_completion(session_id, "n + m = m + n")

        assert len(hints) == 2
        assert hints[0].suggested_tactic == "decide"
        assert hints[1].suggested_tactic == "simp [Nat.add_comm]"


class TestCounterexampleFuzzer:
    def test_fuzzer_discovers_counterexample(self):
        fuzzer = CounterexampleFuzzer()

        # False hypothesis: all numbers < 10 are even
        def is_even(n: int) -> bool:
            return n % 2 == 0

        res = fuzzer.fuzz_predicate(is_even, input_range=(2, 10))
        assert res.counterexample_found is True
        assert res.failing_input == 3

    def test_fuzzer_valid_hypothesis(self):
        fuzzer = CounterexampleFuzzer()

        # Valid hypothesis: n^2 >= 0
        def square_non_negative(n: int) -> bool:
            return (n * n) >= 0

        res = fuzzer.fuzz_predicate(square_non_negative, input_range=(1, 50))
        assert res.counterexample_found is False
