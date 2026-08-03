"""
Tests for @sip Foundation Modules (F1: contract, F2: evidence, F3: permission, F4: partition)

Covers:
    - F1: @sip/contract input and output JSON Schema gate validation & fallback
    - F2: @sip/evidence audit logging, inspection stats, and Markdown export
    - F3: @sip/permission filesystem, network, and tool whitelisting fences
    - F4: @sip/partition workspace execution isolation
    - Progressive module composition via compose():
        - 1 module: F1 Hello World (~30 lines pattern)
        - 2 modules: F1 + F2
        - 3 modules: F1 + F2 + F3
        - 4 modules: F1 + F2 + F3 + F4
"""

from __future__ import annotations

from schemamath_api.k0.decision import Decision
from schemamath_api.sip import (
    compose,
    createFence,
    createGate,
    createLedger,
    createPartition,
)


class TestSipContractF1:
    def test_gate_valid_input_and_output(self):
        gate = createGate(
            input={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            output={"type": "object", "properties": {"answer": {"type": "string"}}, "required": ["answer"]},
        )
        sandbox = compose(gate)

        def echo_handler(ctx):
            ctx.output_data = {"answer": "42"}

        res = sandbox.run("query_task", input_data={"query": "meaning of life"}, core_handler=echo_handler)
        assert res.success is True
        assert res.final_decision.approval == Decision.ALLOW

    def test_gate_invalid_input_denied(self):
        gate = createGate(
            input={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
        )
        sandbox = compose(gate)

        res = sandbox.run("query_task", input_data={})  # Missing required 'query'
        assert res.success is False
        assert res.aborted_at.value == "P1_INPUT_NORMALIZATION"
        assert "Input validation failed" in res.abort_reason

    def test_gate_invalid_output_with_fallback(self):
        gate = createGate(
            output={"type": "object", "properties": {"answer": {"type": "string"}}, "required": ["answer"]},
            fallback={"answer": "Fallback answer"},
        )
        sandbox = compose(gate)

        def bad_handler(ctx):
            ctx.output_data = {"answer": 12345}  # Should be string

        res = sandbox.run("query_task", core_handler=bad_handler)
        assert res.success is True
        assert res.context.output_data == {"answer": "Fallback answer"}


class TestSipEvidenceF2:
    def test_audit_logging_and_export(self):
        ledger = createLedger(retention="30d")
        sandbox = compose(ledger)

        res = sandbox.run("task1", input_data={"arg": "val1"})
        assert res.success is True

        stats = ledger.inspect()
        assert stats["total_entries"] == 1
        assert stats["retention_policy"] == "30d"

        report = ledger.export()
        assert "# @sip/evidence Audit Report" in report
        assert "task1" in report


class TestSipPermissionF3:
    def test_fs_fence_allowed_and_denied(self, tmp_path):
        allowed_dir = tmp_path / "allowed"
        allowed_dir.mkdir()
        forbidden_dir = tmp_path / "forbidden"
        forbidden_dir.mkdir()

        fence = createFence(
            fs=[str(allowed_dir)],
            net=["api.openai.com"],
            tools=["python.local"],
        )
        sandbox = compose(fence)

        # Allowed FS call
        res1 = sandbox.run("fs_read", input_data={"requested_fs": str(allowed_dir / "file.txt")})
        assert res1.success is True

        # Denied FS call
        res2 = sandbox.run("fs_read", input_data={"requested_fs": str(forbidden_dir / "secret.txt")})
        assert res2.success is False
        assert "FS access denied" in res2.abort_reason

        # Denied Net call
        res3 = sandbox.run("net_call", input_data={"requested_net": "malicious.com"})
        assert res3.success is False
        assert "Network access denied" in res3.abort_reason


class TestSipPartitionF4:
    def test_partition_isolation(self):
        part = createPartition(mode="PROCESS")
        sandbox = compose(part)

        res = sandbox.run("compute_task")
        assert res.success is True
        assert "partition_dir" in res.context.module_state
        assert res.context.module_state["isolation_mode"] == "PROCESS"


class TestProgressiveComposition:
    def test_all_4_foundation_modules_composed(self, tmp_path):
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        sandbox = compose(
            createGate(
                input={"type": "object", "properties": {"msg": {"type": "string"}}, "required": ["msg"]},
                output={"type": "object", "properties": {"result": {"type": "string"}}, "required": ["result"]},
            ),
            createLedger(retention="90d"),
            createFence(
                fs=[str(workspace)],
                net=["api.openai.com"],
                tools=["python.local"],
            ),
            createPartition(mode="PROCESS"),
        )

        def core_compute(ctx):
            ctx.output_data = {"result": f"processed: {ctx.input_data['msg']}"}

        res = sandbox.run(
            "full_foundation_task",
            input_data={
                "msg": "hello",
                "requested_fs": str(workspace / "data.txt"),
            },
            core_handler=core_compute,
        )

        assert res.success is True
        assert res.context.output_data["result"] == "processed: hello"
        assert len(res.completed_phases) == 11
