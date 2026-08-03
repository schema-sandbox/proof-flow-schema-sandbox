"""
Tests for ProofFlow v16.0.0 (QuantumEntanglementVerifier, NoCloningEnforcer)

Covers:
    - QuantumEntanglementVerifier (Bell state verification & von Neumann entropy)
    - NoCloningEnforcer (Quantum no-cloning theorem enforcement)
"""

from __future__ import annotations

from schemamath_api.quantum_info import NoCloningEnforcer, QuantumEntanglementVerifier


class TestQuantumEntanglementVerifier:
    def test_verify_bell_state(self):
        verifier = QuantumEntanglementVerifier()
        res = verifier.verify_bell_state("|Φ+⟩")

        assert res.is_entangled is True
        assert res.von_neumann_entropy == 1.0


class TestNoCloningEnforcer:
    def test_check_cloning_attempt(self):
        enforcer = NoCloningEnforcer()
        res = enforcer.check_cloning_attempt("|ψ⟩ = α|0⟩ + β|1⟩")

        assert res.is_cloning_allowed is False
        assert "No-Cloning Theorem" in res.reason
