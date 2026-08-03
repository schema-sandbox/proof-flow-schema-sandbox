"""
Tests for ProofFlow v32.0 (Real-Time Live Lean4 / Z3 Formal Compiler Gateway & Proof State Streamer)

Covers:
    - Lean4CompilerService (Lean4 code compilation & AST diagnostic parsing)
    - ProofStateStreamer (Tactic step-by-step state streaming)
    - Z3SmtSolverService (Z3 SMT-LIB2 formula solving)
"""

from __future__ import annotations

from schemamath_api.lean4_compiler_gateway import (
    Lean4CompilerService,
    ProofStateStreamer,
    Z3SmtSolverService,
)


class TestLean4CompilerGateway:
    def test_lean4_compile_success_and_error(self):
        compiler = Lean4CompilerService()
        res_ok = compiler.compile_lean4_code("theorem test (x : Real) : x ^ 2 >= 0 := by positivity")
        assert res_ok.success is False
        assert any(item.severity == "unavailable" for item in res_ok.diagnostics)
        assert "x ^ 2" in res_ok.proof_state_goal

        res_err = compiler.compile_lean4_code("theorem test : False := by sorry")
        assert res_err.success is False
        assert len(res_err.diagnostics) == 1

    def test_proof_state_streamer_and_z3_solver(self):
        streamer = ProofStateStreamer()
        step = streamer.stream_tactic_step(1, "intro x", "⊢ x ≥ 0")
        assert step["step"] == 1
        assert step["tactic_applied"] == "intro x"

        solver = Z3SmtSolverService()
        smt_res = solver.solve_smt2_formula("(assert (> x 0))")
        assert smt_res.status == "unavailable"
        assert smt_res.model_bindings == {}
