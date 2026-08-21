#!/usr/bin/env python3
"""Build detached, reproducible ProofFlow release assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
import zipfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATED_NAMES = {"package_manifest.json", "SHA256SUMS.txt"}
EXCLUDED_NAMES = {".coverage", "tsconfig.tsbuildinfo", *GENERATED_NAMES}
RELEASE_DATE = "2026-08-21"
GENERATED_AT = "2026-08-21T00:00:00Z"
ZIP_TIMESTAMP = (2026, 8, 21, 0, 0, 0)


@dataclass(frozen=True)
class SourceEntry:
    path: str
    data: bytes
    executable: bool


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_git(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        check=False,
        timeout=timeout,
    )


def git_tracked_entries() -> list[SourceEntry]:
    """Read canonical bytes from HEAD, independent of checkout line endings."""
    proc = run_git("ls-tree", "-r", "-z", "--full-tree", "HEAD")
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    objects: list[tuple[str, bytes, bool]] = []
    for raw_record in proc.stdout.split(b"\0"):
        if not raw_record:
            continue
        metadata, raw_path = raw_record.split(b"\t", 1)
        mode, object_type, object_id = metadata.split(b" ", 2)
        path = raw_path.decode("utf-8")
        if object_type != b"blob" or Path(path).name in EXCLUDED_NAMES:
            continue
        if Path(path).is_absolute() or ".." in Path(path).parts:
            raise RuntimeError(f"unsafe path in Git tree: {path}")
        objects.append((path, object_id, mode == b"100755"))
    objects.sort(key=lambda item: item[0])

    batch = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = batch.communicate(b"".join(object_id + b"\n" for _, object_id, _ in objects))
    if batch.returncode != 0:
        raise RuntimeError(stderr.decode("utf-8", errors="replace"))

    entries: list[SourceEntry] = []
    cursor = 0
    for path, expected_id, executable in objects:
        header_end = stdout.index(b"\n", cursor)
        object_id, object_type, raw_size = stdout[cursor:header_end].split(b" ", 2)
        if object_id != expected_id or object_type != b"blob":
            raise RuntimeError(f"unexpected Git object for {path}")
        size = int(raw_size)
        data_start = header_end + 1
        data_end = data_start + size
        entries.append(SourceEntry(path=path, data=stdout[data_start:data_end], executable=executable))
        cursor = data_end + 1
    return entries


def project_version() -> str:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return str(data["project"]["version"])


def collect_test_count() -> int | None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "apps" / "api") + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    try:
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "--collect-only",
                "-p",
                "no:cacheprovider",
            ],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=True,
            timeout=120,
        )
    except Exception:
        return None
    collected_by_file = 0
    for line in reversed(proc.stdout.splitlines()):
        if " tests collected" in line:
            token = line.split(" tests collected", 1)[0].rsplit(" ", 1)[-1]
            if token.isdigit():
                return int(token)
        if ": " in line:
            token = line.rsplit(": ", 1)[-1]
            if token.isdigit():
                collected_by_file += int(token)
    return collected_by_file or None


def schema_metrics(entries: list[SourceEntry]) -> tuple[int, int]:
    total = 0
    runtime = 0
    for entry in entries:
        if not entry.path.startswith("schemas/") or not entry.path.endswith(".json"):
            continue
        try:
            data = json.loads(entry.data)
        except Exception:
            continue
        if isinstance(data, dict):
            total += 1
            if str(data.get("$id", "")).startswith("https://schemamath.org/schemas/runtime/"):
                runtime += 1
    return total, runtime


def openapi_paths(entries: list[SourceEntry]) -> int | None:
    try:
        raw = next(entry.data for entry in entries if entry.path == "api/openapi.json")
        data = json.loads(raw)
    except Exception:
        return None
    return len(data.get("paths", {}))


def git_commit_info() -> dict[str, str | None]:
    info: dict[str, str | None] = {"commit": None, "branch": None, "tag": None}
    commit = run_git("rev-parse", "HEAD", timeout=10)
    if commit.returncode == 0:
        info["commit"] = commit.stdout.decode("utf-8").strip()
    branch = run_git("rev-parse", "--abbrev-ref", "HEAD", timeout=10)
    if branch.returncode == 0:
        value = branch.stdout.decode("utf-8").strip()
        info["branch"] = None if value == "HEAD" else value
    tag = run_git("describe", "--tags", "--exact-match", timeout=10)
    if tag.returncode == 0:
        info["tag"] = tag.stdout.decode("utf-8").strip()
    return info


def source_date_epoch() -> str:
    proc = run_git("show", "-s", "--format=%ct", "HEAD", timeout=10)
    if proc.returncode == 0:
        return proc.stdout.decode("utf-8").strip()
    return "1787241600"


def build_manifest(entries: list[SourceEntry]) -> dict[str, object]:
    schema_total, runtime_schema_total = schema_metrics(entries)
    git_info = git_commit_info()
    records = [
        {
            "path": entry.path,
            "size_bytes": len(entry.data),
            "sha256": sha256_bytes(entry.data),
        }
        for entry in entries
    ]
    return {
        "package": "ProofFlow Schema Sandbox",
        "version": project_version(),
        "release_date": RELEASE_DATE,
        "generated_at": GENERATED_AT,
        "status": "local-first experimental mathematics research sandbox",
        "license": "MIT",
        "git_commit": git_info["commit"],
        "git_tag": git_info["tag"],
        "entrypoints": {
            "api": "schemamath_api.main:app",
            "application": "/app/",
            "prototype": "/prototype/",
            "openapi": "api/openapi.yaml",
        },
        "validated": {
            "pytest_tests_collected": collect_test_count(),
            "runtime_schemas_exported": runtime_schema_total,
            "json_schema_documents_present": schema_total,
            "openapi_paths": openapi_paths(entries),
            "markdown_documents_present": sum(
                1 for entry in entries if entry.path.lower().endswith(".md")
            ),
            "react_build": "built_and_staged_by_release_pipeline",
            "npm_audit_high": "validated_by_ci_outside_offline_builder",
        },
        "security_boundary": {
            "network_binding": "localhost by default",
            "production_authentication": (
                "required via PROOFFLOW_SECRET_KEY and PROOFFLOW_API_KEYS"
            ),
            "production_local_process_plugins": (
                "disabled unless explicitly enabled outside production"
            ),
            "plugin_host_isolation": (
                "process-only for trusted local commands; digest-pinned OCI supported"
            ),
            "silent_network_install": False,
            "os_security_sandbox": False,
        },
        "file_count_excluding_manifest_and_checksum": len(records),
        "total_bytes_excluding_manifest_and_checksum": sum(
            int(record["size_bytes"]) for record in records
        ),
        "files": records,
    }


def manifest_bytes(manifest: dict[str, object]) -> bytes:
    return (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def source_checksums(entries: list[SourceEntry], manifest_data: bytes) -> bytes:
    lines = [
        f"{sha256_bytes(entry.data)}  {entry.path}"
        for entry in entries
    ]
    lines.append(f"{sha256_bytes(manifest_data)}  package_manifest.json")
    return ("\n".join(lines) + "\n").encode("utf-8")


def zip_info(name: str, executable: bool = False) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = ((0o755 if executable else 0o644) & 0xFFFF) << 16
    return info


def write_zip(
    destination: Path,
    version: str,
    entries: list[SourceEntry],
    manifest_data: bytes,
    checksum_data: bytes,
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    prefix = f"ProofFlow_Schema_Sandbox_v{version}"
    with zipfile.ZipFile(
        destination,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for entry in entries:
            archive.writestr(
                zip_info(f"{prefix}/{entry.path}", executable=entry.executable),
                entry.data,
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )
        archive.writestr(
            zip_info(f"{prefix}/package_manifest.json"),
            manifest_data,
            compress_type=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        )
        archive.writestr(
            zip_info(f"{prefix}/SHA256SUMS.txt"),
            checksum_data,
            compress_type=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        )
    with zipfile.ZipFile(destination) as archive:
        bad_member = archive.testzip()
    if bad_member is not None:
        raise RuntimeError(f"release archive failed integrity check at {bad_member}")


def run_checked(
    command: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
) -> None:
    subprocess.run(command, cwd=cwd, env=env, check=True)


def prepare_generated_inputs() -> None:
    run_checked([sys.executable, str(ROOT / "scripts" / "generate_sbom.py")])
    run_checked([sys.executable, str(ROOT / "scripts" / "validate_sbom.py")])
    run_checked([sys.executable, str(ROOT / "scripts" / "validate_release_metadata.py")])
    diff = run_git(
        "diff",
        "--exit-code",
        "--",
        "sbom.cyclonedx.json",
        "THIRD_PARTY_NOTICES.md",
    )
    if diff.returncode != 0:
        sys.stdout.buffer.write(diff.stdout)
        sys.stderr.buffer.write(diff.stderr)
        raise RuntimeError("generated SBOM or attribution inventory differs from the committed files")
    if not (ROOT / "apps" / "web" / "dist" / "index.html").is_file():
        raise RuntimeError("frontend bundle is absent; run npm build before the release builder")


def materialize_source_tree(destination: Path, entries: list[SourceEntry]) -> None:
    for entry in entries:
        target = destination / Path(entry.path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(entry.data)
        if entry.executable:
            target.chmod(0o755)


def build_wheel(dist_dir: Path, entries: list[SourceEntry]) -> Path:
    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = source_date_epoch()
    temporary_root = ROOT / ".venv"
    temporary_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="alpha9-release-", dir=temporary_root) as value:
        source_tree = Path(value)
        materialize_source_tree(source_tree, entries)
        shutil.copytree(
            ROOT / "apps" / "web" / "dist",
            source_tree / "apps" / "web" / "dist",
            dirs_exist_ok=True,
        )
        run_checked(
            [sys.executable, str(source_tree / "scripts" / "stage_wheel_ui.py")],
            cwd=source_tree,
            env=env,
        )
        run_checked(
            [
                sys.executable,
                "-m",
                "pip",
                "wheel",
                ".",
                "--no-deps",
                "--no-build-isolation",
                "-w",
                str(dist_dir),
            ],
            cwd=source_tree,
            env=env,
        )
    wheels = sorted(dist_dir.glob("*.whl"))
    if len(wheels) != 1:
        raise RuntimeError(f"expected one wheel, found {len(wheels)}")
    return wheels[0]


def write_dist_checksums(dist_dir: Path) -> None:
    lines = [
        f"{sha256_file(path)}  {path.name}"
        for path in sorted(dist_dir.iterdir())
        if path.is_file() and path.name != "SHA256SUMS.txt"
    ]
    (dist_dir / "SHA256SUMS.txt").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def build_dist_assets(
    version: str,
    entries: list[SourceEntry],
    manifest_data: bytes,
    checksum_data: bytes,
) -> None:
    dist_dir = ROOT / "dist"
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir(parents=True)
    build_wheel(dist_dir, entries)
    write_zip(
        dist_dir / f"ProofFlow_Schema_Sandbox_v{version}.zip",
        version,
        entries,
        manifest_data,
        checksum_data,
    )
    (dist_dir / "package_manifest.json").write_bytes(manifest_data)
    shutil.copyfile(ROOT / "sbom.cyclonedx.json", dist_dir / "sbom.cyclonedx.json")
    write_dist_checksums(dist_dir)
    print(f"Wrote {len(list(dist_dir.iterdir()))} files to {dist_dir}.")


def assert_clean_worktree() -> None:
    status = run_git("status", "--porcelain")
    dirty = status.stdout.decode("utf-8", errors="replace").splitlines()
    if dirty:
        print(f"Release build failed: dirty working tree ({len(dirty)} entries)")
        for entry in dirty:
            print(f"  {entry}")
        raise SystemExit(1)


def assert_strict_release(version: str) -> None:
    assert_clean_worktree()
    expected_tag = f"v{version}"
    actual_tag = git_commit_info()["tag"]
    if actual_tag != expected_tag:
        raise SystemExit(
            f"Strict release build failed: HEAD must have tag {expected_tag!r}, "
            f"got {actual_tag!r}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", dest="zip_path", type=Path)
    parser.add_argument("--dist", action="store_true")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Require a clean working tree and an exact version tag.",
    )
    args = parser.parse_args()
    version = project_version()
    if args.strict:
        assert_strict_release(version)
    elif args.dist or args.zip_path:
        assert_clean_worktree()

    if args.dist:
        prepare_generated_inputs()
    entries = git_tracked_entries()
    manifest = build_manifest(entries)
    manifest_data = manifest_bytes(manifest)
    checksum_data = source_checksums(entries, manifest_data)

    if not args.dist:
        (ROOT / "package_manifest.json").write_bytes(manifest_data)
        (ROOT / "SHA256SUMS.txt").write_bytes(checksum_data)
    if args.zip_path:
        write_zip(
            args.zip_path.resolve(),
            version,
            entries,
            manifest_data,
            checksum_data,
        )
        print(f"Wrote {args.zip_path.resolve()}")
    if args.dist:
        build_dist_assets(version, entries, manifest_data, checksum_data)
    print(
        f"Generated detached manifest for "
        f"{manifest['file_count_excluding_manifest_and_checksum']} files."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
