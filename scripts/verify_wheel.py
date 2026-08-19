#!/usr/bin/env python3
"""Verify standalone isolated wheel installation and built-in plugin discovery."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    whl_path = ROOT / "dist" / "proof_flow_schema_sandbox-0.1.0a7-py3-none-any.whl"
    if not whl_path.is_file():
        raise SystemExit(f"Wheel not found: {whl_path}")

    with tempfile.TemporaryDirectory() as td:
        venv_dir = Path(td) / ".test_venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)

        py_bin = venv_dir / "Scripts" / "python.exe" if (venv_dir / "Scripts" / "python.exe").exists() else venv_dir / "bin" / "python"

        # Install wheel
        subprocess.run([str(py_bin), "-m", "pip", "install", "--no-cache-dir", str(whl_path)], check=True)

        # Run verification inside isolated venv
        verify_code = (
            "import schemamath_api\n"
            "from schemamath_api.plugin_host import PluginHost\n"
            "from pathlib import Path\n"
            "import tempfile\n"
            "\n"
            "print('Installed version:', schemamath_api.__version__)\n"
            "assert schemamath_api.__version__ == '0.1.0-alpha.7', 'Version mismatch'\n"
            "\n"
            "with tempfile.TemporaryDirectory() as root:\n"
            "    host = PluginHost(\n"
            "        repository_root=Path(root),\n"
            "        plugin_root=Path(root) / 'plugins',\n"
            "        maximum_output_bytes=10*1024*1024,\n"
            "        maximum_output_files=64,\n"
            "    )\n"
            "    manifests = host.available_manifests()\n"
            "    print('Available manifests count:', len(manifests))\n"
            "    ids = [m.plugin_id for m in manifests]\n"
            "    print('Plugin IDs:', ids)\n"
            "    assert 'graphviz.local' in ids, 'graphviz.local missing'\n"
            "    assert 'python.local' in ids, 'python.local missing'\n"
            "    print('=== ALL ISOLATED WHEEL VERIFICATIONS PASSED! ===')\n"
        )
        subprocess.run([str(py_bin), "-c", verify_code], check=True)

    print("Isolated wheel verification succeeded!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
