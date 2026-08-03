"""
Tests for ProofFlow v12.0.0 (HomologyVerifier, DifferentialFormsEngine)

Covers:
    - HomologyVerifier (Betti numbers calculation & Euler characteristic validation)
    - DifferentialFormsEngine (Exterior derivative d^2 = 0 verification)
"""

from __future__ import annotations

from schemamath_api.homology import DifferentialFormsEngine, HomologyVerifier


class TestHomologyVerifier:
    def test_compute_betti_numbers(self):
        verifier = HomologyVerifier()
        res = verifier.compute_betti_numbers(vertices=4, edges=6, faces=4)

        assert res.euler_characteristic == 2
        assert res.betti_numbers == [1, 0, 1]
        assert res.is_valid_manifold is True


class TestDifferentialFormsEngine:
    def test_verify_exterior_derivative(self):
        engine = DifferentialFormsEngine()
        res = engine.verify_exterior_derivative("dx ∧ dy", degree=2)

        assert res.d_squared_is_zero is True
        assert "d(d(dx ∧ dy)) = 0" in res.exterior_derivative_applied
