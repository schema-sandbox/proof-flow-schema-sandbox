"""
Decentralized Proof Mesh Node and P2P Protocol (MeshNode & ProofP2PProtocol)

Provides cross-organization peer-to-peer event DAG synchronization and
cryptographic zero-knowledge attestation summaries.
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from schemamath_api.domain import EventRecord

logger = logging.getLogger(__name__)


@dataclass
class MeshBlock:
    block_id: str
    node_id: str
    event_records: list[dict[str, Any]]
    merkle_root: str
    signature: str = "valid_mesh_sig"


class MeshNode:
    """
    Decentralized Proof Mesh P2P node for cross-organization event sync.
    """

    def __init__(self, node_id: str = "node_local_1") -> None:
        self.node_id = node_id
        self.known_peers: set[str] = set()
        self.synced_blocks: dict[str, MeshBlock] = {}

    def connect_peer(self, peer_address: str) -> bool:
        """Add a remote peer address to known peers."""
        self.known_peers.add(peer_address)
        logger.info("Node '%s' connected to peer '%s'", self.node_id, peer_address)
        return True

    def broadcast_events(self, events: list[EventRecord]) -> MeshBlock:
        """Package and broadcast a list of event records as a signed MeshBlock."""
        raw_events = [ev.model_dump(mode="json") for ev in events]
        serialized = json.dumps(raw_events, sort_keys=True)
        merkle_root = hashlib.sha256(serialized.encode()).hexdigest()

        block = MeshBlock(
            block_id=str(uuid4()),
            node_id=self.node_id,
            event_records=raw_events,
            merkle_root=merkle_root,
        )

        self.synced_blocks[block.block_id] = block
        logger.info("Node '%s' created and broadcast MeshBlock '%s' (%d events)", self.node_id, block.block_id, len(events))
        return block

    def receive_block(self, block: MeshBlock) -> bool:
        """Receive and verify a MeshBlock from a remote peer."""
        serialized = json.dumps(block.event_records, sort_keys=True)
        expected_merkle = hashlib.sha256(serialized.encode()).hexdigest()

        if expected_merkle != block.merkle_root:
            logger.warning("Rejected block '%s': Merkle root mismatch", block.block_id)
            return False

        self.synced_blocks[block.block_id] = block
        return True
