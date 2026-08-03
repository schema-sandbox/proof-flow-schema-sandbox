"""
Tests for ProofFlow v21.0.0 (SingularityMatrix, TranscendentProofKernel)

Covers:
    - SingularityMatrix (Multi-modal proof matrix computation)
    - TranscendentProofKernel (Ultimate v21.0.0 kernel status verification)
"""

from __future__ import annotations

from schemamath_api.transcendent import SingularityMatrix, TranscendentProofKernel


class TestSingularityMatrix:
    def test_compute_singularity_matrix(self):
        matrix = SingularityMatrix()
        metrics = matrix.compute_singularity_matrix()

        assert metrics["singularity_resonance"] > 0.99
        assert metrics["logic_consistency"] == 1.0


class TestTranscendentProofKernel:
    def test_get_transcendent_status(self):
        kernel = TranscendentProofKernel()
        status = kernel.get_transcendent_status()

        assert status.kernel_version == "21.0.0"
        assert status.total_versions_integrated == 21
        assert status.transcendent_epistemic_index == 0.0
        assert status.status == "EXPERIMENTAL_UNVERIFIED"
