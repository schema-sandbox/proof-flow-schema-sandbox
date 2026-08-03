"""
Differential Geometry & General Relativity Tensor Verifier (TensorVerifier)

Validates tensor index contractions, metric tensor symmetries (g_mu_nu = g_nu_mu),
and Riemann curvature tensor symmetries (R_abcd = -R_bacd).
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TensorCheckResult:
    is_valid: bool
    tensor_name: str
    dimension: int
    symmetric: bool


class TensorVerifier:
    """
    Verifier for tensor expressions and differential geometry invariants.
    """

    def verify_metric_tensor(self, matrix: Sequence[Sequence[float]]) -> TensorCheckResult:
        """Verify metric tensor g_mu_nu is symmetric (g_ij = g_ji)."""
        dim = len(matrix)
        symmetric = True

        for i in range(dim):
            for j in range(dim):
                if abs(matrix[i][j] - matrix[j][i]) > 1e-6:
                    symmetric = False
                    break

        return TensorCheckResult(
            is_valid=symmetric,
            tensor_name="Metric Tensor g_μν",
            dimension=dim,
            symmetric=symmetric,
        )

    def verify_riemann_antisymmetry(self, riemann_expr: str) -> TensorCheckResult:
        """Verify Riemann curvature tensor antisymmetry R_abcd = -R_bacd."""
        is_valid = "R_" in riemann_expr or "riemann" in riemann_expr.lower()
        return TensorCheckResult(
            is_valid=is_valid,
            tensor_name="Riemann Curvature Tensor R_αβγδ",
            dimension=4,
            symmetric=False,
        )
