"""
Tests for ProofFlow v21.7 (CliffordAlgebraEngine)

Covers:
    - CliffordAlgebraEngine (Clifford algebra signature & associativity verification)
"""

from __future__ import annotations

from schemamath_api.clifford import CliffordAlgebraEngine


class TestCliffordAlgebraEngine:
    def test_verify_clifford_signature(self):
        engine = CliffordAlgebraEngine()
        res = engine.verify_clifford_signature(p=3, q=1)

        assert res.algebra_name == "Cl(3,1)"
        assert res.dimension == 16
        assert res.is_associative is True
