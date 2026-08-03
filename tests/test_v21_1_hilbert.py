"""
Tests for ProofFlow v21.1 (HilbertSpaceVerifier)

Covers:
    - HilbertSpaceVerifier (Self-adjoint operator and spectral norm verification)
"""

from __future__ import annotations

from schemamath_api.hilbert_space import HilbertSpaceVerifier


class TestHilbertSpaceVerifier:
    def test_verify_self_adjoint_operator(self):
        verifier = HilbertSpaceVerifier()
        res = verifier.verify_self_adjoint_operator("H_hamiltonian")

        assert res.is_self_adjoint is True
        assert res.is_bounded is True
        assert res.spectral_norm == 1.0
