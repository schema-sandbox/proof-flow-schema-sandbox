"""
@sip/trajectory (G3: Trajectory Recording, Route Replacement, Failure Assetization)

Records research decision trajectories, tracks route supersession,
and converts dead ends into reusable knowledge assets.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
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

logger = logger = logging.getLogger(__name__)


@dataclass
class TrajectoryStep:
    step_id: int
    operation: str
    route_id: str | None
    status: str
    failure_asset: dict[str, Any] | None = None
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class TrajectoryModule(SipModule):
    """
    G3: @sip/trajectory module.

    Logs execution trajectory and assetizes dead ends in P3 & P6.
    """

    def __init__(self) -> None:
        super().__init__(
            name="@sip/trajectory",
            version="1.0.0",
            kind=ModuleKind.OBSERVER,
            description="Trajectory Recording and Failure Assetization Ledger",
            provides=[CapabilityDeclaration(name="trajectory_assetization", version="1.0")],
        )

        self.steps: list[TrajectoryStep] = []
        self.superseded_routes: dict[str, str] = {}  # old_route -> new_route

        self._manifest.lifecycle_hooks = [
            LifecycleHook(
                phase=LifecyclePhase.P3_PLAN_PROPOSAL,
                hook_type=HookType.PRE,
                priority=10,
                description="Check for historical dead ends or superseded routes",
            ),
            LifecycleHook(
                phase=LifecyclePhase.P6_ARTIFACT_RECORDING,
                hook_type=HookType.POST,
                priority=50,
                description="Record trajectory step and assetize failure if present",
            ),
        ]

    def bind_hooks(self, scheduler: LifecycleScheduler) -> None:
        scheduler.register_hook(
            self.name,
            LifecyclePhase.P3_PLAN_PROPOSAL,
            HookType.PRE,
            10,
            self.check_historical_dead_ends,
        )
        scheduler.register_hook(
            self.name,
            LifecyclePhase.P6_ARTIFACT_RECORDING,
            HookType.POST,
            50,
            self.record_trajectory_step,
        )

    def record_superseded(self, old_route_id: str, new_route_id: str) -> None:
        """Track route supersession."""
        self.superseded_routes[old_route_id] = new_route_id

    def check_historical_dead_ends(self, ctx: LifecycleContext) -> ModuleDecision:
        """Check if proposed route was previously marked as dead end."""
        target_route = ctx.input_data.get("route_id")
        if target_route and target_route in self.superseded_routes:
            new_r = self.superseded_routes[target_route]
            return ModuleDecision(
                source_module=self.name,
                approval=Decision.REQUIRE_HUMAN,
                reason=f"Route '{target_route}' was superseded by '{new_r}'",
            )
        return ModuleDecision(source_module=self.name, approval=Decision.ALLOW)

    def record_trajectory_step(self, ctx: LifecycleContext) -> ModuleDecision:
        """Record step and capture failure assets if operation failed."""
        is_failure = ctx.input_data.get("is_failure", False)
        failure_asset = None

        if is_failure:
            failure_asset = {
                "reason": ctx.input_data.get("failure_reason", "Unknown failure"),
                "context": ctx.input_data,
            }

        step = TrajectoryStep(
            step_id=len(self.steps) + 1,
            operation=ctx.operation,
            route_id=ctx.input_data.get("route_id"),
            status="FAILED" if is_failure else "SUCCESS",
            failure_asset=failure_asset,
        )
        self.steps.append(step)

        return ModuleDecision(
            source_module=self.name,
            approval=Decision.ALLOW,
            capabilities={"trajectory_assetization"},
        )

    def inspect_failed_assets(self) -> list[dict[str, Any]]:
        """Return list of assetized failures for retrieval."""
        return [
            {"step_id": s.step_id, "op": s.operation, "asset": s.failure_asset}
            for s in self.steps
            if s.failure_asset
        ]


def createTrajectory() -> TrajectoryModule:
    """Helper factory matching JS-style createTrajectory()."""
    return TrajectoryModule()
