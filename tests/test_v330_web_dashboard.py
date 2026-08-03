"""
Tests for ProofFlow v33.0 (Full-Stack Web Dashboard API & GraphQL Epistemic Query Engine)

Covers:
    - EpistemicGraphQLRouter (GraphQL query execution & data resolving)
    - DashboardMetricsStream (Telemetry broadcast formatting)
    - InteractiveWorkbenchController (3D WebGL render configuration)
"""

from __future__ import annotations

from schemamath_api.web_dashboard_api import (
    DashboardMetricsStream,
    EpistemicGraphQLRouter,
    InteractiveWorkbenchController,
)


class TestWebDashboardApi:
    def test_graphql_router_and_telemetry(self):
        router = EpistemicGraphQLRouter()
        res = router.execute_query("{ theorems { id name status } }")
        assert "theorems" in res.data
        assert res.data["theorems"][0]["name"] == "Fermat-Wiles"

        stream = DashboardMetricsStream()
        evt = stream.broadcast_telemetry("cpu_utilization", 42.5)
        assert evt["event"] == "TELEMETRY_UPDATE"
        assert evt["value"] == 42.5

    def test_workbench_controller(self):
        controller = InteractiveWorkbenchController()
        cfg = controller.get_workbench_config("Klein_Bottle")
        assert cfg.manifold_type == "Klein_Bottle"
        assert cfg.enable_webgl_3d is True
        assert cfg.color_palette == "plasma"
