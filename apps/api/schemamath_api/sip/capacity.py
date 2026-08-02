"""
@sip/capacity (O2: Elastic Capacity, Leases, and Verification Debt)

Manages compute leases, token rate limits, and verification debt tracking.

Verification Debt:
    If unverified or uncertified claims exceed `max_verification_debt`,
    new exploratory moves are automatically suspended until debt is paid down.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any

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
class ComputeLease:
    lease_id: str
    owner: str
    expires_at: float
    token_quota: int
    used_tokens: int = 0


class CapacityModule(SipModule):
    """
    O2: @sip/capacity module.

    Lease management and verification debt tracking in P4_ACTION_AUTH.
    """

    def __init__(
        self,
        max_verification_debt: int = 5,
        default_lease_duration_sec: int = 3600,
    ) -> None:
        super().__init__(
            name="@sip/capacity",
            version="1.1.0",
            kind=ModuleKind.SCHEDULER,
            description="Compute Leases and Verification Debt Regulator",
            provides=[CapabilityDeclaration(name="capacity_management", version="1.1")],
        )

        self.max_verification_debt = max_verification_debt
        self.default_lease_duration_sec = default_lease_duration_sec
        self.active_leases: dict[str, ComputeLease] = {}

        self._manifest.lifecycle_hooks = [
            LifecycleHook(
                phase=LifecyclePhase.P4_ACTION_AUTH,
                hook_type=HookType.PRE,
                priority=15,
                description="Check compute leases and verification debt limits",
            ),
        ]

    def bind_hooks(self, scheduler: LifecycleScheduler) -> None:
        scheduler.register_hook(
            self.name,
            LifecyclePhase.P4_ACTION_AUTH,
            HookType.PRE,
            15,
            self.check_capacity_and_debt,
        )

    def issue_lease(
        self, lease_id: str, owner: str, token_quota: int = 100000
    ) -> ComputeLease:
        """Issue a new compute lease."""
        lease = ComputeLease(
            lease_id=lease_id,
            owner=owner,
            expires_at=time.time() + self.default_lease_duration_sec,
            token_quota=token_quota,
        )
        self.active_leases[lease_id] = lease
        return lease

    def check_capacity_and_debt(self, ctx: LifecycleContext) -> ModuleDecision:
        """Evaluate verification debt and lease status."""
        # 1. Verification Debt Check
        unverified_debt = ctx.input_data.get("unverified_claim_count", 0)
        if unverified_debt > self.max_verification_debt:
            return ModuleDecision(
                source_module=self.name,
                approval=Decision.DENY,
                reason=(
                    f"Verification debt exceeded limit: {unverified_debt} > {self.max_verification_debt}. "
                    "New exploration suspended until pending claims are verified or pruned."
                ),
                risk_level=RiskLevel.HIGH,
                risk_factors=["Excessive unverified claim backlog"],
            )

        # 2. Lease Expiry Check
        lease_id = ctx.input_data.get("lease_id")
        if lease_id and lease_id in self.active_leases:
            lease = self.active_leases[lease_id]
            if time.time() > lease.expires_at:
                return ModuleDecision(
                    source_module=self.name,
                    approval=Decision.REQUIRE_HUMAN,
                    reason=f"Compute lease '{lease_id}' has expired. Lease renewal required.",
                )

        return ModuleDecision(
            source_module=self.name,
            approval=Decision.ALLOW,
            capabilities={"capacity_management"},
        )


def createCapacity(maxVerificationDebt: int = 5) -> CapacityModule:
    """Helper factory matching JS-style createCapacity()."""
    return CapacityModule(max_verification_debt=maxVerificationDebt)
