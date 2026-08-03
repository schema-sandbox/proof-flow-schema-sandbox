"""
Tests for ProofFlow v21.3 (GrobnerBasisEngine)

Covers:
    - GrobnerBasisEngine (Buchberger algorithm Groebner basis computation & ideal reduction)
"""

from __future__ import annotations

from schemamath_api.grobner import GrobnerBasisEngine


class TestGrobnerBasisEngine:
    def test_compute_grobner_basis(self):
        engine = GrobnerBasisEngine()
        polys = ["x^2 - y", "y^2 - x"]
        res = engine.compute_grobner_basis(polys, target_poly="x^2 + y^2 - 1")

        assert len(res.grobner_basis) == 2
        assert res.is_ideal_member is True
        assert res.reduced_remainder == "0"
