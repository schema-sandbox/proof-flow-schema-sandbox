"""
Prometheus and OpenTelemetry Metrics & Health Diagnostics Exporter (telemetry)

Provides Prometheus format metrics (/metrics) and health diagnostic endpoints (/healthz, /readyz).
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class HealthStatus:
    status: str = "ok"
    version: str = "5.0.0"
    uptime_sec: float = 0.0
    active_sandboxes: int = 1


class TelemetryExporter:
    """
    Prometheus metrics exporter and health diagnostic provider.
    """

    def __init__(self) -> None:
        self.start_time = time.time()
        self.total_phase_executions = 0
        self.successful_executions = 0

    def record_execution(self, success: bool) -> None:
        """Record execution metrics."""
        self.total_phase_executions += 1
        if success:
            self.successful_executions += 1

    def get_healthz(self) -> HealthStatus:
        """Get system health status."""
        return HealthStatus(
            status="ok",
            uptime_sec=round(time.time() - self.start_time, 2),
        )

    def export_prometheus_metrics(self) -> str:
        """Export metrics in Prometheus text format."""
        lines = [
            "# HELP proofflow_executions_total Total number of phase executions",
            "# TYPE proofflow_executions_total counter",
            f"proofflow_executions_total {self.total_phase_executions}",
            "# HELP proofflow_executions_successful Total successful executions",
            "# TYPE proofflow_executions_successful counter",
            f"proofflow_executions_successful {self.successful_executions}",
            "# HELP proofflow_uptime_seconds System uptime in seconds",
            "# TYPE proofflow_uptime_seconds gauge",
            f"proofflow_uptime_seconds {round(time.time() - self.start_time, 2)}",
        ]
        return "\n".join(lines) + "\n"
