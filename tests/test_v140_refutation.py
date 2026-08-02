"""
Tests for ProofFlow v14.0.0 (RefutationSearchEngine, FalsificationMetric)

Covers:
    - RefutationSearchEngine (Counterexample search & conjecture refutation)
    - FalsificationMetric (Karl Popper falsifiability index computation)
"""

from __future__ import annotations

import pytest

from schemamath_api.refutation import RefutationSearchEngine


class TestRefutationSearchEngine:
    def test_search_counterexample_refuted(self):
        engine = RefutationSearchEngine()
        res = engine.search_counterexample("false_conjecture: all odd numbers are prime")

        assert res.is_refuted is True
        assert res.counterexample is not None

    def test_compute_falsifiability(self):
        engine = RefutationSearchEngine()
        metric = engine.compute_falsifiability("For all integers x, x^2 >= 0")

        assert metric.falsifiability_index > 0.0
        assert metric.is_testable is True
