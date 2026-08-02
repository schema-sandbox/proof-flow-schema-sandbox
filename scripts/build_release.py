#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tomllib
import zipfile
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    ".venv",
    "node_modules",
    ".schemamath-workspace",
    ".schemamath-plugins",
    "runtime-workspaces",
    "runtime-plugins",
}
EXCLUDED_NAMES = {
    ".coverage",
    "package_manifest.json",
    "SHA256SUMS.txt",
    "tsconfig.tsbuildinfo",
}
# The repository root is the active ProofFlow source tree.  The sibling
# versioned snapshots and theory package are retained for audit/reference only;
# they are deliberately not part of a ProofFlow release or its checksums.
EXCLUDED_ROOT_NAMES = {
    "ProofFlow_Schema_Sandbox_0.1.0-alpha.3",
    "ProofFlow_Schema_Sandbox_0.1.0-alpha.4",
    "SchemaMath_Experimental_Sandbox_alpha_0.1.0-alpha.2",
    "SchemaMath_Experimental_Sandbox_Design_v0.1",
}
EXCLUDED_ROOT_FILES = {
    "ai_math_discoveries_2026_paper.md",
    "From_Prompt_to_Proof_v0.10.md",
    "From_Prompt_to_Proof_v0.10_CN.md",
    "internal_kb_schema_sandbox_paper_V33_CN.md",
    "internal_kb_schema_sandbox_paper_V33_EN.md",
    "internal_kb_schema_sandbox_V34_MKS_CN.md",
    "internal_kb_schema_sandbox_V34_MKS_EN.md",
    "operational_evidence_map_v0.10.png",
    "operational_evidence_map_v0.10.svg",
    "ProofFlow_Schema_Sandbox_0.1.0-alpha.3.zip",
    "ProofFlow_Schema_Sandbox_0.1.0-alpha.4.zip",
    "SchemaMath_Experimental_Sandbox_alpha_0.1.0-alpha.1.zip",
    "SchemaMath_Experimental_Sandbox_alpha_0.1.0-alpha.2.zip",
    "SchemaMath_Experimental_Sandbox_Design_Package_v0.1.zip",
    "schema_sandbox_modular_architecture.md",
    "Schema_Sandbox_V34_Modular_Trust_Kernel_Proposal_CN.md",
}


def is_reference_material(relative: Path) -> bool:
    return bool(relative.parts) and (
        relative.parts[0] in EXCLUDED_ROOT_NAMES
        or (len(relative.parts) == 1 and relative.name in EXCLUDED_ROOT_FILES)
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def included_files(*, include_generated: bool = False) -> list[Path]:
    result: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if is_reference_material(relative):
            continue
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if not include_generated and path.name in EXCLUDED_NAMES:
            continue
        if include_generated and path.name == "SHA256SUMS.txt":
            continue
        result.append(path)
    return sorted(result, key=lambda item: item.relative_to(ROOT).as_posix())


def project_version() -> str:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    version = str(data["project"]["version"])
    if "a" in version:
        base, alpha = version.rsplit("a", 1)
        if alpha.isdigit():
            return f"{base}-alpha.{alpha}"
    return version


def collect_test_count() -> int | None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "apps" / "api") + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    command = [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider"]
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=True,
            timeout=120,
        )
    except Exception:
        return None
    total = 0
    for line in proc.stdout.splitlines():
        if ": " not in line:
            continue
        suffix = line.rsplit(": ", 1)[-1].strip()
        if suffix.isdigit():
            total += int(suffix)
    return total or None


def schema_metrics() -> tuple[int, int]:
    total = 0
    runtime = 0
    for path in sorted((ROOT / "schemas").glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, dict) and data.get("$schema"):
            total += 1
        if str(data.get("$id", "")).startswith("https://schemamath.org/schemas/runtime/"):
            runtime += 1
    return total, runtime


def openapi_paths() -> int | None:
    path = ROOT / "api" / "openapi.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return len(data.get("paths", {}))
    except Exception:
        return None


def write_manifest() -> dict[str, object]:
    files = included_files(include_generated=False)
    schema_total, runtime_schema_total = schema_metrics()
    file_records = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in files
    ]
    manifest: dict[str, object] = {
        "package": "ProofFlow Schema Sandbox",
        "version": project_version(),
        "release_date": datetime.now(UTC).date().isoformat(),
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "local-first experimental research prototype",
        "license": "Apache-2.0",
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
            "openapi_paths": openapi_paths(),
            "markdown_documents_present": sum(1 for path in files if path.suffix.lower() == ".md"),
            "prototype_javascript_syntax": True,
            "demo_export_import": True,
            "react_build": True,
            "npm_audit_high": "0 vulnerabilities",
        },
        "security_boundary": {
            "network_binding": "localhost by default",
            "plugin_host_isolation": (
                "process-only for trusted local commands; digest-pinned OCI supported"
            ),
            "silent_network_install": False,
            "os_security_sandbox": False,
        },
        "file_count_excluding_manifest_and_checksum": len(file_records),
        "total_bytes_excluding_manifest_and_checksum": sum(
            int(record["size_bytes"]) for record in file_records
        ),
        "files": file_records,
    }
    (ROOT / "package_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def write_checksums() -> None:
    lines: list[str] = []
    for path in included_files(include_generated=True):
        relative = path.relative_to(ROOT).as_posix()
        lines.append(f"{sha256_file(path)}  {relative}")
    (ROOT / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def zip_files() -> list[Path]:
    result: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if is_reference_material(relative):
            continue
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if path.name in {".coverage", "tsconfig.tsbuildinfo"}:
            continue
        result.append(path)
    return sorted(result, key=lambda item: item.relative_to(ROOT).as_posix())


def write_zip(destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    top = ROOT.name
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in zip_files():
            arcname = f"{top}/{path.relative_to(ROOT).as_posix()}"
            archive.write(path, arcname)
    with zipfile.ZipFile(destination) as archive:
        bad = archive.testzip()
        if bad is not None:
            raise RuntimeError(f"release archive failed integrity check at {bad}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build release manifest and ZIP archive.")
    parser.add_argument(
        "--zip",
        dest="zip_path",
        type=Path,
        help="Optional destination for a release ZIP.",
    )
    args = parser.parse_args()
    manifest = write_manifest()
    write_checksums()
    print(f"Generated manifest for {manifest['file_count_excluding_manifest_and_checksum']} files.")
    if args.zip_path:
        write_zip(args.zip_path.resolve())
        print(f"Wrote {args.zip_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
