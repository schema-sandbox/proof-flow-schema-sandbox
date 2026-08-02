"""
Axiom System Inconsistency & Contradiction Detector (InconsistencyDetector)

Detects logical contradictions (P ∧ ¬P) or trivializing Principle of Explosion traps
within candidate axiom frameworks.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class InconsistencyReport:
    has_contradiction: bool
    contradictory_axioms: list[str]
    is_trivialized: bool


class InconsistencyDetector:
    """
    Detects logical contradictions and trivializing inconsistencies in axiom sets.
    """

    def check_consistency(self, axioms: list[str]) -> InconsistencyReport:
        """Check a list of axiom statements for logical contradictions."""
        contradictions: list[str] = []

        # Detect direct P and NOT P pattern
        for ax1 in axioms:
            for ax2 in axioms:
                if f"not {ax1.lower()}" == ax2.lower() or f"¬({ax1})" in ax2:
                    contradictions.append(f"{ax1} vs {ax2}")

        has_bad = len(contradictions) > 0
        return InconsistencyReport(
            has_contradiction=has_bad,
            contradictory_axioms=contradictions,
            is_trivialized=has_bad,
        )
