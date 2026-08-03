import pytest
from pydantic import ValidationError
from schemamath_api.k0.decision import (
    Decision,
    DecisionMerger,
    MergedDecision,
    ModuleDecision,
    RiskLevel,
    decision_priority,
    more_restrictive,
)


def _make_decision(source: str = "test_mod", approval: Decision = Decision.ALLOW, **kwargs) -> ModuleDecision:
    """Helper to concisely create a ModuleDecision for testing."""
    return ModuleDecision(source_module=source, approval=approval, **kwargs)


class TestDecisionEnum:
    def test_decision_values(self):
        """Test that all 5 values exist."""
        assert Decision.ALLOW == "allow"
        assert Decision.REQUIRE_EVIDENCE == "require_evidence"
        assert Decision.DEFER == "defer"
        assert Decision.REQUIRE_HUMAN == "require_human"
        assert Decision.DENY == "deny"
        assert len(list(Decision)) == 5

    def test_decision_priority(self):
        """Test that priority ordering is correct."""
        assert decision_priority(Decision.ALLOW) == 0
        assert decision_priority(Decision.REQUIRE_EVIDENCE) == 1
        assert decision_priority(Decision.DEFER) == 2
        assert decision_priority(Decision.REQUIRE_HUMAN) == 3
        assert decision_priority(Decision.DENY) == 4

    def test_more_restrictive(self):
        """Test returning the more restrictive of two decisions."""
        assert more_restrictive(Decision.ALLOW, Decision.ALLOW) == Decision.ALLOW
        assert more_restrictive(Decision.ALLOW, Decision.DENY) == Decision.DENY
        assert more_restrictive(Decision.DENY, Decision.ALLOW) == Decision.DENY
        assert more_restrictive(Decision.REQUIRE_EVIDENCE, Decision.DEFER) == Decision.DEFER
        assert more_restrictive(Decision.REQUIRE_HUMAN, Decision.REQUIRE_EVIDENCE) == Decision.REQUIRE_HUMAN
        assert more_restrictive(Decision.DENY, Decision.REQUIRE_HUMAN) == Decision.DENY


class TestRiskLevelEnum:
    def test_risk_level_values(self):
        """Test that all RiskLevel values exist and have correct integers."""
        assert RiskLevel.NONE == 0
        assert RiskLevel.LOW == 25
        assert RiskLevel.MEDIUM == 50
        assert RiskLevel.HIGH == 75
        assert RiskLevel.CRITICAL == 100
        assert len(list(RiskLevel)) == 5


class TestModuleDecision:
    def test_creation_defaults(self):
        """Test ModuleDecision creation with just the required source_module."""
        md = ModuleDecision(source_module="mod_a")
        assert md.source_module == "mod_a"
        assert md.approval == Decision.DEFER
        assert md.reason == ""
        assert md.capabilities == set()
        assert md.risk_level == RiskLevel.NONE
        assert md.risk_factors == []
        assert md.required_evidence == set()
        assert md.assertion_ceiling == 100
        assert md.metadata == {}

    def test_creation_all_fields(self):
        """Test ModuleDecision creation with all fields provided."""
        md = ModuleDecision(
            source_module="mod_b",
            approval=Decision.REQUIRE_EVIDENCE,
            reason="Needs more info",
            capabilities={"read", "write"},
            risk_level=RiskLevel.MEDIUM,
            risk_factors=["factor1"],
            required_evidence={"id_scan"},
            assertion_ceiling=90,
            metadata={"key": "val"},
        )
        assert md.approval == Decision.REQUIRE_EVIDENCE
        assert md.reason == "Needs more info"
        assert md.capabilities == {"read", "write"}
        assert md.risk_level == RiskLevel.MEDIUM
        assert md.risk_factors == ["factor1"]
        assert md.required_evidence == {"id_scan"}
        assert md.assertion_ceiling == 90
        assert md.metadata == {"key": "val"}

    def test_frozen_immutability(self):
        """Test that ModuleDecision is frozen and immutable."""
        md = ModuleDecision(source_module="mod_a")
        with pytest.raises(ValidationError):
            md.approval = Decision.ALLOW


class TestMergedDecision:
    def test_properties(self):
        """Test properties for various MergedDecision states."""
        # ALLOW
        md_allow = MergedDecision(approval=Decision.ALLOW)
        assert md_allow.is_approved is True
        assert md_allow.needs_evidence is False
        assert md_allow.needs_human is False
        assert md_allow.is_denied is False

        # REQUIRE_EVIDENCE
        md_ev = MergedDecision(approval=Decision.REQUIRE_EVIDENCE)
        assert md_ev.is_approved is False
        assert md_ev.needs_evidence is True
        assert md_ev.needs_human is False
        assert md_ev.is_denied is False

        # ALLOW but needs evidence
        md_allow_ev = MergedDecision(approval=Decision.ALLOW, all_required_evidence={"id_scan"})
        assert md_allow_ev.is_approved is True
        assert md_allow_ev.needs_evidence is True
        assert md_allow_ev.needs_human is False
        assert md_allow_ev.is_denied is False

        # REQUIRE_HUMAN
        md_human = MergedDecision(approval=Decision.REQUIRE_HUMAN)
        assert md_human.is_approved is False
        assert md_human.needs_evidence is False
        assert md_human.needs_human is True
        assert md_human.is_denied is False

        # DENY
        md_deny = MergedDecision(approval=Decision.DENY)
        assert md_deny.is_approved is False
        assert md_deny.needs_evidence is False
        assert md_deny.needs_human is False
        assert md_deny.is_denied is True


class TestDecisionMergerMerge:
    def setup_method(self):
        self.merger = DecisionMerger()

    def test_single_allow(self):
        res = self.merger.merge([_make_decision(approval=Decision.ALLOW)])
        assert res.approval == Decision.ALLOW

    def test_single_deny(self):
        res = self.merger.merge([_make_decision(approval=Decision.DENY)])
        assert res.approval == Decision.DENY

    def test_allow_plus_deny(self):
        res = self.merger.merge([
            _make_decision(approval=Decision.ALLOW),
            _make_decision(approval=Decision.DENY)
        ])
        assert res.approval == Decision.DENY

    def test_allow_plus_require_human(self):
        res = self.merger.merge([
            _make_decision(approval=Decision.ALLOW),
            _make_decision(approval=Decision.REQUIRE_HUMAN)
        ])
        assert res.approval == Decision.REQUIRE_HUMAN

    def test_allow_plus_require_evidence(self):
        res = self.merger.merge([
            _make_decision(approval=Decision.ALLOW),
            _make_decision(approval=Decision.REQUIRE_EVIDENCE)
        ])
        assert res.approval == Decision.REQUIRE_EVIDENCE

    def test_multiple_allows(self):
        res = self.merger.merge([
            _make_decision(approval=Decision.ALLOW),
            _make_decision(approval=Decision.ALLOW),
            _make_decision(approval=Decision.ALLOW)
        ])
        assert res.approval == Decision.ALLOW

    def test_deny_overrides_everything(self):
        res = self.merger.merge([
            _make_decision(approval=Decision.ALLOW),
            _make_decision(approval=Decision.REQUIRE_EVIDENCE),
            _make_decision(approval=Decision.REQUIRE_HUMAN),
            _make_decision(approval=Decision.DENY),
        ])
        assert res.approval == Decision.DENY

    def test_defer_is_ignored(self):
        res = self.merger.merge([
            _make_decision(approval=Decision.ALLOW),
            _make_decision(approval=Decision.DEFER),
        ])
        assert res.approval == Decision.ALLOW

    def test_all_defer(self):
        res = self.merger.merge([
            _make_decision(approval=Decision.DEFER),
            _make_decision(approval=Decision.DEFER),
        ])
        assert res.approval == Decision.DENY  # default_on_empty

    def test_empty_list(self):
        res = self.merger.merge([])
        assert res.approval == Decision.DENY  # default_on_empty
        assert "defaulting to deny" in res.denial_reasons[0]

    def test_capability_intersection(self):
        res = self.merger.merge([
            _make_decision(capabilities={"a", "b", "c"}),
            _make_decision(capabilities={"b", "c", "d"}),
            _make_decision(capabilities={"c", "e"}),
        ])
        assert res.effective_capabilities == {"c"}

    def test_capability_intersection_empty(self):
        res = self.merger.merge([
            _make_decision(capabilities={"a"}),
            _make_decision(capabilities={"b"}),
        ])
        assert res.effective_capabilities == set()
        
    def test_risk_maximum(self):
        res = self.merger.merge([
            _make_decision(risk_level=RiskLevel.LOW),
            _make_decision(risk_level=RiskLevel.HIGH),
            _make_decision(risk_level=RiskLevel.MEDIUM),
        ])
        assert res.effective_risk == RiskLevel.HIGH

    def test_evidence_union(self):
        res = self.merger.merge([
            _make_decision(required_evidence={"doc1"}),
            _make_decision(required_evidence={"doc2", "doc3"}),
            _make_decision(required_evidence={"doc1", "doc4"}),
        ])
        assert res.all_required_evidence == {"doc1", "doc2", "doc3", "doc4"}

    def test_assertion_ceiling_minimum(self):
        res = self.merger.merge([
            _make_decision(assertion_ceiling=100),
            _make_decision(assertion_ceiling=80),
            _make_decision(assertion_ceiling=90),
        ])
        assert res.assertion_ceiling == 80

    def test_audit_trail_denial_reasons(self):
        res = self.merger.merge([
            _make_decision(source="m1", approval=Decision.DENY, reason="Rule 1 failed"),
            _make_decision(source="m2", approval=Decision.ALLOW, reason="All good"),
            _make_decision(source="m3", approval=Decision.REQUIRE_HUMAN, reason="Needs review"),
        ])
        assert res.denial_reasons == ["[m1] Rule 1 failed", "[m3] Needs review"]

    def test_audit_trail_all_risk_factors(self):
        res = self.merger.merge([
            _make_decision(risk_factors=["r1", "r2"]),
            _make_decision(risk_factors=["r3"]),
            _make_decision(risk_factors=[]),
        ])
        assert res.all_risk_factors == ["r1", "r2", "r3"]


class TestDecisionMergerMergeApprovalsOnly:
    def setup_method(self):
        self.merger = DecisionMerger()

    def test_merge_approvals_only(self):
        # Empty list
        assert self.merger.merge_approvals_only([]) == Decision.DENY
        # All DEFER
        assert self.merger.merge_approvals_only([
            _make_decision(approval=Decision.DEFER)
        ]) == Decision.DENY
        # ALLOW + DEFER
        assert self.merger.merge_approvals_only([
            _make_decision(approval=Decision.ALLOW),
            _make_decision(approval=Decision.DEFER)
        ]) == Decision.ALLOW
        # Mixed
        assert self.merger.merge_approvals_only([
            _make_decision(approval=Decision.ALLOW),
            _make_decision(approval=Decision.REQUIRE_EVIDENCE),
            _make_decision(approval=Decision.DENY)
        ]) == Decision.DENY


class TestDecisionMergerCustomDefault:
    def test_custom_default_on_empty(self):
        merger = DecisionMerger(default_on_empty=Decision.ALLOW)
        
        # Empty list
        res = merger.merge([])
        assert res.approval == Decision.ALLOW
        
        # All DEFER
        res = merger.merge([_make_decision(approval=Decision.DEFER)])
        assert res.approval == Decision.ALLOW
        
        # merge_approvals_only
        assert merger.merge_approvals_only([]) == Decision.ALLOW
        assert merger.merge_approvals_only([_make_decision(approval=Decision.DEFER)]) == Decision.ALLOW
