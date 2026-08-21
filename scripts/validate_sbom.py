#!/usr/bin/env python3
"""Validate ProofFlow's CycloneDX SBOM, optionally against the official schema."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

from jsonschema import Draft7Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_BASE = (
    "https://raw.githubusercontent.com/CycloneDX/specification/1.5.1/schema/"
)
SCHEMA_FILES = ("bom-1.5.schema.json", "spdx.schema.json", "jsf-0.82.schema.json")
HEX_LENGTHS = {32, 40, 64, 96, 128}

sys.path.insert(0, str(ROOT / "scripts"))
from generate_sbom import (  # noqa: E402
    get_npm_dependencies,
    get_python_dependencies,
    project_versions,
)


def validate_internal(bom: dict[str, object]) -> list[str]:
    errors: list[str] = []
    display_version, normalized_version = project_versions()
    root_ref = f"pkg:pypi/proof-flow-schema-sandbox@{normalized_version}"

    if bom.get("$schema") != "http://cyclonedx.org/schema/bom-1.5.schema.json":
        errors.append("missing or incorrect CycloneDX 1.5 $schema")
    if bom.get("bomFormat") != "CycloneDX" or bom.get("specVersion") != "1.5":
        errors.append("incorrect CycloneDX format or specification version")

    metadata = bom.get("metadata")
    if not isinstance(metadata, dict):
        return [*errors, "metadata must be an object"]
    application = metadata.get("component")
    if not isinstance(application, dict):
        errors.append("metadata.component must be an object")
    else:
        if application.get("name") != "ProofFlow Schema Sandbox":
            errors.append("metadata component name mismatch")
        if application.get("version") != display_version:
            errors.append("metadata component version mismatch")
        if application.get("bom-ref") != root_ref or application.get("purl") != root_ref:
            errors.append("metadata component purl mismatch")
        if application.get("licenses") != [{"license": {"id": "MIT"}}]:
            errors.append("metadata component license must be MIT")

    components = bom.get("components")
    if not isinstance(components, list):
        return [*errors, "components must be an array"]
    refs: list[str] = []
    actual: set[tuple[str, str, str]] = set()
    for index, component in enumerate(components):
        if not isinstance(component, dict):
            errors.append(f"component {index} must be an object")
            continue
        ref = component.get("bom-ref")
        purl = component.get("purl")
        if not isinstance(ref, str) or ref != purl:
            errors.append(f"component {index} must use its purl as bom-ref")
        else:
            refs.append(ref)
        name = component.get("name")
        version = component.get("version")
        if isinstance(purl, str) and isinstance(name, str) and isinstance(version, str):
            actual.add((purl, name, version))
        licenses = component.get("licenses")
        if not isinstance(licenses, list) or len(licenses) != 1:
            errors.append(f"component {index} must have exactly one license declaration")
        else:
            choice = licenses[0]
            if not isinstance(choice, dict) or set(choice) not in ({"license"}, {"expression"}):
                errors.append(f"component {index} has an invalid license declaration")
        for hash_index, item in enumerate(component.get("hashes", [])):
            if not isinstance(item, dict):
                errors.append(f"component {index} hash {hash_index} must be an object")
                continue
            content = item.get("content")
            if (
                not isinstance(content, str)
                or len(content) not in HEX_LENGTHS
                or re.fullmatch(r"[0-9a-fA-F]+", content) is None
            ):
                errors.append(f"component {index} hash {hash_index} is not hexadecimal")

    if len(refs) != len(set(refs)):
        errors.append("component bom-ref values must be unique")

    expected_dependencies = [*get_python_dependencies(), *get_npm_dependencies()]
    expected = {
        (dependency["purl"], dependency["name"], dependency["version"])
        for dependency in expected_dependencies
    }
    if actual != expected:
        errors.append(
            f"component inventory differs from lock files: missing={len(expected - actual)}, "
            f"extra={len(actual - expected)}"
        )

    dependency_graph = bom.get("dependencies")
    if not isinstance(dependency_graph, list):
        errors.append("dependencies graph must be present")
    else:
        graph = {
            entry.get("ref"): entry.get("dependsOn")
            for entry in dependency_graph
            if isinstance(entry, dict)
        }
        if set(graph) != {root_ref, *refs}:
            errors.append("dependency graph references do not match component inventory")
        elif set(graph.get(root_ref, [])) != set(refs):
            errors.append("root dependency graph does not reference every component")
    return errors


def fetch_official_schemas() -> tuple[dict[str, object], dict[str, object]]:
    store: dict[str, object] = {}
    documents: dict[str, object] = {}
    for filename in SCHEMA_FILES:
        url = SCHEMA_BASE + filename
        with urllib.request.urlopen(url, timeout=30) as response:
            document = json.load(response)
        documents[filename] = document
        schema_id = str(document.get("$id", ""))
        if schema_id:
            store[schema_id] = document
            store[schema_id.replace("http://", "https://")] = document
        store[url] = document
    return documents, store


def validate_official(bom: dict[str, object]) -> list[str]:
    documents, store = fetch_official_schemas()
    schema = documents["bom-1.5.schema.json"]
    registry = Registry().with_resources(
        (uri, Resource.from_contents(document)) for uri, document in store.items()
    )
    validation_errors = sorted(
        Draft7Validator(
            schema,
            format_checker=FormatChecker(),
            registry=registry,
        ).iter_errors(bom),
        key=lambda error: list(error.absolute_path),
    )
    return [
        "/" + "/".join(str(part) for part in error.absolute_path) + ": " + error.message
        for error in validation_errors
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, default=ROOT / "sbom.cyclonedx.json")
    parser.add_argument(
        "--official",
        action="store_true",
        help="Also validate against CycloneDX's immutable 1.5.1 JSON Schema.",
    )
    args = parser.parse_args()
    bom = json.loads(args.path.read_text(encoding="utf-8"))
    errors = validate_internal(bom)
    if args.official:
        errors.extend(validate_official(bom))
    if errors:
        print(f"SBOM validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors[:30]:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        f"Validated {args.path}: {len(bom.get('components', []))} components, "
        f"official_schema={args.official}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
