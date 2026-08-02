"""
K0 Trust Kernel — Lifecycle Scheduler

Instead of arbitrary compose() middleware chains where safety depends
on loading order, execution follows fixed phases P0→P10.  Modules
register hooks into specific phases; the LifecycleScheduler runs
them in the correct order.

Execution model:
    For each phase P0 through P10:
        1. Run all PRE hooks (sorted by priority, ascending)
        2. Run the phase's core handler (if registered)
        3. Run all POST hooks (sorted by priority, ascending)
        4. Merge all decisions from hooks
        5. If merged decision is DENY → abort remaining phases

    The scheduler never executes side-effects itself.  Side-effects
    are proposals that the TransactionExecutor commits in P9.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

from schemamath_api.k0.decision import (
    Decision,
    DecisionMerger,
    MergedDecision,
    ModuleDecision,
)
from schemamath_api.k0.manifest import (
    HookType,
    LifecyclePhase,
    ModuleManifest,
)
from schemamath_api.k0.registry import ManifestRegistry

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Context — passed through the lifecycle
# ---------------------------------------------------------------------------

@dataclass
class LifecycleContext:
    """
    Mutable context that flows through all lifecycle phases.

    Each phase and hook can read from and write to this context.
    The context accumulates state as phases execute.
    """

    # The operation being performed
    operation: str = ""
    """Name of the operation, e.g. 'create_route', 'add_artifact'."""

    # Input data for the operation
    input_data: dict[str, Any] = field(default_factory=dict)

    # Accumulated outputs from phases
    output_data: dict[str, Any] = field(default_factory=dict)

    # Artifacts proposed during execution (committed in P9)
    proposed_artifacts: list[dict[str, Any]] = field(default_factory=list)

    # Events proposed during execution (committed in P9)
    proposed_events: list[dict[str, Any]] = field(default_factory=list)

    # Decisions collected from hooks
    decisions: list[ModuleDecision] = field(default_factory=list)

    # Phase execution log (for audit trail)
    phase_log: list[PhaseLogEntry] = field(default_factory=list)

    # Arbitrary per-module state (keyed by module name)
    module_state: dict[str, Any] = field(default_factory=dict)

    # Whether the lifecycle was aborted early
    aborted: bool = False
    abort_reason: str = ""
    abort_phase: LifecyclePhase | None = None

    def add_decision(self, decision: ModuleDecision) -> None:
        """Add a module decision to the context."""
        self.decisions.append(decision)

    def propose_event(self, event: dict[str, Any]) -> None:
        """Propose an event to be committed in P9."""
        self.proposed_events.append(event)

    def propose_artifact(self, artifact: dict[str, Any]) -> None:
        """Propose an artifact to be recorded in P6."""
        self.proposed_artifacts.append(artifact)


@dataclass(frozen=True)
class PhaseLogEntry:
    """Record of a phase execution for audit purposes."""

    phase: LifecyclePhase
    hook_type: HookType | None  # None for core handler
    module_name: str | None  # None for core handler
    decision: Decision | None
    duration_ms: float
    error: str | None = None


# ---------------------------------------------------------------------------
# Hook Protocol — what modules implement
# ---------------------------------------------------------------------------

class LifecycleHookFn(Protocol):
    """
    Protocol for lifecycle hook functions.

    A hook receives the lifecycle context and returns a ModuleDecision.
    It may modify the context (add outputs, propose events, etc.)
    but must NOT perform side-effects (disk I/O, network calls).
    """

    def __call__(self, ctx: LifecycleContext) -> ModuleDecision: ...


# Type for core phase handlers (registered by the application, not modules)
PhaseHandler = Callable[[LifecycleContext], None]


# ---------------------------------------------------------------------------
# Lifecycle Result
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LifecycleResult:
    """Final result of a complete lifecycle execution."""

    success: bool
    """Whether all phases completed without DENY."""

    final_decision: MergedDecision
    """The merged decision from all modules across all phases."""

    completed_phases: list[LifecyclePhase]
    """Phases that were fully executed."""

    aborted_at: LifecyclePhase | None = None
    """Phase where execution was aborted (if any)."""

    abort_reason: str = ""
    """Why execution was aborted."""

    context: LifecycleContext | None = None
    """The final context state (for debugging / audit)."""

    duration_ms: float = 0.0
    """Total execution duration in milliseconds."""


# ---------------------------------------------------------------------------
# Lifecycle Scheduler
# ---------------------------------------------------------------------------

class LifecycleScheduler:
    """
    Schedules and executes lifecycle phases P0→P10 in fixed order.

    Usage:
        registry = ManifestRegistry()
        # ... register modules ...
        registry.freeze()

        scheduler = LifecycleScheduler(registry)
        scheduler.register_core_handler(LifecyclePhase.P5_EXECUTION, my_handler)

        # Register hook implementations from modules
        scheduler.register_hook("@sip/contract", LifecyclePhase.P1_INPUT_NORMALIZATION,
                                HookType.PRE, 10, my_validation_hook)

        ctx = LifecycleContext(operation="create_route", input_data={...})
        result = scheduler.execute(ctx)
    """

    def __init__(
        self,
        registry: ManifestRegistry,
        *,
        decision_merger: DecisionMerger | None = None,
    ) -> None:
        self._registry = registry
        self._merger = decision_merger or DecisionMerger()

        # Hook implementations: (module_name, phase, hook_type) -> function
        self._hooks: dict[
            tuple[str, LifecyclePhase, HookType], list[tuple[int, LifecycleHookFn]]
        ] = {}

        # Core phase handlers (application logic, not module hooks)
        self._core_handlers: dict[LifecyclePhase, PhaseHandler] = {}

        # Phase gate conditions
        self._gate_conditions: dict[
            LifecyclePhase, list[Callable[[LifecycleContext], str | None]]
        ] = {}

    # --- Registration -------------------------------------------------------

    def register_hook(
        self,
        module_name: str,
        phase: LifecyclePhase,
        hook_type: HookType,
        priority: int,
        fn: LifecycleHookFn,
    ) -> None:
        """
        Register a hook function for a module at a specific phase.

        Args:
            module_name: Name of the module providing this hook.
            phase: Which lifecycle phase to hook into.
            hook_type: PRE or POST.
            priority: Execution priority (lower = earlier).
            fn: The hook function to execute.
        """
        key = (module_name, phase, hook_type)
        if key not in self._hooks:
            self._hooks[key] = []
        self._hooks[key].append((priority, fn))
        logger.debug(
            "Registered hook: %s %s:%s @%d",
            module_name,
            phase.value,
            hook_type.value,
            priority,
        )

    def register_core_handler(
        self, phase: LifecyclePhase, handler: PhaseHandler
    ) -> None:
        """
        Register the core handler for a phase.

        Core handlers contain the application's business logic for that phase.
        There can be only one core handler per phase.
        """
        if phase in self._core_handlers:
            logger.warning(
                "Overwriting existing core handler for phase %s", phase.value
            )
        self._core_handlers[phase] = handler

    def register_gate(
        self,
        phase: LifecyclePhase,
        condition: Callable[[LifecycleContext], str | None],
    ) -> None:
        """
        Register a gate condition for a phase.

        The condition is called after all hooks and the core handler.
        If it returns a string (error message), the phase fails.
        If it returns None, the phase passes.
        """
        self._gate_conditions.setdefault(phase, []).append(condition)

    # --- Execution ----------------------------------------------------------

    def execute(self, ctx: LifecycleContext) -> LifecycleResult:
        """
        Execute all lifecycle phases P0→P10 in order.

        For each phase:
            1. Run PRE hooks (sorted by priority)
            2. Run core handler
            3. Run POST hooks (sorted by priority)
            4. Check gate conditions
            5. Merge decisions — if DENY, abort

        Args:
            ctx: The lifecycle context to pass through all phases.

        Returns:
            LifecycleResult with success/failure and audit trail.
        """
        start = time.perf_counter()
        completed: list[LifecyclePhase] = []
        all_decisions: list[ModuleDecision] = []

        for phase in LifecyclePhase:
            phase_result = self._execute_phase(phase, ctx)

            if phase_result.decisions:
                all_decisions.extend(phase_result.decisions)

            if phase_result.aborted:
                ctx.aborted = True
                ctx.abort_reason = phase_result.abort_reason
                ctx.abort_phase = phase

                elapsed = (time.perf_counter() - start) * 1000
                return LifecycleResult(
                    success=False,
                    final_decision=self._merger.merge(all_decisions),
                    completed_phases=completed,
                    aborted_at=phase,
                    abort_reason=phase_result.abort_reason,
                    context=ctx,
                    duration_ms=elapsed,
                )

            completed.append(phase)

        elapsed = (time.perf_counter() - start) * 1000
        final_decision = self._merger.merge(all_decisions) if all_decisions else MergedDecision(
            approval=Decision.ALLOW,
        )

        return LifecycleResult(
            success=True,
            final_decision=final_decision,
            completed_phases=completed,
            context=ctx,
            duration_ms=elapsed,
        )

    # --- Internal phase execution -------------------------------------------

    def _execute_phase(
        self, phase: LifecyclePhase, ctx: LifecycleContext
    ) -> _PhaseResult:
        """Execute a single lifecycle phase with all its hooks."""
        decisions: list[ModuleDecision] = []

        # 1. PRE hooks
        pre_hooks = self._collect_hooks(phase, HookType.PRE)
        for module_name, priority, fn in pre_hooks:
            result = self._run_hook(phase, HookType.PRE, module_name, fn, ctx)
            if result is not None:
                decisions.append(result)
                # Check for immediate DENY
                if result.approval == Decision.DENY:
                    return _PhaseResult(
                        aborted=True,
                        abort_reason=(
                            f"Module '{module_name}' DENIED at "
                            f"{phase.value}:pre — {result.reason}"
                        ),
                        decisions=decisions,
                    )

        # 2. Core handler
        if phase in self._core_handlers:
            self._run_core_handler(phase, ctx)

        # 3. POST hooks
        post_hooks = self._collect_hooks(phase, HookType.POST)
        for module_name, priority, fn in post_hooks:
            result = self._run_hook(phase, HookType.POST, module_name, fn, ctx)
            if result is not None:
                decisions.append(result)
                if result.approval == Decision.DENY:
                    return _PhaseResult(
                        aborted=True,
                        abort_reason=(
                            f"Module '{module_name}' DENIED at "
                            f"{phase.value}:post — {result.reason}"
                        ),
                        decisions=decisions,
                    )

        # 4. Gate conditions
        gate_error = self._check_gates(phase, ctx)
        if gate_error:
            return _PhaseResult(
                aborted=True,
                abort_reason=f"Gate failed at {phase.value}: {gate_error}",
                decisions=decisions,
            )

        # 5. Phase-level decision merge
        if decisions:
            phase_merged = self._merger.merge(decisions)
            if phase_merged.is_denied:
                return _PhaseResult(
                    aborted=True,
                    abort_reason=(
                        f"Merged decision DENIED at {phase.value}: "
                        + "; ".join(phase_merged.denial_reasons)
                    ),
                    decisions=decisions,
                )

        return _PhaseResult(aborted=False, decisions=decisions)

    def _collect_hooks(
        self, phase: LifecyclePhase, hook_type: HookType
    ) -> list[tuple[str, int, LifecycleHookFn]]:
        """
        Collect all hooks for a phase+type, sorted by priority.

        Returns list of (module_name, priority, fn).
        """
        result: list[tuple[str, int, LifecycleHookFn]] = []
        for (mod_name, ph, ht), hook_list in self._hooks.items():
            if ph == phase and ht == hook_type:
                for priority, fn in hook_list:
                    result.append((mod_name, priority, fn))

        # Sort by priority ascending (lower = earlier)
        result.sort(key=lambda x: x[1])
        return result

    def _run_hook(
        self,
        phase: LifecyclePhase,
        hook_type: HookType,
        module_name: str,
        fn: LifecycleHookFn,
        ctx: LifecycleContext,
    ) -> ModuleDecision | None:
        """Run a single hook and record timing."""
        start = time.perf_counter()
        error_msg = None
        decision = None

        try:
            decision = fn(ctx)
        except Exception as exc:
            error_msg = f"{type(exc).__name__}: {exc}"
            logger.error(
                "Hook %s at %s:%s failed: %s",
                module_name,
                phase.value,
                hook_type.value,
                error_msg,
            )
            # Hook failure → check module's failure semantics
            manifest = self._registry.get(module_name)
            if manifest:
                from schemamath_api.k0.manifest import FailureSemantics

                if manifest.failure_semantics == FailureSemantics.FAIL_CLOSED:
                    decision = ModuleDecision(
                        source_module=module_name,
                        approval=Decision.DENY,
                        reason=f"Hook failed (fail_closed): {error_msg}",
                    )
                elif manifest.failure_semantics == FailureSemantics.REQUIRE_HUMAN:
                    decision = ModuleDecision(
                        source_module=module_name,
                        approval=Decision.REQUIRE_HUMAN,
                        reason=f"Hook failed (require_human): {error_msg}",
                    )
                elif manifest.failure_semantics == FailureSemantics.DEFER:
                    decision = ModuleDecision(
                        source_module=module_name,
                        approval=Decision.DEFER,
                        reason=f"Hook failed (defer): {error_msg}",
                    )
                else:
                    # DEGRADE — allow but note the degradation
                    decision = ModuleDecision(
                        source_module=module_name,
                        approval=Decision.ALLOW,
                        reason=f"Hook failed (degrade): {error_msg}",
                    )
            else:
                # Unknown module → fail closed
                decision = ModuleDecision(
                    source_module=module_name,
                    approval=Decision.DENY,
                    reason=f"Hook failed (unknown module): {error_msg}",
                )

        elapsed = (time.perf_counter() - start) * 1000
        ctx.phase_log.append(
            PhaseLogEntry(
                phase=phase,
                hook_type=hook_type,
                module_name=module_name,
                decision=decision.approval if decision else None,
                duration_ms=elapsed,
                error=error_msg,
            )
        )

        return decision

    def _run_core_handler(
        self, phase: LifecyclePhase, ctx: LifecycleContext
    ) -> None:
        """Run the core handler for a phase."""
        start = time.perf_counter()
        error_msg = None

        try:
            self._core_handlers[phase](ctx)
        except Exception as exc:
            error_msg = f"{type(exc).__name__}: {exc}"
            logger.error("Core handler for %s failed: %s", phase.value, error_msg)
            raise

        elapsed = (time.perf_counter() - start) * 1000
        ctx.phase_log.append(
            PhaseLogEntry(
                phase=phase,
                hook_type=None,
                module_name=None,
                decision=None,
                duration_ms=elapsed,
                error=error_msg,
            )
        )

    def _check_gates(
        self, phase: LifecyclePhase, ctx: LifecycleContext
    ) -> str | None:
        """Check all gate conditions for a phase.  Returns error message or None."""
        conditions = self._gate_conditions.get(phase, [])
        for condition in conditions:
            error = condition(ctx)
            if error is not None:
                return error
        return None

    # --- Introspection ------------------------------------------------------

    def registered_hook_count(self) -> int:
        """Total number of registered hooks."""
        return sum(len(hooks) for hooks in self._hooks.values())

    def phases_with_hooks(self) -> set[LifecyclePhase]:
        """Return the set of phases that have at least one hook registered."""
        phases = set()
        for mod_name, phase, hook_type in self._hooks:
            phases.add(phase)
        return phases

    def phases_with_core_handlers(self) -> set[LifecyclePhase]:
        """Return the set of phases that have a core handler."""
        return set(self._core_handlers.keys())


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

@dataclass
class _PhaseResult:
    """Internal result of a single phase execution."""

    aborted: bool = False
    abort_reason: str = ""
    decisions: list[ModuleDecision] = field(default_factory=list)
