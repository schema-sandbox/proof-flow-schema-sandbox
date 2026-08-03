"""
@sip/telos (G1: Goal Anchoring, Drift Detection, and Stagnation Alerts)

Anchors operations to explicit goals and non-goals, detects goal drift in P2,
and emits stagnation alerts when equivalent operations repeat endlessly.

Usage:
    telos_mod = TelosModule(
        goal="Analyze competitor pricing strategy",
        non_goals=["Do not modify production database", "Do not send emails"],
        max_equivalent_retries=3,
    )
"""

from __future__ import annotations

import hashlib
import json
import logging
from collections.abc import Sequence
from dataclasses import dataclass

from schemamath_api.k0.decision import Decision, ModuleDecision, RiskLevel
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
class StagnationConfig:
    max_equivalent_retries: int = 3
    window_steps: int = 10


class TelosModule(SipModule):
    """
    G1: @sip/telos module.

    Goal anchoring & drift detection in P2_GOAL_BINDING.
    """

    def __init__(
        self,
        goal: str = "",
        non_goals: Sequence[str] | None = None,
        max_equivalent_retries: int = 3,
        window_steps: int = 10,
    ) -> None:
        super().__init__(
            name="@sip/telos",
            version="1.0.0",
            kind=ModuleKind.GATE,
            description="Goal Anchoring, Drift Detection, and Stagnation Guard",
            provides=[CapabilityDeclaration(name="goal_anchoring", version="1.0")],
            requires=[CapabilityDeclaration(name="schema_validation", version="1.0")],
        )

        self.goal = goal
        self.non_goals = list(non_goals or [])
        self.stagnation_config = StagnationConfig(
            max_equivalent_retries=max_equivalent_retries,
            window_steps=window_steps,
        )
        self._action_history: list[str] = []

        self._manifest.lifecycle_hooks = [
            LifecycleHook(
                phase=LifecyclePhase.P2_GOAL_BINDING,
                hook_type=HookType.PRE,
                priority=10,
                description="Anchor operation to goal and check drift/stagnation",
            ),
        ]

    def bind_hooks(self, scheduler: LifecycleScheduler) -> None:
        scheduler.register_hook(
            self.name,
            LifecyclePhase.P2_GOAL_BINDING,
            HookType.PRE,
            10,
            self.evaluate_goal_binding,
        )

    def evaluate_goal_binding(self, ctx: LifecycleContext) -> ModuleDecision:
        """Evaluate operation against non-goals and stagnation rules."""
        # 1. Non-goal drift check
        op_text = f"{ctx.operation} {json.dumps(ctx.input_data, default=str)}".lower()
        for non_goal in self.non_goals:
            ng_lower = non_goal.lower()
            if ng_lower in op_text or any(word in op_text for word in ng_lower.split() if len(word) > 4):
                return ModuleDecision(
                    source_module=self.name,
                    approval=Decision.DENY,
                    reason=f"Goal drift detected: operation violates non-goal '{non_goal}'",
                    risk_level=RiskLevel.HIGH,
                    risk_factors=["Operation matched explicit non-goal pattern"],
                )

        # 2. Stagnation check
        fingerprint = hashlib.sha256(
            f"{ctx.operation}:{json.dumps(ctx.input_data, sort_keys=True, default=str)}".encode()
        ).hexdigest()

        self._action_history.append(fingerprint)
        recent = self._action_history[-self.stagnation_config.window_steps :]
        consecutive_repeats = 0

        for item in reversed(recent):
            if item == fingerprint:
                consecutive_repeats += 1
            else:
                break

        if consecutive_repeats >= self.stagnation_config.max_equivalent_retries:
            return ModuleDecision(
                source_module=self.name,
                approval=Decision.REQUIRE_HUMAN,
                reason=(
                    f"Stagnation detected: operation '{ctx.operation}' "
                    f"repeated {consecutive_repeats} consecutive times without state change"
                ),
                risk_level=RiskLevel.MEDIUM,
                risk_factors=["Infinite retry loop / stagnation detected"],
                metadata={"consecutive_repeats": consecutive_repeats},
            )

        return ModuleDecision(
            source_module=self.name,
            approval=Decision.ALLOW,
            capabilities={"goal_anchoring"},
            metadata={"current_goal": self.goal},
        )


def createTelos(
    goal: str = "",
    nonGoals: Sequence[str] | None = None,
    stagnation: dict[str, int] | None = None,
) -> TelosModule:
    """Helper factory matching JS-style createTelos({ goal, nonGoals, stagnation })."""
    stag = stagnation or {}
    return TelosModule(
        goal=goal,
        non_goals=nonGoals,
        max_equivalent_retries=stag.get("maxEquivalentRetries", 3),
        window_steps=stag.get("windowSteps", 10),
    )
