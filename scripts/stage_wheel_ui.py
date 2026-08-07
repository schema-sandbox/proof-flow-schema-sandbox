#!/usr/bin/env python3
"""Stage source and Vite UI assets as package data before building a wheel."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "apps" / "api" / "schemamath_api"
TARGET = PACKAGE / "_ui"


def main() -> int:
    prototype = ROOT / "prototype"
    web_dist = ROOT / "apps" / "web" / "dist"
    if not prototype.is_dir():
        raise SystemExit("prototype directory is missing")
    if not web_dist.is_dir():
        raise SystemExit("apps/web/dist is missing; run the Vite build first")
    if TARGET.exists():
        shutil.rmtree(TARGET)
    (TARGET / "prototype").parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(prototype, TARGET / "prototype")
    shutil.copytree(web_dist, TARGET / "web_dist")
    print(f"Staged wheel UI under {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
