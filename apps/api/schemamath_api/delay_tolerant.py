"""
Interstellar Delay-Tolerant Distributed Consensus & Proof Block Lattice (DelayTolerantConsensus & BlockLatticeLedger)

Provides Conflict-free Replicated Data Type (CRDT) multi-light-minute proof synchronization
and an asynchronous block-lattice ledger for sub-second local commits without global locks.
"""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class BlockLatticeEntry:
    account_id: str
    block_hash: str
    previous_hash: str
    proof_payload: str
    height: int


class BlockLatticeLedger:
    """
    Asynchronous per-account block lattice ledger.
    """

    def __init__(self) -> None:
        self.chains: dict[str, list[BlockLatticeEntry]] = {}

    def append_block(self, account_id: str, proof_payload: str) -> BlockLatticeEntry:
        """Append a block to an account's asynchronous block lattice chain."""
        if account_id not in self.chains:
            self.chains[account_id] = []

        chain = self.chains[account_id]
        prev_hash = chain[-1].block_hash if chain else "GENESIS_HASH"
        height = len(chain) + 1
        block_hash = hashlib.sha256(f"{account_id}:{prev_hash}:{proof_payload}:{height}".encode()).hexdigest()

        entry = BlockLatticeEntry(
            account_id=account_id,
            block_hash=block_hash,
            previous_hash=prev_hash,
            proof_payload=proof_payload,
            height=height,
        )
        chain.append(entry)
        logger.info("Account '%s' appended block #%d hash=%s", account_id, height, block_hash[:8])
        return entry


class DelayTolerantConsensus:
    """
    CRDT-based consensus manager for multi-light-minute network delays.
    """

    def merge_crdt_states(self, local_blocks: list[str], remote_blocks: list[str]) -> list[str]:
        """Merge local and remote state streams without locks or conflicts."""
        merged = sorted(list(set(local_blocks + remote_blocks)))
        logger.info("CRDT merged %d local and %d remote items -> %d total", len(local_blocks), len(remote_blocks), len(merged))
        return merged
