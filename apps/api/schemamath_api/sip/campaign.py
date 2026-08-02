"""
@sip/campaign (O3: Campaign Accounting, Deduplication, and Token Economics)

Manages multi-project research campaigns, batch target deduplication,
and token expenditure accounting.
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, field
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
class CampaignBudget:
    max_total_tokens: int = 1_000_000
    used_tokens: int = 0
    max_projects: int = 10


class CampaignModule(SipModule):
    """
    O3: @sip/campaign module.

    Campaign accounting & deduplication in P2_GOAL_BINDING and P9_ATOMIC_COMMIT.
    """

    def __init__(self, campaign_name: str = "default_campaign", max_total_tokens: int = 1_000_000) -> None:
        super().__init__(
            name="@sip/campaign",
            version="1.1.0",
            kind=ModuleKind.SCHEDULER,
            description="Campaign Accounting, Token Economics, and Batch Deduplication",
            provides=[CapabilityDeclaration(name="campaign_accounting", version="1.1")],
        )

        self.campaign_name = campaign_name
        self.budget = CampaignBudget(max_total_tokens=max_total_tokens)
        self.seen_target_fingerprints: set[str] = set()

        self._manifest.lifecycle_hooks = [
            LifecycleHook(
                phase=LifecyclePhase.P2_GOAL_BINDING,
                hook_type=HookType.PRE,
                priority=20,
                description="Check campaign target deduplication and budget limits",
            ),
            LifecycleHook(
                phase=LifecyclePhase.P9_ATOMIC_COMMIT,
                hook_type=HookType.POST,
                priority=100,
                description="Record campaign token consumption",
            ),
        ]

    def bind_hooks(self, scheduler: LifecycleScheduler) -> None:
        scheduler.register_hook(
            self.name,
            LifecyclePhase.P2_GOAL_BINDING,
            HookType.PRE,
            20,
            self.check_deduplication,
        )
        scheduler.register_hook(
            self.name,
            LifecyclePhase.P9_ATOMIC_COMMIT,
            HookType.POST,
            100,
            self.record_consumption,
        )

    def check_deduplication(self, ctx: LifecycleContext) -> ModuleDecision:
        """Check for duplicate targets across campaign operations."""
        # 1. Token Budget Check
        if self.budget.used_tokens >= self.budget.max_total_tokens:
            return ModuleDecision(
                source_module=self.name,
                approval=Decision.DENY,
                reason=f"Campaign '{self.campaign_name}' token budget exhausted ({self.budget.used_tokens}/{self.budget.max_total_tokens})",
            )

        # 2. Target Deduplication Check
        target_payload = ctx.input_data.get("campaign_target")
        if target_payload:
            fp = hashlib.sha256(json.dumps(target_payload, sort_keys=True, default=str).encode()).hexdigest()
            if fp in self.seen_target_fingerprints:
                return ModuleDecision(
                    source_module=self.name,
                    approval=Decision.REQUIRE_HUMAN,
                    reason=f"Duplicate campaign target detected: identical research target was already processed in campaign '{self.campaign_name}'",
                )
            self.seen_target_fingerprints.add(fp)

        return ModuleDecision(
            source_module=self.name,
            approval=Decision.ALLOW,
            capabilities={"campaign_accounting"},
        )

    def record_consumption(self, ctx: LifecycleContext) -> ModuleDecision:
        """Record token usage during phase execution."""
        tokens_spent = ctx.input_data.get("tokens_used", 100)
        self.budget.used_tokens += tokens_spent
        return ModuleDecision(source_module=self.name, approval=Decision.ALLOW)


def createCampaign(name: str = "campaign_1", maxTokens: int = 1_000_000) -> CampaignModule:
    """Helper factory matching JS-style createCampaign()."""
    return CampaignModule(campaign_name=name, max_total_tokens=maxTokens)
