#!/usr/bin/env python3
"""Fail closed when active release metadata diverges from pyproject.toml."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

import yaml
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_NAME = "ProofFlow Schema Sandbox"
EXPECTED_PACKAGE = "proof-flow-schema-sandbox"
EXPECTED_LICENSE = "MIT"
EXPECTED_REPOSITORY = "https://github.com/schema-sandbox/proof-flow-schema-sandbox.git"
EXPECTED_REPOSITORY_WEB = EXPECTED_REPOSITORY.removesuffix(".git")


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def requirement_map(values: list[str]) -> dict[str, tuple[tuple[str, ...], str, str]]:
    result: dict[str, tuple[tuple[str, ...], str, str]] = {}
    for value in values:
        requirement = Requirement(value)
        result[canonicalize_name(requirement.name)] = (
            tuple(sorted(requirement.extras)),
            str(requirement.specifier),
            str(requirement.marker or ""),
        )
    return result


def main() -> int:
    failures: list[str] = []
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]
    version = str(project["version"])
    if project["name"] != EXPECTED_PACKAGE:
        fail("pyproject package name mismatch", failures)
    if project.get("license") != EXPECTED_LICENSE:
        fail("pyproject license mismatch", failures)
    if project.get("urls", {}).get("Repository") != EXPECTED_REPOSITORY_WEB:
        fail("pyproject repository URL mismatch", failures)

    init_text = (ROOT / "apps" / "api" / "schemamath_api" / "__init__.py").read_text(
        encoding="utf-8"
    )
    match = re.search(r'^__version__ = "([^"]+)"$', init_text, re.MULTILINE)
    if match is None or match.group(1) != version:
        fail("Python package version mismatch", failures)

    package_json = json.loads((ROOT / "apps" / "web" / "package.json").read_text(encoding="utf-8"))
    package_lock = json.loads(
        (ROOT / "apps" / "web" / "package-lock.json").read_text(encoding="utf-8")
    )
    if package_json.get("version") != version:
        fail("frontend package.json version mismatch", failures)
    if package_json.get("license") != EXPECTED_LICENSE:
        fail("frontend package.json license mismatch", failures)
    if package_lock.get("version") != version:
        fail("frontend package-lock.json version mismatch", failures)
    if package_lock.get("packages", {}).get("", {}).get("version") != version:
        fail("frontend lock root version mismatch", failures)
    if package_lock.get("packages", {}).get("", {}).get("license") != EXPECTED_LICENSE:
        fail("frontend lock root license mismatch", failures)

    openapi_json = json.loads((ROOT / "api" / "openapi.json").read_text(encoding="utf-8"))
    openapi_yaml = yaml.safe_load((ROOT / "api" / "openapi.yaml").read_text(encoding="utf-8"))
    if openapi_json.get("info", {}).get("version") != version:
        fail("OpenAPI JSON version mismatch", failures)
    if openapi_yaml.get("info", {}).get("version") != version:
        fail("OpenAPI YAML version mismatch", failures)

    release_notes = ROOT / "docs" / f"RELEASE_NOTES_v{version}.md"
    if not release_notes.is_file():
        fail(f"missing release notes {release_notes.name}", failures)
        release_text = ""
    else:
        release_text = release_notes.read_text(encoding="utf-8")
    required_release_tokens = {
        EXPECTED_NAME,
        f"v{version}",
        EXPECTED_LICENSE,
        EXPECTED_REPOSITORY,
    }
    for token in required_release_tokens:
        if token not in release_text:
            fail(f"release notes missing {token!r}", failures)
    if "github.com/psi-run/ProofFlow" in release_text:
        fail("release notes contain the retired repository URL", failures)

    for path in (ROOT / "README.md", ROOT / "README_CN.md", ROOT / "SECURITY.md"):
        text = path.read_text(encoding="utf-8")
        if EXPECTED_NAME not in text or version not in text:
            fail(f"{path.name} name/version mismatch", failures)
    if "License: MIT." not in (ROOT / "README.md").read_text(encoding="utf-8"):
        fail("README.md license mismatch", failures)
    if "许可证：MIT。" not in (ROOT / "README_CN.md").read_text(encoding="utf-8"):
        fail("README_CN.md license mismatch", failures)
    if version not in (ROOT / "apps" / "web" / "README.md").read_text(encoding="utf-8"):
        fail("frontend README version mismatch", failures)
    if version not in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"):
        fail("CHANGELOG version mismatch", failures)
    compose = (ROOT / "docker-compose.prod.yml").read_text(encoding="utf-8")
    if f"proofflow/proofflow-api:{version}" not in compose:
        fail("production Compose image version mismatch", failures)

    locked: dict[str, str] = {}
    for line in (ROOT / "requirements-release.lock").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        requirement = Requirement(line)
        pins = [spec.version for spec in requirement.specifier if spec.operator == "=="]
        if len(pins) != 1:
            fail(f"release lock is not exact: {line}", failures)
            continue
        locked[canonicalize_name(requirement.name)] = pins[0]
    declared_requirements = [
        *project["dependencies"],
        *project["optional-dependencies"]["dev"],
        *pyproject["build-system"]["requires"],
    ]
    for requirement_text in declared_requirements:
        requirement = Requirement(requirement_text)
        pins = [spec.version for spec in requirement.specifier if spec.operator == "=="]
        name = canonicalize_name(requirement.name)
        if len(pins) != 1 or locked.get(name) != pins[0]:
            fail(f"pyproject dependency is not aligned with release lock: {requirement_text}", failures)

    requirement_files = {
        "requirements.txt": project["dependencies"],
        "requirements-dev.txt": project["optional-dependencies"]["dev"],
    }
    for filename, expected_values in requirement_files.items():
        actual_values = [
            line.strip()
            for line in (ROOT / filename).read_text(encoding="utf-8").splitlines()
            if line.strip()
            and not line.lstrip().startswith("#")
            and not line.lstrip().startswith("-r ")
        ]
        actual = requirement_map(actual_values)
        expected = requirement_map(expected_values)
        if actual != expected:
            fail(f"{filename} differs from pyproject dependency declarations", failures)

    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    if 'tags: [ "v*" ]' not in workflow:
        fail("CI does not trigger on version tags", failures)
    frontend_position = workflow.find("Build and stage frontend before tests")
    pytest_position = workflow.find("Run Pytest Test Suite")
    if frontend_position < 0 or pytest_position < 0 or frontend_position > pytest_position:
        fail("CI runs tests before staging the frontend", failures)
    for token in (
        "python -m pip_audit -r requirements-release.lock",
        "needs: release-gate",
        'gh release create "$GITHUB_REF_NAME"',
        f"RELEASE_NOTES_v{version}.md",
    ):
        if token not in workflow:
            fail(f"CI release workflow missing {token!r}", failures)

    if (ROOT / ".git").exists():
        tracked_fixture = subprocess.run(
            ["git", "ls-files", "--error-unmatch", "examples/demo_open_research_project_alpha2.smath.zip"],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
        if tracked_fixture.returncode != 0:
            fail("required Alpha.2 ZIP fixture is not tracked", failures)
        for generated in ("package_manifest.json", "SHA256SUMS.txt"):
            tracked = subprocess.run(
                ["git", "ls-files", "--error-unmatch", generated],
                cwd=ROOT,
                capture_output=True,
                check=False,
            )
            if tracked.returncode == 0:
                fail(f"detached release output remains tracked: {generated}", failures)

    if failures:
        print(f"Release metadata validation failed with {len(failures)} error(s):", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"Release metadata is consistent for {EXPECTED_NAME} {version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
