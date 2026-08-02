"""
ProofFlow Schema Sandbox — Official CLI (proofflow / schemamath)

Commands:
    init             — Initialize a new ProofFlow workspace
    serve            — Start the local ProofFlow API server
    status           — Display workspace status and summary
    integrity        — Check SHA-256 event chain integrity
    rebuild          — Rebuild SQLite projection database from JSONL event log
    export           — Export workspace to .smath.zip package
    import           — Import .smath.zip archive into workspace (with preflight)
    plugin           — List, install, enable, or disable plugins
    replay           — Replay events from log with progress
    research-packet  — Generate LLM research packet markdown
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence
from uuid import UUID

from schemamath_api.config import Settings
from schemamath_api.event_store import EventStore
from schemamath_api.k0.replay import ReplayEngine
from schemamath_api.service import SchemaMathService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="proofflow",
        description="ProofFlow Schema Sandbox CLI Tool",
    )
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--workspace", type=str, default=None, help="Path to workspace directory")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # init
    p_init = subparsers.add_parser("init", help="Initialize a new research project workspace")
    p_init.add_argument("title", type=str, help="Project title")
    p_init.add_argument("--description", type=str, default="", help="Project description")
    p_init.add_argument("--problem", type=str, default="Initial problem formulation", help="Problem statement")

    # serve
    p_serve = subparsers.add_parser("serve", help="Start local API server")
    p_serve.add_argument("--host", type=str, default="127.0.0.1", help="Host address")
    p_serve.add_argument("--port", type=int, default=8000, help="Port number")

    # status
    p_status = subparsers.add_parser("status", help="Show project status")
    p_status.add_argument("--project-id", type=str, required=True, help="Project UUID")

    # integrity
    p_integrity = subparsers.add_parser("integrity", help="Verify event log integrity")
    p_integrity.add_argument("--project-id", type=str, required=True, help="Project UUID")

    # rebuild
    p_rebuild = subparsers.add_parser("rebuild", help="Rebuild SQLite projections from event log")
    p_rebuild.add_argument("--project-id", type=str, required=True, help="Project UUID")

    # export
    p_export = subparsers.add_parser("export", help="Export workspace as .smath.zip")
    p_export.add_argument("--project-id", type=str, required=True, help="Project UUID")
    p_export.add_argument("--output", type=str, default=None, help="Target ZIP output path")

    # import
    p_import = subparsers.add_parser("import", help="Import .smath.zip archive")
    p_import.add_argument("zip_path", type=str, help="Path to .smath.zip package")

    # plugin
    p_plugin = subparsers.add_parser("plugin", help="Manage plugins")
    p_plugin.add_argument("action", choices=["list", "health"], help="Plugin action")

    # replay
    p_replay = subparsers.add_parser("replay", help="Replay event log")
    p_replay.add_argument("--project-id", type=str, required=True, help="Project UUID")
    p_replay.add_argument("--offset", type=int, default=0, help="Start offset")
    p_replay.add_argument("--limit", type=int, default=None, help="Max events limit")

    # research-packet
    p_rp = subparsers.add_parser("research-packet", help="Generate research packet markdown")
    p_rp.add_argument("--project-id", type=str, required=True, help="Project UUID")

    # arena
    p_arena = subparsers.add_parser("arena", help="Run multi-agent Arena tournament")
    p_arena.add_argument("--author-model", type=str, default="openai/gpt-4o", help="Author model ID")
    p_arena.add_argument("--reviewer-model", type=str, default="anthropic/claude-3-5-sonnet", help="Reviewer model ID")

    return parser


def main(args: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parsed = parser.parse_args(args)

    if not parsed.command:
        parser.print_help()
        return 0

    settings = Settings.from_environment(
        workspace_root=Path(parsed.workspace).resolve() if parsed.workspace else None
    )

    service = SchemaMathService(settings)

    try:
        if parsed.command == "init":
            from schemamath_api.domain import Actor, ActorType, ProblemContract, ProjectCreate

            req = ProjectCreate(
                title=parsed.title,
                description=parsed.description,
                problem=ProblemContract(source_text=parsed.problem, author_notes="CLI init"),
                actor=Actor(type=ActorType.HUMAN, id="cli_user"),
            )
            manifest = service.create_project(req)
            status_str = manifest.project_status.value if hasattr(manifest.project_status, "value") else str(manifest.project_status)
            data = {"project_id": str(manifest.project_id), "title": manifest.title, "status": status_str}
            if parsed.json:
                print(json.dumps(data, indent=2))
            else:
                print(f"✅ Initialized project '{manifest.title}' (ID: {manifest.project_id})")

        elif parsed.command == "serve":
            import uvicorn
            print(f"🚀 Starting ProofFlow server on http://{parsed.host}:{parsed.port}")
            uvicorn.run("schemamath_api.main:app", host=parsed.host, port=parsed.port, reload=False)

        elif parsed.command == "status":
            project_id = UUID(parsed.project_id)
            manifest = service.get_project(project_id)
            data = manifest.model_dump(mode="json")
            if parsed.json:
                print(json.dumps(data, indent=2))
            else:
                status_str = manifest.project_status.value if hasattr(manifest.project_status, "value") else str(manifest.project_status)
                print(f"Project: {manifest.title} ({manifest.project_id})")
                print(f"Status: {status_str}")
                print(f"Updated: {manifest.updated_at}")

        elif parsed.command == "integrity":
            project_id = UUID(parsed.project_id)
            report = service.integrity_report(project_id)
            data = report.model_dump(mode="json")
            if parsed.json:
                print(json.dumps(data, indent=2))
            else:
                status_icon = "✅" if report.valid else "❌"
                print(f"{status_icon} Event Chain Integrity: valid={report.valid}, total_events={report.total_events}")

        elif parsed.command == "rebuild":
            project_id = UUID(parsed.project_id)
            count = service.rebuild_projection(project_id)
            data = {"rebuilt_events": count}
            if parsed.json:
                print(json.dumps(data, indent=2))
            else:
                print(f"✅ Rebuilt SQLite projection ({count} events replayed)")

        elif parsed.command == "export":
            import shutil
            project_id = UUID(parsed.project_id)
            exported_path = service.export_project_zip(project_id)
            if parsed.output:
                out_path = Path(parsed.output)
                out_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(exported_path, out_path)
            else:
                out_path = exported_path

            data = {"export_path": str(out_path), "size_bytes": out_path.stat().st_size}
            if parsed.json:
                print(json.dumps(data, indent=2))
            else:
                print(f"📦 Exported archive to {out_path} ({out_path.stat().st_size} bytes)")

        elif parsed.command == "import":
            zip_path = Path(parsed.zip_path)
            preflight = service.preflight_project_zip(zip_path)
            if not preflight.can_import:
                print(f"❌ Import failed preflight: {preflight.errors}")
                return 1

            manifest = service.import_project_zip(zip_path)
            data = {"project_id": str(manifest.project_id), "title": manifest.title}
            if parsed.json:
                print(json.dumps(data, indent=2))
            else:
                print(f"✅ Successfully imported '{manifest.title}' ({manifest.project_id})")

        elif parsed.command == "plugin":
            if parsed.action == "list":
                plugins = service.available_plugins()
                data = [p.model_dump(mode="json") for p in plugins]
                if parsed.json:
                    print(json.dumps(data, indent=2))
                else:
                    print(f"Available plugins ({len(plugins)}):")
                    for p in plugins:
                        print(f"  - {p.name} v{p.version} [{p.runner_type.value}]")

        elif parsed.command == "replay":
            project_id = UUID(parsed.project_id)
            events_path = service.project_dir(project_id) / "events" / "events.jsonl"
            event_store = EventStore(events_path)
            engine = ReplayEngine(event_store)

            res = engine.replay(from_offset=parsed.offset, limit=parsed.limit)
            data = {
                "success": res.success,
                "events_processed": res.events_processed,
                "start_offset": res.start_offset,
                "end_offset": res.end_offset,
            }
            if parsed.json:
                print(json.dumps(data, indent=2))
            else:
                print(f"▶ Replayed {res.events_processed} events from offset {res.start_offset} to {res.end_offset}")

        elif parsed.command == "research-packet":
            project_id = UUID(parsed.project_id)
            from schemamath_api.domain import ResearchPacketRequest
            packet = service.build_research_packet(project_id, ResearchPacketRequest())
            if parsed.json:
                print(json.dumps({"markdown": packet.markdown}, indent=2))
            else:
                print(packet.markdown)

        elif parsed.command == "arena":
            from schemamath_api.sip import compose, createFederation
            fed = createFederation()
            sandbox = compose(fed)
            res = sandbox.run("arena_match", input_data={
                "author_model": parsed.author_model,
                "reviewer_model": parsed.reviewer_model,
            })
            data = {
                "success": res.success,
                "approval": res.final_decision.approval.value,
                "needs_evidence": res.final_decision.needs_evidence,
                "author_model": parsed.author_model,
                "reviewer_model": parsed.reviewer_model,
            }
            if parsed.json:
                print(json.dumps(data, indent=2))
            else:
                print(f"🏟 Arena Match Complete: success={res.success}, approval={res.final_decision.approval.value}")

        return 0

    except Exception as exc:
        if parsed.json:
            print(json.dumps({"error": str(exc)}, indent=2))
        else:
            print(f"❌ Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
