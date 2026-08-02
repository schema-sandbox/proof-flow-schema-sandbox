"""
Tests for ProofFlow v22.0 (Cloud Execution Infrastructure & Microservice Gateway)

Covers:
    - TenantIsolationManager (Quota, leaky bucket rate limiting, slot release)
    - MicroserviceGatewayRouter (HMAC signature verification & routing)
    - CloudClusterLoadBalancer (Consistent hashing & node selection)
    - ClusterMetricsAggregator (Heartbeat failover tracking)
"""

from __future__ import annotations

import hashlib
import pytest

from schemamath_api.cloud_gateway import (
    CloudClusterLoadBalancer,
    ClusterMetricsAggregator,
    MicroserviceGatewayRouter,
    ServiceNode,
    TenantIsolationManager,
)


class TestTenantIsolationManager:
    def test_register_and_quota_acquire(self):
        mgr = TenantIsolationManager()
        mgr.register_tenant("tenant_a", max_sandboxes=2, max_rpm=60)

        assert mgr.acquire_sandbox_slot("tenant_a") is True
        assert mgr.acquire_sandbox_slot("tenant_a") is True
        assert mgr.acquire_sandbox_slot("tenant_a") is False

        mgr.release_sandbox_slot("tenant_a")
        assert mgr.acquire_sandbox_slot("tenant_a") is True

    def test_rate_limiting(self):
        mgr = TenantIsolationManager()
        mgr.register_tenant("tenant_b", max_sandboxes=5, max_rpm=2)

        assert mgr.allow_request("tenant_b") is True
        assert mgr.allow_request("tenant_b") is True
        assert mgr.allow_request("tenant_b") is False


class TestMicroserviceGatewayRouter:
    def test_verify_signature_and_routing(self):
        router = MicroserviceGatewayRouter()
        payload = "req_1001"
        secret = "my_secret"
        sig = hashlib.sha256(f"{payload}:{secret}".encode()).hexdigest()

        assert router.verify_signature(payload, sig, secret) is True
        assert router.verify_signature(payload, "invalid_sig", secret) is False

        assert router.route_request("/api/v1/sandbox/create") == "sandbox_service"
        assert router.route_request("/api/v1/verifier/check") == "verifier_service"


class TestCloudClusterLoadBalancer:
    def test_load_balancer_selection(self):
        lb = CloudClusterLoadBalancer()
        n1 = ServiceNode(node_id="node_1", host="10.0.0.1", port=8000)
        n2 = ServiceNode(node_id="node_2", host="10.0.0.2", port=8000, is_healthy=False)
        lb.add_node(n1)
        lb.add_node(n2)

        selected = lb.select_node("request_key_abc")
        assert selected is not None
        assert selected.node_id == "node_1"

        aggregator = ClusterMetricsAggregator()
        assert aggregator.check_node_heartbeats(lb) == 1
