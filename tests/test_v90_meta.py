"""
Tests for ProofFlow v9.0.0 (CounterfactualUniverse, MetaTheoremGenerator, InconsistencyDetector)

Covers:
    - CounterfactualUniverse (Intuitionistic logic LEM rejection vs Classical logic evaluation)
    - MetaTheoremGenerator (Category theory functor synthesis across domains)
    - InconsistencyDetector (Logical contradiction & Principle of Explosion detection)
"""

from __future__ import annotations

from schemamath_api.counterfactual import CounterfactualUniverse, LogicFramework
from schemamath_api.inconsistency_detector import InconsistencyDetector
from schemamath_api.meta_theorem import MetaTheoremGenerator


class TestCounterfactualUniverse:
    def test_intuitionistic_logic_lem_rejection(self):
        univ = CounterfactualUniverse()
        steps = ["Assume P", "Apply law of excluded middle", "Conclude Q"]

        res = univ.evaluate_proof(steps, framework=LogicFramework.INTUITIONISTIC)
        assert res.is_valid is False
        assert res.requires_lem is True

    def test_classical_logic_lem_accepted(self):
        univ = CounterfactualUniverse()
        steps = ["Assume P", "Apply law of excluded middle", "Conclude Q"]

        res = univ.evaluate_proof(steps, framework=LogicFramework.CLASSICAL)
        assert res.is_valid is True


class TestMetaTheoremGenerator:
    def test_synthesize_meta_theorem(self):
        generator = MetaTheoremGenerator()
        meta = generator.synthesize_meta_theorem(domain_a="Topology", domain_b="Algebra")

        assert "Topology" in meta.meta_name
        assert meta.functor.source_category == "Topology"
        assert meta.functor.target_category == "Algebra"


class TestInconsistencyDetector:
    def test_check_consistency_no_contradiction(self):
        detector = InconsistencyDetector()
        axioms = ["x > 0", "y > 0"]
        report = detector.check_consistency(axioms)

        assert report.has_contradiction is False
        assert report.is_trivialized is False

    def test_check_consistency_with_contradiction(self):
        detector = InconsistencyDetector()
        axioms = ["P", "not P"]
        report = detector.check_consistency(axioms)

        assert report.has_contradiction is True
        assert report.is_trivialized is True
