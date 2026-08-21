from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_sbom import license_choice, sri_hashes  # noqa: E402
from validate_sbom import validate_internal  # noqa: E402


def test_sri_hashes_are_converted_to_cyclonedx_hex() -> None:
    digest = bytes(range(32))
    integrity = "sha256-" + base64.b64encode(digest).decode("ascii")

    assert sri_hashes(integrity) == [
        {"alg": "SHA-256", "content": digest.hex()}
    ]


def test_spdx_expressions_are_not_emitted_as_license_ids() -> None:
    assert license_choice("MIT") == {"license": {"id": "MIT"}}
    assert license_choice("(MPL-2.0 OR Apache-2.0)") == {
        "expression": "MPL-2.0 OR Apache-2.0"
    }


def test_committed_sbom_matches_the_release_locks() -> None:
    bom = json.loads((ROOT / "sbom.cyclonedx.json").read_text(encoding="utf-8"))

    assert validate_internal(bom) == []
