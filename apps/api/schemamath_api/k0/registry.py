"""
K0 Trust Kernel — Manifest Registry

The ManifestRegistry is responsible for loading, validating, storing,
and querying module manifests.  It enforces:

    1. No duplicate module names (uniqueness)
    2. All required capabilities are satisfied by some provider
    3. No conflicting capability providers (when exclusivity is declared)
    4. Lifecycle hooks are resolvable in deterministic order

The registry is the K0 kernel's view of "what modules exist and what
they can do."  It does NOT execute modules — that is the job of the
LifecycleScheduler and TransactionExecutor.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from schemamath_api.k0.manifest import (
    LifecycleHook,
    LifecyclePhase,
    ModuleKind,
    ModuleManifest,
)

logger = logging.getLogger(__name__)


class ManifestRegistryError(Exception):
    """Base exception for registry operations."""


class DuplicateModuleError(ManifestRegistryError):
    """Raised when attempting to register a module with a name that already exists."""


class MissingCapabilityError(ManifestRegistryError):
    """Raised when a required capability is not provided by any registered module."""


class CapabilityConflictError(ManifestRegistryError):
    """Raised when capability providers conflict in an unresolvable way."""


class ManifestRegistry:
    """
    Registry for K0 module manifests.

    Thread safety: This class is NOT thread-safe.  External callers must
    synchronize access if used from multiple threads.  In the current
    single-process ProofFlow architecture, this is not a concern.
    """

    def __init__(self) -> None:
        self._manifests: dict[str, ModuleManifest] = {}
        self._frozen: bool = False

    # --- Registration -------------------------------------------------------

    def register(self, manifest: ModuleManifest) -> None:
        """
        Register a module manifest.

        Raises:
            DuplicateModuleError: If a module with the same name is already registered.
            ManifestRegistryError: If the registry is frozen.
        """
        if self._frozen:
            raise ManifestRegistryError(
                "Registry is frozen.  No new modules can be registered after freeze()."
            )

        if manifest.name in self._manifests:
            raise DuplicateModuleError(
                f"Module '{manifest.name}' is already registered.  "
                f"Unregister it first or use a different name."
            )

        self._manifests[manifest.name] = manifest
        logger.info(
            "Registered module: %s v%s (kind=%s, criticality=%s)",
            manifest.name,
            manifest.version,
            manifest.kind,
            manifest.criticality,
        )

    def unregister(self, name: str) -> ModuleManifest:
        """
        Unregister a module by name.

        Returns the removed manifest.

        Raises:
            KeyError: If no module with that name is registered.
            ManifestRegistryError: If the registry is frozen.
        """
        if self._frozen:
            raise ManifestRegistryError(
                "Registry is frozen.  Modules cannot be removed after freeze()."
            )

        if name not in self._manifests:
            raise KeyError(f"Module '{name}' is not registered.")

        manifest = self._manifests.pop(name)
        logger.info("Unregistered module: %s v%s", manifest.name, manifest.version)
        return manifest

    # --- Query --------------------------------------------------------------

    def get(self, name: str) -> ModuleManifest | None:
        """Get a manifest by module name.  Returns None if not found."""
        return self._manifests.get(name)

    def get_or_raise(self, name: str) -> ModuleManifest:
        """Get a manifest by name, raising KeyError if not found."""
        if name not in self._manifests:
            raise KeyError(f"Module '{name}' is not registered.")
        return self._manifests[name]

    def all_manifests(self) -> list[ModuleManifest]:
        """Return all registered manifests in registration order."""
        return list(self._manifests.values())

    def all_names(self) -> list[str]:
        """Return all registered module names."""
        return list(self._manifests.keys())

    @property
    def count(self) -> int:
        """Number of registered modules."""
        return len(self._manifests)

    @property
    def is_frozen(self) -> bool:
        """Whether the registry is frozen (no more registrations allowed)."""
        return self._frozen

    def modules_by_kind(self, kind: ModuleKind) -> list[ModuleManifest]:
        """Return all modules of a given kind."""
        return [m for m in self._manifests.values() if m.kind == kind]

    def modules_providing(self, capability_name: str) -> list[ModuleManifest]:
        """Return all modules that provide a named capability."""
        return [
            m
            for m in self._manifests.values()
            if m.provides_capability(capability_name)
        ]

    def modules_requiring(self, capability_name: str) -> list[ModuleManifest]:
        """Return all modules that require a named capability."""
        return [
            m
            for m in self._manifests.values()
            if m.requires_capability(capability_name)
        ]

    # --- Validation ---------------------------------------------------------

    def validate_dependencies(self) -> list[str]:
        """
        Check that all required capabilities are provided by some module.

        Returns a list of error messages.  Empty list means all dependencies
        are satisfied.
        """
        # Build the set of all provided capabilities
        provided: dict[str, list[str]] = {}  # cap_name -> [module_names]
        for manifest in self._manifests.values():
            for cap in manifest.provides:
                provided.setdefault(cap.name, []).append(manifest.name)

        # Check every required capability
        errors: list[str] = []
        for manifest in self._manifests.values():
            for req in manifest.requires:
                if req.name not in provided:
                    errors.append(
                        f"Module '{manifest.name}' requires capability "
                        f"'{req.name}' (v{req.version}), but no module provides it."
                    )
                else:
                    # Check version compatibility (major version must match)
                    providers = provided[req.name]
                    req_major = req.version.split(".")[0]
                    compatible = False
                    for provider_name in providers:
                        provider = self._manifests[provider_name]
                        for cap in provider.provides:
                            if cap.name == req.name:
                                cap_major = cap.version.split(".")[0]
                                if cap_major == req_major:
                                    compatible = True
                                    break
                        if compatible:
                            break
                    if not compatible:
                        errors.append(
                            f"Module '{manifest.name}' requires capability "
                            f"'{req.name}' v{req.version}, but available providers "
                            f"{providers} offer incompatible versions."
                        )

        return errors

    def detect_conflicts(self) -> list[str]:
        """
        Detect potential capability conflicts between modules.

        Returns a list of warning messages.  These are informational —
        multiple providers for the same capability is not necessarily
        an error, but may indicate a configuration issue.
        """
        provided: dict[str, list[str]] = {}
        for manifest in self._manifests.values():
            for cap in manifest.provides:
                provided.setdefault(cap.name, []).append(manifest.name)

        warnings: list[str] = []
        for cap_name, providers in provided.items():
            if len(providers) > 1:
                warnings.append(
                    f"Capability '{cap_name}' is provided by multiple modules: "
                    f"{providers}.  K0 will use intersection semantics for "
                    f"capability range composition."
                )

        return warnings

    def validate_all(self) -> tuple[list[str], list[str]]:
        """
        Run all validation checks.

        Returns:
            Tuple of (errors, warnings).  Empty errors list means
            the registry is valid.
        """
        errors = self.validate_dependencies()
        warnings = self.detect_conflicts()
        return errors, warnings

    # --- Lifecycle Resolution -----------------------------------------------

    def resolve_hooks_for_phase(
        self, phase: LifecyclePhase
    ) -> list[tuple[ModuleManifest, LifecycleHook]]:
        """
        Return all (manifest, hook) pairs for a given phase, sorted by
        hook priority (ascending — lower priority number runs first).

        Within the same priority, hooks are ordered by module registration
        order (deterministic).
        """
        result: list[tuple[ModuleManifest, LifecycleHook]] = []
        for manifest in self._manifests.values():
            for hook in manifest.lifecycle_hooks:
                if hook.phase == phase:
                    result.append((manifest, hook))

        # Sort by priority (stable sort preserves registration order for ties)
        result.sort(key=lambda pair: pair[1].priority)
        return result

    def resolve_phase_order(self) -> list[LifecyclePhase]:
        """
        Return the fixed lifecycle phase order P0→P10.

        This is always the same regardless of what modules are registered.
        The fixed order is a core K0 invariant.
        """
        return list(LifecyclePhase)

    # --- Freeze / Snapshot --------------------------------------------------

    def freeze(self) -> None:
        """
        Freeze the registry.  No more registrations or removals allowed.

        This should be called after all modules are loaded and validated,
        before the lifecycle scheduler begins execution.
        """
        self._frozen = True
        logger.info(
            "Registry frozen with %d modules: %s",
            self.count,
            ", ".join(self.all_names()),
        )

    def snapshot(self) -> dict[str, Any]:
        """
        Return a serializable snapshot of the registry state.

        Useful for debugging, auditing, and event logging.
        """
        return {
            "module_count": self.count,
            "frozen": self._frozen,
            "modules": [
                {
                    "name": m.name,
                    "version": m.version,
                    "kind": m.kind.value,
                    "criticality": m.criticality.value,
                    "provides": [c.name for c in m.provides],
                    "requires": [c.name for c in m.requires],
                    "hooks": [
                        f"{h.phase.value}:{h.hook_type.value}@{h.priority}"
                        for h in m.lifecycle_hooks
                    ],
                    "failure_semantics": m.failure_semantics.value,
                }
                for m in self._manifests.values()
            ],
        }

    # --- Loading from files -------------------------------------------------

    @classmethod
    def from_manifest_files(cls, *paths: Path) -> ManifestRegistry:
        """
        Create a registry by loading manifests from JSON files.

        Each file must contain a valid ModuleManifest JSON object.

        Raises:
            ManifestRegistryError: If any file is invalid or contains duplicates.
        """
        registry = cls()
        for path in paths:
            if not path.exists():
                raise ManifestRegistryError(f"Manifest file not found: {path}")
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                manifest = ModuleManifest.model_validate(data)
                registry.register(manifest)
            except Exception as exc:
                raise ManifestRegistryError(
                    f"Failed to load manifest from {path}: {exc}"
                ) from exc
        return registry

    # --- String representation ----------------------------------------------

    def __repr__(self) -> str:
        frozen = " (frozen)" if self._frozen else ""
        return f"<ManifestRegistry modules={self.count}{frozen}>"

    def __contains__(self, name: str) -> bool:
        return name in self._manifests

    def __len__(self) -> int:
        return self.count
