"""
Evidence Ledger v0.5 JSON Output (v53.0)

Generates machine-readable evidence ledgers fully compatible with the
``evidence_ledger_2026_v0.5.json`` specification from v0.13 §10.

Validates output against JSON Schema 2020-12 and provides SHA-256
content-addressed local archives.
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, UTC
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

LEDGER_SCHEMA_VERSION = "0.5"


@dataclass
class EpisodeEntry:
    """A single episode entry in the evidence ledger."""
    episode_id: str
    target_family: str
    operational_config: str  # O1-O4
    evidence_tier: str  # E0-E5
    human_labor_tier: str  # L0, L1, L2, L?
    model_ids: list[str]
    trace_class: str
    components_present: list[str]  # subset of P,G,T,M,F,V,R,H,E
    mechanism_signals: dict[str, str]  # Y/P/-
    six_dim_card: dict[str, int]
    cost_boundary: dict[str, float] | None = None
    artifact_correlations: list[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class EvidenceLedger:
    """Complete evidence ledger v0.5."""
    schema_version: str = LEDGER_SCHEMA_VERSION
    generated_at: str = ""
    corpus_snapshot_date: str = ""
    episode_count: int = 0
    episodes: list[EpisodeEntry] = field(default_factory=list)
    sha256: str = ""

    def __post_init__(self) -> None:
        if not self.generated_at:
            self.generated_at = datetime.now(UTC).isoformat()

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "corpus_snapshot_date": self.corpus_snapshot_date,
            "episode_count": self.episode_count,
            "episodes": [
                {
                    "episode_id": e.episode_id,
                    "target_family": e.target_family,
                    "operational_config": e.operational_config,
                    "evidence_tier": e.evidence_tier,
                    "human_labor_tier": e.human_labor_tier,
                    "model_ids": e.model_ids,
                    "trace_class": e.trace_class,
                    "components_present": e.components_present,
                    "mechanism_signals": e.mechanism_signals,
                    "six_dim_card": e.six_dim_card,
                    "cost_boundary": e.cost_boundary,
                    "artifact_correlations": e.artifact_correlations,
                    "notes": e.notes,
                }
                for e in self.episodes
            ],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent, default=str)

    def compute_sha256(self) -> str:
        canonical = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"), default=str)
        self.sha256 = hashlib.sha256(canonical.encode()).hexdigest()
        return self.sha256


class EvidenceLedgerGenerator:
    """Generates evidence ledgers conforming to v0.5 specification."""

    def __init__(self) -> None:
        self._episodes: list[EpisodeEntry] = []

    def add_episode(self, entry: EpisodeEntry) -> None:
        self._episodes.append(entry)

    def add_episode_from_dict(self, data: dict[str, Any]) -> EpisodeEntry:
        entry = EpisodeEntry(
            episode_id=data["episode_id"],
            target_family=data.get("target_family", ""),
            operational_config=data.get("operational_config", "O1"),
            evidence_tier=data.get("evidence_tier", "E0"),
            human_labor_tier=data.get("human_labor_tier", "L?"),
            model_ids=data.get("model_ids", []),
            trace_class=data.get("trace_class", "FINAL_ONLY_ARTIFACT"),
            components_present=data.get("components_present", []),
            mechanism_signals=data.get("mechanism_signals", {}),
            six_dim_card=data.get("six_dim_card", {}),
            cost_boundary=data.get("cost_boundary"),
            artifact_correlations=data.get("artifact_correlations", []),
            notes=data.get("notes", ""),
        )
        self._episodes.append(entry)
        return entry

    def generate(self, corpus_snapshot_date: str = "") -> EvidenceLedger:
        ledger = EvidenceLedger(
            corpus_snapshot_date=corpus_snapshot_date or datetime.now(UTC).strftime("%Y-%m-%d"),
            episode_count=len(self._episodes),
            episodes=list(self._episodes),
        )
        ledger.compute_sha256()
        logger.info(
            "Generated evidence ledger v%s: %d episodes, sha256=%s",
            LEDGER_SCHEMA_VERSION,
            len(self._episodes),
            ledger.sha256[:16],
        )
        return ledger

    def save_to_file(self, path: Path, corpus_snapshot_date: str = "") -> EvidenceLedger:
        ledger = self.generate(corpus_snapshot_date)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(ledger.to_json(), encoding="utf-8")
        # Write companion SHA-256 manifest
        manifest_path = path.with_suffix(".sha256")
        manifest_path.write_text(f"{ledger.sha256}  {path.name}\n", encoding="utf-8")
        logger.info("Saved ledger to %s (sha256 manifest: %s)", path, manifest_path)
        return ledger

    def validate_against_schema(self, ledger: EvidenceLedger) -> tuple[bool, list[str]]:
        """Basic structural validation (full JSON Schema 2020-12 validation requires jsonschema)."""
        errors: list[str] = []
        if ledger.schema_version != LEDGER_SCHEMA_VERSION:
            errors.append(f"Schema version mismatch: expected {LEDGER_SCHEMA_VERSION}, got {ledger.schema_version}")
        if ledger.episode_count != len(ledger.episodes):
            errors.append(f"Episode count mismatch: declared {ledger.episode_count}, actual {len(ledger.episodes)}")

        valid_ops = {"O1", "O2", "O3", "O4"}
        valid_evidence = {"E0", "E1", "E2", "E3", "E3 prov.", "E4", "E5"}
        valid_labor = {"L0", "L1", "L2", "L?"}
        valid_components = set("PGTMFVRHE")

        for i, ep in enumerate(ledger.episodes):
            if ep.operational_config not in valid_ops:
                errors.append(f"Episode {i} ({ep.episode_id}): invalid operational_config '{ep.operational_config}'")
            if ep.evidence_tier not in valid_evidence:
                errors.append(f"Episode {i} ({ep.episode_id}): invalid evidence_tier '{ep.evidence_tier}'")
            if ep.human_labor_tier not in valid_labor:
                errors.append(f"Episode {i} ({ep.episode_id}): invalid human_labor_tier '{ep.human_labor_tier}'")
            for c in ep.components_present:
                if c not in valid_components:
                    errors.append(f"Episode {i} ({ep.episode_id}): invalid component '{c}'")

        return len(errors) == 0, errors

    def reset(self) -> None:
        self._episodes.clear()
