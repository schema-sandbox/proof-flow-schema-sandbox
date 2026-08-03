"""
Tests for ProofFlow v44.0 (Visible Human Labor & Attribution Tracker)

Covers:
    - HumanLaborTracker (L0, L1, L2 labor tier recording & attribution)
"""

from __future__ import annotations

from schemamath_api.human_labor_tracker import HumanLaborTracker


class TestHumanLaborTracker:
    def test_record_labor_tiers(self):
        tracker = HumanLaborTracker()

        rec_l0 = tracker.record_labor("ep_l0")
        assert rec_l0.labor_tier == "L0"
        assert rec_l0.total_human_hours == 0.0

        rec_l1 = tracker.record_labor("ep_l1", curation_hours=2.0, repair_hours=3.0)
        assert rec_l1.labor_tier == "L1"
        assert rec_l1.total_human_hours == 5.0

        rec_l2 = tracker.record_labor("ep_l2", formalization_hours=15.0, manuscript_hours=10.0)
        assert rec_l2.labor_tier == "L2"
        assert rec_l2.total_human_hours == 25.0
