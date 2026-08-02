"""
Tests for ProofFlow CLI (schemamath_api.cli)

Covers:
    - proofflow init
    - proofflow status
    - proofflow integrity
    - proofflow rebuild
    - proofflow export & import
    - proofflow plugin list
    - proofflow replay
    - proofflow research-packet
    - --json output flag across commands
"""

from __future__ import annotations

import json
from uuid import uuid4

import pytest

from schemamath_api.cli import main


class TestCLICommands:
    def test_cli_init_and_status(self, tmp_path, capsys):
        ws = str(tmp_path / "workspace")

        # 1. init
        code = main(["--workspace", ws, "--json", "init", "Test CLI Project", "--description", "CLI desc"])
        assert code == 0
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["title"] == "Test CLI Project"
        project_id = data["project_id"]

        # 2. status
        code = main(["--workspace", ws, "--json", "status", "--project-id", project_id])
        assert code == 0
        captured = capsys.readouterr()
        status_data = json.loads(captured.out)
        assert status_data["project_id"] == project_id

        # 3. integrity
        code = main(["--workspace", ws, "--json", "integrity", "--project-id", project_id])
        assert code == 0
        captured = capsys.readouterr()
        integrity_data = json.loads(captured.out)
        assert integrity_data["valid"] is True

        # 4. rebuild
        code = main(["--workspace", ws, "--json", "rebuild", "--project-id", project_id])
        assert code == 0
        captured = capsys.readouterr()
        rebuild_data = json.loads(captured.out)
        assert rebuild_data["rebuilt_events"] >= 1

        # 5. export
        zip_out = str(tmp_path / "export.zip")
        code = main(["--workspace", ws, "--json", "export", "--project-id", project_id, "--output", zip_out])
        assert code == 0
        captured = capsys.readouterr()
        export_data = json.loads(captured.out)
        assert export_data["size_bytes"] > 0

        # 6. import
        ws2 = str(tmp_path / "workspace2")
        code = main(["--workspace", ws2, "--json", "import", zip_out])
        assert code == 0
        captured = capsys.readouterr()
        import_data = json.loads(captured.out)
        assert import_data["project_id"] == project_id

        # 7. replay
        code = main(["--workspace", ws, "--json", "replay", "--project-id", project_id])
        assert code == 0
        captured = capsys.readouterr()

        # 8. research-packet
        code = main(["--workspace", ws, "--json", "research-packet", "--project-id", project_id])
        assert code == 0
        captured = capsys.readouterr()
        rp_data = json.loads(captured.out)
        assert "# ProofFlow Research Packet:" in rp_data["markdown"]

        # 9. plugin list
        code = main(["--workspace", ws, "--json", "plugin", "list"])
        assert code == 0
        captured = capsys.readouterr()

        # 10. arena
        code = main(["--workspace", ws, "--json", "arena", "--author-model", "gpt-4o", "--reviewer-model", "claude-3-5-sonnet"])
        assert code == 0
        captured = capsys.readouterr()
        arena_data = json.loads(captured.out)
        assert arena_data["success"] is True
