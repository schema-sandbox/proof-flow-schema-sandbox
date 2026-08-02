"""
Tests for ProofFlow v43.0 (Automated Eight Recurrent Failure Mode Auditor)

Covers:
    - FailureModeAuditor (Auditing pseudo-formalization & same-model bias)
"""

from __future__ import annotations

import pytest

from schemamath_api.failure_auditor import FailureModeAuditor


class TestFailureAuditor:
    def test_audit_workflow(self):
        auditor = FailureModeAuditor()
        res_fail = auditor.audit_workflow(
            workflow_id="wf_101",
            lean_code="theorem test : False := by sorry",
            proposer_model="GPT-5.6-Pro",
            auditor_model="GPT-5.6-Pro",
        )

        assert res_fail.is_audit_passed is False
        assert res_fail.has_pseudo_formalization is True
        assert res_fail.has_same_model_bias is True
        assert len(res_fail.failure_modes_detected) == 2

        res_pass = auditor.audit_workflow(
            workflow_id="wf_102",
            lean_code="theorem test : True := by trivial",
            proposer_model="GPT-5.6-Pro",
            auditor_model="Claude-3.5-Sonnet",
        )
        assert res_pass.is_audit_passed is True
        assert len(res_pass.failure_modes_detected) == 0
