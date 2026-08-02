"""
@sip Core — Module Interface and Composition Algebra

Defines the SipModule base class/protocol and the compose() function
that chains multiple SIP modules into a K0-compatible scheduler context.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Protocol, Sequence

from schemamath_api.k0.decision import Decision, DecisionMerger, ModuleDecision
from schemamath_api.k0.lifecycle import (
    HookType,
    LifecycleContext,
    LifecyclePhase,
    LifecycleResult,
    LifecycleScheduler,
)
from schemamath_api.k0.manifest import (
    CapabilityDeclaration,
    CriticalityLevel,
    FailureSemantics,
    LifecycleHook,
    ModuleKind,
    ModuleManifest,
)
from schemamath_api.k0.registry import ManifestRegistry

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Base SIP Module Class
# ---------------------------------------------------------------------------

class SipModule:
    """
    Base class for all @sip modules.

    A SipModule exposes a manifest and registers lifecycle hooks into
    a LifecycleScheduler.
    """

    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
        kind: ModuleKind = ModuleKind.GATE,
        description: str = "",
        provides: Sequence[CapabilityDeclaration] | None = None,
        requires: Sequence[CapabilityDeclaration] | None = None,
        failure_semantics: FailureSemantics = FailureSemantics.FAIL_CLOSED,
    ) -> None:
        self.name = name
        self.version = version
        self.kind = kind
        self.description = description

        self._manifest = ModuleManifest(
            name=name,
            version=version,
            kind=kind,
            description=description,
            provides=list(provides or []),
            requires=list(requires or []),
            failure_semantics=failure_semantics,
        )

    @property
    def manifest(self) -> ModuleManifest:
        return self._manifest

    def register_into(self, registry: ManifestRegistry, scheduler: LifecycleScheduler) -> None:
        """Register manifest in registry and hooks in scheduler."""
        if self.name not in registry:
            registry.register(self._manifest)

        self.bind_hooks(scheduler)

    def bind_hooks(self, scheduler: LifecycleScheduler) -> None:
        """Override to register specific phase hooks into scheduler."""
        pass


# ---------------------------------------------------------------------------
# Composed Sandbox
# ---------------------------------------------------------------------------

class ComposedSandbox:
    """
    A sandbox composed of multiple SIP modules.
    """

    def __init__(self, modules: list[SipModule]) -> None:
        self.modules = list(modules)
        self.registry = ManifestRegistry()
        self.scheduler = LifecycleScheduler(self.registry)

        for mod in self.modules:
            mod.register_into(self.registry, self.scheduler)

        self.registry.freeze()

    def run(
        self,
        operation: str,
        input_data: dict[str, Any] | None = None,
        core_handler: Callable[[LifecycleContext], None] | None = None,
    ) -> LifecycleResult:
        """Run an operation through the composed sandbox."""
        if core_handler:
            self.scheduler.register_core_handler(
                LifecyclePhase.P5_EXECUTION, core_handler
            )

        ctx = LifecycleContext(
            operation=operation,
            input_data=input_data or {},
        )
        return self.scheduler.execute(ctx)


def compose(*modules: SipModule) -> ComposedSandbox:
    """
    Compose multiple SIP modules into a single sandbox.

    Usage:
        sandbox = compose(
            ContractModule(output_schema={...}),
            EvidenceModule(retention="30d"),
            PermissionModule(allowed_fs=["/workspace"]),
        )
        result = sandbox.run("validate_output", input_data={...})
    """
    return ComposedSandbox(list(modules))
