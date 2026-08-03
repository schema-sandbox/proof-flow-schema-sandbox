"""Export ModuleManifest JSON Schema to schemas/ directory."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add the API package to path
api_dir = Path(__file__).resolve().parent.parent / "apps" / "api"
sys.path.insert(0, str(api_dir))

from schemamath_api.k0.manifest import ModuleManifest  # noqa: E402


def main() -> None:
    schema = ModuleManifest.model_json_schema()
    out = Path(__file__).resolve().parent.parent / "schemas" / "module-manifest.schema.json"
    out.write_text(
        json.dumps(schema, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Exported: {out}  ({out.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
