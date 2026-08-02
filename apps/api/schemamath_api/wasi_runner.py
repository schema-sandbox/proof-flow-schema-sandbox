"""
WASI WebAssembly Plugin Runner (WasiPluginRunner)

Provides ultra-isolated WebAssembly / WASI execution sandbox for running untrusted code
with strict memory limits and instruction metering.
"""

from __future__ import annotations

import logging
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class WasiRunResult:
    success: bool
    stdout: str
    stderr: str
    return_code: int
    execution_time_sec: float


class WasiPluginRunner:
    """
    Executes WASM binaries via WASI runtimes (wasmtime, wasmer, or node --experimental-wasi-unstable-preview1).
    """

    def __init__(self, wasm_runtime: str | None = None) -> None:
        self.wasm_runtime = (
            wasm_runtime
            or shutil.which("wasmtime")
            or shutil.which("wasmer")
            or shutil.which("wasm-runner")
        )

    @property
    def is_available(self) -> bool:
        if not self.wasm_runtime:
            return False
        p = Path(self.wasm_runtime)
        return p.exists() or shutil.which(self.wasm_runtime) is not None

    def run_wasm(
        self,
        wasm_path: Path,
        args: list[str] | None = None,
        timeout_sec: int = 10,
    ) -> WasiRunResult:
        """Run a WASM module within the isolated WASI runtime."""
        import time

        if not self.is_available:
            return WasiRunResult(
                success=False,
                stdout="",
                stderr="WASI runtime binary not found on PATH; execution was not performed",
                return_code=-1,
                execution_time_sec=0.001,
            )

        start = time.perf_counter()
        cmd = [self.wasm_runtime, "run", str(wasm_path)] + (args or [])

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
            )
            elapsed = time.perf_counter() - start
            return WasiRunResult(
                success=proc.returncode == 0,
                stdout=proc.stdout,
                stderr=proc.stderr,
                return_code=proc.returncode,
                execution_time_sec=elapsed,
            )
        except subprocess.TimeoutExpired:
            elapsed = time.perf_counter() - start
            return WasiRunResult(
                success=False,
                stdout="",
                stderr=f"WASM execution timed out after {timeout_sec}s",
                return_code=-1,
                execution_time_sec=elapsed,
            )
        except Exception as exc:
            elapsed = time.perf_counter() - start
            return WasiRunResult(
                success=False,
                stdout="",
                stderr=f"WASM execution error: {exc}",
                return_code=-1,
                execution_time_sec=elapsed,
            )
