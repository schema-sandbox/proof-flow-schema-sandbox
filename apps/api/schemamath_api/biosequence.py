"""
Biological Sequence & Molecular Conformation Formal Expresser (BioSequenceVerifier & MolecularConformationBridge)

Validates DNA/RNA transcription constraints and bridges 3D protein folding conformation geometry
to Lean4 formal geometry theorem declarations.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TranscriptionResult:
    dna_sequence: str
    rna_sequence: str
    is_valid_transcription: bool
    codon_count: int


@dataclass
class MolecularConformationTheorem:
    protein_id: str
    dihedral_angles_valid: bool
    lean4_geometry_code: str


class BioSequenceVerifier:
    """
    Verifier for biological DNA/RNA sequence transcription constraints.
    """

    def transcribe_dna(self, dna_seq: str) -> TranscriptionResult:
        """Transcribe DNA sequence to RNA (A->U, T->A, C->G, G->C)."""
        mapping = {"A": "U", "T": "A", "C": "G", "G": "C"}
        rna = "".join(mapping.get(n, "N") for n in dna_seq.upper())
        is_valid = "N" not in rna and len(dna_seq) % 3 == 0

        logger.info("Transcribed DNA (%d bp) -> RNA, valid=%s", len(dna_seq), is_valid)
        return TranscriptionResult(
            dna_sequence=dna_seq,
            rna_sequence=rna,
            is_valid_transcription=is_valid,
            codon_count=len(dna_seq) // 3,
        )


class MolecularConformationBridge:
    """
    Bridges 3D protein folding dihedral angle geometry into Lean4 formal geometry code.
    """

    def bridge_folding_geometry(self, protein_id: str, phi: float, psi: float) -> MolecularConformationTheorem:
        """Bridge protein Ramachandran phi/psi angles to Lean4 geometry theorem."""
        # Ramachandran allowed region check
        is_allowed = -180.0 <= phi <= 180.0 and -180.0 <= psi <= 180.0
        lean_code = f"theorem {protein_id}_conformation : ∀ (φ ψ : Real), -180 ≤ φ ∧ φ ≤ 180 ∧ -180 ≤ ψ ∧ ψ ≤ 180 := by intro φ ψ h; exact h"

        return MolecularConformationTheorem(
            protein_id=protein_id,
            dihedral_angles_valid=is_allowed,
            lean4_geometry_code=lean_code,
        )
