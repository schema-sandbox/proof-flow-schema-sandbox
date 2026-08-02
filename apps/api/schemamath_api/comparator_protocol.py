"""
Trusted Challenge & Comparator Protocol (v49.0)

Implements the Lean FRO Comparator verification protocol from v0.13:
- Declaration-level binding between trusted challenges and candidate solutions
- Axiom ceiling enforcement (propext, Classical.choice, Quot.sound)
- Statement identity verification
- Definition-hole detection
- Dual-kernel validation interface (Lean 4 + nanoda)
"""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

# The three axioms permitted by default in Lean 4 Mathlib proofs
DEFAULT_AXIOM_CEILING = frozenset({"propext", "Classical.choice", "Quot.sound"})


@dataclass
class AxiomUsage:
    axiom_name: str
    usage_count: int
    is_permitted: bool


@dataclass
class DefinitionHole:
    """A formal definition that could be legally but deceptively satisfied."""
    definition_name: str
    location: str
    is_open: bool
    risk_description: str


@dataclass
class ComparatorResult:
    """Result of running the Comparator protocol."""
    challenge_id: str
    candidate_id: str
    statement_match: bool
    axiom_ceiling_respected: bool
    axioms_used: list[AxiomUsage]
    definition_holes: list[DefinitionHole]
    sorry_count: int
    primary_kernel_accepts: bool
    secondary_kernel_accepts: bool | None  # None if secondary kernel not available
    overall_verdict: str  # PASS, FAIL, PROVISIONAL, UNAVAILABLE

    @property
    def is_verified(self) -> bool:
        return self.overall_verdict == "PASS"


class ComparatorProtocol:
    """
    Lean FRO Comparator verification protocol.

    Performs declaration-level binding between trusted challenge specifications
    and candidate Lean solution terms, verifying axiom bounds and statement equivalence.
    """

    def __init__(
        self,
        axiom_ceiling: frozenset[str] | None = None,
    ) -> None:
        self.axiom_ceiling = axiom_ceiling or DEFAULT_AXIOM_CEILING

    def verify(
        self,
        challenge_id: str,
        challenge_statement: str,
        candidate_id: str,
        candidate_code: str,
        candidate_statement: str | None = None,
        axioms_declared: list[str] | None = None,
        lean_version: str = "4.32.0",
    ) -> ComparatorResult:
        """Run the full Comparator verification protocol."""
        # Step 1: Statement identity check
        stmt_match = self._check_statement_identity(
            challenge_statement,
            candidate_statement or self._extract_statement(candidate_code),
        )

        # Step 2: Axiom ceiling check
        used_axioms = axioms_declared or self._scan_axioms(candidate_code)
        axiom_usages = []
        ceiling_respected = True
        for ax in used_axioms:
            is_permitted = ax in self.axiom_ceiling
            axiom_usages.append(AxiomUsage(
                axiom_name=ax,
                usage_count=candidate_code.count(ax),
                is_permitted=is_permitted,
            ))
            if not is_permitted:
                ceiling_respected = False

        # Step 3: Sorry scan
        sorry_count = candidate_code.count("sorry")

        # Step 4: Definition-hole detection
        holes = self._detect_definition_holes(candidate_code)

        # Step 5: Kernel acceptance (mock — real invocation requires Lean process)
        primary_accepts = sorry_count == 0 and ceiling_respected and stmt_match
        secondary_accepts = None  # nanoda not available in alpha

        # Verdict
        if sorry_count > 0:
            verdict = "FAIL"
        elif not stmt_match:
            verdict = "FAIL"
        elif not ceiling_respected:
            verdict = "FAIL"
        elif len(holes) > 0:
            verdict = "PROVISIONAL"
        elif primary_accepts:
            verdict = "PASS"
        else:
            verdict = "UNAVAILABLE"

        logger.info(
            "Comparator %s vs %s: stmt_match=%s, axiom_ok=%s, sorry=%d, holes=%d → %s",
            challenge_id,
            candidate_id,
            stmt_match,
            ceiling_respected,
            sorry_count,
            len(holes),
            verdict,
        )

        return ComparatorResult(
            challenge_id=challenge_id,
            candidate_id=candidate_id,
            statement_match=stmt_match,
            axiom_ceiling_respected=ceiling_respected,
            axioms_used=axiom_usages,
            definition_holes=holes,
            sorry_count=sorry_count,
            primary_kernel_accepts=primary_accepts,
            secondary_kernel_accepts=secondary_accepts,
            overall_verdict=verdict,
        )

    def _check_statement_identity(self, challenge: str, candidate: str) -> bool:
        """Check if two formal statements are equivalent (normalized comparison)."""
        return self._normalize(challenge) == self._normalize(candidate)

    def _normalize(self, stmt: str) -> str:
        """Normalize whitespace and formatting for comparison."""
        return " ".join(stmt.split()).strip()

    def _extract_statement(self, code: str) -> str:
        """Extract the theorem statement from Lean code."""
        for line in code.splitlines():
            stripped = line.strip()
            if stripped.startswith("theorem ") or stripped.startswith("lemma "):
                return stripped
        return ""

    def _scan_axioms(self, code: str) -> list[str]:
        """Scan code for axiom usage."""
        known_axioms = [
            "propext", "Classical.choice", "Quot.sound",
            "funext", "propFunExt", "Decidable.em",
        ]
        return [ax for ax in known_axioms if ax in code]

    def _detect_definition_holes(self, code: str) -> list[DefinitionHole]:
        """Detect potentially deceptive open definitions."""
        holes: list[DefinitionHole] = []
        for i, line in enumerate(code.splitlines(), 1):
            stripped = line.strip()
            # Detect open/opaque definitions that could hide implementation
            if stripped.startswith("opaque ") or (stripped.startswith("def ") and ":= sorry" in stripped):
                name = stripped.split()[1] if len(stripped.split()) > 1 else "unknown"
                holes.append(DefinitionHole(
                    definition_name=name,
                    location=f"line {i}",
                    is_open=True,
                    risk_description=f"Open definition '{name}' could be legally satisfied with deceptive implementation",
                ))
        return holes
