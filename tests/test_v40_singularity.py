"""
Tests for ProofFlow v4.0.0 (AxiomSynthesizerEngine, EpistemicKnowledgeGraph, FieldsCandidateSynthesizer)

Covers:
    - AxiomSynthesizerEngine (synthesizing and validating candidate axiom frameworks)
    - EpistemicKnowledgeGraph (connecting cross-domain concepts into unified hypergraph)
    - FieldsCandidateSynthesizer (evaluating theorem novelty and breakthrough status)
"""

from __future__ import annotations

from schemamath_api.axiom_engine import AxiomSynthesizerEngine
from schemamath_api.fields_evaluator import FieldsCandidateSynthesizer
from schemamath_api.knowledge_graph import EpistemicKnowledgeGraph


class TestAxiomSynthesizerEngine:
    def test_synthesize_domain_axioms(self):
        engine = AxiomSynthesizerEngine()
        system = engine.synthesize_domain("Non-Archimedean Geometry")

        assert system.domain_name == "Non-Archimedean Geometry"
        assert system.is_consistent is True
        assert len(system.axioms) >= 3
        assert system.expressive_score > 0.9


class TestEpistemicKnowledgeGraph:
    def test_add_and_connect_concepts(self):
        graph = EpistemicKnowledgeGraph()
        n1 = graph.add_concept("c1", "Riemann Zeta Function", "NumberTheory")
        graph.add_concept("c2", "Spectral Operators", "FunctionalAnalysis")

        connected = graph.connect_concepts("c1", "c2")
        assert connected is True
        assert "c2" in n1.connected_nodes

        bridge = graph.find_cross_domain_bridge("NumberTheory", "FunctionalAnalysis")
        assert len(bridge) == 2
        assert "c1" in bridge and "c2" in bridge


class TestFieldsCandidateSynthesizer:
    def test_evaluate_breakthrough_theorem(self):
        evaluator = FieldsCandidateSynthesizer()
        res = evaluator.evaluate_breakthrough(
            theorem_title="Proof of Birch and Swinnerton-Dyer Conjecture",
            proof_length_steps=250,
            cross_domain_connections=4,
        )

        assert res.theorem_title == "Proof of Birch and Swinnerton-Dyer Conjecture"
        assert res.novelty_score > 0.8
        assert res.resonance_score > 0.8
        assert res.impact_tier in ["BREAKTHROUGH", "SINGULARITY"]
        assert res.is_fields_medal_candidate is True
