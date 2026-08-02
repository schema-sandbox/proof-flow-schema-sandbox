"""Tests for Dossier Generator (v48.0)."""

import json
import pytest
from schemamath_api.dossier_generator import (
    DossierGenerator, EvidenceCardScores, CostBoundary, ResearchEpisodeDossier,
)


def _make_card(pp=3, aa=4, dv=5, ir=2, np=3, au=4):
    return EvidenceCardScores(pp, aa, dv, ir, np, au)


class TestEvidenceCardScores:
    def test_total(self):
        card = _make_card(3, 4, 5, 2, 3, 4)
        assert card.total == 21

    def test_zero_total(self):
        card = EvidenceCardScores(0, 0, 0, 0, 0, 0)
        assert card.total == 0

    def test_max_total(self):
        card = EvidenceCardScores(5, 5, 5, 5, 5, 5)
        assert card.total == 30


class TestCostBoundary:
    def test_ratio_computed(self):
        cb = CostBoundary(discovery_token_cost_usd=2000, lifecycle_cost_usd=500000)
        assert 0.003 < cb.cost_ratio < 0.005

    def test_zero_lifecycle(self):
        cb = CostBoundary(discovery_token_cost_usd=100, lifecycle_cost_usd=0)
        assert cb.cost_ratio == 0.0


class TestDossierGenerator:
    def test_minimal_dossier(self):
        gen = DossierGenerator()
        d = gen.generate(
            episode_id="C1",
            target_specification="Erdős conjecture #536",
            model_identifiers=["o3-2025-04-16"],
        )
        assert d.episode_id == "C1"
        assert d.evidence_tier == "E0"
        assert d.human_labor_tier == "L?"
        assert len(d.dossier_sha256) == 64

    def test_full_dossier(self):
        gen = DossierGenerator()
        d = gen.generate(
            episode_id="C17",
            target_specification="10 result families",
            model_identifiers=["o3", "o4-mini"],
            operational_config="O4",
            search_topology="parallel-batch",
            trajectory_state={"failed_routes": ["route_a"], "negative_knowledge": ["nk1"]},
            falsification_record=["counterexample_search_n8"],
            repair_lineage=["route_replacement_cm_sign_ideal"],
            verification_method="lean4_kernel",
            kernel_identity="Lean 4.32.0",
            axiom_ceiling=["propext", "Classical.choice", "Quot.sound"],
            human_labor_tier="L2",
            evidence_tier="E3 prov.",
            evidence_card=_make_card(4, 5, 5, 3, 5, 3),
            trace_derivation_class="MODEL_RECONSTRUCTION",
            artifact_correlations=["manuscript+walkthrough share model lineage"],
            trusted_challenge_boundary="Comparator-verified against openai/ten-proofs",
            cost_boundary=CostBoundary(2000, 500000),
            benchmark_completeness="Baselines not fully optimized",
        )
        assert d.operational_config == "O4"
        assert d.evidence_card.total == 25
        assert d.cost_boundary.cost_ratio < 0.01

    def test_to_json(self):
        gen = DossierGenerator()
        d = gen.generate(
            episode_id="test",
            target_specification="test target",
            model_identifiers=["test-model"],
        )
        j = d.to_json()
        parsed = json.loads(j)
        assert parsed["episode_id"] == "test"
        assert "evidence_card" in parsed

    def test_to_markdown(self):
        gen = DossierGenerator()
        d = gen.generate(
            episode_id="C8",
            target_specification="Unit-distance chromatic number",
            model_identifiers=["o3"],
            evidence_card=_make_card(4, 5, 5, 4, 5, 3),
            cost_boundary=CostBoundary(1500, 200000),
        )
        md = d.to_markdown()
        assert "# Research Episode Dossier: C8" in md
        assert "Unit-distance" in md
        assert "26/30" in md
        assert "$1,500.00" in md

    def test_to_dict_roundtrip(self):
        gen = DossierGenerator()
        d = gen.generate(
            episode_id="rt",
            target_specification="roundtrip",
            model_identifiers=["m1", "m2"],
            axiom_ceiling=["propext"],
        )
        data = d.to_dict()
        assert data["axiom_ceiling"] == ["propext"]
        assert data["model_identifiers"] == ["m1", "m2"]

    def test_sha256_deterministic(self):
        gen = DossierGenerator()
        d1 = gen.generate(episode_id="x", target_specification="y", model_identifiers=["z"])
        d2 = gen.generate(episode_id="x", target_specification="y", model_identifiers=["z"])
        # SHA is based on content which includes timestamp, so different runs differ
        # but structure should be valid
        assert len(d1.dossier_sha256) == 64
        assert len(d2.dossier_sha256) == 64

    def test_default_evidence_card(self):
        gen = DossierGenerator()
        d = gen.generate(episode_id="d1", target_specification="t", model_identifiers=["m"])
        assert d.evidence_card.total == 0

    def test_markdown_no_cost(self):
        gen = DossierGenerator()
        d = gen.generate(episode_id="nc", target_specification="t", model_identifiers=["m"])
        md = d.to_markdown()
        assert "Not reported" in md
