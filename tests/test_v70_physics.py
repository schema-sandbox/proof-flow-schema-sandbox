"""
Tests for ProofFlow v7.0.0 (PhysicsSymEngine, TensorVerifier, NeuralSymbolicBridge)

Covers:
    - PhysicsSymEngine (mechanical energy conservation & Euler-Lagrange variational principle)
    - TensorVerifier (metric tensor symmetry & Riemann curvature tensor antisymmetry)
    - NeuralSymbolicBridge (neural embedding vector translation to Lean4 & Z3)
"""

from __future__ import annotations

from schemamath_api.neural_symbolic_bridge import NeuralSymbolicBridge
from schemamath_api.physics_sym import PhysicsSymEngine
from schemamath_api.tensor_verifier import TensorVerifier


class TestPhysicsSymEngine:
    def test_verify_energy_conservation(self):
        engine = PhysicsSymEngine()
        res = engine.verify_energy_conservation(
            initial_kinetic=10.0,
            initial_potential=5.0,
            final_kinetic=7.0,
            final_potential=8.0,
        )
        assert res.is_conserved is True
        assert res.residual_error == 0.0
        assert "Conservation of Mechanical Energy" in res.law_name

    def test_verify_lagrangian_action(self):
        engine = PhysicsSymEngine()
        res = engine.verify_lagrangian_action("L = T - V")
        assert res.is_conserved is True
        assert "Euler-Lagrange" in res.law_name


class TestTensorVerifier:
    def test_verify_metric_tensor_symmetric(self):
        verifier = TensorVerifier()
        g_mu_nu = [
            [1.0, 0.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, -1.0],
        ]
        res = verifier.verify_metric_tensor(g_mu_nu)
        assert res.is_valid is True
        assert res.symmetric is True

    def test_verify_riemann_antisymmetry(self):
        verifier = TensorVerifier()
        res = verifier.verify_riemann_antisymmetry("R_abcd")
        assert res.is_valid is True


class TestNeuralSymbolicBridge:
    def test_vector_to_symbolic(self):
        bridge = NeuralSymbolicBridge()
        emb = [0.1, 0.5, -0.2, 0.8]
        translation = bridge.vector_to_symbolic(emb, theorem_name="physics_lemma")

        assert translation.embedding_dim == 4
        assert "theorem physics_lemma" in translation.lean4_code
        assert "assert" in translation.z3_smt_code
        assert translation.confidence > 0.0
