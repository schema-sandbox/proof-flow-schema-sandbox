"""
Tests for K0 Trust Kernel — Lifecycle Scheduler

Covers:
    - LifecycleContext initialization and helper methods
    - LifecycleScheduler hook, handler, and gate registration
    - Fixed phase execution order (P0 -> P10)
    - Hook priority and PRE/POST hook ordering
    - Core handler execution timing
    - Early termination on DENY or Gate condition failure
    - Module failure semantics handling during hook errors
    - Audit logging and introspection
"""

from __future__ import annotations

import pytest

from schemamath_api.k0.decision import (
    Decision,
    DecisionMerger,
    ModuleDecision,
)
from schemamath_api.k0.lifecycle import (
    LifecycleContext,
    LifecycleResult,
    LifecycleScheduler,
    PhaseLogEntry,
)
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
)
from schemamath_api.k0.registry import ManifestRegistry


# ---------------------------------------------------------------------------
# Helpers & Fixtures
# ---------------------------------------------------------------------------

def _make_manifest(
    name: str = "@sip/gate-module",
    failure_semantics: FailureSemantics = FailureSemantics.FAIL_CLOSED,
    degradation_spec: DegradationSpec | None = None,
) -> ModuleManifest:
    return ModuleManifest(
        name=name,
        version="1.0.0",
        kind=ModuleKind.GATE,
        provides=[CapabilityDeclaration(name="gate_capability")],
        failure_semantics=failure_semantics,
        degradation_spec=degradation_spec,
    )


@pytest.fixture
def registry() -> ManifestRegistry:
    reg = ManifestRegistry()
    reg.register(_make_manifest("@sip/mod1"))
    reg.register(_make_manifest("@sip/mod2"))
    reg.register(
        _make_manifest(
            "@sip/degrade-mod",
            failure_semantics=FailureSemantics.DEGRADE,
            degradation_spec=DegradationSpec(
                affected_capabilities=["gate_capability"],
                fallback_behavior="Log error and continue",
            ),
        )
    )
    reg.freeze()
    return reg


# ---------------------------------------------------------------------------
# LifecycleContext Tests
# ---------------------------------------------------------------------------

class TestLifecycleContext:
    def test_context_defaults(self):
        ctx = LifecycleContext(operation="test_op")
        assert ctx.operation == "test_op"
        assert ctx.input_data == {}
        assert ctx.output_data == {}
        assert ctx.proposed_artifacts == []
        assert ctx.proposed_events == []
        assert ctx.decisions == []
        assert ctx.aborted is False

    def test_context_mutations(self):
        ctx = LifecycleContext(operation="op")
        ctx.add_decision(ModuleDecision(source_module="mod1", approval=Decision.ALLOW))
        ctx.propose_event({"event_type": "TEST"})
        ctx.propose_artifact({"artifact_id": "123"})

        assert len(ctx.decisions) == 1
        assert len(ctx.proposed_events) == 1
        assert len(ctx.proposed_artifacts) == 1


# ---------------------------------------------------------------------------
# LifecycleScheduler Execution Tests
# ---------------------------------------------------------------------------

class TestLifecycleSchedulerExecution:
    def test_empty_scheduler_executes_all_phases(self, registry):
        scheduler = LifecycleScheduler(registry)
        ctx = LifecycleContext(operation="run_all")
        result = scheduler.execute(ctx)

        assert result.success is True
        assert len(result.completed_phases) == 11
        assert result.completed_phases[0] == LifecyclePhase.P0_LOAD_ATTEST
        assert result.completed_phases[-1] == LifecyclePhase.P10_TEARDOWN_COMPACT
        assert result.final_decision.approval == Decision.ALLOW

    def test_execution_order_and_priority(self, registry):
        scheduler = LifecycleScheduler(registry)
        order: list[str] = []

        def pre_hook1(ctx: LifecycleContext) -> ModuleDecision:
            order.append("P1_pre_p20")
            return ModuleDecision(source_module="@sip/mod1", approval=Decision.ALLOW)

        def pre_hook2(ctx: LifecycleContext) -> ModuleDecision:
            order.append("P1_pre_p10")
            return ModuleDecision(source_module="@sip/mod2", approval=Decision.ALLOW)

        def core_handler(ctx: LifecycleContext) -> None:
            order.append("P1_core")

        def post_hook(ctx: LifecycleContext) -> ModuleDecision:
            order.append("P1_post")
            return ModuleDecision(source_module="@sip/mod1", approval=Decision.ALLOW)

        scheduler.register_hook(
            "@sip/mod1", LifecyclePhase.P1_INPUT_NORMALIZATION, HookType.PRE, 20, pre_hook1
        )
        scheduler.register_hook(
            "@sip/mod2", LifecyclePhase.P1_INPUT_NORMALIZATION, HookType.PRE, 10, pre_hook2
        )
        scheduler.register_core_handler(LifecyclePhase.P1_INPUT_NORMALIZATION, core_handler)
        scheduler.register_hook(
            "@sip/mod1", LifecyclePhase.P1_INPUT_NORMALIZATION, HookType.POST, 10, post_hook
        )

        ctx = LifecycleContext(operation="order_test")
        result = scheduler.execute(ctx)

        assert result.success is True
        assert order == ["P1_pre_p10", "P1_pre_p20", "P1_core", "P1_post"]

    def test_pre_hook_deny_aborts_lifecycle(self, registry):
        scheduler = LifecycleScheduler(registry)

        def deny_hook(ctx: LifecycleContext) -> ModuleDecision:
            return ModuleDecision(
                source_module="@sip/mod1",
                approval=Decision.DENY,
                reason="Unauthorized operation",
            )

        executed_p5 = False

        def core_p5(ctx: LifecycleContext) -> None:
            nonlocal executed_p5
            executed_p5 = True

        scheduler.register_hook(
            "@sip/mod1", LifecyclePhase.P2_GOAL_BINDING, HookType.PRE, 10, deny_hook
        )
        scheduler.register_core_handler(LifecyclePhase.P5_EXECUTION, core_p5)

        ctx = LifecycleContext(operation="deny_test")
        result = scheduler.execute(ctx)

        assert result.success is False
        assert result.aborted_at == LifecyclePhase.P2_GOAL_BINDING
        assert "DENIED at P2_GOAL_BINDING:pre" in result.abort_reason
        assert executed_p5 is False
        assert LifecyclePhase.P0_LOAD_ATTEST in result.completed_phases
        assert LifecyclePhase.P1_INPUT_NORMALIZATION in result.completed_phases
        assert LifecyclePhase.P2_GOAL_BINDING not in result.completed_phases

    def test_gate_condition_failure(self, registry):
        scheduler = LifecycleScheduler(registry)

        def fail_gate(ctx: LifecycleContext) -> str | None:
            return "Goal not bound"

        scheduler.register_gate(LifecyclePhase.P2_GOAL_BINDING, fail_gate)

        ctx = LifecycleContext(operation="gate_test")
        result = scheduler.execute(ctx)

        assert result.success is False
        assert result.aborted_at == LifecyclePhase.P2_GOAL_BINDING
        assert "Gate failed at P2_GOAL_BINDING: Goal not bound" in result.abort_reason


# ---------------------------------------------------------------------------
# Module Failure Semantics Tests
# ---------------------------------------------------------------------------

class TestLifecycleSchedulerFailureSemantics:
    def test_fail_closed_on_hook_exception(self, registry):
        scheduler = LifecycleScheduler(registry)

        def failing_hook(ctx: LifecycleContext) -> ModuleDecision:
            raise RuntimeError("Unexpected boom")

        scheduler.register_hook(
            "@sip/mod1", LifecyclePhase.P1_INPUT_NORMALIZATION, HookType.PRE, 10, failing_hook
        )

        ctx = LifecycleContext(operation="fail_closed_test")
        result = scheduler.execute(ctx)

        assert result.success is False
        assert result.aborted_at == LifecyclePhase.P1_INPUT_NORMALIZATION
        assert "fail_closed" in result.abort_reason

    def test_degrade_on_hook_exception(self, registry):
        scheduler = LifecycleScheduler(registry)

        def failing_hook(ctx: LifecycleContext) -> ModuleDecision:
            raise RuntimeError("Minor glitch")

        scheduler.register_hook(
            "@sip/degrade-mod",
            LifecyclePhase.P1_INPUT_NORMALIZATION,
            HookType.PRE,
            10,
            failing_hook,
        )

        ctx = LifecycleContext(operation="degrade_test")
        result = scheduler.execute(ctx)

        assert result.success is True
        assert len(result.completed_phases) == 11
        # Check log entry recorded error
        error_logs = [log for log in ctx.phase_log if log.error is not None]
        assert len(error_logs) == 1
        assert "Minor glitch" in error_logs[0].error


# ---------------------------------------------------------------------------
# Introspection Tests
# ---------------------------------------------------------------------------

class TestLifecycleSchedulerIntrospection:
    def test_scheduler_stats(self, registry):
        scheduler = LifecycleScheduler(registry)
        scheduler.register_hook(
            "@sip/mod1", LifecyclePhase.P0_LOAD_ATTEST, HookType.PRE, 10, lambda ctx: ModuleDecision(source_module="mod1", approval=Decision.ALLOW)
        )
        scheduler.register_core_handler(LifecyclePhase.P5_EXECUTION, lambda ctx: None)

        assert scheduler.registered_hook_count() == 1
        assert scheduler.phases_with_hooks() == {LifecyclePhase.P0_LOAD_ATTEST}
        assert scheduler.phases_with_core_handlers() == {LifecyclePhase.P5_EXECUTION}
