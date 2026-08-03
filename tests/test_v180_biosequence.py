"""
Tests for ProofFlow v18.0.0 (BioSequenceVerifier, MolecularConformationBridge)

Covers:
    - BioSequenceVerifier (DNA to RNA transcription & codon validation)
    - MolecularConformationBridge (3D protein folding Ramachandran geometry to Lean4)
"""

from __future__ import annotations

from schemamath_api.biosequence import BioSequenceVerifier, MolecularConformationBridge


class TestBioSequenceVerifier:
    def test_transcribe_dna(self):
        verifier = BioSequenceVerifier()
        res = verifier.transcribe_dna("ATCGGA")

        assert res.is_valid_transcription is True
        assert res.rna_sequence == "UAGCCU"
        assert res.codon_count == 2


class TestMolecularConformationBridge:
    def test_bridge_folding_geometry(self):
        bridge = MolecularConformationBridge()
        res = bridge.bridge_folding_geometry("protein_101", phi=-60.0, psi=-45.0)

        assert res.dihedral_angles_valid is True
        assert "theorem protein_101_conformation" in res.lean4_geometry_code
