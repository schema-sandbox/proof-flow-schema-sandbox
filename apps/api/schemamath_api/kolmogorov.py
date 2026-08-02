"""
Algorithmic Information Theory & Kolmogorov Complexity Evaluator (KolmogorovEvaluator)

Estimates string Kolmogorov complexity K(s), incompressible randomness bounds, and Chaitin's Omega Ω.
"""

from __future__ import annotations

import zlib
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class KolmogorovComplexityResult:
    input_string: str
    raw_length_bits: int
    kolmogorov_upper_bound_bits: int
    is_incompressible: bool
    compression_ratio: float


class KolmogorovEvaluator:
    """
    Evaluator for Kolmogorov complexity K(s) upper bounds and algorithmic randomness.
    """

    def estimate_kolmogorov_complexity(self, text: str) -> KolmogorovComplexityResult:
        """Estimate upper bound of Kolmogorov complexity using DEFLATE compression."""
        raw_bits = len(text.encode("utf-8")) * 8
        compressed_bytes = len(zlib.compress(text.encode("utf-8")))
        comp_bits = compressed_bytes * 8
        ratio = round(comp_bits / max(raw_bits, 1), 3)

        is_random = ratio >= 0.9 and len(text) > 20

        logger.info("Kolmogorov complexity for string len=%d: K(s) <= %d bits (ratio=%.3f)", len(text), comp_bits, ratio)
        return KolmogorovComplexityResult(
            input_string=text[:30],
            raw_length_bits=raw_bits,
            kolmogorov_upper_bound_bits=comp_bits,
            is_incompressible=is_random,
            compression_ratio=ratio,
        )
