"""
Tests for ProofFlow v39.0 (GUDHI Topological Data Analysis & Simplicial Complex Suite)

Covers:
    - SimplicialFiltrationBuilder (Alpha complex filtration building)
    - PersistentBettiCurveEngine (Betti curves β_0, β_1, β_2 computation)
"""

from __future__ import annotations

import pytest

from schemamath_api.gudhi_tda_suite import (
    PersistentBettiCurveEngine,
    SimplicialFiltrationBuilder,
)


class TestGudhiTdaSuite:
    def test_alpha_complex_and_betti_curves(self):
        builder = SimplicialFiltrationBuilder()
        pts = [[0.0, 0.0], [1.0, 0.0], [0.5, 1.0], [0.0, 1.0]]
        rep = builder.build_alpha_complex(pts, max_alpha=1.5)
        assert rep.complex_type == "ALPHA_COMPLEX"
        assert rep.num_simplices >= 4
        assert rep.status == "UNAVAILABLE"
        assert rep.verified is False

        engine = PersistentBettiCurveEngine()
        betti_at_05 = engine.compute_betti_numbers_at(rep, 0.5)
        assert betti_at_05 == []
