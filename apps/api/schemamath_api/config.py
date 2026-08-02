from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings for the local-only experimental service."""

    workspace_root: Path
    plugin_root: Path
    maximum_upload_bytes: int = 25 * 1024 * 1024
    maximum_chat_import_chars: int = 2_000_000
    maximum_plugin_output_bytes: int = 10 * 1024 * 1024
    maximum_plugin_output_files: int = 64

    @classmethod
    def from_environment(
        cls, workspace_root: Path | None = None, plugin_root: Path | None = None
    ) -> Settings:
        def env_value(preferred: str, legacy: str, default: str) -> str:
            """Read the ProofFlow name first while preserving Alpha.2 variables."""
            return os.environ.get(preferred, os.environ.get(legacy, default))

        root = (
            workspace_root
            or Path(
                env_value(
                    "PROOFFLOW_WORKSPACE",
                    "SCHEMAMATH_WORKSPACE",
                    "~/.schemamath/workspaces",
                )
            ).expanduser()
        )
        plugin_root = (
            plugin_root
            or Path(
                env_value(
                    "PROOFFLOW_PLUGIN_ROOT",
                    "SCHEMAMATH_PLUGIN_ROOT",
                    "~/.schemamath/plugins",
                )
            ).expanduser()
        )
        max_upload = int(
            env_value(
                "PROOFFLOW_MAX_UPLOAD_BYTES",
                "SCHEMAMATH_MAX_UPLOAD_BYTES",
                str(25 * 1024 * 1024),
            )
        )
        max_chat_chars = int(
            env_value(
                "PROOFFLOW_MAX_CHAT_IMPORT_CHARS",
                "SCHEMAMATH_MAX_CHAT_IMPORT_CHARS",
                "2000000",
            )
        )
        max_plugin_output = int(
            env_value(
                "PROOFFLOW_MAX_PLUGIN_OUTPUT_BYTES",
                "SCHEMAMATH_MAX_PLUGIN_OUTPUT_BYTES",
                str(10 * 1024 * 1024),
            )
        )
        max_plugin_files = int(
            env_value(
                "PROOFFLOW_MAX_PLUGIN_OUTPUT_FILES",
                "SCHEMAMATH_MAX_PLUGIN_OUTPUT_FILES",
                "64",
            )
        )
        root.mkdir(parents=True, exist_ok=True)
        plugin_root.mkdir(parents=True, exist_ok=True)
        return cls(
            workspace_root=root.resolve(),
            plugin_root=plugin_root.resolve(),
            maximum_upload_bytes=max_upload,
            maximum_chat_import_chars=max_chat_chars,
            maximum_plugin_output_bytes=max_plugin_output,
            maximum_plugin_output_files=max_plugin_files,
        )
