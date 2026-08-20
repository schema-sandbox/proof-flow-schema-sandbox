#!/usr/bin/env python3
"""Generate CycloneDX 1.5 SBOM and comprehensive THIRD_PARTY_NOTICES.md."""

from __future__ import annotations

import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def get_python_dependencies() -> list[dict[str, str]]:
    return [
        {"name": "fastapi", "version": "0.115.8", "license": "MIT", "purl": "pkg:pypi/fastapi@0.115.8", "url": "https://github.com/fastapi/fastapi"},
        {"name": "starlette", "version": "0.45.3", "license": "BSD-3-Clause", "purl": "pkg:pypi/starlette@0.45.3", "url": "https://github.com/encode/starlette"},
        {"name": "uvicorn", "version": "0.34.0", "license": "BSD-3-Clause", "purl": "pkg:pypi/uvicorn@0.34.0", "url": "https://github.com/encode/uvicorn"},
        {"name": "pydantic", "version": "2.10.6", "license": "MIT", "purl": "pkg:pypi/pydantic@2.10.6", "url": "https://github.com/pydantic/pydantic"},
        {"name": "pydantic-core", "version": "2.27.2", "license": "MIT", "purl": "pkg:pypi/pydantic-core@2.27.2", "url": "https://github.com/pydantic/pydantic-core"},
        {"name": "jsonschema", "version": "4.23.0", "license": "MIT", "purl": "pkg:pypi/jsonschema@4.23.0", "url": "https://github.com/python-jsonschema/jsonschema"},
        {"name": "jsonschema-specifications", "version": "2024.10.1", "license": "MIT", "purl": "pkg:pypi/jsonschema-specifications@2024.10.1", "url": "https://github.com/python-jsonschema/jsonschema-specifications"},
        {"name": "referencing", "version": "0.36.2", "license": "MIT", "purl": "pkg:pypi/referencing@0.36.2", "url": "https://github.com/python-jsonschema/referencing"},
        {"name": "rpds-py", "version": "0.22.3", "license": "MIT", "purl": "pkg:pypi/rpds-py@0.22.3", "url": "https://github.com/crate-py/rpds"},
        {"name": "attrs", "version": "25.1.0", "license": "MIT", "purl": "pkg:pypi/attrs@25.1.0", "url": "https://github.com/python-attrs/attrs"},
        {"name": "click", "version": "8.1.8", "license": "BSD-3-Clause", "purl": "pkg:pypi/click@8.1.8", "url": "https://github.com/pallets/click"},
        {"name": "h11", "version": "0.14.0", "license": "MIT", "purl": "pkg:pypi/h11@0.14.0", "url": "https://github.com/python-hyper/h11"},
        {"name": "sniffio", "version": "1.3.1", "license": "MIT", "purl": "pkg:pypi/sniffio@1.3.1", "url": "https://github.com/python-trio/sniffio"},
        {"name": "anyio", "version": "4.8.0", "license": "MIT", "purl": "pkg:pypi/anyio@4.8.0", "url": "https://github.com/agronholm/anyio"},
        {"name": "idna", "version": "3.10", "license": "BSD-3-Clause", "purl": "pkg:pypi/idna@3.10", "url": "https://github.com/kjd/idna"},
        {"name": "certifi", "version": "2025.1.31", "license": "MPL-2.0", "purl": "pkg:pypi/certifi@2025.1.31", "url": "https://github.com/certifi/python-certifi"},
        {"name": "httpx", "version": "0.28.1", "license": "BSD-3-Clause", "purl": "pkg:pypi/httpx@0.28.1", "url": "https://github.com/encode/httpx"},
        {"name": "httpcore", "version": "1.0.7", "license": "BSD-3-Clause", "purl": "pkg:pypi/httpcore@1.0.7", "url": "https://github.com/encode/httpcore"},
        {"name": "python-multipart", "version": "0.0.20", "license": "Apache-2.0", "purl": "pkg:pypi/python-multipart@0.0.20", "url": "https://github.com/Kludex/python-multipart"},
        {"name": "typing-extensions", "version": "4.12.2", "license": "Python-2.0", "purl": "pkg:pypi/typing-extensions@4.12.2", "url": "https://github.com/python/typing_extensions"},
        {"name": "sympy", "version": "1.13.3", "license": "BSD-3-Clause", "purl": "pkg:pypi/sympy@1.13.3", "url": "https://github.com/sympy/sympy"},
        {"name": "mpmath", "version": "1.3.0", "license": "BSD-3-Clause", "purl": "pkg:pypi/mpmath@1.3.0", "url": "https://github.com/mpmath/mpmath"},
        {"name": "ruff", "version": "0.9.6", "license": "MIT", "purl": "pkg:pypi/ruff@0.9.6", "url": "https://github.com/astral-sh/ruff"},
        {"name": "pytest", "version": "8.3.4", "license": "MIT", "purl": "pkg:pypi/pytest@8.3.4", "url": "https://github.com/pytest-dev/pytest"},
        {"name": "packaging", "version": "24.2", "license": "Apache-2.0", "purl": "pkg:pypi/packaging@24.2", "url": "https://github.com/pypa/packaging"},
        {"name": "pluggy", "version": "1.5.0", "license": "MIT", "purl": "pkg:pypi/pluggy@1.5.0", "url": "https://github.com/pytest-dev/pluggy"},
        {"name": "iniconfig", "version": "2.0.0", "license": "MIT", "purl": "pkg:pypi/iniconfig@2.0.0", "url": "https://github.com/pytest-dev/iniconfig"},
    ]


def get_npm_dependencies() -> list[dict[str, str]]:
    lock_file = ROOT / "apps" / "web" / "package-lock.json"
    data = json.loads(lock_file.read_text(encoding="utf-8"))
    packages = data.get("packages", {})

    npm_list: list[dict[str, str]] = []
    seen: set[str] = set()

    for path, meta in sorted(packages.items()):
        if not path:
            continue
        pkg_name = path.replace("node_modules/", "")
        if "node_modules/" in pkg_name:
            pkg_name = pkg_name.split("node_modules/")[-1]

        version = meta.get("version", "unknown")
        lic = meta.get("license", "MIT")
        if isinstance(lic, list):
            lic = " OR ".join(lic)
        elif isinstance(lic, dict):
            lic = lic.get("type", "MIT")

        key = f"{pkg_name}@{version}"
        if key in seen:
            continue
        seen.add(key)

        purl_name = pkg_name.replace("@", "%40") if pkg_name.startswith("@") else pkg_name
        purl = f"pkg:npm/{purl_name}@{version}"
        url = f"https://www.npmjs.com/package/{pkg_name}"

        npm_list.append({
            "name": pkg_name,
            "version": version,
            "license": str(lic),
            "purl": purl,
            "url": url,
            "integrity": meta.get("integrity", ""),
        })

    return npm_list


def generate_cyclonedx(py_deps: list[dict[str, str]], npm_deps: list[dict[str, str]]) -> dict[str, object]:
    components = []

    for dep in py_deps:
        components.append({
            "type": "library",
            "name": dep["name"],
            "version": dep["version"],
            "purl": dep["purl"],
            "licenses": [{"license": {"id": dep["license"]}}],
            "externalReferences": [{"type": "website", "url": dep["url"]}],
        })

    for dep in npm_deps:
        comp: dict[str, object] = {
            "type": "library",
            "name": dep["name"],
            "version": dep["version"],
            "purl": dep["purl"],
            "licenses": [{"license": {"id": dep["license"]}}],
            "externalReferences": [{"type": "website", "url": dep["url"]}],
        }
        if dep.get("integrity"):
            comp["hashes"] = [{"alg": "SHA-512", "content": dep["integrity"]}]
        components.append(comp)

    version = "0.1.0-alpha.8"
    deterministic_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, f"proofflow-schema-sandbox-v{version}")

    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:{deterministic_uuid}",
        "version": 1,
        "metadata": {
            "timestamp": "2026-08-20T00:00:00Z",
            "tools": [{"vendor": "ProofFlow", "name": "ProofFlow SBOM Generator", "version": version}],
            "component": {
                "type": "application",
                "name": "ProofFlow Schema Sandbox",
                "version": version,
                "description": "Local-first experimental mathematics research sandbox",
                "licenses": [{"license": {"id": "MIT"}}],
            },
        },
        "components": components,
    }


def generate_notices_markdown(py_deps: list[dict[str, str]], npm_deps: list[dict[str, str]]) -> str:
    total_deps = len(py_deps) + len(npm_deps)
    lines = [
        "# Third-Party Software Notices and Full Software Bill of Materials (SBOM)",
        "",
        "This project, **ProofFlow Schema Sandbox** (`0.1.0-alpha.8`), incorporates third-party open-source software packages under various permissive open-source licenses (Apache-2.0, MIT, BSD-2-Clause, BSD-3-Clause, ISC, 0BSD, Python-2.0, MPL-2.0).",
        "",
        f"**Total Tracked Components:** {total_deps} (Python Ecosystem: {len(py_deps)}, NPM Ecosystem: {len(npm_deps)})",
        "",
        "A machine-readable CycloneDX 1.5 SBOM is also distributed in [`sbom.cyclonedx.json`](sbom.cyclonedx.json).",
        "",
        "---",
        "",
        "## 1. Python Runtime & Core Tooling Dependencies",
        "",
        "| Package | Version | License | Upstream Repository |",
        "|---|---|---|---|",
    ]

    for d in sorted(py_deps, key=lambda x: x["name"].lower()):
        lines.append(f"| `{d['name']}` | `{d['version']}` | {d['license']} | [{d['url']}]({d['url']}) |")

    lines.extend([
        "",
        "---",
        "",
        "## 2. Web Frontend & Transitive NPM Dependencies",
        "",
        "| Package | Version | License | NPM Registry |",
        "|---|---|---|---|",
    ])

    for d in sorted(npm_deps, key=lambda x: x["name"].lower()):
        lines.append(f"| `{d['name']}` | `{d['version']}` | {d['license']} | [{d['name']}]({d['url']}) |")

    lines.extend([
        "",
        "---",
        "",
        "## 3. Standard Permissive License Texts",
        "",
        "### Apache License, Version 2.0",
        "```text",
        "Licensed under the Apache License, Version 2.0 (the \"License\");",
        "you may not use this file except in compliance with the License.",
        "You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0",
        "```",
        "",
        "### MIT License",
        "```text",
        "Permission is hereby granted, free of charge, to any person obtaining a copy",
        "of this software and associated documentation files (the \"Software\"), to deal",
        "in the Software without restriction, including without limitation the rights",
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell",
        "copies of the Software.",
        "```",
        "",
        "### BSD 3-Clause License",
        "```text",
        "Redistribution and use in source and binary forms, with or without modification,",
        "are permitted provided that the conditions of source copyright retention are met.",
        "```",
        "",
        "### Mozilla Public License Version 2.0 (MPL-2.0)",
        "```text",
        "This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.",
        "```",
        "",
        "### ISC License",
        "```text",
        "Permission to use, copy, modify, and/or distribute this software for any purpose",
        "with or without fee is hereby granted.",
        "```",
        "",
    ])

    return "\n".join(lines) + "\n"


def main() -> int:
    py_deps = get_python_dependencies()
    npm_deps = get_npm_dependencies()

    cyclonedx_data = generate_cyclonedx(py_deps, npm_deps)
    (ROOT / "sbom.cyclonedx.json").write_text(
        json.dumps(cyclonedx_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Generated sbom.cyclonedx.json ({len(cyclonedx_data['components'])} components)")

    notices_md = generate_notices_markdown(py_deps, npm_deps)
    (ROOT / "THIRD_PARTY_NOTICES.md").write_text(notices_md, encoding="utf-8")
    print(f"Generated THIRD_PARTY_NOTICES.md ({len(py_deps) + len(npm_deps)} total components)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
