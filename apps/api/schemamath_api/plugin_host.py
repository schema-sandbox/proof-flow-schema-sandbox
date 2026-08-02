from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .domain import (
    SCHEMA_VERSION,
    PluginHealthRecord,
    PluginManifestRecord,
    PluginRunnerType,
    PluginRunStatus,
    utc_now,
)


@dataclass(slots=True)
class GeneralExecutionOutcome:
    status: PluginRunStatus
    command: list[str]
    runtime_version: str
    exit_code: int | None
    stdout_path: Path
    stderr_path: Path
    output_files: list[Path]
    output_truncated: bool
    error: str | None


class PluginHost:
    """Manifest-driven host for optional local-command and OCI plugins.

    The host never gives plugins direct access to the event stream. Local-command
    execution remains process-only isolation; OCI execution requires a digest-pinned
    image and a locally available container runtime.
    """

    def __init__(
        self,
        *,
        repository_root: Path,
        plugin_root: Path,
        maximum_output_bytes: int,
        maximum_output_files: int,
    ) -> None:
        self.repository_root = repository_root
        self.plugin_root = plugin_root
        self.maximum_output_bytes = maximum_output_bytes
        self.maximum_output_files = maximum_output_files

    def available_manifests(self) -> list[PluginManifestRecord]:
        manifests: dict[tuple[str, str], PluginManifestRecord] = {}
        roots = [
            self.repository_root / "plugins" / "builtin",
            self.plugin_root / "registry",
        ]
        for root in roots:
            if not root.exists():
                continue
            for path in sorted(root.glob("**/plugin.json")):
                manifest = PluginManifestRecord.model_validate_json(
                    path.read_text(encoding="utf-8")
                )
                manifests[(manifest.plugin_id, manifest.version)] = manifest
        return sorted(manifests.values(), key=lambda item: (item.plugin_id, item.version))

    def install_manifest(self, manifest: PluginManifestRecord) -> Path:
        if manifest.install.allow_network_install:
            raise ValueError(
                "silent network installation is forbidden; install dependencies "
                "outside ProofFlow and retry the health check"
            )
        if manifest.runner_type == PluginRunnerType.OCI:
            image = manifest.install.image or ""
            if "@sha256:" not in image:
                raise ValueError("OCI plugin images must be pinned by sha256 digest")
        destination = (
            self.plugin_root / "registry" / manifest.plugin_id / manifest.version / "plugin.json"
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
        return destination

    def healthcheck(self, manifest: PluginManifestRecord) -> PluginHealthRecord:
        if manifest.runner_type == PluginRunnerType.PYTHON:
            return PluginHealthRecord(
                plugin_id=manifest.plugin_id,
                version=manifest.version,
                healthy=True,
                checked_at=utc_now(),
                message="Dedicated Python environment is managed on first enable.",
                runner_type=manifest.runner_type,
            )

        command = (
            manifest.healthcheck[0]
            if manifest.healthcheck
            else (manifest.entrypoint[0] if manifest.entrypoint else "")
        )
        if manifest.runner_type == PluginRunnerType.OCI:
            command = shutil.which("docker") or shutil.which("podman") or ""
        resolved = shutil.which(command) if command else None
        healthy = resolved is not None
        message = (
            f"Runtime available at {resolved}."
            if healthy
            else "Required runtime is not installed or is not on PATH."
        )
        return PluginHealthRecord(
            plugin_id=manifest.plugin_id,
            version=manifest.version,
            healthy=healthy,
            checked_at=utc_now(),
            message=message,
            runner_type=manifest.runner_type,
        )

    def execute(
        self,
        *,
        manifest: PluginManifestRecord,
        run_dir: Path,
        input_filename: str,
        input_bytes: bytes,
        arguments: list[str],
        timeout_seconds: int,
    ) -> GeneralExecutionOutcome:
        run_dir.mkdir(parents=True, exist_ok=True)
        input_dir = run_dir / "inputs"
        output_dir = run_dir / "outputs"
        input_dir.mkdir(exist_ok=True)
        output_dir.mkdir(exist_ok=True)
        safe_name = Path(input_filename).name or "input.txt"
        input_path = input_dir / safe_name
        input_path.write_bytes(input_bytes)
        stdout_path = run_dir / "stdout.log"
        stderr_path = run_dir / "stderr.log"

        try:
            if not manifest.permissions.subprocess:
                raise ValueError("subprocess execution is not permitted for this plugin")
            command = self._command(
                manifest=manifest,
                input_path=input_path,
                output_dir=output_dir,
                arguments=arguments,
            )
        except ValueError as exc:
            stdout_path.write_bytes(b"")
            stderr_path.write_text(str(exc), encoding="utf-8")
            return GeneralExecutionOutcome(
                status=PluginRunStatus.FAILED,
                command=[],
                runtime_version=manifest.runner_type.value,
                exit_code=None,
                stdout_path=stdout_path,
                stderr_path=stderr_path,
                output_files=[],
                output_truncated=False,
                error=str(exc),
            )
        timeout = min(timeout_seconds, manifest.maximum_timeout_seconds)
        environment = {
            "PATH": os.environ.get("PATH", ""),
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
            "WINDIR": os.environ.get("WINDIR", ""),
            "TMP": str(run_dir),
            "TEMP": str(run_dir),
            "HOME": str(run_dir),
            "PYTHONNOUSERSITE": "1",
            "PROOFFLOW_RUN_DIR": str(run_dir),
        }
        for key in manifest.permissions.environment_variables:
            value = os.environ.get(key)
            if value is not None:
                environment[key] = value
        status = PluginRunStatus.FAILED
        exit_code: int | None = None
        error: str | None = None
        runtime_version = manifest.runner_type.value
        try:
            with stdout_path.open("wb") as stdout_handle, stderr_path.open("wb") as stderr_handle:
                process = subprocess.Popen(
                    command,
                    cwd=run_dir,
                    env=environment,
                    stdin=subprocess.DEVNULL,
                    stdout=stdout_handle,
                    stderr=stderr_handle,
                    shell=False,
                )
                try:
                    exit_code = process.wait(timeout=timeout)
                    status = PluginRunStatus.SUCCEEDED if exit_code == 0 else PluginRunStatus.FAILED
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
                    status = PluginRunStatus.TIMED_OUT
                    error = f"plugin exceeded the {timeout}-second timeout"
        except OSError as exc:
            stderr_path.write_text(str(exc), encoding="utf-8")
            error = str(exc)

        output_files, truncated = self._collect_outputs(output_dir)
        for log_path in (stdout_path, stderr_path):
            if log_path.exists() and log_path.stat().st_size > self.maximum_output_bytes:
                with log_path.open("r+b") as handle:
                    handle.truncate(self.maximum_output_bytes)
                truncated = True
        return GeneralExecutionOutcome(
            status=status,
            command=command,
            runtime_version=runtime_version,
            exit_code=exit_code,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            output_files=output_files,
            output_truncated=truncated,
            error=error,
        )

    def _command(
        self,
        *,
        manifest: PluginManifestRecord,
        input_path: Path,
        output_dir: Path,
        arguments: list[str],
    ) -> list[str]:
        replacements = {
            "{input}": str(input_path),
            "{output_dir}": str(output_dir),
        }

        def expand(value: str) -> str:
            result = value
            for marker, replacement in replacements.items():
                result = result.replace(marker, replacement)
            return result

        entrypoint = [expand(value) for value in manifest.entrypoint]
        if manifest.runner_type == PluginRunnerType.LOCAL_COMMAND:
            if not entrypoint:
                raise ValueError("local-command plugin has no entrypoint")
            return [*entrypoint, *arguments]
        if manifest.runner_type == PluginRunnerType.OCI:
            runtime = shutil.which("docker") or shutil.which("podman")
            if runtime is None:
                raise ValueError("no supported OCI runtime is available")
            image = manifest.install.image or ""
            if "@sha256:" not in image:
                raise ValueError("OCI plugin image is not digest-pinned")
            network = "bridge" if manifest.permissions.network else "none"
            return [
                runtime,
                "run",
                "--rm",
                "--network",
                network,
                "--memory",
                f"{manifest.resources.max_memory_mb}m",
                "--volume",
                f"{input_path.parent}:/proof-flow/inputs:ro",
                "--volume",
                f"{output_dir}:/proof-flow/outputs:rw",
                image,
                *entrypoint,
                *arguments,
            ]
        raise ValueError("python.local uses the dedicated compatibility runner")

    def _collect_outputs(self, output_dir: Path) -> tuple[list[Path], bool]:
        files: list[Path] = []
        total = 0
        truncated = False
        for path in sorted(output_dir.rglob("*")):
            if path.is_symlink() or not path.is_file():
                continue
            if len(files) >= self.maximum_output_files:
                truncated = True
                break
            remaining = self.maximum_output_bytes - total
            if remaining <= 0:
                truncated = True
                break
            if path.stat().st_size > remaining:
                with path.open("r+b") as handle:
                    handle.truncate(remaining)
                truncated = True
            files.append(path)
            total += path.stat().st_size
        return files, truncated

    @staticmethod
    def lock_payload(records: list[dict[str, object]]) -> str:
        return json.dumps(
            {"schema_version": SCHEMA_VERSION, "plugins": records},
            ensure_ascii=False,
            indent=2,
        )
