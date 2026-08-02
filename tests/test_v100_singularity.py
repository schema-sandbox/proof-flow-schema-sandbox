"""
Tests for ProofFlow v10.0.0 (UniversalKnowledgeMesh & SingularityHub)

Covers:
    - UniversalKnowledgeMesh (planetary node registration & event log synchronization)
    - SingularityHub (global epistemic summary calculation & omniscient status)
"""

from __future__ import annotations

import pytest
from uuid import uuid4

from schemamath_api.domain import Actor, ActorType, EventRecord
from schemamath_api.singularity_hub import SingularityHub
from schemamath_api.universal_mesh import UniversalKnowledgeMesh


class TestUniversalKnowledgeMesh:
    def test_node_registration_and_event_sync(self):
        mesh = UniversalKnowledgeMesh()
        mesh.register_node("earth_node_1", "Earth Primary")

        ev1 = EventRecord(
            event_id=uuid4(),
            project_id=uuid4(),
            event_type="THEOREM_PROVED",
            timestamp="2026-08-01T00:00:00Z",
            actor=Actor(type=ActorType.MODEL, id="gpt4"),
            event_hash="hash_earth_1",
        )

        synced = mesh.sync_events("earth_node_1", [ev1])
        assert synced == 1
        assert len(mesh.synchronized_events) == 1

        # Idempotent deduplication
        synced_again = mesh.sync_events("earth_node_1", [ev1])
        assert synced_again == 0


class TestSingularityHub:
    def test_compute_global_summary(self):
        mesh = UniversalKnowledgeMesh()
        hub = SingularityHub(mesh)

        mesh.register_node("mars_node_1", "Mars Relay")
        ev = EventRecord(
            event_id=uuid4(),
            project_id=uuid4(),
            event_type="AXIOM_SYNTHESIZED",
            timestamp="2026-08-01T00:00:00Z",
            actor=Actor(type=ActorType.MODEL, id="claude"),
            event_hash="hash_mars_1",
        )
        mesh.sync_events("mars_node_1", [ev])

        summary = hub.compute_global_summary()
        assert summary.total_verified_theorems == 0
        assert summary.active_planetary_nodes == 1
        assert summary.status == "EXPERIMENTAL_UNVERIFIED"
        assert summary.global_epistemic_score == 0.0
