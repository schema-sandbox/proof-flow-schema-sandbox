"""
Tests for ProofFlow v41.0 (Cross-Model Handoff & Failure Note Artifact Manager)

Covers:
    - HandoffArtifact (Hash computation & immutable payload creation)
    - ModelHandoffManager (Cross-model state handoff DeepSeek-R1 -> GPT-4o)
"""

from __future__ import annotations

import pytest

from schemamath_api.model_handoff import ModelHandoffManager


class TestModelHandoff:
    def test_create_and_retrieve_handoff(self):
        mgr = ModelHandoffManager()
        handoff = mgr.create_handoff(
            source_model="DeepSeek-R1",
            target_model="GPT-4o",
            failure_notes="Injectivity mapping failed at boundary x=0",
            bridge_lemmas=["lemma_bounded_domain"],
            open_obligations=["prove_positivity_on_interval"],
        )

        assert handoff.source_model == "DeepSeek-R1"
        assert handoff.target_model == "GPT-4o"
        assert len(handoff.artifact_hash) == 64
        assert mgr.get_handoff(handoff.handoff_id) is not None
