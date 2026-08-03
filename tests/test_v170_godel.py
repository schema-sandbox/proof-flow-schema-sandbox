"""
Tests for ProofFlow v17.0.0 (GodelBoundaryExplorer, ConsistencyGuarantee)

Covers:
    - GodelBoundaryExplorer (Godel sentence undecidability analysis)
    - Relative consistency bound evaluation
"""

from __future__ import annotations

from schemamath_api.godel import GodelBoundaryExplorer


class TestGodelBoundaryExplorer:
    def test_analyze_godel_sentence(self):
        explorer = GodelBoundaryExplorer()
        res = explorer.analyze_godel_sentence("ZFC")

        assert res.is_undecidable is True
        assert res.godel_number > 0
        assert "G_ZFC" in res.statement

    def test_evaluate_relative_consistency(self):
        explorer = GodelBoundaryExplorer()
        bound = explorer.evaluate_relative_consistency("ZFC", "Continuum Hypothesis")

        assert bound.relative_consistency_proven is True
        assert bound.consistency_strength_level == 2
