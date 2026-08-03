"""Tests for Cost Tracker (v50.0)."""

from schemamath_api.cost_tracker import CostTracker


class TestCostTracker:
    def test_empty_report(self):
        t = CostTracker()
        r = t.generate_report("ep1")
        assert r.discovery_token_cost_usd == 0.0
        assert r.lifecycle_cost_usd == 0.0
        assert r.total_tokens == 0
        assert r.total_human_hours == 0.0

    def test_token_cost_only(self):
        t = CostTracker()
        t.record_token_cost("o3", "search", 10000, 5000, 0.50)
        t.record_token_cost("o3", "repair", 8000, 3000, 0.35)
        r = t.generate_report("ep2")
        assert r.discovery_token_cost_usd == 0.85
        assert r.total_tokens == 26000
        assert r.by_model["o3"] == 0.85

    def test_human_cost_only(self):
        t = CostTracker()
        t.record_human_cost("alice", "L2", 40.0, "formalization")
        r = t.generate_report("ep3", hourly_rate_usd=150.0)
        assert r.total_human_hours == 40.0
        assert r.lifecycle_cost_usd == 6000.0
        assert r.discovery_token_cost_usd == 0.0

    def test_combined_costs(self):
        t = CostTracker()
        t.record_token_cost("o3", "search", 100000, 50000, 2000.0)
        t.record_human_cost("bob", "L2", 160.0, "formalization")
        t.record_human_cost("alice", "L1", 8.0, "review")
        r = t.generate_report("ep4", hourly_rate_usd=100.0)
        assert r.discovery_token_cost_usd == 2000.0
        assert r.lifecycle_cost_usd == 2000.0 + 16800.0
        assert r.total_human_hours == 168.0

    def test_cost_ratio(self):
        t = CostTracker()
        t.record_token_cost("o3", "search", 100000, 50000, 2000.0)
        t.record_human_cost("team", "L2", 4980.0, "everything_else")
        r = t.generate_report("ep5", hourly_rate_usd=100.0)
        # ratio = 2000 / (2000 + 498000) = 0.004
        assert r.cost_ratio < 0.01
        assert r.is_cost_compressed

    def test_not_cost_compressed(self):
        t = CostTracker()
        t.record_token_cost("model", "search", 1000, 500, 50.0)
        t.record_human_cost("dev", "L1", 1.0, "review")
        r = t.generate_report("ep6", hourly_rate_usd=100.0)
        assert not r.is_cost_compressed

    def test_by_phase_aggregation(self):
        t = CostTracker()
        t.record_token_cost("o3", "search", 10000, 5000, 1.0)
        t.record_token_cost("claude", "search", 8000, 4000, 0.8)
        t.record_token_cost("o3", "verification", 5000, 2000, 0.5)
        r = t.generate_report("ep7")
        assert r.by_phase["search"] == 1.8
        assert r.by_phase["verification"] == 0.5

    def test_by_model_aggregation(self):
        t = CostTracker()
        t.record_token_cost("o3", "search", 10000, 5000, 1.0)
        t.record_token_cost("claude", "search", 8000, 4000, 0.8)
        t.record_token_cost("o3", "repair", 5000, 2000, 0.5)
        r = t.generate_report("ep8")
        assert r.by_model["o3"] == 1.5
        assert r.by_model["claude"] == 0.8

    def test_reset(self):
        t = CostTracker()
        t.record_token_cost("m", "p", 100, 50, 0.01)
        t.record_human_cost("a", "L0", 1.0, "x")
        t.reset()
        r = t.generate_report("reset_ep")
        assert r.total_tokens == 0
        assert r.total_human_hours == 0.0

    def test_record_returns_entry(self):
        t = CostTracker()
        te = t.record_token_cost("m", "p", 100, 50, 0.01)
        assert te.model_id == "m"
        he = t.record_human_cost("a", "L1", 2.0, "review")
        assert he.labor_tier == "L1"

    def test_multiple_human_activities(self):
        t = CostTracker()
        t.record_human_cost("a", "L2", 10.0, "formalization")
        t.record_human_cost("b", "L1", 5.0, "review")
        t.record_human_cost("a", "L2", 20.0, "manuscript")
        r = t.generate_report("ep9")
        assert r.total_human_hours == 35.0
        assert len(r.human_entries) == 3
