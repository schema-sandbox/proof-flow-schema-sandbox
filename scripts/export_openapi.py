from __future__ import annotations

import json
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

from schemamath_api.main import create_app  # noqa: E402


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="schemamath-openapi-") as temp_dir:
        temp_root = Path(temp_dir)
        app = create_app(temp_root / "workspaces", temp_root / "plugins")
        schema = app.openapi()
    destination = ROOT / "api"
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "openapi.json").write_text(
        json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (destination / "openapi.yaml").write_text(
        yaml.safe_dump(schema, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    print(f"Exported OpenAPI with {len(schema.get('paths', {}))} paths.")


if __name__ == "__main__":
    main()
