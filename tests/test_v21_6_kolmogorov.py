"""
Tests for ProofFlow v21.6 (KolmogorovEvaluator)

Covers:
    - KolmogorovEvaluator (Complexity upper bound & compressibility estimation)
"""

from __future__ import annotations

from schemamath_api.kolmogorov import KolmogorovEvaluator


class TestKolmogorovEvaluator:
    def test_estimate_kolmogorov_complexity(self):
        evaluator = KolmogorovEvaluator()
        repetitive = "ABC" * 100
        res = evaluator.estimate_kolmogorov_complexity(repetitive)

        assert res.raw_length_bits == 2400
        assert res.kolmogorov_upper_bound_bits < res.raw_length_bits
        assert res.compression_ratio < 0.5
        assert res.is_incompressible is False
