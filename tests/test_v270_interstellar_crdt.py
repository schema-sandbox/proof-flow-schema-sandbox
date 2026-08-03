"""
Tests for ProofFlow v27.0 (Interstellar Delay-Tolerant Block Lattice & CRDT Distributed Storage)

Covers:
    - CrdtLwwElementSet (LWW-Element-Set state merge with vector clocks)
    - InterstellarBlockLattice (Account block chain DAG publishing)
    - MerkleDAGStateVerifier (Root Merkle DAG hash computation)
"""

from __future__ import annotations

from schemamath_api.interstellar_crdt import (
    CrdtLwwElementSet,
    InterstellarBlockLattice,
    MerkleDAGStateVerifier,
)


class TestInterstellarCrdt:
    def test_crdt_lww_merge(self):
        crdt1 = CrdtLwwElementSet()
        crdt2 = CrdtLwwElementSet()

        crdt1.add("fact_a", timestamp=10.0, vector_clock={"node_1": 1})
        crdt2.add("fact_a", timestamp=12.0, vector_clock={"node_2": 2})

        crdt1.merge(crdt2)
        assert crdt1.add_set["fact_a"].timestamp == 12.0

    def test_block_lattice_and_merkle_verifier(self):
        lattice = InterstellarBlockLattice()
        b1 = lattice.publish_block("mars_station_1", "theorem_alpha")
        b2 = lattice.publish_block("mars_station_1", "theorem_beta")

        assert b2.height == 2
        assert b2.parent_hash == b1.block_hash

        verifier = MerkleDAGStateVerifier()
        root_hash = verifier.compute_root_hash([b1, b2])
        assert len(root_hash) == 64
