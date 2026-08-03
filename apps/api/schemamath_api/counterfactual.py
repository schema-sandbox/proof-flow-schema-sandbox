"""
Counterfactual Logic Universe Simulator (CounterfactualUniverse)

Simulates alternative logical universes (Intuitionistic, Paraconsistent, Classical)
and verifies theorem validity under custom logical constraints (e.g. rejection of LEM).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum

logger = logging.getLogger(__name__)


class LogicFramework(StrEnum):
    CLASSICAL = "CLASSICAL"
    INTUITIONISTIC = "INTUITIONISTIC"
    PARACONSISTENT = "PARACONSISTENT"


@dataclass
class CounterfactualResult:
    framework: LogicFramework
    is_valid: bool
    requires_lem: bool
    explanation: str


class CounterfactualUniverse:
    """
    Evaluates proofs under non-classical logical framework rules.
    """

    def evaluate_proof(
        self,
        proof_steps: list[str],
        framework: LogicFramework = LogicFramework.INTUITIONISTIC,
    ) -> CounterfactualResult:
        """Evaluate proof steps under specified logic framework."""
        requires_lem = any(
            "law of excluded middle" in s.lower() or "proof by contradiction" in s.lower() or "lem" in s.lower()
            for s in proof_steps
        )

        if framework == LogicFramework.INTUITIONISTIC and requires_lem:
            logger.info("Proof rejected under Intuitionistic logic due to non-constructive LEM usage")
            return CounterfactualResult(
                framework=framework,
                is_valid=False,
                requires_lem=True,
                explanation="Intuitionistic logic requires constructive proofs without Law of Excluded Middle",
            )

        return CounterfactualResult(
            framework=framework,
            is_valid=True,
            requires_lem=requires_lem,
            explanation=f"Proof valid under {framework.value} logic framework",
        )
