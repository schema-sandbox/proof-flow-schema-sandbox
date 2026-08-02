#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"


def main() -> int:
    failures: list[str] = []
    schema_count = 0
    for path in sorted(SCHEMA_DIR.glob("*.json")):
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            schema_count += 1
        except Exception as exc:
            failures.append(f"{path.relative_to(ROOT)}: {exc}")

    if failures:
        print("Schema validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Validated {schema_count} JSON Schema documents.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
