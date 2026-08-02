"""
Tests for ProofFlow v26.0 (Automated Deep Counterexample Fuzzer & SAT/SMT Solver Suite)

Covers:
    - PropertyBasedFuzzer (Property-based randomized fuzzing & counterexample discovery)
    - SmtFormulaEncoder (SMT-LIB2 format constraint encoding)
    - CounterexampleMinimizer (Delta debugging counterexample minimization)
"""

from __future__ import annotations

import pytest

from schemamath_api.deep_fuzzer import (
    CounterexampleMinimizer,
    PropertyBasedFuzzer,
    SmtFormulaEncoder,
)


class TestDeepFuzzer:
    def test_property_fuzzer_and_smt_encoder(self):
        fuzzer = PropertyBasedFuzzer()
        res = fuzzer.fuzz_property("is_positive_integer", max_iterations=50)
        assert res.iterations > 0
        assert res.counterexample_found is not None

        encoder = SmtFormulaEncoder()
        smt_code = encoder.encode_constraint(["x", "y"], "> (+ x y) 0")
        assert "(declare-const x Real)" in smt_code
        assert "(check-sat)" in smt_code

    def test_counterexample_minimizer(self):
        minimizer = CounterexampleMinimizer()
        raw = [100, 42, 999, 15, 200]
        minimized = minimizer.minimize(raw)
        assert len(minimized) == 1
        assert minimized[0] == 15
