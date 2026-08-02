from __future__ import annotations

from pathlib import Path

import pytest
from schemamath_api.config import Settings
from schemamath_api.service import SchemaMathService


@pytest.fixture
def service(tmp_path: Path) -> SchemaMathService:
    return SchemaMathService(
        Settings.from_environment(tmp_path / "workspaces", tmp_path / "plugins")
    )
