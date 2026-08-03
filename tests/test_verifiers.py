"""
Tests for Formal Verifier Adapters (Lean4 and Z3)

Covers:
    - Lean4Adapter graceful fallback when binary is absent
    - Lean4VerificationRequest payload handling
    - Z3Adapter graceful fallback when binary is absent
    - Integration with @sip/verifier (G4) module
"""

from __future__ import annotations

import sys

from schemamath_api.sip import createVerifier
from schemamath_api.verifiers import (
    Lean4Adapter,
    Lean4VerificationRequest,
    Z3Adapter,
    Z3VerificationRequest,
)
from schemamath_api.verifiers import lean4 as lean4_module


class _FakeProc:
    def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


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

    def test_z3_unsat_is_not_reported_as_sat(self, monkeypatch):
        """'sat' must NOT be considered present inside 'unsat'."""
        adapter = Z3Adapter(z3_executable=sys.executable)

        def fake_run(_cmd, **_kw):
            return _FakeProc(returncode=0, stdout="unsat\n")

        monkeypatch.setattr(lean4_module.subprocess, "run", fake_run)
        res = adapter.verify_smt(Z3VerificationRequest(smtlib2_code="(check-sat)"))
        assert res.valid is False

    def test_z3_sat_is_reported_as_sat(self, monkeypatch):
        adapter = Z3Adapter(z3_executable=sys.executable)

        def fake_run(_cmd, **_kw):
            return _FakeProc(returncode=0, stdout="sat\n")

        monkeypatch.setattr(lean4_module.subprocess, "run", fake_run)
        res = adapter.verify_smt(Z3VerificationRequest(smtlib2_code="(check-sat)"))
        assert res.valid is True

    def test_lean_sorry_is_not_reported_as_verified(self, monkeypatch):
        """Exit 0 with a 'sorry'/'admit' must not be treated as a verified theorem."""
        adapter = Lean4Adapter(lean_executable=sys.executable)

        def fake_run(_cmd, **_kw):
            return _FakeProc(
                returncode=0,
                stdout="",
                stderr="declaration uses 'sorry'\n",
            )

        monkeypatch.setattr(lean4_module.subprocess, "run", fake_run)
        res = adapter.verify_theorem(
            Lean4VerificationRequest(code="theorem t : True := by sorry")
        )
        assert res.valid is False
        assert "sorry" in res.details.lower()

    def test_lean_lake_uses_lake_env_lean(self, monkeypatch, tmp_path):
        captured: list[list[str]] = []

        def fake_run(cmd, **_kwargs):
            captured.append(list(cmd))
            return _FakeProc(returncode=0, stdout="", stderr="")

        monkeypatch.setattr(lean4_module.subprocess, "run", fake_run)
        fake_lake = tmp_path / "lake"
        fake_lake.write_bytes(b"#!/bin/sh\n")
        adapter = Lean4Adapter(lean_executable=str(fake_lake))
        res = adapter.verify_theorem(
            Lean4VerificationRequest(code="theorem t : True := by trivial")
        )
        assert captured and captured[0][0] == "lake"
        assert captured[0][1:3] == ["env", "lean"]
        assert res.valid is True
