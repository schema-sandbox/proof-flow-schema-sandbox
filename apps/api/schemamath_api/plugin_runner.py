from __future__ import annotations

import hashlib
import json
import os
import signal
import subprocess
import sys
import threading
import venv
from dataclasses import dataclass
from pathlib import Path
from time import monotonic
from uuid import UUID

from .domain import PluginRunStatus

_ENV_LOCKS_GUARD = threading.Lock()
_ENV_LOCKS: dict[str, threading.Lock] = {}


def _environment_lock(path: Path) -> threading.Lock:
    key = str(path.resolve())
    with _ENV_LOCKS_GUARD:
        return _ENV_LOCKS.setdefault(key, threading.Lock())


@dataclass(frozen=True, slots=True)
class PythonExecutionOutcome:
    status: PluginRunStatus
    command: list[str]
    runtime_version: str
    exit_code: int | None
    stdout_path: Path
    stderr_path: Path
    output_files: list[Path]
    output_truncated: bool
    error: str | None
    elapsed_seconds: float


class PythonPluginRunner:
    """A local process runner for the first optional math-tool plugin.

    This runner scrubs environment variables, uses an isolated project run directory,
    creates a dedicated venv, caps time and output, and does not expose event-store paths.
    It is *not* an OS security sandbox: user Python can still access the local machine with
    the permissions of the user running ProofFlow. Strong isolation is deferred to an OCI
    or microVM runner.
    """

    plugin_id = "python.local"
    plugin_version = "0.1.0"
    isolation_level = "process-only"

    def __init__(
        self,
        *,
        plugin_root: Path,
        maximum_output_bytes: int,
        maximum_output_files: int,
    ) -> None:
        self.plugin_root = plugin_root
        self.maximum_output_bytes = maximum_output_bytes
        self.maximum_output_files = maximum_output_files
        self.environment_dir = self.plugin_root / self.plugin_id / self.plugin_version / "venv"

    def ensure_environment(self) -> Path:
        python_path = self._venv_python_path()
        if python_path.exists():
            return python_path
        lock = _environment_lock(self.environment_dir)
        with lock:
            if python_path.exists():
                return python_path
            self.environment_dir.parent.mkdir(parents=True, exist_ok=True)
            builder = venv.EnvBuilder(
                system_site_packages=False,
                clear=False,
                symlinks=os.name != "nt",
                with_pip=False,
            )
            builder.create(self.environment_dir)
            marker = self.environment_dir.parent / "environment.json"
            marker.write_text(
                json.dumps(
                    {
                        "plugin_id": self.plugin_id,
                        "plugin_version": self.plugin_version,
                        "created_with": sys.version,
                        "python": str(python_path),
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
        return python_path

    def environment_fingerprint(self) -> str:
        python_path = self.ensure_environment()
        payload = {
            "plugin_id": self.plugin_id,
            "version": self.plugin_version,
            "python_path": str(python_path),
            "host_python": sys.version,
            "isolation": self.isolation_level,
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

    def execute(
        self,
        *,
        project_id: UUID,
        run_id: UUID,
        run_dir: Path,
        source_code: str,
        stdin_text: str,
        arguments: list[str],
        timeout_seconds: int,
        input_files: list[tuple[str, bytes]],
    ) -> PythonExecutionOutcome:
        python_path = self.ensure_environment()
        run_dir.mkdir(parents=True, exist_ok=False)
        input_dir = run_dir / "inputs"
        output_dir = run_dir / "outputs"
        temp_dir = run_dir / "tmp"
        input_dir.mkdir()
        output_dir.mkdir()
        temp_dir.mkdir()

        source_path = run_dir / "main.py"
        source_path.write_text(source_code, encoding="utf-8")
        for filename, content in input_files:
            destination = input_dir / self._safe_filename(filename)
            destination.write_bytes(content)

        stdout_path = run_dir / "stdout.log"
        stderr_path = run_dir / "stderr.log"
        command = [str(python_path), "-I", "-B", str(source_path.name), *arguments]
        environment = {
            "PYTHONNOUSERSITE": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONUNBUFFERED": "1",
            "HOME": str(run_dir),
            "TMPDIR": str(temp_dir),
            "TEMP": str(temp_dir),
            "TMP": str(temp_dir),
            "LANG": os.environ.get("LANG", "C.UTF-8"),
            "LC_ALL": os.environ.get("LC_ALL", "C.UTF-8"),
            "SCHEMAMATH_PROJECT_ID": str(project_id),
            "SCHEMAMATH_RUN_ID": str(run_id),
            "SCHEMAMATH_INPUT_DIR": str(input_dir),
            "SCHEMAMATH_OUTPUT_DIR": str(output_dir),
        }

        started = monotonic()
        process: subprocess.Popen[bytes] | None = None
        status = PluginRunStatus.FAILED
        exit_code: int | None = None
        error: str | None = None
        try:
            with stdout_path.open("wb") as stdout_handle, stderr_path.open("wb") as stderr_handle:
                process = subprocess.Popen(
                    command,
                    cwd=run_dir,
                    env=environment,
                    stdin=subprocess.PIPE,
                    stdout=stdout_handle,
                    stderr=stderr_handle,
                    start_new_session=True,
                    preexec_fn=self._resource_limiter(timeout_seconds)
                    if os.name == "posix"
                    else None,
                )
                try:
                    process.communicate(input=stdin_text.encode("utf-8"), timeout=timeout_seconds)
                    exit_code = process.returncode
                    status = PluginRunStatus.SUCCEEDED if exit_code == 0 else PluginRunStatus.FAILED
                except subprocess.TimeoutExpired:
                    status = PluginRunStatus.TIMED_OUT
                    error = f"plugin exceeded {timeout_seconds} second timeout"
                    self._terminate_process_tree(process)
                    exit_code = process.returncode
        except Exception as exc:
            status = PluginRunStatus.FAILED
            error = f"runner failure: {type(exc).__name__}: {exc}"
            if process and process.poll() is None:
                self._terminate_process_tree(process)

        output_files, output_truncated = self._collect_outputs(output_dir)
        for log_path in (stdout_path, stderr_path):
            if log_path.exists() and log_path.stat().st_size > self.maximum_output_bytes:
                self._truncate_file(log_path)
                output_truncated = True

        metadata = {
            "plugin_id": self.plugin_id,
            "plugin_version": self.plugin_version,
            "command": command,
            "status": status.value,
            "exit_code": exit_code,
            "timeout_seconds": timeout_seconds,
            "elapsed_seconds": monotonic() - started,
            "environment_fingerprint": self.environment_fingerprint(),
            "isolation_level": self.isolation_level,
            "warning": ("process-only isolation; this alpha runner is not an OS security sandbox"),
            "error": error,
        }
        (run_dir / "run.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return PythonExecutionOutcome(
            status=status,
            command=command,
            runtime_version=sys.version,
            exit_code=exit_code,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            output_files=output_files,
            output_truncated=output_truncated,
            error=error,
            elapsed_seconds=metadata["elapsed_seconds"],
        )

    def _venv_python_path(self) -> Path:
        if os.name == "nt":
            return self.environment_dir / "Scripts" / "python.exe"
        return self.environment_dir / "bin" / "python"

    @staticmethod
    def _safe_filename(filename: str) -> str:
        name = Path(filename).name.replace("\x00", "")
        return name[:240] or "input.bin"

    def _collect_outputs(self, output_dir: Path) -> tuple[list[Path], bool]:
        files: list[Path] = []
        truncated = False
        for path in sorted(output_dir.rglob("*")):
            if path.is_symlink() or not path.is_file():
                continue
            if len(files) >= self.maximum_output_files:
                truncated = True
                path.unlink(missing_ok=True)
                continue
            if path.stat().st_size > self.maximum_output_bytes:
                self._truncate_file(path)
                truncated = True
            files.append(path)
        return files, truncated

    def _truncate_file(self, path: Path) -> None:
        with path.open("r+b") as handle:
            handle.truncate(self.maximum_output_bytes)

    def _resource_limiter(self, timeout_seconds: int):
        def limit() -> None:
            try:
                import resource

                output_limit = max(self.maximum_output_bytes, 1_048_576)
                resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
                resource.setrlimit(
                    resource.RLIMIT_CPU,
                    (max(timeout_seconds + 1, 2), max(timeout_seconds + 2, 3)),
                )
                resource.setrlimit(resource.RLIMIT_FSIZE, (output_limit, output_limit))
                memory_limit = 1024 * 1024 * 1024
                resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
            except Exception:
                # Resource limits are a best-effort alpha safeguard, never a security claim.
                return

        return limit

    @staticmethod
    def _terminate_process_tree(process: subprocess.Popen[bytes]) -> None:
        try:
            if os.name == "posix":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
        except ProcessLookupError:
            pass
        finally:
            try:
                process.wait(timeout=5)
            except Exception:
                pass
