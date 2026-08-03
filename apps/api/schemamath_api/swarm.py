"""
Autonomous Research Swarm Coordinator (ResearchSwarmCoordinator)

Orchestrates autonomous multi-agent swarms running continuous, self-driven research loops
over days/weeks with goal decomposition, active route selection, and bottleneck resolution.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any

from schemamath_api.k0.decision import Decision
from schemamath_api.k0.lifecycle import LifecycleResult
from schemamath_api.sip import ComposedSandbox, compose, createFederation

logger = logging.getLogger(__name__)


@dataclass
class SwarmStatus:
    completed_steps: int = 0
    active_route_id: str | None = None
    bottleneck_detected: bool = False
    is_converged: bool = False
    last_step_result: str = "INITIALIZED"


class ResearchSwarmCoordinator:
    """
    Coordinates autonomous multi-agent research loops over ProofFlow composed sandboxes.
    """

    def __init__(self, sandbox: ComposedSandbox | None = None) -> None:
        self.sandbox = sandbox or compose(createFederation())
        self.status = SwarmStatus()
        self.history: list[dict[str, Any]] = []

    def execute_swarm_step(
        self,
        task_name: str,
        input_payload: dict[str, Any] | None = None,
    ) -> LifecycleResult:
        """Execute one autonomous swarm step inside the Trust Kernel lifecycle."""
        payload = input_payload or {}
        res = self.sandbox.run(task_name, input_data=payload)

        self.status.completed_steps += 1
        self.status.last_step_result = "SUCCESS" if res.success else f"ABORTED: {res.abort_reason}"

        if res.final_decision.approval == Decision.REQUIRE_HUMAN:
            self.status.bottleneck_detected = True

        self.history.append({
            "step_index": self.status.completed_steps,
            "task_name": task_name,
            "success": res.success,
            "approval": res.final_decision.approval.value,
        })

        return res

    def run_swarm_loop(
        self,
        target_steps: int = 5,
        delay_sec: float = 0.0,
    ) -> SwarmStatus:
        """Run a continuous loop of swarm steps up to target_steps or until human intervention required."""
        for step in range(target_steps):
            if self.status.bottleneck_detected:
                logger.info("Swarm paused: human intervention required")
                break

            res = self.execute_swarm_step(
                task_name=f"autonomous_swarm_step_{step+1}",
                input_payload={"step": step + 1},
            )

            if not res.success:
                logger.warning("Swarm step %d aborted: %s", step + 1, res.abort_reason)
                break

            if delay_sec > 0:
                time.sleep(delay_sec)

        return self.status
