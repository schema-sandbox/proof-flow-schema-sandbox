"""Tests for Campaign Auditor & updated Failure Auditor (v47.0)."""

from schemamath_api.campaign_auditor import CampaignAuditor
from schemamath_api.failure_auditor import FailureModeAuditor


class TestFailureModeAuditorV47:
    """Tests for the upgraded 9-mode failure auditor."""

    def test_clean_workflow_passes(self):
        auditor = FailureModeAuditor()
        report = auditor.audit_workflow(
            workflow_id="w1",
            lean_code="theorem x : True := trivial",
            proposer_model="gpt-4o",
            auditor_model="claude-4",
        )
        assert report.is_audit_passed
        assert len(report.failure_modes_detected) == 0

    def test_sorry_triggers_fm3(self):
        auditor = FailureModeAuditor()
        report = auditor.audit_workflow(
            workflow_id="w2",
            lean_code="theorem x : True := sorry",
            proposer_model="gpt-4o",
            auditor_model="claude-4",
        )
        assert "FM3_PSEUDO_FORMALIZATION_VIA_SORRY" in report.failure_modes_detected
        assert report.has_pseudo_formalization

    def test_same_model_triggers_fm5(self):
        auditor = FailureModeAuditor()
        report = auditor.audit_workflow(
            workflow_id="w3",
            lean_code="theorem x : True := trivial",
            proposer_model="gpt-4o",
            auditor_model="GPT-4o",
        )
        assert "FM5_SAME_MODEL_AUDITING_CORRELATION_BIAS" in report.failure_modes_detected
        assert report.has_same_model_bias

    def test_narrative_laundering_fm9(self):
        auditor = FailureModeAuditor()
        report = auditor.audit_workflow(
            workflow_id="w4",
            lean_code="theorem x : True := trivial",
            proposer_model="gpt-4o",
            auditor_model="claude-4",
            trace_class="MODEL_RECONSTRUCTION",
            has_raw_event_stream=False,
        )
        assert "FM9_RETROSPECTIVE_NARRATIVE_LAUNDERING" in report.failure_modes_detected
        assert report.has_narrative_laundering

    def test_narrative_laundering_not_triggered_with_raw_stream(self):
        auditor = FailureModeAuditor()
        report = auditor.audit_workflow(
            workflow_id="w5",
            lean_code="theorem x : True := trivial",
            proposer_model="gpt-4o",
            auditor_model="claude-4",
            trace_class="MODEL_RECONSTRUCTION",
            has_raw_event_stream=True,
        )
        assert "FM9_RETROSPECTIVE_NARRATIVE_LAUNDERING" not in report.failure_modes_detected

    def test_all_nine_modes_detectable(self):
        auditor = FailureModeAuditor()
        report = auditor.audit_workflow(
            workflow_id="w6",
            lean_code="sorry error",
            proposer_model="gpt-4o",
            auditor_model="gpt-4o",
            target_drift_detected=True,
            trace_class="MODEL_RECONSTRUCTION",
            has_raw_event_stream=False,
            repair_verified=False,
            intermediary_assets_present=False,
            prior_art_checked=False,
            build_env_pinned=False,
            claim_scope_matches_result=False,
        )
        assert len(report.failure_modes_detected) == 9
        assert not report.is_audit_passed

    def test_nine_failure_mode_constants_exist(self):
        assert len(FailureModeAuditor.FAILURE_MODES) == 9

    def test_target_drift_fm2(self):
        auditor = FailureModeAuditor()
        report = auditor.audit_workflow(
            workflow_id="w7",
            lean_code="theorem x : True := trivial",
            proposer_model="a",
            auditor_model="b",
            target_drift_detected=True,
        )
        assert "FM2_TARGET_BINDING_DRIFT" in report.failure_modes_detected

    def test_unverified_repair_fm4(self):
        auditor = FailureModeAuditor()
        report = auditor.audit_workflow(
            workflow_id="w8",
            lean_code="theorem x : True := trivial",
            proposer_model="a",
            auditor_model="b",
            repair_verified=False,
        )
        assert "FM4_UNVERIFIED_REPAIR" in report.failure_modes_detected

    def test_unreproducible_env_fm8(self):
        auditor = FailureModeAuditor()
        report = auditor.audit_workflow(
            workflow_id="w9",
            lean_code="theorem x : True := trivial",
            proposer_model="a",
            auditor_model="b",
            build_env_pinned=False,
        )
        assert "FM8_UNREPRODUCIBLE_BUILD_ENV" in report.failure_modes_detected


class TestCampaignAuditor:
    """Tests for 6 single-campaign audit hazards."""

    def test_clean_campaign(self):
        auditor = CampaignAuditor()
        report = auditor.audit_campaign(
            campaign_id="c1",
            result_families=["algebra", "geometry", "topology"],
        )
        assert report.is_clean
        assert report.hazard_count == 0
        assert report.result_family_count == 3

    def test_h1_counting_inflation(self):
        auditor = CampaignAuditor()
        report = auditor.audit_campaign(
            campaign_id="c2",
            result_families=["algebra", "algebra", "geometry"],
        )
        assert any(h.hazard_id == "H1_RESULT_FAMILY_COUNTING" for h in report.hazards_detected)

    def test_h2_cross_dependence(self):
        auditor = CampaignAuditor()
        report = auditor.audit_campaign(
            campaign_id="c3",
            result_families=["a", "b"],
            shared_dependencies=[("a", "b"), ("b", "a")],
        )
        assert any(h.hazard_id == "H2_CROSS_RESULT_DEPENDENCE" for h in report.hazards_detected)

    def test_h3_trace_coherence_gap(self):
        auditor = CampaignAuditor()
        report = auditor.audit_campaign(
            campaign_id="c4",
            result_families=["x"],
            trace_derivation_class="MODEL_RECONSTRUCTION",
        )
        assert any(h.hazard_id == "H3_TRACE_COHERENCE_GAP" for h in report.hazards_detected)

    def test_h4_artifact_triangulation(self):
        auditor = CampaignAuditor()
        report = auditor.audit_campaign(
            campaign_id="c5",
            result_families=["x"],
            artifact_producers=["openai", "openai", "openai"],
        )
        assert any(h.hazard_id == "H4_ARTIFACT_TRIANGULATION" for h in report.hazards_detected)

    def test_h5_challenge_laundering(self):
        auditor = CampaignAuditor()
        report = auditor.audit_campaign(
            campaign_id="c6",
            result_families=["x"],
            challenge_definitions_audited=False,
        )
        assert any(h.hazard_id == "H5_CHALLENGE_LAUNDERING" for h in report.hazards_detected)
        assert report.hazards_detected[0].severity == "CRITICAL"

    def test_h6_cost_compression(self):
        auditor = CampaignAuditor()
        report = auditor.audit_campaign(
            campaign_id="c7",
            result_families=["x"],
            reported_discovery_cost=2000.0,
            estimated_lifecycle_cost=500000.0,
        )
        assert any(h.hazard_id == "H6_COST_COMPRESSION" for h in report.hazards_detected)

    def test_h6_no_trigger_when_ratio_above_threshold(self):
        auditor = CampaignAuditor()
        report = auditor.audit_campaign(
            campaign_id="c8",
            result_families=["x"],
            reported_discovery_cost=5000.0,
            estimated_lifecycle_cost=10000.0,
        )
        assert not any(h.hazard_id == "H6_COST_COMPRESSION" for h in report.hazards_detected)

    def test_multiple_hazards_combined(self):
        auditor = CampaignAuditor()
        report = auditor.audit_campaign(
            campaign_id="c9",
            result_families=["a", "a"],
            trace_derivation_class="HUMAN_SYNTHESIS",
            challenge_definitions_audited=False,
        )
        assert report.hazard_count >= 3
        assert not report.is_clean
