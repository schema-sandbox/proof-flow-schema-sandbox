"""
Tests for ProofFlow v15.0.0 (DelayTolerantConsensus, BlockLatticeLedger)

Covers:
    - BlockLatticeLedger (Asynchronous account block chain appends)
    - DelayTolerantConsensus (CRDT conflict-free state merge)
"""

from __future__ import annotations

import pytest

from schemamath_api.delay_tolerant import BlockLatticeLedger, DelayTolerantConsensus


class TestBlockLatticeLedger:
    def test_append_block(self):
        ledger = BlockLatticeLedger()
        b1 = ledger.append_block("account_mars", "proof_part_1")
        assert b1.height == 1
        assert b1.previous_hash == "GENESIS_HASH"

        b2 = ledger.append_block("account_mars", "proof_part_2")
        assert b2.height == 2
        assert b2.previous_hash == b1.block_hash


class TestDelayTolerantConsensus:
    def test_merge_crdt_states(self):
        consensus = DelayTolerantConsensus()
        merged = consensus.merge_crdt_states(["b1", "b2"], ["b2", "b3"])

        assert merged == ["b1", "b2", "b3"]
