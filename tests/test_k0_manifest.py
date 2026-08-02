"""
Tests for K0 Trust Kernel — Module Manifest and Registry

Covers:
    - ModuleManifest creation and validation
    - ModuleKind, FailureSemantics, CriticalityLevel enums
    - LifecyclePhase and LifecycleHook declarations
    - ManifestRegistry registration, query, and conflict detection
    - Dependency validation and version compatibility
    - Lifecycle phase resolution and ordering
    - Registry freeze semantics
    - File-based manifest loading
    - Existing plugin migration to ModuleManifest format
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from uuid import uuid4

import pytest

from schemamath_api.k0.manifest import (
    CapabilityDeclaration,
    CriticalityLevel,
    DegradationSpec,
    FailureSemantics,
    HookType,
    LifecycleHook,
    LifecyclePhase,
    ModuleKind,
    ModuleManifest,
    SecurityPrivilege,
)
from schemamath_api.k0.registry import (
    DuplicateModuleError,
    ManifestRegistry,
    ManifestRegistryError,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_manifest(
    name: str = "@sip/test-module",
    version: str = "1.0.0",
    kind: ModuleKind = ModuleKind.GATE,
    provides: list[CapabilityDeclaration] | None = None,
    requires: list[CapabilityDeclaration] | None = None,
    lifecycle_hooks: list[LifecycleHook] | None = None,
    failure_semantics: FailureSemantics = FailureSemantics.FAIL_CLOSED,
    degradation_spec: DegradationSpec | None = None,
    **kwargs,
) -> ModuleManifest:
    """Helper to create a ModuleManifest with sensible defaults."""
    if provides is None:
        provides = [CapabilityDeclaration(name="test_capability")]
    return ModuleManifest(
        name=name,
        version=version,
        kind=kind,
        provides=provides,
        requires=requires or [],
        lifecycle_hooks=lifecycle_hooks or [],
        failure_semantics=failure_semantics,
        degradation_spec=degradation_spec,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# ModuleManifest — Creation & Validation
# ---------------------------------------------------------------------------


class TestModuleManifestCreation:
    """Tests for creating ModuleManifest instances."""

    def test_minimal_gate_module(self):
        m = _make_manifest()
        assert m.name == "@sip/test-module"
        assert m.version == "1.0.0"
        assert m.kind == ModuleKind.GATE
        assert len(m.provides) == 1
        assert m.provides[0].name == "test_capability"
        assert m.failure_semantics == FailureSemantics.FAIL_CLOSED
        assert m.schema_version == "1.0"

    def test_full_manifest(self):
        m = ModuleManifest(
            name="@sip/contract",
            version="1.0.0",
            description="Input/output JSON Schema constraints",
            author="ProofFlow",
            license="BSL-1.1",
            kind=ModuleKind.GATE,
            criticality=CriticalityLevel.RECOMMENDED,
            provides=[
                CapabilityDeclaration(
                    name="schema_validation",
                    version="1.0",
                    description="Validates input/output against JSON Schema",
                ),
            ],
            requires=[],
            lifecycle_hooks=[
                LifecycleHook(
                    phase=LifecyclePhase.P1_INPUT_NORMALIZATION,
                    hook_type=HookType.PRE,
                    priority=10,
                    description="Validate input against declared schema",
                ),
                LifecycleHook(
                    phase=LifecyclePhase.P8_RELEASE_AUTH,
                    hook_type=HookType.PRE,
                    priority=10,
                    description="Validate output against declared schema",
                ),
            ],
            privileges=[
                SecurityPrivilege(
                    resource="event_store",
                    access="read",
                    justification="Read schemas from event metadata",
                ),
            ],
            failure_semantics=FailureSemantics.FAIL_CLOSED,
            guarantees=[
                "All outputs conform to declared JSON Schema",
                "Violations are reported with structured error details",
            ],
            non_guarantees=[
                "Does not validate semantic correctness of content",
                "Does not enforce business logic beyond schema structure",
            ],
            tags=["foundation", "validation", "schema"],
        )
        assert m.kind == ModuleKind.GATE
        assert m.criticality == CriticalityLevel.RECOMMENDED
        assert len(m.lifecycle_hooks) == 2
        assert m.provides_capability("schema_validation")
        assert not m.provides_capability("nonexistent")
        assert len(m.guarantees) == 2
        assert len(m.non_guarantees) == 2

    def test_observer_can_have_no_provides(self):
        """OBSERVER is the only kind that can have empty provides."""
        m = ModuleManifest(
            name="@sip/monitor",
            version="1.0.0",
            kind=ModuleKind.OBSERVER,
            provides=[],
        )
        assert m.kind == ModuleKind.OBSERVER
        assert len(m.provides) == 0

    def test_non_observer_requires_provides(self):
        """Non-OBSERVER modules must provide at least one capability."""
        with pytest.raises(ValueError, match="should provide at least one capability"):
            ModuleManifest(
                name="@sip/empty-gate",
                version="1.0.0",
                kind=ModuleKind.GATE,
                provides=[],
            )

    def test_degrade_requires_degradation_spec(self):
        """DEGRADE failure semantics must include a degradation spec."""
        with pytest.raises(ValueError, match="degradation_spec"):
            _make_manifest(failure_semantics=FailureSemantics.DEGRADE)

    def test_degrade_with_valid_spec(self):
        m = _make_manifest(
            failure_semantics=FailureSemantics.DEGRADE,
            degradation_spec=DegradationSpec(
                affected_capabilities=["test_capability"],
                fallback_behavior="Return last known good result",
                max_degradation_duration_seconds=300,
            ),
        )
        assert m.failure_semantics == FailureSemantics.DEGRADE
        assert m.degradation_spec is not None
        assert m.degradation_spec.max_degradation_duration_seconds == 300

    def test_duplicate_hooks_rejected(self):
        """No two hooks can have the same phase+type+priority."""
        hook = LifecycleHook(
            phase=LifecyclePhase.P1_INPUT_NORMALIZATION,
            hook_type=HookType.PRE,
            priority=10,
        )
        with pytest.raises(ValueError, match="Duplicate lifecycle hook"):
            _make_manifest(lifecycle_hooks=[hook, hook])

    def test_different_priority_hooks_allowed(self):
        """Same phase+type but different priority is fine."""
        m = _make_manifest(
            lifecycle_hooks=[
                LifecycleHook(
                    phase=LifecyclePhase.P1_INPUT_NORMALIZATION,
                    hook_type=HookType.PRE,
                    priority=10,
                ),
                LifecycleHook(
                    phase=LifecyclePhase.P1_INPUT_NORMALIZATION,
                    hook_type=HookType.PRE,
                    priority=20,
                ),
            ],
        )
        assert len(m.lifecycle_hooks) == 2


class TestModuleManifestValidation:
    """Tests for manifest field validation."""

    def test_invalid_module_name_rejected(self):
        with pytest.raises(ValueError):
            _make_manifest(name="")

    def test_name_with_special_chars_rejected(self):
        with pytest.raises(ValueError):
            _make_manifest(name="module with spaces")

    def test_valid_scoped_name(self):
        m = _make_manifest(name="@sip/contract")
        assert m.name == "@sip/contract"

    def test_valid_dotted_name(self):
        m = _make_manifest(name="python.local")
        assert m.name == "python.local"

    def test_invalid_version_rejected(self):
        with pytest.raises(ValueError):
            _make_manifest(version="not-a-version")

    def test_valid_semver(self):
        m = _make_manifest(version="1.2.3")
        assert m.version == "1.2.3"

    def test_semver_with_prerelease(self):
        m = _make_manifest(version="1.0.0-alpha.1")
        assert m.version == "1.0.0-alpha.1"

    def test_invalid_security_resource_rejected(self):
        with pytest.raises(ValueError, match="Unknown resource type"):
            SecurityPrivilege(resource="nuclear_launch", access="execute")

    def test_invalid_security_access_rejected(self):
        with pytest.raises(ValueError, match="Unknown access level"):
            SecurityPrivilege(resource="fs", access="destroy")

    def test_valid_security_privilege(self):
        sp = SecurityPrivilege(
            resource="fs",
            access="read",
            scope="/workspace/blobs",
            justification="Read content-addressed artifacts",
        )
        assert sp.resource == "fs"
        assert sp.access == "read"


class TestModuleManifestUtilities:
    """Tests for manifest utility methods."""

    def test_provides_capability(self):
        m = _make_manifest(
            provides=[
                CapabilityDeclaration(name="cap_a"),
                CapabilityDeclaration(name="cap_b"),
            ],
        )
        assert m.provides_capability("cap_a")
        assert m.provides_capability("cap_b")
        assert not m.provides_capability("cap_c")

    def test_requires_capability(self):
        m = _make_manifest(
            requires=[CapabilityDeclaration(name="dependency")],
        )
        assert m.requires_capability("dependency")
        assert not m.requires_capability("other")

    def test_hooks_into_phase(self):
        m = _make_manifest(
            lifecycle_hooks=[
                LifecycleHook(
                    phase=LifecyclePhase.P5_EXECUTION,
                    hook_type=HookType.PRE,
                ),
            ],
        )
        assert m.hooks_into_phase(LifecyclePhase.P5_EXECUTION)
        assert not m.hooks_into_phase(LifecyclePhase.P0_LOAD_ATTEST)

    def test_capability_name_sets(self):
        m = _make_manifest(
            provides=[
                CapabilityDeclaration(name="a"),
                CapabilityDeclaration(name="b"),
            ],
            requires=[CapabilityDeclaration(name="x")],
        )
        assert m.provided_capability_names() == {"a", "b"}
        assert m.required_capability_names() == {"x"}


# ---------------------------------------------------------------------------
# ManifestRegistry — Registration & Query
# ---------------------------------------------------------------------------


class TestManifestRegistration:
    """Tests for registering and unregistering modules."""

    def test_register_and_get(self):
        reg = ManifestRegistry()
        m = _make_manifest(name="@sip/contract")
        reg.register(m)
        assert reg.get("@sip/contract") is m
        assert reg.count == 1

    def test_register_duplicate_rejected(self):
        reg = ManifestRegistry()
        reg.register(_make_manifest(name="@sip/contract"))
        with pytest.raises(DuplicateModuleError, match="already registered"):
            reg.register(_make_manifest(name="@sip/contract"))

    def test_unregister(self):
        reg = ManifestRegistry()
        m = _make_manifest(name="@sip/contract")
        reg.register(m)
        removed = reg.unregister("@sip/contract")
        assert removed is m
        assert reg.count == 0
        assert reg.get("@sip/contract") is None

    def test_unregister_nonexistent_raises(self):
        reg = ManifestRegistry()
        with pytest.raises(KeyError, match="not registered"):
            reg.unregister("@sip/nonexistent")

    def test_get_or_raise(self):
        reg = ManifestRegistry()
        reg.register(_make_manifest(name="@sip/contract"))
        assert reg.get_or_raise("@sip/contract").name == "@sip/contract"
        with pytest.raises(KeyError):
            reg.get_or_raise("@sip/missing")

    def test_all_manifests_and_names(self):
        reg = ManifestRegistry()
        reg.register(_make_manifest(name="@sip/a"))
        reg.register(_make_manifest(name="@sip/b"))
        reg.register(_make_manifest(name="@sip/c"))
        assert reg.all_names() == ["@sip/a", "@sip/b", "@sip/c"]
        assert len(reg.all_manifests()) == 3

    def test_contains_and_len(self):
        reg = ManifestRegistry()
        reg.register(_make_manifest(name="@sip/contract"))
        assert "@sip/contract" in reg
        assert "@sip/missing" not in reg
        assert len(reg) == 1


class TestManifestQuery:
    """Tests for querying the registry."""

    def test_modules_by_kind(self):
        reg = ManifestRegistry()
        reg.register(_make_manifest(name="@sip/gate1", kind=ModuleKind.GATE))
        reg.register(_make_manifest(name="@sip/gate2", kind=ModuleKind.GATE))
        reg.register(
            _make_manifest(name="@sip/observer", kind=ModuleKind.OBSERVER, provides=[])
        )
        gates = reg.modules_by_kind(ModuleKind.GATE)
        assert len(gates) == 2
        observers = reg.modules_by_kind(ModuleKind.OBSERVER)
        assert len(observers) == 1

    def test_modules_providing(self):
        reg = ManifestRegistry()
        reg.register(
            _make_manifest(
                name="@sip/a",
                provides=[CapabilityDeclaration(name="schema_validation")],
            )
        )
        reg.register(
            _make_manifest(
                name="@sip/b",
                provides=[CapabilityDeclaration(name="audit_logging")],
            )
        )
        result = reg.modules_providing("schema_validation")
        assert len(result) == 1
        assert result[0].name == "@sip/a"

    def test_modules_requiring(self):
        reg = ManifestRegistry()
        reg.register(
            _make_manifest(
                name="@sip/telos",
                requires=[CapabilityDeclaration(name="schema_validation")],
            )
        )
        reg.register(_make_manifest(name="@sip/contract"))
        result = reg.modules_requiring("schema_validation")
        assert len(result) == 1
        assert result[0].name == "@sip/telos"


# ---------------------------------------------------------------------------
# ManifestRegistry — Validation
# ---------------------------------------------------------------------------


class TestDependencyValidation:
    """Tests for capability dependency validation."""

    def test_satisfied_dependencies(self):
        reg = ManifestRegistry()
        reg.register(
            _make_manifest(
                name="@sip/contract",
                provides=[CapabilityDeclaration(name="schema_validation")],
            )
        )
        reg.register(
            _make_manifest(
                name="@sip/telos",
                provides=[CapabilityDeclaration(name="goal_binding")],
                requires=[CapabilityDeclaration(name="schema_validation")],
            )
        )
        errors = reg.validate_dependencies()
        assert errors == []

    def test_unsatisfied_dependency(self):
        reg = ManifestRegistry()
        reg.register(
            _make_manifest(
                name="@sip/telos",
                provides=[CapabilityDeclaration(name="goal_binding")],
                requires=[CapabilityDeclaration(name="schema_validation")],
            )
        )
        errors = reg.validate_dependencies()
        assert len(errors) == 1
        assert "schema_validation" in errors[0]
        assert "@sip/telos" in errors[0]

    def test_version_incompatibility(self):
        reg = ManifestRegistry()
        reg.register(
            _make_manifest(
                name="@sip/contract",
                provides=[
                    CapabilityDeclaration(name="schema_validation", version="2.0")
                ],
            )
        )
        reg.register(
            _make_manifest(
                name="@sip/telos",
                provides=[CapabilityDeclaration(name="goal_binding")],
                requires=[
                    CapabilityDeclaration(name="schema_validation", version="1.0")
                ],
            )
        )
        errors = reg.validate_dependencies()
        assert len(errors) == 1
        assert "incompatible versions" in errors[0]

    def test_version_compatible_same_major(self):
        reg = ManifestRegistry()
        reg.register(
            _make_manifest(
                name="@sip/contract",
                provides=[
                    CapabilityDeclaration(name="schema_validation", version="1.2")
                ],
            )
        )
        reg.register(
            _make_manifest(
                name="@sip/telos",
                provides=[CapabilityDeclaration(name="goal_binding")],
                requires=[
                    CapabilityDeclaration(name="schema_validation", version="1.0")
                ],
            )
        )
        errors = reg.validate_dependencies()
        assert errors == []


class TestConflictDetection:
    """Tests for capability conflict detection."""

    def test_no_conflicts(self):
        reg = ManifestRegistry()
        reg.register(
            _make_manifest(
                name="@sip/contract",
                provides=[CapabilityDeclaration(name="schema_validation")],
            )
        )
        reg.register(
            _make_manifest(
                name="@sip/evidence",
                provides=[CapabilityDeclaration(name="audit_logging")],
            )
        )
        warnings = reg.detect_conflicts()
        assert warnings == []

    def test_multiple_providers_warning(self):
        reg = ManifestRegistry()
        reg.register(
            _make_manifest(
                name="@sip/contract",
                provides=[CapabilityDeclaration(name="schema_validation")],
            )
        )
        reg.register(
            _make_manifest(
                name="@sip/strict-contract",
                provides=[CapabilityDeclaration(name="schema_validation")],
            )
        )
        warnings = reg.detect_conflicts()
        assert len(warnings) == 1
        assert "schema_validation" in warnings[0]
        assert "multiple modules" in warnings[0]

    def test_validate_all(self):
        reg = ManifestRegistry()
        reg.register(
            _make_manifest(
                name="@sip/telos",
                provides=[CapabilityDeclaration(name="goal_binding")],
                requires=[CapabilityDeclaration(name="missing_cap")],
            )
        )
        errors, warnings = reg.validate_all()
        assert len(errors) == 1
        assert len(warnings) == 0


# ---------------------------------------------------------------------------
# ManifestRegistry — Lifecycle Resolution
# ---------------------------------------------------------------------------


class TestLifecycleResolution:
    """Tests for lifecycle phase hook resolution."""

    def test_resolve_hooks_for_phase(self):
        reg = ManifestRegistry()
        reg.register(
            _make_manifest(
                name="@sip/contract",
                lifecycle_hooks=[
                    LifecycleHook(
                        phase=LifecyclePhase.P1_INPUT_NORMALIZATION,
                        hook_type=HookType.PRE,
                        priority=10,
                    ),
                ],
            )
        )
        reg.register(
            _make_manifest(
                name="@sip/evidence",
                lifecycle_hooks=[
                    LifecycleHook(
                        phase=LifecyclePhase.P1_INPUT_NORMALIZATION,
                        hook_type=HookType.POST,
                        priority=50,
                    ),
                ],
            )
        )
        hooks = reg.resolve_hooks_for_phase(LifecyclePhase.P1_INPUT_NORMALIZATION)
        assert len(hooks) == 2
        assert hooks[0][0].name == "@sip/contract"  # priority 10 first
        assert hooks[1][0].name == "@sip/evidence"  # priority 50 second

    def test_priority_ordering(self):
        """Lower priority number runs first."""
        reg = ManifestRegistry()
        reg.register(
            _make_manifest(
                name="@sip/late",
                lifecycle_hooks=[
                    LifecycleHook(
                        phase=LifecyclePhase.P5_EXECUTION,
                        hook_type=HookType.PRE,
                        priority=200,
                    ),
                ],
            )
        )
        reg.register(
            _make_manifest(
                name="@sip/early",
                lifecycle_hooks=[
                    LifecycleHook(
                        phase=LifecyclePhase.P5_EXECUTION,
                        hook_type=HookType.PRE,
                        priority=5,
                    ),
                ],
            )
        )
        hooks = reg.resolve_hooks_for_phase(LifecyclePhase.P5_EXECUTION)
        assert hooks[0][0].name == "@sip/early"
        assert hooks[1][0].name == "@sip/late"

    def test_empty_phase(self):
        reg = ManifestRegistry()
        reg.register(_make_manifest(name="@sip/contract"))
        hooks = reg.resolve_hooks_for_phase(LifecyclePhase.P0_LOAD_ATTEST)
        assert hooks == []

    def test_fixed_phase_order(self):
        reg = ManifestRegistry()
        phases = reg.resolve_phase_order()
        assert len(phases) == 11  # P0 through P10
        assert phases[0] == LifecyclePhase.P0_LOAD_ATTEST
        assert phases[-1] == LifecyclePhase.P10_TEARDOWN_COMPACT
        # Verify strict ordering by enum declaration index
        all_phases = list(LifecyclePhase)
        for i in range(len(phases) - 1):
            assert all_phases.index(phases[i]) < all_phases.index(phases[i + 1])


# ---------------------------------------------------------------------------
# ManifestRegistry — Freeze
# ---------------------------------------------------------------------------


class TestRegistryFreeze:
    """Tests for registry freeze semantics."""

    def test_freeze_prevents_registration(self):
        reg = ManifestRegistry()
        reg.register(_make_manifest(name="@sip/contract"))
        reg.freeze()
        assert reg.is_frozen
        with pytest.raises(ManifestRegistryError, match="frozen"):
            reg.register(_make_manifest(name="@sip/new"))

    def test_freeze_prevents_unregistration(self):
        reg = ManifestRegistry()
        reg.register(_make_manifest(name="@sip/contract"))
        reg.freeze()
        with pytest.raises(ManifestRegistryError, match="frozen"):
            reg.unregister("@sip/contract")

    def test_frozen_queries_still_work(self):
        reg = ManifestRegistry()
        reg.register(_make_manifest(name="@sip/contract"))
        reg.freeze()
        assert reg.get("@sip/contract") is not None
        assert reg.count == 1
        assert len(reg.all_manifests()) == 1


# ---------------------------------------------------------------------------
# ManifestRegistry — Snapshot
# ---------------------------------------------------------------------------


class TestRegistrySnapshot:
    """Tests for registry snapshot serialization."""

    def test_snapshot_structure(self):
        reg = ManifestRegistry()
        reg.register(
            _make_manifest(
                name="@sip/contract",
                provides=[CapabilityDeclaration(name="schema_validation")],
                lifecycle_hooks=[
                    LifecycleHook(
                        phase=LifecyclePhase.P1_INPUT_NORMALIZATION,
                        hook_type=HookType.PRE,
                        priority=10,
                    ),
                ],
            )
        )
        snap = reg.snapshot()
        assert snap["module_count"] == 1
        assert snap["frozen"] is False
        assert len(snap["modules"]) == 1
        mod = snap["modules"][0]
        assert mod["name"] == "@sip/contract"
        assert "schema_validation" in mod["provides"]
        assert "P1_INPUT_NORMALIZATION:pre@10" in mod["hooks"]

    def test_snapshot_is_json_serializable(self):
        reg = ManifestRegistry()
        reg.register(_make_manifest(name="@sip/contract"))
        snap = reg.snapshot()
        # Must not raise
        json_str = json.dumps(snap)
        assert isinstance(json_str, str)


# ---------------------------------------------------------------------------
# ManifestRegistry — File Loading
# ---------------------------------------------------------------------------


class TestManifestFileLoading:
    """Tests for loading manifests from JSON files."""

    def test_load_from_file(self, tmp_path):
        manifest_data = {
            "name": "@sip/contract",
            "version": "1.0.0",
            "kind": "gate",
            "provides": [{"name": "schema_validation"}],
        }
        f = tmp_path / "contract.manifest.json"
        f.write_text(json.dumps(manifest_data), encoding="utf-8")

        reg = ManifestRegistry.from_manifest_files(f)
        assert reg.count == 1
        assert reg.get("@sip/contract") is not None

    def test_load_multiple_files(self, tmp_path):
        for name in ["contract", "evidence"]:
            data = {
                "name": f"@sip/{name}",
                "version": "1.0.0",
                "kind": "gate",
                "provides": [{"name": f"{name}_cap"}],
            }
            f = tmp_path / f"{name}.manifest.json"
            f.write_text(json.dumps(data), encoding="utf-8")

        files = list(tmp_path.glob("*.manifest.json"))
        reg = ManifestRegistry.from_manifest_files(*files)
        assert reg.count == 2

    def test_load_nonexistent_file_raises(self):
        with pytest.raises(ManifestRegistryError, match="not found"):
            ManifestRegistry.from_manifest_files(Path("/nonexistent/file.json"))

    def test_load_invalid_json_raises(self, tmp_path):
        f = tmp_path / "bad.manifest.json"
        f.write_text("not valid json", encoding="utf-8")
        with pytest.raises(ManifestRegistryError, match="Failed to load"):
            ManifestRegistry.from_manifest_files(f)

    def test_load_invalid_manifest_raises(self, tmp_path):
        f = tmp_path / "bad.manifest.json"
        f.write_text(json.dumps({"name": "", "version": "nope"}), encoding="utf-8")
        with pytest.raises(ManifestRegistryError, match="Failed to load"):
            ManifestRegistry.from_manifest_files(f)


# ---------------------------------------------------------------------------
# Existing Plugin Migration
# ---------------------------------------------------------------------------


class TestPluginMigration:
    """
    Tests verifying that existing plugin manifests can be expressed
    as ModuleManifest instances, ensuring backward compatibility.
    """

    def test_python_local_as_module_manifest(self):
        """python.local plugin expressed as a ModuleManifest."""
        m = ModuleManifest(
            name="python.local",
            version="0.1.0",
            description="Local Python experiment runner",
            kind=ModuleKind.ADAPTER,
            criticality=CriticalityLevel.OPTIONAL,
            provides=[
                CapabilityDeclaration(
                    name="python_execution",
                    version="1.0",
                    description="Execute Python scripts in isolated virtualenv",
                ),
            ],
            lifecycle_hooks=[
                LifecycleHook(
                    phase=LifecyclePhase.P5_EXECUTION,
                    hook_type=HookType.PRE,
                    priority=100,
                    description="Execute Python experiment",
                ),
                LifecycleHook(
                    phase=LifecyclePhase.P6_ARTIFACT_RECORDING,
                    hook_type=HookType.POST,
                    priority=100,
                    description="Record execution outputs as artifacts",
                ),
            ],
            privileges=[
                SecurityPrivilege(
                    resource="fs",
                    access="execute",
                    scope="/workspace/runs",
                    justification="Execute Python scripts in run directories",
                ),
                SecurityPrivilege(
                    resource="fs",
                    access="write",
                    scope="/workspace/blobs",
                    justification="Write output artifacts to content-addressed store",
                ),
            ],
            failure_semantics=FailureSemantics.FAIL_CLOSED,
            guarantees=[
                "Execution in isolated virtualenv",
                "stdout/stderr captured",
                "Resource limits enforced (POSIX)",
                "Failed runs produce artifacts",
            ],
            non_guarantees=[
                "No container/WASM isolation",
                "No network blocking",
                "Not safe for untrusted code",
            ],
            tags=["plugin", "adapter", "python", "execution"],
            metadata={
                "legacy_runner": "python",
                "legacy_category": "COMPUTE",
                "legacy_schema_version": "0.3",
            },
        )
        assert m.name == "python.local"
        assert m.kind == ModuleKind.ADAPTER
        assert m.provides_capability("python_execution")
        assert m.hooks_into_phase(LifecyclePhase.P5_EXECUTION)
        assert m.hooks_into_phase(LifecyclePhase.P6_ARTIFACT_RECORDING)
        assert len(m.privileges) == 2

    def test_graphviz_local_as_module_manifest(self):
        """graphviz.local plugin expressed as a ModuleManifest."""
        m = ModuleManifest(
            name="graphviz.local",
            version="0.1.0",
            description="Local Graphviz SVG renderer",
            kind=ModuleKind.ADAPTER,
            criticality=CriticalityLevel.OPTIONAL,
            provides=[
                CapabilityDeclaration(
                    name="graphviz_rendering",
                    version="1.0",
                    description="Render DOT graphs to SVG",
                ),
            ],
            lifecycle_hooks=[
                LifecycleHook(
                    phase=LifecyclePhase.P5_EXECUTION,
                    hook_type=HookType.PRE,
                    priority=100,
                    description="Render Graphviz DOT to SVG",
                ),
            ],
            privileges=[
                SecurityPrivilege(
                    resource="tool",
                    access="execute",
                    scope="dot",
                    justification="Execute Graphviz dot command",
                ),
            ],
            failure_semantics=FailureSemantics.DEGRADE,
            degradation_spec=DegradationSpec(
                affected_capabilities=["graphviz_rendering"],
                fallback_behavior="Return error message instead of SVG",
                max_degradation_duration_seconds=None,
            ),
            guarantees=["SVG output when Graphviz is installed"],
            non_guarantees=["Graphviz binary availability"],
            tags=["plugin", "adapter", "graphviz", "visualization"],
            metadata={
                "legacy_runner": "local_command",
                "legacy_category": "VISUALIZE",
                "legacy_schema_version": "0.3",
            },
        )
        assert m.name == "graphviz.local"
        assert m.provides_capability("graphviz_rendering")
        assert m.failure_semantics == FailureSemantics.DEGRADE
        assert m.degradation_spec is not None


# ---------------------------------------------------------------------------
# Enum Completeness
# ---------------------------------------------------------------------------


class TestEnumCompleteness:
    """Verify enum values are complete and consistent."""

    def test_lifecycle_phases_complete(self):
        phases = list(LifecyclePhase)
        assert len(phases) == 11
        assert phases[0].value.startswith("P0")
        assert phases[-1].value.startswith("P10")

    def test_module_kinds_complete(self):
        kinds = list(ModuleKind)
        expected = {
            "observer", "gate", "state_machine", "transformer",
            "verifier", "router", "scheduler", "adapter",
        }
        assert {k.value for k in kinds} == expected

    def test_failure_semantics_complete(self):
        fs = list(FailureSemantics)
        expected = {"fail_closed", "defer", "degrade", "require_human"}
        assert {f.value for f in fs} == expected

    def test_criticality_levels_complete(self):
        cl = list(CriticalityLevel)
        expected = {"required", "recommended", "optional"}
        assert {c.value for c in cl} == expected
