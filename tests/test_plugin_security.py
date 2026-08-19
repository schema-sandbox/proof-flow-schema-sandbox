from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

import pytest
from schemamath_api.plugin_runner import PythonPluginRunner


@pytest.fixture(scope="module")
def runner(tmp_path_factory) -> PythonPluginRunner:
    return PythonPluginRunner(
        plugin_root=tmp_path_factory.mktemp("plugins"),
        maximum_output_bytes=4096,
        maximum_output_files=8,
    )


def _run(runner: PythonPluginRunner, tmp_path: Path, source_code: str):
    return runner.execute(
        project_id=uuid4(),
        run_id=uuid4(),
        run_dir=tmp_path / "run",
        source_code=source_code,
        stdin_text="",
        arguments=[],
        timeout_seconds=60,
        input_files=[],
    )


def test_plugin_environment_is_scrubbed_of_host_secrets(
    runner: PythonPluginRunner, tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("PROOFFLOW_API_TOKEN", "super-secret-token-value")
    monkeypatch.setenv("PROOFFLOW_PLUGIN_ROOT", "must-not-leak")
    outcome = _run(
        runner,
        tmp_path,
        (
            "import json, os\n"
            "snapshot = dict(os.environ)\n"
            "with open(os.path.join(os.environ['SCHEMAMATH_OUTPUT_DIR'], 'env.json'), 'w', encoding='utf-8') as f:\n"
            "    f.write(json.dumps(snapshot))\n"
        ),
    )
    assert outcome.status.value == "SUCCEEDED"
    env_file = next(p for p in outcome.output_files if p.name == "env.json")
    snapshot = json.loads(env_file.read_text(encoding="utf-8"))
    assert "PROOFFLOW_API_TOKEN" not in snapshot
    assert "PROOFFLOW_PLUGIN_ROOT" not in snapshot
    assert snapshot["SCHEMAMATH_OUTPUT_DIR"] == str(outcome.output_files[0].parent)
    assert snapshot["PYTHONDONTWRITEBYTECODE"] == "1"


def test_plugin_runs_in_isolated_interpreter(
    runner: PythonPluginRunner, tmp_path: Path
) -> None:
    outcome = _run(
        runner,
        tmp_path,
        (
            "import json, os, sys\n"
            "flags = {'isolated': bool(sys.flags.isolated), 'no_user_site': sys.flags.no_user_site, 'dont_write_bytecode': sys.dont_write_bytecode, 'cwd': os.getcwd(), 'home': os.environ.get('HOME'), 'tmp': os.environ.get('TMP')}\n"
            "with open(os.path.join(os.environ['SCHEMAMATH_OUTPUT_DIR'], 'flags.json'), 'w', encoding='utf-8') as f:\n"
            "    f.write(json.dumps(flags))\n"
        ),
    )
    assert outcome.status.value == "SUCCEEDED"
    flags_file = next(p for p in outcome.output_files if p.name == "flags.json")
    flags = json.loads(flags_file.read_text(encoding="utf-8"))
    assert flags["isolated"] == 1
    assert flags["no_user_site"] == 1
    assert flags["dont_write_bytecode"] is True
    assert flags["cwd"] == str(tmp_path / "run")
    assert flags["tmp"] == str(tmp_path / "run" / "tmp")


def test_plugin_output_symlinks_are_not_collected(
    runner: PythonPluginRunner, tmp_path: Path
) -> None:
    secret = tmp_path.parent / "outside-secret.txt"
    secret.write_text("EXFILTRATED-SECRET-DATA", encoding="utf-8")
    source_code = (
        "import os\n"
        "from pathlib import Path\n"
        "out = Path(os.environ['SCHEMAMATH_OUTPUT_DIR'])\n"
        "try:\n"
        "    os.symlink(r" + repr(str(secret)) + ", str(out / 'leak.txt'))\n"
        "except (NotImplementedError, OSError, AttributeError):\n"
        "    pass\n"
        "regular = out / 'legit.txt'\n"
        "regular.write_text('ok', encoding='utf-8')\n"
    )
    outcome = _run(runner, tmp_path, source_code)
    assert outcome.status.value == "SUCCEEDED"
    collected = {path.name for path in outcome.output_files}
    assert "leak.txt" not in collected
    assert "legit.txt" in collected
    leaked = [path for path in outcome.output_files if path.name == "leak.txt"]
    assert not leaked


def test_plugin_output_larger_than_limit_is_truncated(
    runner: PythonPluginRunner, tmp_path: Path
) -> None:
    outcome = _run(
        runner,
        tmp_path,
        (
            "import os\n"
            "from pathlib import Path\n"
            "out = Path(os.environ['SCHEMAMATH_OUTPUT_DIR']) / 'big.bin'\n"
            "out.write_bytes(b'x' * 100_000)\n"
        ),
    )
    assert outcome.status.value == "SUCCEEDED"
    assert outcome.output_truncated is True
    big = next(p for p in outcome.output_files if p.name == "big.bin")
    assert big.stat().st_size == 4096


def test_host_security_validation_fails_on_insecure_remote_binding(tmp_path: Path) -> None:
    from schemamath_api.config import Settings

    settings = Settings(
        workspace_root=tmp_path / "workspaces",
        plugin_root=tmp_path / "plugins",
        environment="local",
        auth_enabled=False,
        secret_key=None,
        api_keys=(),
        allow_local_plugins=True,
        maximum_import_bytes=10_000_000,
        maximum_upload_bytes=10_000_000,
        maximum_chat_import_chars=500_000,
        maximum_plugin_output_bytes=4096,
        maximum_plugin_output_files=8,
    )

    # Loopback bindings must succeed
    settings.validate_host_security("127.0.0.1")
    settings.validate_host_security("localhost")
    settings.validate_host_security("::1")

    # Non-loopback binding without auth must fail closed
    with pytest.raises(ValueError, match="Binding to non-loopback host '0.0.0.0'"):
        settings.validate_host_security("0.0.0.0")

    with pytest.raises(ValueError, match="Binding to non-loopback host '192.168.1.100'"):
        settings.validate_host_security("192.168.1.100")


def test_loopback_security_guard_rejects_remote_client(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient
    from schemamath_api.main import create_app

    app = create_app(tmp_path / "workspaces", tmp_path / "plugins")
    client = TestClient(app, client=("192.168.1.100", 54321))
    response = client.get("/api/v1/projects")
    assert response.status_code == 403
    assert b"Forbidden: Unauthenticated remote access is disabled" in response.content

    # Loopback client must succeed
    local_client = TestClient(app, client=("127.0.0.1", 54321))
    local_response = local_client.get("/api/v1/projects")
    assert local_response.status_code == 200


