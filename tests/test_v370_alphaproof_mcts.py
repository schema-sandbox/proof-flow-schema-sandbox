"""
Tests for ProofFlow v37.0 (DeepMind AlphaProof Reinforcement Learning MCTS Search Engine)

Covers:
    - PolicyValueNetworkEvaluator (Neural policy prior & state value evaluation)
    - MctsProofTreeSearch (MCTS proof search over Lean4 tactic space)
"""

from __future__ import annotations

import pytest

from schemamath_api.alphaproof_mcts import (
    MctsProofTreeSearch,
    PolicyValueNetworkEvaluator,
)


class TestAlphaProofMcts:
    def test_evaluator_and_mcts_search(self):
        evaluator = PolicyValueNetworkEvaluator()
        priors, val = evaluator.evaluate_state("⊢ x^2 >= 0")
        assert "by simp" in priors
        assert val > 0.8

        mcts = MctsProofTreeSearch()
        res = mcts.search_proof("sq_nonneg", "⊢ x^2 >= 0", max_simulations=30)
        assert res.is_fully_verified is False
        assert len(res.proof_tactics_found) >= 2
        assert res.nodes_expanded == 30
