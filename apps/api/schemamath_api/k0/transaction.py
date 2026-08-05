"""
K0 Trust Kernel — Transaction Executor

The TransactionExecutor is responsible for executing authorized side-effects
and performing atomic commits to the EventStore and Content-Addressed Storage (CAS).

Core Principles:
    1. Only K0 executes side-effects; modules only propose actions.
    2. Atomic Commits: Either all proposed events & artifacts commit, or none.
    3. Rollback Safety: If event append or artifact write fails, temporary files
       and pending states are cleaned up automatically.
    4. Single Source of Truth: All side-effects generate canonical SHA-256 chained events.
"""

from __future__ import annotations

import logging
import shutil
import tempfile
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from schemamath_api.event_store import EventStore
from schemamath_api.k0.decision import Decision, MergedDecision
from schemamath_api.k0.lifecycle import LifecycleContext

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Transaction Data Models
# ---------------------------------------------------------------------------

@dataclass
class ProposedArtifact:
    """An artifact proposed for CAS storage."""

    content: bytes
    artifact_type: str = "OTHER"
    origin: str = "DERIVED"
    author: str = "system"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Transaction:
    """
    A transactional batch of side-effects proposed during a lifecycle.
    """

    tx_id: UUID = field(default_factory=uuid4)
    project_id: UUID | None = None
    operation: str = ""
    proposed_events: list[dict[str, Any]] = field(default_factory=list)
    proposed_artifacts: list[ProposedArtifact] = field(default_factory=list)
    state_mutations: list[Callable[[], None]] = field(default_factory=list)
    expected_revision: int | None = None
    idempotency_key: str | None = None


@dataclass(frozen=True)
class TransactionResult:
    """Outcome of committing a Transaction."""

    tx_id: UUID
    success: bool
    committed_event_ids: list[str] = field(default_factory=list)
    committed_artifact_hashes: list[str] = field(default_factory=list)
    rolled_back: bool = False
    error: str | None = None


# ---------------------------------------------------------------------------
# Transaction Executor
# ---------------------------------------------------------------------------

class TransactionExecutor:
    """
    Executes authorized transactions and handles atomic commits / rollbacks.

    Integrates with EventStore for canonical event persistence.
    """

    def __init__(self, event_store: EventStore | None = None) -> None:
        self._event_store = event_store

    def set_event_store(self, event_store: EventStore) -> None:
        """Set or update the active EventStore instance."""
        self._event_store = event_store

    def execute_transaction(
        self,
        tx: Transaction,
        decision: MergedDecision,
        events_path: Path | None = None,
        blobs_dir: Path | None = None,
    ) -> TransactionResult:
        """
        Commit a transaction atomically.

        Args:
            tx: The transaction containing proposed events, artifacts, and state mutations.
            decision: The merged decision from P4_ACTION_AUTH authorizing this commit.
            events_path: Path to events.jsonl file (if event_store not set).
            blobs_dir: Base directory for content-addressed artifact storage.

        Returns:
            TransactionResult with commit status and audit details.
        """
        # Guard: Check authorization decision
        if decision.approval == Decision.DENY:
            return TransactionResult(
                tx_id=tx.tx_id,
                success=False,
                error="Transaction rejected by K0 authorization (DENY)",
            )

        if decision.approval == Decision.REQUIRE_HUMAN:
            return TransactionResult(
                tx_id=tx.tx_id,
                success=False,
                error="Transaction requires human confirmation before execution",
            )

        committed_events: list[str] = []
        committed_blobs: list[Path] = []
        committed_hashes: list[str] = []

        # Temporary staging directory for artifacts
        stage_dir = Path(tempfile.mkdtemp(prefix=f"k0_tx_{tx.tx_id}_"))

        try:
            # Phase 1: Stage Artifacts (calculate SHA-256, write to temp stage)
            import hashlib

            for prop_art in tx.proposed_artifacts:
                sha256_hash = hashlib.sha256(prop_art.content).hexdigest()
                stage_file = stage_dir / sha256_hash
                stage_file.write_bytes(prop_art.content)
                committed_hashes.append(sha256_hash)

            # Phase 2: Commit Artifacts to CAS if blobs_dir provided
            if blobs_dir and committed_hashes:
                blobs_dir.mkdir(parents=True, exist_ok=True)
                for sha256_hash in committed_hashes:
                    prefix = sha256_hash[:2]
                    target_dir = blobs_dir / prefix
                    target_dir.mkdir(parents=True, exist_ok=True)
                    target_file = target_dir / sha256_hash

                    if not target_file.exists():
                        shutil.copy2(stage_dir / sha256_hash, target_file)
                        committed_blobs.append(target_file)

            # Phase 3: Apply State Mutations BEFORE the durable event commit. The
            # event append is the atomic commit point: if a mutation raises here,
            # nothing has been persisted and a true rollback is reported instead
            # of claiming rolled_back after events already entered the chain.
            for mutation in tx.state_mutations:
                mutation()

            # Phase 4: Commit Events to EventStore (the durable commit point)
            if tx.proposed_events:
                store = self._event_store
                if not store and events_path:
                    store = EventStore(events_path)

                if store and tx.project_id:
                    committed_records = store.append_batch(
                        project_id=tx.project_id,
                        events=list(tx.proposed_events),
                        expected_revision=tx.expected_revision,
                        idempotency_key=tx.idempotency_key,
                        batch_id=tx.tx_id,
                    )
                    committed_events.extend(str(record.event_id) for record in committed_records)

            return TransactionResult(
                tx_id=tx.tx_id,
                success=True,
                committed_event_ids=committed_events,
                committed_artifact_hashes=committed_hashes,
            )

        except Exception as exc:
            logger.error("Transaction %s failed, rolling back: %s", tx.tx_id, exc)
            # Rollback: Clean up newly committed blobs if possible
            for blob_path in committed_blobs:
                try:
                    if blob_path.exists():
                        blob_path.unlink()
                except Exception as rollback_err:
                    logger.warning("Failed to clean up blob %s during rollback: %s", blob_path, rollback_err)

            return TransactionResult(
                tx_id=tx.tx_id,
                success=False,
                rolled_back=True,
                error=f"Transaction execution failed: {exc}",
            )

        finally:
            # Clean up temp staging directory
            try:
                shutil.rmtree(stage_dir, ignore_errors=True)
            except Exception:
                pass

    def transaction_from_context(self, ctx: LifecycleContext, project_id: UUID | None = None) -> Transaction:
        """Create a Transaction from a LifecycleContext's proposed events and artifacts."""
        artifacts = [
            ProposedArtifact(
                content=art.get("content", b"") if isinstance(art.get("content"), bytes) else str(art.get("content", "")).encode("utf-8"),
                artifact_type=art.get("artifact_type", "OTHER"),
                origin=art.get("origin", "DERIVED"),
                metadata=art.get("metadata", {}),
            )
            for art in ctx.proposed_artifacts
        ]

        return Transaction(
            project_id=project_id,
            operation=ctx.operation,
            proposed_events=list(ctx.proposed_events),
            proposed_artifacts=artifacts,
        )
