"""
Tests for ProofFlow v21.8 (TemporalLogicVerifier)

Covers:
    - TemporalLogicVerifier (LTL and CTL model checking formula verification)
"""

from __future__ import annotations

from schemamath_api.temporal import TemporalLogicVerifier


class TestTemporalLogicVerifier:
    def test_verify_ltl_formula(self):
        verifier = TemporalLogicVerifier()
        res = verifier.verify_ltl_formula("G(req -> F ack)")

        assert res.logic_type == "LTL"
        assert res.is_satisfied is True
        assert res.counterexample_trace is None
