"""
Tests for ProofFlow v2.1.0 (MeshNode, GpuVerifierKernel, ProofDebugger)

Covers:
    - MeshNode (P2P block packaging, Merkle root verification, and peer sync)
    - GpuVerifierKernel (parallel SIMD assertion verification)
    - ProofDebugger (time-travel stepping forward/backward and jump)
"""

from __future__ import annotations

from uuid import uuid4

from schemamath_api.domain import Actor, ActorType, EventRecord
from schemamath_api.gpu_verifier import GpuVerifierKernel, ParallelAssertion
from schemamath_api.mesh import MeshBlock, MeshNode
from schemamath_api.proof_debugger import ProofDebugger


class TestMeshNode:
    def test_peer_connection_and_block_broadcast(self):
        node_a = MeshNode(node_id="node_a")
        node_b = MeshNode(node_id="node_b")

        node_a.connect_peer("ws://node_b:8080")
        assert "ws://node_b:8080" in node_a.known_peers

        ev = EventRecord(
            event_id=uuid4(),
            project_id=uuid4(),
            event_type="LEMMA_PROVED",
            timestamp="2026-08-01T00:00:00Z",
            actor=Actor(type=ActorType.MODEL, id="gpt4"),
            event_hash="dummy_hash_1",
        )

        block = node_a.broadcast_events([ev])
        assert block.block_id in node_a.synced_blocks

        # Node B receives block and validates Merkle root
        valid = node_b.receive_block(block)
        assert valid is True
        assert block.block_id in node_b.synced_blocks

    def test_corrupted_block_rejected(self):
        node = MeshNode()
        bad_block = MeshBlock(
            block_id="b_bad",
            node_id="attacker",
            event_records=[{"key": "data"}],
            merkle_root="invalid_hash_value",
        )
        assert node.receive_block(bad_block) is False


class TestGpuVerifierKernel:
    def test_batch_verify_assertions(self):
        kernel = GpuVerifierKernel(enable_simd=True)
        assertions = [
            ParallelAssertion(assertion_id="a1", expression="n + m == m + n", expected_val=True),
            ParallelAssertion(assertion_id="a2", expression="x * 0 == 0", expected_val=True),
        ]
        results = kernel.batch_verify_assertions(assertions)

        assert len(results) == 2
        assert results[0].valid is True
        assert results[1].valid is True
        assert results[0].verifier_name == "GpuVerifierKernel"


class TestProofDebugger:
    def test_time_travel_stepping(self):
        ev1 = EventRecord(
            event_id=uuid4(), project_id=uuid4(), event_type="STEP_1",
            timestamp="2026-08-01T00:00:00Z", actor=Actor(type=ActorType.HUMAN, id="u1"),
            event_hash="h1",
        )
        ev2 = EventRecord(
            event_id=uuid4(), project_id=uuid4(), event_type="STEP_2",
            timestamp="2026-08-01T00:00:01Z", actor=Actor(type=ActorType.HUMAN, id="u1"),
            event_hash="h2",
        )
        ev3 = EventRecord(
            event_id=uuid4(), project_id=uuid4(), event_type="STEP_3",
            timestamp="2026-08-01T00:00:02Z", actor=Actor(type=ActorType.HUMAN, id="u1"),
            event_hash="h3",
        )

        debugger = ProofDebugger([ev1, ev2, ev3])
        assert debugger.state.current_event.event_type == "STEP_1"

        debugger.step_forward()
        assert debugger.state.current_event.event_type == "STEP_2"

        debugger.step_forward()
        assert debugger.state.current_event.event_type == "STEP_3"

        debugger.step_backward()
        assert debugger.state.current_event.event_type == "STEP_2"

        debugger.jump_to_offset(0)
        assert debugger.state.current_event.event_type == "STEP_1"
