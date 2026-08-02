"""Tests for Evidence Ledger v0.5 (v53.0)."""

import json
import pytest
from pathlib import Path
from schemamath_api.evidence_ledger import (
    EvidenceLedgerGenerator, EpisodeEntry, EvidenceLedger, LEDGER_SCHEMA_VERSION,
)


def _make_episode(eid="C1", **kwargs):
    defaults = {
        "episode_id": eid,
        "target_family": "number_theory",
        "operational_config": "O3",
        "evidence_tier": "E3",
        "human_labor_tier": "L2",
        "model_ids": ["o3"],
        "trace_class": "RAW_EVENT_STREAM",
        "components_present": ["P", "G", "T", "M", "F", "V", "R", "H"],
        "mechanism_signals": {"certificate_asymmetry": "Y", "destructive_critique": "P"},
        "six_dim_card": {"pp": 4, "aa": 5, "dv": 5, "ir": 3, "np": 4, "au": 3},
    }
    defaults.update(kwargs)
    return EpisodeEntry(**defaults)


class TestEpisodeEntry:
    def test_creation(self):
        e = _make_episode()
        assert e.episode_id == "C1"
        assert e.operational_config == "O3"

    def test_default_fields(self):
        e = _make_episode()
        assert e.artifact_correlations == []
        assert e.notes == ""
        assert e.cost_boundary is None


class TestEvidenceLedger:
    def test_schema_version(self):
        assert LEDGER_SCHEMA_VERSION == "0.5"

    def test_empty_ledger(self):
        ledger = EvidenceLedger()
        assert ledger.episode_count == 0
        assert len(ledger.episodes) == 0

    def test_to_json(self):
        ledger = EvidenceLedger(episodes=[_make_episode()], episode_count=1)
        j = ledger.to_json()
        parsed = json.loads(j)
        assert parsed["schema_version"] == "0.5"
        assert len(parsed["episodes"]) == 1

    def test_sha256(self):
        ledger = EvidenceLedger(episodes=[_make_episode()], episode_count=1)
        sha = ledger.compute_sha256()
        assert len(sha) == 64
        assert sha == ledger.sha256


class TestEvidenceLedgerGenerator:
    def test_add_and_generate(self):
        gen = EvidenceLedgerGenerator()
        gen.add_episode(_make_episode("C1"))
        gen.add_episode(_make_episode("C2"))
        ledger = gen.generate()
        assert ledger.episode_count == 2
        assert len(ledger.sha256) == 64

    def test_add_from_dict(self):
        gen = EvidenceLedgerGenerator()
        entry = gen.add_episode_from_dict({
            "episode_id": "C17",
            "target_family": "mixed",
            "operational_config": "O4",
            "evidence_tier": "E3",
            "human_labor_tier": "L2",
            "model_ids": ["o3", "o4-mini"],
            "trace_class": "MODEL_RECONSTRUCTION",
            "components_present": ["P", "G", "T", "M", "F", "V", "R", "H", "E"],
            "mechanism_signals": {},
            "six_dim_card": {"pp": 4, "aa": 5, "dv": 5, "ir": 3, "np": 5, "au": 3},
        })
        assert entry.episode_id == "C17"
        ledger = gen.generate()
        assert ledger.episode_count == 1

    def test_save_to_file(self, tmp_path):
        gen = EvidenceLedgerGenerator()
        gen.add_episode(_make_episode("C1"))
        path = tmp_path / "ledger.json"
        ledger = gen.save_to_file(path, corpus_snapshot_date="2026-08-01")
        assert path.exists()
        content = json.loads(path.read_text())
        assert content["corpus_snapshot_date"] == "2026-08-01"
        # SHA-256 manifest
        manifest = tmp_path / "ledger.sha256"
        assert manifest.exists()
        assert ledger.sha256 in manifest.read_text()

    def test_validate_clean(self):
        gen = EvidenceLedgerGenerator()
        gen.add_episode(_make_episode("C1"))
        ledger = gen.generate()
        valid, errors = gen.validate_against_schema(ledger)
        assert valid
        assert errors == []

    def test_validate_bad_operational_config(self):
        gen = EvidenceLedgerGenerator()
        gen.add_episode(_make_episode("C1", operational_config="O9"))
        ledger = gen.generate()
        valid, errors = gen.validate_against_schema(ledger)
        assert not valid
        assert any("O9" in e for e in errors)

    def test_validate_bad_evidence_tier(self):
        gen = EvidenceLedgerGenerator()
        gen.add_episode(_make_episode("C1", evidence_tier="E9"))
        ledger = gen.generate()
        valid, errors = gen.validate_against_schema(ledger)
        assert not valid

    def test_validate_bad_labor_tier(self):
        gen = EvidenceLedgerGenerator()
        gen.add_episode(_make_episode("C1", human_labor_tier="L9"))
        ledger = gen.generate()
        valid, errors = gen.validate_against_schema(ledger)
        assert not valid

    def test_validate_bad_component(self):
        gen = EvidenceLedgerGenerator()
        gen.add_episode(_make_episode("C1", components_present=["X", "Y"]))
        ledger = gen.generate()
        valid, errors = gen.validate_against_schema(ledger)
        assert not valid

    def test_validate_episode_count_mismatch(self):
        ledger = EvidenceLedger(episodes=[_make_episode()], episode_count=5)
        gen = EvidenceLedgerGenerator()
        valid, errors = gen.validate_against_schema(ledger)
        assert not valid
        assert any("count mismatch" in e for e in errors)

    def test_reset(self):
        gen = EvidenceLedgerGenerator()
        gen.add_episode(_make_episode())
        gen.reset()
        ledger = gen.generate()
        assert ledger.episode_count == 0

    def test_corpus_snapshot_date(self):
        gen = EvidenceLedgerGenerator()
        gen.add_episode(_make_episode())
        ledger = gen.generate(corpus_snapshot_date="2026-08-01")
        assert ledger.corpus_snapshot_date == "2026-08-01"
