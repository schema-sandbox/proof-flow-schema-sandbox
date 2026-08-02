"""
Tests for ProofFlow v21.10 (EpistemicSynthesisCore)

Covers:
    - EpistemicSynthesisCore (Consolidation of v21.1 through v21.10 modules)
"""

from __future__ import annotations

import pytest

from schemamath_api.synthesis_core import EpistemicSynthesisCore


class TestEpistemicSynthesisCore:
    def test_get_synthesis_status(self):
        core = EpistemicSynthesisCore()
        status = core.get_synthesis_status()

        assert status.version == "21.10"
        assert status.consolidated_minor_modules == 10
        assert status.all_systems_operational is True
        assert status.synthesis_resonance_index == 1.0
