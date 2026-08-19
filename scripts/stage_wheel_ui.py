#!/usr/bin/env python3
"""Stage source/Vite UI assets and built-in plugins as package data before building a wheel."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "apps" / "api" / "schemamath_api"
TARGET_UI = PACKAGE / "_ui"
TARGET_PLUGINS = PACKAGE / "_plugins"


def main() -> int:
    prototype = ROOT / "prototype"
    web_dist = ROOT / "apps" / "web" / "dist"
    plugins_builtin = ROOT / "plugins" / "builtin"
    if not prototype.is_dir():
        raise SystemExit("prototype directory is missing")
    if not web_dist.is_dir():
        raise SystemExit("apps/web/dist is missing; run the Vite build first")
    if not plugins_builtin.is_dir():
        raise SystemExit("plugins/builtin directory is missing")

    if TARGET_UI.exists():
        shutil.rmtree(TARGET_UI)
    (TARGET_UI / "prototype").parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(prototype, TARGET_UI / "prototype")
    shutil.copytree(web_dist, TARGET_UI / "web_dist")
    print(f"Staged wheel UI under {TARGET_UI}")

    if TARGET_PLUGINS.exists():
        shutil.rmtree(TARGET_PLUGINS)
    (TARGET_PLUGINS / "builtin").parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(plugins_builtin, TARGET_PLUGINS / "builtin")
    print(f"Staged wheel plugins under {TARGET_PLUGINS}")

    notices_file = ROOT / "THIRD_PARTY_NOTICES.md"
    if notices_file.is_file():
        shutil.copy2(notices_file, PACKAGE / "THIRD_PARTY_NOTICES.md")
        print(f"Staged THIRD_PARTY_NOTICES.md under {PACKAGE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
