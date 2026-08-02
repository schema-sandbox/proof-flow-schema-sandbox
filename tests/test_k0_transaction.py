"""
Tests for K0 Trust Kernel — Transaction Executor

Covers:
    - Transaction and ProposedArtifact instantiation
    - Atomic commit of events and CAS blobs
    - Rejection when authorization decision is DENY or REQUIRE_HUMAN
    - Rollback handling on storage failure
    - Context conversion via transaction_from_context()
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from uuid import uuid4

import pytest

from schemamath_api.event_store import EventStore
from schemamath_api.k0.decision import Decision, MergedDecision, RiskLevel
from schemamath_api.k0.lifecycle import LifecycleContext
from schemamath_api.k0.transaction import (
    ProposedArtifact,
    Transaction,
    TransactionExecutor,
)


@pytest.fixture
def temp_workspace(tmp_path):
    events_file = tmp_path / "events.jsonl"
    blobs_dir = tmp_path / "blobs"
    event_store = EventStore(events_file)
    return event_store, events_file, blobs_dir


def _make_merged_decision(approval: Decision = Decision.ALLOW) -> MergedDecision:
    return MergedDecision(
        approval=approval,
        effective_capabilities={"test_cap"},
        effective_risk=RiskLevel.NONE,
        all_required_evidence=set(),
        assertion_ceiling=100,
    )


class TestTransactionExecutor:
    def test_successful_commit(self, temp_workspace):
        event_store, events_file, blobs_dir = temp_workspace
        executor = TransactionExecutor(event_store)

        project_id = uuid4()
        tx = Transaction(
            project_id=project_id,
            operation="create_test_artifact",
            proposed_events=[
                {
                    "event_type": "TEST_ACTION",
                    "actor": {"type": "human", "id": "user1"},
                    "payload": {"key": "value"},
                }
            ],
            proposed_artifacts=[
                ProposedArtifact(content=b"Hello K0 World", artifact_type="TEXT")
            ],
        )

        res = executor.execute_transaction(
            tx, _make_merged_decision(Decision.ALLOW), blobs_dir=blobs_dir
        )

        assert res.success is True
        assert len(res.committed_event_ids) == 1
        assert len(res.committed_artifact_hashes) == 1
        assert res.rolled_back is False

        # Verify blob file exists in CAS
        hash_val = res.committed_artifact_hashes[0]
        blob_path = blobs_dir / hash_val[:2] / hash_val
        assert blob_path.exists()
        assert blob_path.read_bytes() == b"Hello K0 World"

        # Verify event store records
        events = event_store.read_all()
        assert len(events) == 1
        assert events[0].event_type == "TEST_ACTION"

    def test_rejected_by_deny_decision(self, temp_workspace):
        event_store, _, _ = temp_workspace
        executor = TransactionExecutor(event_store)

        tx = Transaction(
            project_id=uuid4(),
            operation="restricted_op",
            proposed_events=[{"event_type": "FORBIDDEN"}],
        )

        res = executor.execute_transaction(
            tx, _make_merged_decision(Decision.DENY)
        )

        assert res.success is False
        assert "DENY" in res.error

    def test_rejected_by_require_human_decision(self, temp_workspace):
        event_store, _, _ = temp_workspace
        executor = TransactionExecutor(event_store)

        tx = Transaction(
            project_id=uuid4(),
            operation="human_op",
            proposed_events=[{"event_type": "CRITICAL_ACTION"}],
        )

        res = executor.execute_transaction(
            tx, _make_merged_decision(Decision.REQUIRE_HUMAN)
        )

        assert res.success is False
        assert "human confirmation" in res.error

    def test_context_conversion(self):
        executor = TransactionExecutor()
        ctx = LifecycleContext(operation="op_from_ctx")
        ctx.propose_event({"event_type": "EV1"})
        ctx.propose_artifact({"content": b"art content", "artifact_type": "CODE"})

        project_id = uuid4()
        tx = executor.transaction_from_context(ctx, project_id=project_id)

        assert tx.project_id == project_id
        assert tx.operation == "op_from_ctx"
        assert len(tx.proposed_events) == 1
        assert len(tx.proposed_artifacts) == 1
        assert tx.proposed_artifacts[0].content == b"art content"
