"""
@sip/permission (F3: File, Network, and Tool Permission Fences)

Enforces declarative permission boundaries for file paths, network domains, and tools.

Usage:
    perm_mod = PermissionModule(
        fs=["/workspace", "/tmp"],
        net=["api.openai.com"],
        tools=["python.local", "graphviz.local"],
    )
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Sequence

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
    SecurityPrivilege,
)
from schemamath_api.sip.core import SipModule

logger = logging.getLogger(__name__)


class PermissionModule(SipModule):
    """
    F3: @sip/permission module.

    Interprets filesystem, network, and tool white-lists and enforces fences in P4.
    """

    def __init__(
        self,
        fs: Sequence[str] | None = None,
        net: Sequence[str] | None = None,
        tools: Sequence[str] | None = None,
    ) -> None:
        super().__init__(
            name="@sip/permission",
            version="1.0.0",
            kind=ModuleKind.GATE,
            description="Declarative Security and Scope Fence",
            provides=[CapabilityDeclaration(name="permission_fence", version="1.0")],
        )

        self.fs_allowed = [str(Path(p).resolve()) if p != "*" else "*" for p in (fs or [])]
        self.net_allowed = list(net or [])
        self.tools_allowed = list(tools or [])

        # Add privileges to manifest for audit trail
        privs = []
        if self.fs_allowed:
            privs.append(SecurityPrivilege(resource="fs", access="read", scope=";".join(self.fs_allowed)))
        if self.net_allowed:
            privs.append(SecurityPrivilege(resource="net", access="execute", scope=";".join(self.net_allowed)))
        if self.tools_allowed:
            privs.append(SecurityPrivilege(resource="tool", access="execute", scope=";".join(self.tools_allowed)))
        self._manifest.privileges = privs

        self._manifest.lifecycle_hooks = [
            LifecycleHook(
                phase=LifecyclePhase.P4_ACTION_AUTH,
                hook_type=HookType.PRE,
                priority=10,
                description="Authorize operation against security fences",
            ),
        ]

    def bind_hooks(self, scheduler: LifecycleScheduler) -> None:
        scheduler.register_hook(
            self.name,
            LifecyclePhase.P4_ACTION_AUTH,
            HookType.PRE,
            10,
            self.authorize_action,
        )

    def authorize_action(self, ctx: LifecycleContext) -> ModuleDecision:
        """Check operation requested resources against white-lists."""
        requested_fs = ctx.input_data.get("requested_fs")
        requested_net = ctx.input_data.get("requested_net")
        requested_tool = ctx.input_data.get("requested_tool")

        # Check FS fence
        if requested_fs and self.fs_allowed and "*" not in self.fs_allowed:
            req_path = str(Path(requested_fs).resolve())
            if not any(req_path.startswith(allowed) for allowed in self.fs_allowed):
                return ModuleDecision(
                    source_module=self.name,
                    approval=Decision.DENY,
                    reason=f"FS access denied: '{req_path}' is outside allowed paths {self.fs_allowed}",
                    risk_level=RiskLevel.HIGH,
                    risk_factors=["Unauthorized filesystem access attempt"],
                )

        # Check Network fence
        if requested_net and self.net_allowed and "*" not in self.net_allowed:
            if requested_net not in self.net_allowed:
                return ModuleDecision(
                    source_module=self.name,
                    approval=Decision.DENY,
                    reason=f"Network access denied: '{requested_net}' is not in allowed endpoints {self.net_allowed}",
                    risk_level=RiskLevel.HIGH,
                    risk_factors=["Unauthorized network endpoint attempt"],
                )

        # Check Tool fence
        if requested_tool and self.tools_allowed and "*" not in self.tools_allowed:
            if requested_tool not in self.tools_allowed:
                return ModuleDecision(
                    source_module=self.name,
                    approval=Decision.DENY,
                    reason=f"Tool access denied: '{requested_tool}' is not in allowed tools {self.tools_allowed}",
                    risk_level=RiskLevel.HIGH,
                    risk_factors=["Unauthorized tool execution attempt"],
                )

        return ModuleDecision(
            source_module=self.name,
            approval=Decision.ALLOW,
            capabilities={"permission_fence"},
        )


def createFence(
    fs: Sequence[str] | None = None,
    net: Sequence[str] | None = None,
    tools: Sequence[str] | None = None,
) -> PermissionModule:
    """Helper factory matching JS-style createFence({ fs, net, tools })."""
    return PermissionModule(fs=fs, net=net, tools=tools)
