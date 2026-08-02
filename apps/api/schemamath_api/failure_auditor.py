"""
Automated Nine Recurrent Failure Mode Auditor (v47.0)

Scans research workflows for the nine failure modes identified in v0.13 AI math literature:
1. Prompt Claim Inflation
2. Target Binding Drift
3. Pseudo-Formalization (via sorry)
4. Unverified Repair
5. Same-Model Auditing Correlation Bias
6. Lost Intermediary Assets
7. Missing Prior Art
8. Unreproducible Build Environment
9. Retrospective Narrative Laundering (NEW in v0.13)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class FailureAuditReport:
    workflow_id: str
    failure_modes_detected: list[str]
    has_pseudo_formalization: bool
    has_same_model_bias: bool
    has_narrative_laundering: bool
    is_audit_passed: bool


class FailureModeAuditor:
    """
    Scans and flags the 9 recurrent failure modes in AI mathematical discovery workflows.
    """

    FAILURE_MODES = [
        "FM1_PROMPT_CLAIM_INFLATION",
        "FM2_TARGET_BINDING_DRIFT",
        "FM3_PSEUDO_FORMALIZATION_VIA_SORRY",
        "FM4_UNVERIFIED_REPAIR",
        "FM5_SAME_MODEL_AUDITING_CORRELATION_BIAS",
        "FM6_LOST_INTERMEDIARY_ASSETS",
        "FM7_MISSING_PRIOR_ART",
        "FM8_UNREPRODUCIBLE_BUILD_ENV",
        "FM9_RETROSPECTIVE_NARRATIVE_LAUNDERING",
    ]

    def audit_workflow(
        self,
        workflow_id: str,
        lean_code: str,
        proposer_model: str,
        auditor_model: str,
        target_drift_detected: bool = False,
        trace_class: str = "FINAL_ONLY_ARTIFACT",
        has_raw_event_stream: bool = True,
        repair_verified: bool = True,
        intermediary_assets_present: bool = True,
        prior_art_checked: bool = True,
        build_env_pinned: bool = True,
        claim_scope_matches_result: bool = True,
    ) -> FailureAuditReport:
        failures: list[str] = []

        # FM1: Prompt Claim Inflation
        if not claim_scope_matches_result:
            failures.append("FM1_PROMPT_CLAIM_INFLATION")

        # FM2: Target Binding Drift
        if target_drift_detected:
            failures.append("FM2_TARGET_BINDING_DRIFT")

        # FM3: Pseudo-Formalization via sorry
        if "sorry" in lean_code:
            failures.append("FM3_PSEUDO_FORMALIZATION_VIA_SORRY")

        # FM4: Unverified Repair
        if not repair_verified:
            failures.append("FM4_UNVERIFIED_REPAIR")

        # FM5: Same-Model Auditing Correlation Bias
        if proposer_model.lower() == auditor_model.lower():
            failures.append("FM5_SAME_MODEL_AUDITING_CORRELATION_BIAS")

        # FM6: Lost Intermediary Assets
        if not intermediary_assets_present:
            failures.append("FM6_LOST_INTERMEDIARY_ASSETS")

        # FM7: Missing Prior Art
        if not prior_art_checked:
            failures.append("FM7_MISSING_PRIOR_ART")

        # FM8: Unreproducible Build Environment
        if not build_env_pinned:
            failures.append("FM8_UNREPRODUCIBLE_BUILD_ENV")

        # FM9: Retrospective Narrative Laundering (v0.13 new)
        # Triggered when trace is a model reconstruction without raw event backing
        if trace_class == "MODEL_RECONSTRUCTION" and not has_raw_event_stream:
            failures.append("FM9_RETROSPECTIVE_NARRATIVE_LAUNDERING")

        is_passed = len(failures) == 0
        logger.info(
            "Audited workflow '%s': detected %d/%d failure modes (passed=%s)",
            workflow_id,
            len(failures),
            len(self.FAILURE_MODES),
            is_passed,
        )
        return FailureAuditReport(
            workflow_id=workflow_id,
            failure_modes_detected=failures,
            has_pseudo_formalization="FM3_PSEUDO_FORMALIZATION_VIA_SORRY" in failures,
            has_same_model_bias="FM5_SAME_MODEL_AUDITING_CORRELATION_BIAS" in failures,
            has_narrative_laundering="FM9_RETROSPECTIVE_NARRATIVE_LAUNDERING" in failures,
            is_audit_passed=is_passed,
        )
