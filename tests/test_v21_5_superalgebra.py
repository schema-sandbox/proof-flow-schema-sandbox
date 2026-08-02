"""
Tests for ProofFlow v21.5 (LieSuperalgebraEngine)

Covers:
    - LieSuperalgebraEngine (Z_2-graded Lie superalgebra & supertrace verification)
"""

from __future__ import annotations

import pytest

from schemamath_api.superalgebra import LieSuperalgebraEngine


class TestLieSuperalgebraEngine:
    def test_verify_superalgebra(self):
        engine = LieSuperalgebraEngine()
        res = engine.verify_superalgebra("gl(1|1)")

        assert res.is_supersymmetric is True
        assert res.even_dim == 2
        assert res.odd_dim == 2
        assert res.supertrace_value == 0.0
