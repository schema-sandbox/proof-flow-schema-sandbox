"""
Tests for ProofFlow v21.4 (TqftInvariantEngine)

Covers:
    - TqftInvariantEngine (Jones polynomial & Chern-Simons invariant computation)
"""

from __future__ import annotations

import pytest

from schemamath_api.tqft import TqftInvariantEngine


class TestTqftInvariantEngine:
    def test_compute_knot_invariant(self):
        engine = TqftInvariantEngine()
        res = engine.compute_knot_invariant("Trefoil_Knot")

        assert res.is_topological_invariant is True
        assert "q" in res.jones_polynomial
        assert res.chern_simons_value > 0.0
