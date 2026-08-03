"""
Self-Healing Formal Verifier Protocol (SelfHealingVerifierProtocol)

Automatically repairs broken formal proof scripts (Lean4 / Z3) by generating tactic
mutations and re-running formal verification loop until proof passes.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from schemamath_api.sip.verifier import VerificationResult
from schemamath_api.verifiers import Lean4Adapter, Lean4VerificationRequest

logger = logging.getLogger(__name__)


@dataclass
class HealingResult:
    repaired: bool
    repaired_code: str
    attempts: int
    final_verification: VerificationResult


class SelfHealingVerifierProtocol:
    """
    Self-healing protocol for Lean4 / Z3 formal proof scripts.
    """

    def __init__(self, lean_adapter: Lean4Adapter | None = None) -> None:
        self.adapter = lean_adapter or Lean4Adapter()
        self.tactic_replacements = [
            ("sorry", "decide"),
            ("simp", "simp [Nat.add_comm]"),
            ("rfl", "decide"),
        ]

    def heal_proof_script(
        self,
        broken_code: str,
        max_attempts: int = 3,
    ) -> HealingResult:
        """Attempt to repair broken Lean4 proof script by applying tactic mutations."""
        req = Lean4VerificationRequest(code=broken_code)
        res = self.adapter.verify_theorem(req)

        if res.valid:
            return HealingResult(
                repaired=True,
                repaired_code=broken_code,
                attempts=1,
                final_verification=res,
            )

        current_code = broken_code
        for attempt in range(1, max_attempts + 1):
            # Mutate tactic code
            for old_tactic, new_tactic in self.tactic_replacements:
                if old_tactic in current_code:
                    current_code = current_code.replace(old_tactic, new_tactic, 1)
                    break

            req = Lean4VerificationRequest(code=current_code)
            res = self.adapter.verify_theorem(req)

            if res.valid:
                logger.info("Proof script repaired on attempt %d", attempt + 1)
                return HealingResult(
                    repaired=True,
                    repaired_code=current_code,
                    attempts=attempt + 1,
                    final_verification=res,
                )

        return HealingResult(
            repaired=False,
            repaired_code=broken_code,
            attempts=max_attempts,
            final_verification=res,
        )
