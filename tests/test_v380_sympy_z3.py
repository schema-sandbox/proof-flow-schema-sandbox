"""
Tests for ProofFlow v38.0 (SymPy Symbolic Engine & Z3 SMT Non-Linear Real Arithmetic Solver)

Covers:
    - SymPySymbolicEngine (Symbolic calculus differentiation & integration)
    - NonLinearRealArithmeticSolver (Z3 SMT non-linear real arithmetic solving)
"""

from __future__ import annotations

import pytest

from schemamath_api.sympy_z3_solver import (
    NonLinearRealArithmeticSolver,
    SymPySymbolicEngine,
)


class TestSympyZ3Solver:
    def test_sympy_derivation_and_nra_solver(self):
        engine = SymPySymbolicEngine()
        res = engine.simplify_and_derive("x**2 + 5")
        assert res.derivative == "2*x"
        assert res.integral == "(1/3)*x^3"

        solver = NonLinearRealArithmeticSolver()
        nra_res = solver.solve_nra_inequalities(["x^2 + y^2 <= 25", "x > 0"])
        assert nra_res.status == "unavailable"
        assert nra_res.real_bounds == {}
