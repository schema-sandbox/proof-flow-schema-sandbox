from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings for the local-first service.

    Local mode deliberately remains compatible with the Alpha.4 workflow.  Production
    mode is fail-closed: authentication and explicit secrets are required, and local
    process plugins are disabled unless an operator opts back in.
    """

    workspace_root: Path
    plugin_root: Path
    environment: str = "local"
    auth_enabled: bool = False
    secret_key: str | None = None
    api_keys: tuple[str, ...] = ()
    allow_local_plugins: bool = True
    maximum_import_bytes: int = 500 * 1024 * 1024
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

        def bool_value(value: str) -> bool:
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "on"}:
                return True
            if normalized in {"0", "false", "no", "off"}:
                return False
            raise ValueError(f"invalid boolean environment value: {value!r}")

        def positive_int(value: str, name: str) -> int:
            parsed = int(value)
            if parsed <= 0:
                raise ValueError(f"{name} must be greater than zero")
            return parsed

        environment = env_value("PROOFFLOW_ENV", "SCHEMAMATH_ENV", "local").strip().lower()
        auth_enabled = bool_value(
            env_value(
                "PROOFFLOW_AUTH_ENABLED",
                "SCHEMAMATH_AUTH_ENABLED",
                "true" if environment == "production" else "false",
            )
        )
        secret_key = os.environ.get("PROOFFLOW_SECRET_KEY") or os.environ.get(
            "SCHEMAMATH_SECRET_KEY"
        )
        raw_api_keys = os.environ.get("PROOFFLOW_API_KEYS") or os.environ.get(
            "SCHEMAMATH_API_KEYS", ""
        )
        api_keys = tuple(key.strip() for key in raw_api_keys.split(",") if key.strip())
        if auth_enabled and not secret_key:
            raise ValueError("PROOFFLOW_SECRET_KEY is required when API authentication is enabled")
        if auth_enabled and not api_keys:
            raise ValueError("PROOFFLOW_API_KEYS must contain at least one key when authentication is enabled")
        allow_local_plugins = bool_value(
            env_value(
                "PROOFFLOW_ALLOW_LOCAL_PLUGINS",
                "SCHEMAMATH_ALLOW_LOCAL_PLUGINS",
                "false" if environment == "production" else "true",
            )
        )

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
        max_upload = positive_int(
            env_value(
                "PROOFFLOW_MAX_UPLOAD_BYTES",
                "SCHEMAMATH_MAX_UPLOAD_BYTES",
                str(25 * 1024 * 1024),
            ),
            "PROOFFLOW_MAX_UPLOAD_BYTES",
        )
        max_import = positive_int(
            env_value(
                "PROOFFLOW_MAX_IMPORT_BYTES",
                "SCHEMAMATH_MAX_IMPORT_BYTES",
                str(500 * 1024 * 1024),
            ),
            "PROOFFLOW_MAX_IMPORT_BYTES",
        )
        max_chat_chars = positive_int(
            env_value(
                "PROOFFLOW_MAX_CHAT_IMPORT_CHARS",
                "SCHEMAMATH_MAX_CHAT_IMPORT_CHARS",
                "2000000",
            ),
            "PROOFFLOW_MAX_CHAT_IMPORT_CHARS",
        )
        max_plugin_output = positive_int(
            env_value(
                "PROOFFLOW_MAX_PLUGIN_OUTPUT_BYTES",
                "SCHEMAMATH_MAX_PLUGIN_OUTPUT_BYTES",
                str(10 * 1024 * 1024),
            ),
            "PROOFFLOW_MAX_PLUGIN_OUTPUT_BYTES",
        )
        max_plugin_files = positive_int(
            env_value(
                "PROOFFLOW_MAX_PLUGIN_OUTPUT_FILES",
                "SCHEMAMATH_MAX_PLUGIN_OUTPUT_FILES",
                "64",
            ),
            "PROOFFLOW_MAX_PLUGIN_OUTPUT_FILES",
        )
        root.mkdir(parents=True, exist_ok=True)
        plugin_root.mkdir(parents=True, exist_ok=True)
        return cls(
            workspace_root=root.resolve(),
            plugin_root=plugin_root.resolve(),
            environment=environment,
            auth_enabled=auth_enabled,
            secret_key=secret_key,
            api_keys=api_keys,
            allow_local_plugins=allow_local_plugins,
            maximum_import_bytes=max_import,
            maximum_upload_bytes=max_upload,
            maximum_chat_import_chars=max_chat_chars,
            maximum_plugin_output_bytes=max_plugin_output,
            maximum_plugin_output_files=max_plugin_files,
        )
