"""
Tests for ProofFlow v45.0 (S10 Telos & Piagetian Accommodation Engine)

Covers:
    - TelosAccommodationEngine (Evaluating progress, local vs structural accommodation)
"""

from __future__ import annotations

import pytest

from schemamath_api.telos_accommodation import TelosAccommodationEngine


class TestTelosAccommodation:
    def test_evaluate_progress_local_and_structural(self):
        engine = TelosAccommodationEngine()

        dec_local = engine.evaluate_progress(
            goal_id="g_101",
            original_objective="Prove Erdős #650",
            consecutive_failures=1,
            stagnation_detected=False,
        )
        assert dec_local.accommodation_type == "LOCAL_REPAIR"
        assert dec_local.objective_anchor_preserved is True

        dec_struct = engine.evaluate_progress(
            goal_id="g_101",
            original_objective="Prove Erdős #650",
            consecutive_failures=4,
            stagnation_detected=True,
        )
        assert dec_struct.accommodation_type == "STRUCTURAL_REFRAME"
        assert len(dec_struct.competing_schemas_generated) == 2
        assert dec_struct.objective_anchor_preserved is True
