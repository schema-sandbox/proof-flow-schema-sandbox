"""
Tests for Formal Verifier Adapters (Lean4 and Z3)

Covers:
    - Lean4Adapter graceful fallback when binary is absent
    - Lean4VerificationRequest payload handling
    - Z3Adapter graceful fallback when binary is absent
    - Integration with @sip/verifier (G4) module
"""

from __future__ import annotations

import pytest

from schemamath_api.sip import createVerifier
from schemamath_api.verifiers import (
    Lean4Adapter,
    Lean4VerificationRequest,
    Z3Adapter,
    Z3VerificationRequest,
)


class TestFormalVerifiers:
    def test_lean4_graceful_fallback(self):
        adapter = Lean4Adapter(lean_executable="/nonexistent/path/to/lean")
        req = Lean4VerificationRequest(
            code="theorem add_comm (n m : Nat) : n + m = m + n := Nat.add_comm n m",
            theorem_name="add_comm",
        )
        res = adapter.verify_theorem(req)
        assert res.valid is False
        assert "not verified" in res.details

    def test_z3_graceful_fallback(self):
        adapter = Z3Adapter(z3_executable="/nonexistent/path/to/z3")
        req = Z3VerificationRequest(smtlib2_code="(assert (= x y)) (check-sat)")
        res = adapter.verify_smt(req)
        assert res.valid is False
        assert "not verified" in res.details

    def test_verifier_module_integration(self):
        verifier_mod = createVerifier()
        lean_adapter = Lean4Adapter()

        def lean_check(payload):
            return lean_adapter.verify_theorem(
                Lean4VerificationRequest(code=payload.get("code", ""))
            )

        verifier_mod.register_verifier("lean4_formal", lean_check)

        res = verifier_mod._verifiers["lean4_formal"]({"code": "def x := 1"})
        assert res.valid is False
