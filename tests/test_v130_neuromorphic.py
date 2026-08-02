"""
Tests for ProofFlow v13.0.0 (NeuromorphicAccelerator, MicroTacticCache)

Covers:
    - NeuromorphicAccelerator (SNN spike hardware acceleration)
    - MicroTacticCache (Sub-millisecond tactic completion cache)
"""

from __future__ import annotations

import pytest

from schemamath_api.neuromorphic import MicroTacticCache, NeuromorphicAccelerator


class TestNeuromorphicAccelerator:
    def test_accelerate_tactic_search(self):
        acc = NeuromorphicAccelerator()
        res = acc.accelerate_tactic_search("goal: x + y = y + x")

        assert res.accelerated is True
        assert res.spike_count > 0
        assert res.latency_ns == 450


class TestMicroTacticCache:
    def test_get_or_store(self):
        cache = MicroTacticCache()
        item1 = cache.get_or_store("goal_1", "by ring")
        assert item1.hit_count == 1
        assert item1.tactic_code == "by ring"

        item2 = cache.get_or_store("goal_1", "by ring")
        assert item2.hit_count == 2
