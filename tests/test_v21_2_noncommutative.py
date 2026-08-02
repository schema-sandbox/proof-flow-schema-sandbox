"""
Tests for ProofFlow v21.2 (NonCommutativeGeometryEngine)

Covers:
    - NonCommutativeGeometryEngine (Spectral triple verification)
"""

from __future__ import annotations

import pytest

from schemamath_api.noncommutative import NonCommutativeGeometryEngine


class TestNonCommutativeGeometryEngine:
    def test_verify_spectral_triple(self):
        engine = NonCommutativeGeometryEngine()
        res = engine.verify_spectral_triple("Quantum_Torus_NC", dimension=2)

        assert res.is_noncommutative is True
        assert res.dirac_operator_self_adjoint is True
        assert res.dimension == 2
