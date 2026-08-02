"""
@sip/contract (F1: Input/Output JSON Schema constraints)

Enforces JSON Schema validation on input data (P1) and output data (P8).

Usage:
    contract_mod = ContractModule(
        input_schema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
        output_schema={"type": "object", "properties": {"answer": {"type": "string"}}, "required": ["answer"]},
    )
"""

from __future__ import annotations

import logging
from typing import Any

import jsonschema

from schemamath_api.k0.decision import Decision, ModuleDecision
from schemamath_api.k0.lifecycle import (
    HookType,
    LifecycleContext,
    LifecyclePhase,
    LifecycleScheduler,
)
from schemamath_api.k0.manifest import (
    CapabilityDeclaration,
    FailureSemantics,
    LifecycleHook,
    ModuleKind,
)
from schemamath_api.sip.core import SipModule

logger = logging.getLogger(__name__)


class ContractModule(SipModule):
    """
    F1: @sip/contract module.

    Validates inputs (P1_INPUT_NORMALIZATION) and outputs (P8_RELEASE_AUTH)
    against JSON Schemas using jsonschema.
    """

    def __init__(
        self,
        input_schema: dict[str, Any] | None = None,
        output_schema: dict[str, Any] | None = None,
        fallback_output: dict[str, Any] | None = None,
        failure_semantics: FailureSemantics = FailureSemantics.FAIL_CLOSED,
    ) -> None:
        super().__init__(
            name="@sip/contract",
            version="1.0.0",
            kind=ModuleKind.GATE,
            description="Input and Output JSON Schema Validation Gate",
            provides=[CapabilityDeclaration(name="schema_validation", version="1.0")],
            failure_semantics=failure_semantics,
        )

        self.input_schema = input_schema
        self.output_schema = output_schema
        self.fallback_output = fallback_output

        # Update manifest lifecycle hooks
        hooks = []
        if self.input_schema:
            hooks.append(
                LifecycleHook(
                    phase=LifecyclePhase.P1_INPUT_NORMALIZATION,
                    hook_type=HookType.PRE,
                    priority=10,
                    description="Validate input_data against input_schema",
                )
            )
        if self.output_schema:
            hooks.append(
                LifecycleHook(
                    phase=LifecyclePhase.P8_RELEASE_AUTH,
                    hook_type=HookType.PRE,
                    priority=10,
                    description="Validate output_data against output_schema",
                )
            )

        self._manifest.lifecycle_hooks = hooks

    def bind_hooks(self, scheduler: LifecycleScheduler) -> None:
        if self.input_schema:
            scheduler.register_hook(
                self.name,
                LifecyclePhase.P1_INPUT_NORMALIZATION,
                HookType.PRE,
                10,
                self.validate_input,
            )
        if self.output_schema:
            scheduler.register_hook(
                self.name,
                LifecyclePhase.P8_RELEASE_AUTH,
                HookType.PRE,
                10,
                self.validate_output,
            )

    def validate_input(self, ctx: LifecycleContext) -> ModuleDecision:
        """Validate input_data against input_schema."""
        if not self.input_schema:
            return ModuleDecision(source_module=self.name, approval=Decision.ALLOW)

        violations = self._validate(ctx.input_data, self.input_schema)
        if not violations:
            return ModuleDecision(
                source_module=self.name,
                approval=Decision.ALLOW,
                capabilities={"schema_validation"},
            )

        return ModuleDecision(
            source_module=self.name,
            approval=Decision.DENY,
            reason=f"Input validation failed: {'; '.join(violations)}",
            metadata={"violations": violations},
        )

    def validate_output(self, ctx: LifecycleContext) -> ModuleDecision:
        """Validate output_data against output_schema."""
        if not self.output_schema:
            return ModuleDecision(source_module=self.name, approval=Decision.ALLOW)

        violations = self._validate(ctx.output_data, self.output_schema)
        if not violations:
            return ModuleDecision(
                source_module=self.name,
                approval=Decision.ALLOW,
                capabilities={"schema_validation"},
            )

        if self.fallback_output is not None:
            ctx.output_data = dict(self.fallback_output)
            logger.info("@sip/contract output invalid, replaced with fallback output")
            return ModuleDecision(
                source_module=self.name,
                approval=Decision.ALLOW,
                reason="Output validation failed but applied fallback output",
                metadata={"violations": violations, "fallback_applied": True},
            )

        return ModuleDecision(
            source_module=self.name,
            approval=Decision.DENY,
            reason=f"Output validation failed: {'; '.join(violations)}",
            metadata={"violations": violations},
        )

    def _validate(self, instance: Any, schema: dict[str, Any]) -> list[str]:
        validator = jsonschema.Draft202012Validator(schema)
        errors = list(validator.iter_errors(instance))
        return [f"{err.json_path}: {err.message}" for err in errors]


def createGate(
    output: dict[str, Any] | None = None,
    input: dict[str, Any] | None = None,
    fallback: dict[str, Any] | None = None,
) -> ContractModule:
    """Helper factory matching JS-style createGate({ output, input, fallback })."""
    return ContractModule(
        input_schema=input,
        output_schema=output,
        fallback_output=fallback,
    )
