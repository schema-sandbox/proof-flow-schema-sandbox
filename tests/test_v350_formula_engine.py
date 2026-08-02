"""
Tests for ProofFlow v35.0 (Universal Mathematical Formula Expression & Multi-Format Renderer Engine)

Covers:
    - UniversalFormulaParser (Canonical MathAST parsing for LaTeX, MathML, Lean4)
    - MultiFormatFormulaRenderer (Multi-format rendering to LaTeX, MathML, Lean4, ASCII)
    - FormulaCompletenessSelfChecker (100+ formula completeness self-checking)
"""

from __future__ import annotations

import pytest

from schemamath_api.formula_engine import (
    FormulaCompletenessSelfChecker,
    MultiFormatFormulaRenderer,
    UniversalFormulaParser,
)


class TestFormulaEngine:
    def test_parse_and_render_all_formats(self):
        parser = UniversalFormulaParser()
        renderer = MultiFormatFormulaRenderer()

        ast_frac = parser.parse_formula("\\frac{a}{b}")
        res_frac = renderer.render_all_formats(ast_frac)
        assert "\\frac" in res_frac.latex
        assert "<mfrac>" in res_frac.mathml
        assert "a / b" in res_frac.lean4
        assert res_frac.is_fully_expressible is True

        ast_int = parser.parse_formula("\\int_a^b f(x) dx")
        res_int = renderer.render_all_formats(ast_int)
        assert "\\int" in res_int.latex
        assert "∫" in res_int.lean4

    def test_completeness_self_checker(self):
        checker = FormulaCompletenessSelfChecker()
        res = checker.run_completeness_self_check()

        assert res["total_domains_verified"] == 0
        assert res["total_domains_evaluated"] == 9
        assert res["total_formulas_tested"] >= 100
        assert res["unexpressible_formulas_count"] > 0
        assert res["completeness_score"] == 0.0
        assert res["status"] == "EXPERIMENTAL_UNVERIFIED"
