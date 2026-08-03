"""
Tests for ProofFlow v38.0 (SymPy Symbolic Engine & Z3 SMT Non-Linear Real Arithmetic Solver)

Covers:
    - SymPySymbolicEngine (Symbolic calculus differentiation & integration)
    - NonLinearRealArithmeticSolver (Z3 SMT non-linear real arithmetic solving)
"""

from __future__ import annotations

from schemamath_api.sympy_z3_solver import (
    NonLinearRealArithmeticSolver,
    SymPySymbolicEngine,
)


class TestSympyZ3Solver:
    def test_sympy_derivation_is_correct_math(self):
        engine = SymPySymbolicEngine()
        res = engine.simplify_and_derive("x**2 + 5")
        assert res.status == "computed"
        assert res.derivative == "2*x"
        # Real indefinite integral of x^2 + 5 is x^3/3 + 5x (the "5x" term
        # was previously dropped by a hard-coded shortcut).
        assert res.integral == "x**3/3 + 5*x"

        high = engine.simplify_and_derive("x**20")
        assert high.status == "computed"
        assert high.derivative == "20*x**19"

    def test_nra_solver_reports_unavailable_honestly(self):
        solver = NonLinearRealArithmeticSolver()
        nra_res = solver.solve_nra_inequalities(["x^2 + y^2 <= 25", "x > 0"])
        assert nra_res.status == "unavailable"
        assert nra_res.real_bounds == {}

    def test_sympy_unavailable_never_fabricates(self, monkeypatch):
        import schemamath_api.sympy_z3_solver as solver_module

        monkeypatch.setattr(solver_module, "_sympy", lambda: None)
        engine = solver_module.SymPySymbolicEngine()
        res = engine.simplify_and_derive("sin(x)")
        assert res.status == "unavailable"
        assert res.derivative is None
        assert res.integral is None
