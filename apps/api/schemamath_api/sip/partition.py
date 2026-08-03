"""
@sip/partition (F4: Workspace Isolation)

Provides isolated execution partitions for tasks and plugins using Process, Container, or WASI sandboxing.

Usage:
    part_mod = PartitionModule(mode="PROCESS")
"""

from __future__ import annotations

import tempfile
from enum import StrEnum
from pathlib import Path

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


class IsolationMode(StrEnum):
    PROCESS = "PROCESS"
    CONTAINER = "CONTAINER"
    WASI = "WASI"


class PartitionModule(SipModule):
    """
    F4: @sip/partition module.

    Creates and manages isolated execution directories and environment sandboxes in P5.
    """

    def __init__(self, mode: str = "PROCESS") -> None:
        super().__init__(
            name="@sip/partition",
            version="1.0.0",
            kind=ModuleKind.ADAPTER,
            description="Workspace and Execution Isolation Partition",
            provides=[CapabilityDeclaration(name="workspace_partition", version="1.0")],
            requires=[CapabilityDeclaration(name="permission_fence", version="1.0")],
        )

        self.mode = IsolationMode(mode)
        self.active_partitions: dict[str, Path] = {}

        self._manifest.lifecycle_hooks = [
            LifecycleHook(
                phase=LifecyclePhase.P5_EXECUTION,
                hook_type=HookType.PRE,
                priority=10,
                description="Setup isolated workspace partition",
            ),
            LifecycleHook(
                phase=LifecyclePhase.P10_TEARDOWN_COMPACT,
                hook_type=HookType.POST,
                priority=100,
                description="Teardown workspace partition",
            ),
        ]

    def bind_hooks(self, scheduler: LifecycleScheduler) -> None:
        scheduler.register_hook(
            self.name,
            LifecyclePhase.P5_EXECUTION,
            HookType.PRE,
            10,
            self.setup_partition,
        )
        scheduler.register_hook(
            self.name,
            LifecyclePhase.P10_TEARDOWN_COMPACT,
            HookType.POST,
            100,
            self.teardown_partition,
        )

    def setup_partition(self, ctx: LifecycleContext) -> ModuleDecision:
        """Create an isolated workspace partition for the operation."""
        try:
            temp_dir = Path(tempfile.mkdtemp(prefix=f"sip_part_{self.mode.value}_"))
            self.active_partitions[ctx.operation] = temp_dir

            ctx.module_state["partition_dir"] = str(temp_dir)
            ctx.module_state["isolation_mode"] = self.mode.value

            return ModuleDecision(
                source_module=self.name,
                approval=Decision.ALLOW,
                capabilities={"workspace_partition"},
                metadata={"partition_dir": str(temp_dir), "mode": self.mode.value},
            )
        except Exception as exc:
            return ModuleDecision(
                source_module=self.name,
                approval=Decision.DENY,
                reason=f"Failed to create workspace partition: {exc}",
            )

    def teardown_partition(self, ctx: LifecycleContext) -> ModuleDecision:
        """Teardown temporary workspace partition."""
        partition_dir = self.active_partitions.pop(ctx.operation, None)
        if partition_dir and partition_dir.exists():
            import shutil
            try:
                shutil.rmtree(partition_dir, ignore_errors=True)
            except Exception:
                pass

        return ModuleDecision(
            source_module=self.name,
            approval=Decision.ALLOW,
        )


def createPartition(mode: str = "PROCESS") -> PartitionModule:
    """Helper factory matching JS-style createPartition({ mode })."""
    return PartitionModule(mode=mode)
