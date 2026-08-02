"""
Tests for ProofFlow v5.0.0 (Python SDK, Prometheus Telemetry, Cloud Distribution)

Covers:
    - proofflow SDK (proofflow.init & compose_sandbox quick start API)
    - TelemetryExporter (Prometheus /metrics formatting & /healthz diagnostics)
    - docker-compose.prod.yml configuration validation
"""

from __future__ import annotations

from pathlib import Path

from schemamath_api import sdk
from schemamath_api.sip import createFence
from schemamath_api.telemetry import TelemetryExporter


class TestProofFlowSDK:
    def test_proofflow_sdk_init_and_sandbox_execution(self, tmp_path):
        client = sdk.init()
        assert client is not None

        ws = tmp_path / "ws"
        ws.mkdir()
        sandbox = client.compose_sandbox([
            createFence(fs=[str(ws)]),
        ])
        res = sandbox.run("sdk_test_step", input_data={"requested_fs": str(ws / "file.txt")})
        assert res.success is True
        assert len(res.completed_phases) == 11


class TestTelemetryExporter:
    def test_healthz_and_prometheus_metrics(self):
        exporter = TelemetryExporter()
        exporter.record_execution(success=True)
        exporter.record_execution(success=False)

        health = exporter.get_healthz()
        assert health.status == "ok"
        assert health.version == "5.0.0"

        metrics = exporter.export_prometheus_metrics()
        assert "proofflow_executions_total 2" in metrics
        assert "proofflow_executions_successful 1" in metrics


class TestDockerComposeProdConfig:
    def test_docker_compose_prod_is_self_contained_and_hardened(self):
        repo_root = Path(__file__).resolve().parents[1]
        prod_file = repo_root / "docker-compose.prod.yml"
        assert prod_file.exists()
        content = prod_file.read_text(encoding="utf-8")
        assert "proofflow/proofflow-api:" in content
        assert "127.0.0.1:8000:8000" in content
        assert "read_only: true" in content
        assert "no-new-privileges:true" in content
        assert "PROOFFLOW_AUTH_ENABLED" in content
        assert "PROOFFLOW_ALLOW_LOCAL_PLUGINS" in content
        assert "tmpfs" in content
