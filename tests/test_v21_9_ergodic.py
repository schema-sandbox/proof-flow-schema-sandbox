"""
Tests for ProofFlow v21.9 (ErgodicEntropyEvaluator)

Covers:
    - ErgodicEntropyEvaluator (KS entropy & Lyapunov chaotic exponent evaluation)
"""

from __future__ import annotations

from schemamath_api.ergodic import ErgodicEntropyEvaluator


class TestErgodicEntropyEvaluator:
    def test_evaluate_dynamical_system(self):
        evaluator = ErgodicEntropyEvaluator()
        res = evaluator.evaluate_dynamical_system("Lorentz_Attractor")

        assert res.is_chaotic is True
        assert res.is_ergodic is True
        assert res.max_lyapunov_exponent > 0.0
        assert res.ks_entropy > 1.0
