"""
Formal Verifier Adapters (Lean4 and Z3 SMT Solver)

Provides computational and formal verification adapters that integrate with
the @sip/verifier (G4) module. Supports Lean4 interactive theorem proving
and Z3 SMT solver satisfiability checks.
"""

from __future__ import annotations

import logging
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from schemamath_api.sip.verifier import VerificationResult

logger = logging.getLogger(__name__)

# Lean prints these when a proof is incomplete ("sorry"/"admit" compile with exit 0
# but do NOT constitute a proof); we must NOT report such a build as verified.
_UNTRUSTED_LEAN_MARKERS = ("sorry", "admit", "unsolved goals", "declaration uses 'sorry'", "failed to synthesize")


def _lean_is_untrusted(output: str) -> bool:
    lowered = output.lower()
    return any(marker in lowered for marker in _UNTRUSTED_LEAN_MARKERS)


def _lean_has_error(output: str) -> bool:
    return "error:" in output.lower()


@dataclass
class Lean4VerificationRequest:
    code: str
    theorem_name: str | None = None
    timeout_sec: int = 10


@dataclass
class Z3VerificationRequest:
    smtlib2_code: str
    expected_status: str = "sat"  # sat, unsat, unknown
    timeout_sec: int = 5


class Lean4Adapter:
    """
    Adapter for Lean 4 theorem prover.

    Runs `lake env lean` or `lean` executable if available on PATH;
    otherwise gracefully degrades with a clear diagnostic message.
    """

    def __init__(self, lean_executable: str | None = None) -> None:
        self.lean_executable = lean_executable or shutil.which("lean") or shutil.which("lake")

    @property
    def is_available(self) -> bool:
        if not self.lean_executable:
            return False
        p = Path(self.lean_executable)
        return p.exists() or shutil.which(self.lean_executable) is not None

    def _build_command(self, file_path: Path) -> list[str]:
        """Run ``lake env lean file.lean`` when the executable is ``lake``,
        otherwise ``<lean> file.lean``. Running ``lake <file>.lean`` directly is not
        the documented invocation."""
        executable_name = Path(self.lean_executable or "").name
        if executable_name == "lake":
            return ["lake", "env", "lean", str(file_path)]
        if executable_name == "lean":
            return [self.lean_executable, str(file_path)]
        # Fall back to the configured/which-resolved path as-is.
        return [self.lean_executable, str(file_path)]

    def verify_theorem(self, req: Lean4VerificationRequest) -> VerificationResult:
        """Verify a Lean4 theorem script."""
        if not self.is_available:
            logger.info("Lean4 executable not found; verification is unavailable")
            return VerificationResult(
                valid=False,
                verifier_name="Lean4",
                details="Lean4 binary not found on PATH; theorem was not verified",
                mutation_tested=False,
            )

        with tempfile.TemporaryDirectory(prefix="lean4_verify_") as tmp_dir:
            file_path = Path(tmp_dir) / "Theorem.lean"
            file_path.write_text(req.code, encoding="utf-8")

            try:
                cmd = self._build_command(file_path)
                proc = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=req.timeout_sec,
                )
                combined = f"{proc.stdout}\n{proc.stderr}"
                if proc.returncode == 0 and not _lean_has_error(combined) and not _lean_is_untrusted(combined):
                    return VerificationResult(
                        valid=True,
                        verifier_name="Lean4",
                        details=f"Lean4 theorem verification succeeded: {proc.stdout.strip()[:200]}",
                        mutation_tested=True,
                    )
                if _lean_is_untrusted(combined):
                    return VerificationResult(
                        valid=False,
                        verifier_name="Lean4",
                        details="Lean4 build contains 'sorry'/'admit' or unsolved goals; theorem is NOT verified",
                        mutation_tested=True,
                    )
                return VerificationResult(
                    valid=False,
                    verifier_name="Lean4",
                    details=f"Lean4 verification failed: {proc.stderr.strip()[:300]}",
                    mutation_tested=True,
                )
            except subprocess.TimeoutExpired:
                return VerificationResult(
                    valid=False,
                    verifier_name="Lean4",
                    details=f"Lean4 verification timed out after {req.timeout_sec}s",
                    mutation_tested=True,
                )
            except Exception as exc:
                return VerificationResult(
                    valid=False,
                    verifier_name="Lean4",
                    details=f"Lean4 execution error: {exc}",
                    mutation_tested=False,
                )


class Z3Adapter:
    """
    Adapter for Z3 SMT Solver.
    """

    def __init__(self, z3_executable: str | None = None) -> None:
        self.z3_executable = z3_executable or shutil.which("z3")

    @property
    def is_available(self) -> bool:
        if not self.z3_executable:
            return False
        p = Path(self.z3_executable)
        return p.exists() or shutil.which(self.z3_executable) is not None

    def verify_smt(self, req: Z3VerificationRequest) -> VerificationResult:
        """Verify SMT-LIB2 script using Z3."""
        if not self.is_available:
            return VerificationResult(
                valid=False,
                verifier_name="Z3",
                details="Z3 executable not found on PATH; formula was not verified",
                mutation_tested=False,
            )

        with tempfile.TemporaryDirectory(prefix="z3_verify_") as tmp_dir:
            file_path = Path(tmp_dir) / "query.smt2"
            file_path.write_text(req.smtlib2_code, encoding="utf-8")

            try:
                cmd = [self.z3_executable, str(file_path)]
                proc = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=req.timeout_sec,
                )

                # Match on whole tokens: a substring test would report "sat" as
                # found inside "unsat", a false-positive success for an unsat system.
                tokens = set(proc.stdout.lower().split())
                if req.expected_status in tokens:
                    return VerificationResult(
                        valid=True,
                        verifier_name="Z3",
                        details=f"Z3 check matched expected status '{req.expected_status}'",
                        mutation_tested=True,
                    )
                return VerificationResult(
                    valid=False,
                    verifier_name="Z3",
                    details=f"Z3 output '{proc.stdout.strip()[:200]}' did not match expected '{req.expected_status}'",
                    mutation_tested=True,
                )
            except Exception as exc:
                return VerificationResult(
                    valid=False,
                    verifier_name="Z3",
                    details=f"Z3 error: {exc}",
                )
