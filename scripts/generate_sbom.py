#!/usr/bin/env python3
"""Generate the deterministic CycloneDX 1.5 SBOM and attribution inventory."""

from __future__ import annotations

import base64
import json
import tomllib
import uuid
from importlib import metadata
from pathlib import Path
from urllib.parse import quote

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version

ROOT = Path(__file__).resolve().parents[1]
LOCK_FILE = ROOT / "requirements-release.lock"
PACKAGE_LOCK = ROOT / "apps" / "web" / "package-lock.json"
GENERATED_AT = "2026-08-21T00:00:00Z"

# License and upstream data is kept explicit so the generated SBOM is identical
# on Windows and Linux. Versions always come from requirements-release.lock and
# active entries are checked against the environment before a release build.
PYTHON_METADATA: dict[str, tuple[str, str]] = {
    "annotated-doc": ("MIT", "https://github.com/fastapi/annotated-doc"),
    "annotated-types": ("MIT", "https://github.com/annotated-types/annotated-types"),
    "anyio": ("MIT", "https://github.com/agronholm/anyio"),
    "attrs": ("MIT", "https://github.com/python-attrs/attrs"),
    "certifi": ("MPL-2.0", "https://github.com/certifi/python-certifi"),
    "click": ("BSD-3-Clause", "https://github.com/pallets/click"),
    "colorama": ("BSD-3-Clause", "https://github.com/tartley/colorama"),
    "coverage": ("Apache-2.0", "https://github.com/nedbat/coveragepy"),
    "fastapi": ("MIT", "https://github.com/fastapi/fastapi"),
    "h11": ("MIT", "https://github.com/python-hyper/h11"),
    "httpcore": ("BSD-3-Clause", "https://github.com/encode/httpcore"),
    "httptools": ("MIT", "https://github.com/MagicStack/httptools"),
    "httpx": ("BSD-3-Clause", "https://github.com/encode/httpx"),
    "idna": ("BSD-3-Clause", "https://github.com/kjd/idna"),
    "iniconfig": ("MIT", "https://github.com/pytest-dev/iniconfig"),
    "jsonschema": ("MIT", "https://github.com/python-jsonschema/jsonschema"),
    "jsonschema-specifications": (
        "MIT",
        "https://github.com/python-jsonschema/jsonschema-specifications",
    ),
    "mpmath": ("BSD-3-Clause", "https://github.com/mpmath/mpmath"),
    "packaging": ("Apache-2.0 OR BSD-2-Clause", "https://github.com/pypa/packaging"),
    "pip": ("MIT", "https://github.com/pypa/pip"),
    "pluggy": ("MIT", "https://github.com/pytest-dev/pluggy"),
    "pydantic": ("MIT", "https://github.com/pydantic/pydantic"),
    "pydantic-core": ("MIT", "https://github.com/pydantic/pydantic-core"),
    "pygments": ("BSD-2-Clause", "https://github.com/pygments/pygments"),
    "pytest": ("MIT", "https://github.com/pytest-dev/pytest"),
    "pytest-cov": ("MIT", "https://github.com/pytest-dev/pytest-cov"),
    "python-dotenv": ("BSD-3-Clause", "https://github.com/theskumar/python-dotenv"),
    "python-multipart": ("Apache-2.0", "https://github.com/Kludex/python-multipart"),
    "pyyaml": ("MIT", "https://github.com/yaml/pyyaml"),
    "referencing": ("MIT", "https://github.com/python-jsonschema/referencing"),
    "rpds-py": ("MIT", "https://github.com/crate-py/rpds"),
    "ruff": ("MIT", "https://github.com/astral-sh/ruff"),
    "setuptools": ("MIT", "https://github.com/pypa/setuptools"),
    "starlette": ("BSD-3-Clause", "https://github.com/Kludex/starlette"),
    "sympy": ("BSD-3-Clause", "https://github.com/sympy/sympy"),
    "typing-extensions": ("PSF-2.0", "https://github.com/python/typing_extensions"),
    "typing-inspection": ("MIT", "https://github.com/pydantic/typing-inspection"),
    "uvicorn": ("BSD-3-Clause", "https://github.com/Kludex/uvicorn"),
    "uvloop": ("MIT OR Apache-2.0", "https://github.com/MagicStack/uvloop"),
    "watchfiles": ("MIT", "https://github.com/samuelcolvin/watchfiles"),
    "websockets": ("BSD-3-Clause", "https://github.com/python-websockets/websockets"),
    "wheel": ("MIT", "https://github.com/pypa/wheel"),
}

SPDX_IDS = {
    "0BSD",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "CC-BY-4.0",
    "CC0-1.0",
    "ISC",
    "MIT",
    "MPL-2.0",
    "PSF-2.0",
    "Unlicense",
}


def project_versions() -> tuple[str, str]:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    display = str(data["project"]["version"])
    return display, str(Version(display))


def license_choice(value: str) -> dict[str, object]:
    value = value.strip() or "UNKNOWN"
    if value.startswith("(") and value.endswith(")"):
        value = value[1:-1].strip()
    if " AND " in value or " OR " in value or " WITH " in value:
        return {"expression": value}
    if value in SPDX_IDS:
        return {"license": {"id": value}}
    return {"license": {"name": value}}


def sri_hashes(integrity: str) -> list[dict[str, str]]:
    hashes: list[dict[str, str]] = []
    algorithms = {"sha256": "SHA-256", "sha384": "SHA-384", "sha512": "SHA-512"}
    for token in integrity.split():
        if "-" not in token:
            continue
        algorithm, encoded = token.split("-", 1)
        if algorithm not in algorithms:
            continue
        try:
            digest = base64.b64decode(encoded, validate=True)
        except ValueError:
            continue
        hashes.append({"alg": algorithms[algorithm], "content": digest.hex()})
    return hashes


def get_python_dependencies() -> list[dict[str, str]]:
    dependencies: list[dict[str, str]] = []
    for raw_line in LOCK_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        requirement = Requirement(line)
        pins = [spec.version for spec in requirement.specifier if spec.operator == "=="]
        if len(pins) != 1:
            raise RuntimeError(f"release lock entry must have one exact pin: {line}")
        name = canonicalize_name(requirement.name)
        if name not in PYTHON_METADATA:
            raise RuntimeError(f"missing Python SBOM metadata for {name}")
        version = pins[0]
        if requirement.marker is None or requirement.marker.evaluate():
            installed = metadata.version(requirement.name)
            if Version(installed) != Version(version):
                raise RuntimeError(
                    f"release environment drift for {name}: locked {version}, installed {installed}"
                )
        license_id, url = PYTHON_METADATA[name]
        dependencies.append(
            {
                "name": name,
                "version": version,
                "license": license_id,
                "purl": f"pkg:pypi/{name}@{version}",
                "url": url,
            }
        )
    return sorted(dependencies, key=lambda item: (item["name"], item["version"]))


def get_npm_dependencies() -> list[dict[str, str]]:
    data = json.loads(PACKAGE_LOCK.read_text(encoding="utf-8"))
    dependencies: list[dict[str, str]] = []
    seen: set[str] = set()
    for path, package in sorted(data.get("packages", {}).items()):
        if not path:
            continue
        name = path.rsplit("node_modules/", 1)[-1]
        version = str(package.get("version", "unknown"))
        key = f"{name}@{version}"
        if key in seen:
            continue
        seen.add(key)
        license_id = package.get("license", "UNKNOWN")
        if isinstance(license_id, list):
            license_id = " OR ".join(str(value) for value in license_id)
        elif isinstance(license_id, dict):
            license_id = license_id.get("type", "UNKNOWN")
        encoded_name = quote(name, safe="/.-_~")
        dependencies.append(
            {
                "name": name,
                "version": version,
                "license": str(license_id),
                "purl": f"pkg:npm/{encoded_name}@{version}",
                "url": f"https://www.npmjs.com/package/{name}",
                "integrity": str(package.get("integrity", "")),
            }
        )
    return dependencies


def dependency_component(dependency: dict[str, str]) -> dict[str, object]:
    component: dict[str, object] = {
        "type": "library",
        "bom-ref": dependency["purl"],
        "name": dependency["name"],
        "version": dependency["version"],
        "purl": dependency["purl"],
        "licenses": [license_choice(dependency["license"])],
        "externalReferences": [{"type": "website", "url": dependency["url"]}],
    }
    hashes = sri_hashes(dependency.get("integrity", ""))
    if hashes:
        component["hashes"] = hashes
    return component


def generate_cyclonedx(
    python_dependencies: list[dict[str, str]],
    npm_dependencies: list[dict[str, str]],
) -> dict[str, object]:
    display_version, normalized_version = project_versions()
    root_ref = f"pkg:pypi/proof-flow-schema-sandbox@{normalized_version}"
    components = [
        dependency_component(dependency)
        for dependency in [*python_dependencies, *npm_dependencies]
    ]
    component_refs = [str(component["bom-ref"]) for component in components]
    deterministic_uuid = uuid.uuid5(uuid.NAMESPACE_URL, f"{root_ref}:cyclonedx-1.5")
    return {
        "$schema": "http://cyclonedx.org/schema/bom-1.5.schema.json",
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:{deterministic_uuid}",
        "version": 1,
        "metadata": {
            "timestamp": GENERATED_AT,
            "tools": [
                {
                    "vendor": "ProofFlow",
                    "name": "ProofFlow SBOM Generator",
                    "version": display_version,
                }
            ],
            "component": {
                "type": "application",
                "bom-ref": root_ref,
                "name": "ProofFlow Schema Sandbox",
                "version": display_version,
                "description": "Local-first experimental mathematics research sandbox",
                "purl": root_ref,
                "licenses": [{"license": {"id": "MIT"}}],
            },
            "properties": [
                {"name": "proof-flow:python-lock", "value": "requirements-release.lock"},
                {"name": "proof-flow:npm-lock", "value": "apps/web/package-lock.json"},
            ],
        },
        "components": components,
        "dependencies": [
            {"ref": root_ref, "dependsOn": component_refs},
            *({"ref": ref, "dependsOn": []} for ref in component_refs),
        ],
    }


def generate_notices_markdown(
    python_dependencies: list[dict[str, str]],
    npm_dependencies: list[dict[str, str]],
) -> str:
    display_version, _ = project_versions()
    total = len(python_dependencies) + len(npm_dependencies)
    lines = [
        "# Third-Party Software Attribution and Component Inventory",
        "",
        f"ProofFlow Schema Sandbox `{display_version}` uses the components listed below.",
        "The corresponding machine-readable CycloneDX 1.5 document is",
        "[`sbom.cyclonedx.json`](sbom.cyclonedx.json). License identifiers and",
        "expressions are taken from the locked package metadata; upstream license",
        "files remain authoritative.",
        "",
        f"**Tracked Components:** {total} (Python: {len(python_dependencies)}, NPM: {len(npm_dependencies)})",
        "",
        "## Python Runtime and Release Tooling",
        "",
        "| Package | Version | License | Upstream |",
        "|---|---|---|---|",
    ]
    for dependency in python_dependencies:
        lines.append(
            f"| `{dependency['name']}` | `{dependency['version']}` | "
            f"{dependency['license']} | [{dependency['url']}]({dependency['url']}) |"
        )
    lines.extend(
        [
            "",
            "## Web Frontend and Build Dependencies",
            "",
            "| Package | Version | License | Registry |",
            "|---|---|---|---|",
        ]
    )
    for dependency in sorted(
        npm_dependencies, key=lambda item: (item["name"].lower(), item["version"])
    ):
        lines.append(
            f"| `{dependency['name']}` | `{dependency['version']}` | "
            f"{dependency['license']} | [{dependency['name']}]({dependency['url']}) |"
        )
    lines.extend(
        [
            "",
            "## Project License",
            "",
            "ProofFlow Schema Sandbox itself is distributed under the MIT License;",
            "see [`LICENSE`](LICENSE). Third-party components retain their own licenses.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    python_dependencies = get_python_dependencies()
    npm_dependencies = get_npm_dependencies()
    cyclonedx_data = generate_cyclonedx(python_dependencies, npm_dependencies)
    (ROOT / "sbom.cyclonedx.json").write_text(
        json.dumps(cyclonedx_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    notices = generate_notices_markdown(python_dependencies, npm_dependencies)
    (ROOT / "THIRD_PARTY_NOTICES.md").write_text(notices, encoding="utf-8")
    total = len(cyclonedx_data["components"])
    print(f"Generated CycloneDX 1.5 SBOM and attribution inventory for {total} components.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
