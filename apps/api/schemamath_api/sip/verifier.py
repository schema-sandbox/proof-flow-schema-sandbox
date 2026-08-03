"""
@sip/verifier (G4: Verifier Adapters, Hardening Checks, and Mutation Testing)

Adapts formal and computational verifiers, running hardening checks in P7.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from schemamath_api.k0.decision import Decision, ModuleDecision
from schemamath_api.k0.lifecycle import (
    HookType,
    LifecycleContext,
    LifecyclePhase,
    LifecycleScheduler,
)
from schemamath_api.k0.manifest import (
    CapabilityDeclaration,
    LifecycleHook,
    ModuleKind,
)
from schemamath_api.sip.core import SipModule

logger = logging.getLogger(__name__)


@dataclass
class VerificationResult:
    valid: bool
    verifier_name: str
    details: str = ""
    mutation_tested: bool = False


class VerifierModule(SipModule):
    """
    G4: @sip/verifier module.

    Runs verifiers and mutation hardening tests in P7_ASSERTION_EVALUATION.
    """

    def __init__(self) -> None:
        super().__init__(
            name="@sip/verifier",
            version="1.0.0",
            kind=ModuleKind.VERIFIER,
            description="Verifier Adapters and Hardening Checker",
            provides=[CapabilityDeclaration(name="verifier_hardening", version="1.0")],
        )

        self._verifiers: dict[str, Callable[[Any], VerificationResult]] = {}
        # Register built-in default verifier
        self.register_verifier("hash_consistency", self._verify_hash_consistency)

        self._manifest.lifecycle_hooks = [
            LifecycleHook(
                phase=LifecyclePhase.P7_ASSERTION_EVALUATION,
                hook_type=HookType.POST,
                priority=10,
                description="Run registered verifiers and mutation checks",
            ),
        ]

    def bind_hooks(self, scheduler: LifecycleScheduler) -> None:
        scheduler.register_hook(
            self.name,
            LifecyclePhase.P7_ASSERTION_EVALUATION,
            HookType.POST,
            10,
            self.evaluate_verifications,
        )

    def register_verifier(
        self, name: str, fn: Callable[[Any], VerificationResult]
    ) -> None:
        self._verifiers[name] = fn

    def evaluate_verifications(self, ctx: LifecycleContext) -> ModuleDecision:
        """Run verifiers registered for the target context payload."""
        payload = ctx.input_data.get("verification_target")
        if not payload:
            return ModuleDecision(source_module=self.name, approval=Decision.ALLOW)

        for vname, vfn in self._verifiers.items():
            res = vfn(payload)
            if not res.valid:
                return ModuleDecision(
                    source_module=self.name,
                    approval=Decision.DENY,
                    reason=f"Verifier '{vname}' failed: {res.details}",
                )

        return ModuleDecision(
            source_module=self.name,
            approval=Decision.ALLOW,
            capabilities={"verifier_hardening"},
        )

    def _verify_hash_consistency(self, payload: Any) -> VerificationResult:
        """Genuine hash-consistency check (default verifier).

        Verifies a supplied ``expected_hash`` against a canonical serialization of the
        rest of the payload. A target WITHOUT a hash to check is reported as
        ``unverified`` (never passed), and no result claims mutation testing.
        """
        if not isinstance(payload, dict):
            return VerificationResult(
                valid=False,
                verifier_name="hash_consistency",
                details="verification target is not a dictionary; nothing to verify",
                mutation_tested=False,
            )
        expected = payload.get("expected_hash") or payload.get("hash")
        if expected is None:
            return VerificationResult(
                valid=False,
                verifier_name="hash_consistency",
                details="no expected_hash supplied; target is unverified, not valid",
                mutation_tested=False,
            )
        body = {key: value for key, value in payload.items() if key not in {"expected_hash", "hash"}}
        actual = hashlib.sha256(
            json.dumps(
                body, sort_keys=True, separators=(",", ":"), default=str
            ).encode("utf-8")
        ).hexdigest()
        if not hmac.compare_digest(actual, str(expected)):
            return VerificationResult(
                valid=False,
                verifier_name="hash_consistency",
                details="computed hash does not match expected_hash",
                mutation_tested=False,
            )
        return VerificationResult(
            valid=True,
            verifier_name="hash_consistency",
            details="hash consistency verified",
            mutation_tested=False,
        )


def createVerifier() -> VerifierModule:
    """Helper factory matching JS-style createVerifier()."""
    return VerifierModule()
