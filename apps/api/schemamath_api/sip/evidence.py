"""
@sip/evidence (F2: Audit Log and Evidence Ledger)

Records immutable audit entries for all operations, with configurable retention.

Usage:
    evidence_mod = EvidenceModule(retention="90d")
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
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


@dataclass
class AuditEntry:
    """A single audit entry recorded by @sip/evidence."""

    timestamp: str
    operation: str
    input_summary: dict[str, Any]
    output_summary: dict[str, Any]
    decision_summary: str
    phase_count: int


class EvidenceModule(SipModule):
    """
    F2: @sip/evidence module.

    Records audit trails in P6 and P9 and generates Markdown reports.
    """

    def __init__(self, retention: str = "90d") -> None:
        super().__init__(
            name="@sip/evidence",
            version="1.0.0",
            kind=ModuleKind.OBSERVER,
            description="Audit Trail and Evidence Retention Ledger",
            provides=[CapabilityDeclaration(name="audit_logging", version="1.0")],
        )

        self.retention = retention
        self.entries: list[AuditEntry] = []

        self._manifest.lifecycle_hooks = [
            LifecycleHook(
                phase=LifecyclePhase.P6_ARTIFACT_RECORDING,
                hook_type=HookType.POST,
                priority=100,
                description="Record audit log entry",
            ),
        ]

    def bind_hooks(self, scheduler: LifecycleScheduler) -> None:
        scheduler.register_hook(
            self.name,
            LifecyclePhase.P6_ARTIFACT_RECORDING,
            HookType.POST,
            100,
            self.record_audit,
        )

    def record_audit(self, ctx: LifecycleContext) -> ModuleDecision:
        """Record audit log entry into context and local entries list."""
        entry = AuditEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            operation=ctx.operation,
            input_summary={k: str(v)[:100] for k, v in ctx.input_data.items()},
            output_summary={k: str(v)[:100] for k, v in ctx.output_data.items()},
            decision_summary=f"{len(ctx.decisions)} decisions evaluated",
            phase_count=len(ctx.phase_log),
        )
        self.entries.append(entry)

        # Propose audit event for P9 commit
        ctx.propose_event({
            "event_type": "AUDIT_LOG_RECORDED",
            "payload": {
                "operation": ctx.operation,
                "retention": self.retention,
                "timestamp": entry.timestamp,
            },
        })

        return ModuleDecision(
            source_module=self.name,
            approval=Decision.ALLOW,
            capabilities={"audit_logging"},
        )

    def inspect(self) -> dict[str, Any]:
        """Return audit statistics."""
        return {
            "total_entries": len(self.entries),
            "retention_policy": self.retention,
            "operations_tracked": list({e.operation for e in self.entries}),
        }

    def export(self) -> str:
        """Export audit log as a Markdown report."""
        lines = [
            "# @sip/evidence Audit Report",
            f"- **Retention Policy**: {self.retention}",
            f"- **Total Audit Entries**: {len(self.entries)}",
            "",
            "## Audit Log Entries",
            "| Timestamp | Operation | Decisions |",
            "|---|---|---|",
        ]
        for e in self.entries:
            lines.append(f"| {e.timestamp} | {e.operation} | {e.decision_summary} |")

        return "\n".join(lines)


def createLedger(retention: str = "90d") -> EvidenceModule:
    """Helper factory matching JS-style createLedger({ retention })."""
    return EvidenceModule(retention=retention)
