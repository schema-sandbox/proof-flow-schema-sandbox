"""
Tests for ProofFlow v36.0 (Lean4 Physlib & Classical/Quantum Field Formalization Suite)

Covers:
    - PhyslibFormalBridge (Lean4 Physlib theorem generation)
    - SchrodingerEquationVerifier (Wavefunction unitary evolution verification)
    - GeneralRelativitySpacetimeVerifier (Einstein Field Equation verification)
"""

from __future__ import annotations

import pytest

from schemamath_api.physlib_bridge import (
    GeneralRelativitySpacetimeVerifier,
    PhyslibFormalBridge,
    SchrodingerEquationVerifier,
)


class TestPhyslibBridge:
    def test_physlib_bridge_and_schrodinger(self):
        bridge = PhyslibFormalBridge()
        code = bridge.generate_lean4_physlib_theorem("schrodinger")
        assert "i * ℏ * ∂ψ/∂t = H ψ" in code

        schrodinger = SchrodingerEquationVerifier()
        res = schrodinger.verify_evolution("hydrogen_1s", energy_ev=-13.6)
        assert res.is_unitary_evolution is True
        assert res.is_hamiltonian_hermitian is True

    def test_einstein_field_verifier(self):
        gr = GeneralRelativitySpacetimeVerifier()
        res = gr.verify_einstein_equations("Kerr_Black_Hole")
        assert res.energy_momentum_conserved is True
        assert res.einstein_tensor_zero_divergence is True
