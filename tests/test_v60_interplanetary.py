"""
Tests for ProofFlow v6.0.0 (IpfsEventStore, Proof3DVisualizer, SelfTuningOptimizer)

Covers:
    - IpfsEventStore (IPFS CID multihash generation & retrieval)
    - Proof3DVisualizer (Three.js WebGL 3D topological manifold export)
    - SelfTuningOptimizer (AI model strategy hyper-parameter tuning)
"""

from __future__ import annotations

from uuid import uuid4

from schemamath_api.domain import Actor, ActorType, EventRecord
from schemamath_api.ipfs_event_store import IpfsEventStore
from schemamath_api.optimizer import SelfTuningOptimizer
from schemamath_api.visualizer import Proof3DVisualizer


class TestIpfsEventStore:
    def test_ipfs_cid_generation_and_retrieval(self):
        store = IpfsEventStore()
        ev = EventRecord(
            event_id=uuid4(),
            project_id=uuid4(),
            event_type="INTERPLANETARY_PROVED",
            timestamp="2026-08-01T00:00:00Z",
            actor=Actor(type=ActorType.MODEL, id="gpt4"),
            event_hash="ipfs_hash_1",
        )

        cid_rec = store.store_event(ev)
        assert cid_rec.cid.startswith("Qm")
        assert cid_rec.content_hash == "ipfs_hash_1"

        retrieved = store.retrieve_by_cid(cid_rec.cid)
        assert retrieved is not None
        assert retrieved.event_id == ev.event_id


class TestProof3DVisualizer:
    def test_generate_3d_manifold(self):
        visualizer = Proof3DVisualizer()
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

        graph = visualizer.generate_3d_manifold([ev1, ev2])
        assert len(graph.nodes) == 2
        assert "ProofFlow3DManifold" in graph.threejs_json
        assert graph.nodes[0].z == 0.0
        assert graph.nodes[1].z == 2.0


class TestSelfTuningOptimizer:
    def test_tune_strategy_low_success_rate(self):
        optimizer = SelfTuningOptimizer()
        cfg = optimizer.tune_strategy(recent_success_rate=0.3)

        assert cfg.temperature == 0.1
        assert cfg.recommended_role == "skeptic"

    def test_tune_strategy_high_success_rate(self):
        optimizer = SelfTuningOptimizer()
        cfg = optimizer.tune_strategy(recent_success_rate=0.8)

        assert cfg.temperature == 0.4
        assert cfg.recommended_role == "explorer"
