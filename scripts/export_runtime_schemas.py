#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from schemamath_api.domain import (
    ArenaRecipeRecord,
    ArtifactRecord,
    BranchRecord,
    BridgeResultRecord,
    CanvasSnapshotRecord,
    ChallengeRecord,
    ChatImportPreviewRecord,
    DeadEndConstraintRecord,
    EpistemicDeltaSummary,
    EventRecord,
    HandoffArtifactRecord,
    HistoricalSearchHit,
    ImportPreflightReport,
    ModelSessionRecord,
    PluginHealthRecord,
    PluginManifestRecord,
    PluginRunRecord,
    ProjectManifest,
    ProjectPluginRecord,
    ResearchCheckpointRecord,
    RouteMergeRequest,
    RouteMergeResponse,
    RouteRecord,
    RouteSplitRequest,
    RouteSplitResponse,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"

MODELS = {
    "project.schema.json": ProjectManifest,
    "route.schema.json": RouteRecord,
    "route-split-request.schema.json": RouteSplitRequest,
    "route-split-response.schema.json": RouteSplitResponse,
    "route-merge-request.schema.json": RouteMergeRequest,
    "route-merge-response.schema.json": RouteMergeResponse,
    "branch.schema.json": BranchRecord,
    "challenge.schema.json": ChallengeRecord,
    "bridge-result.schema.json": BridgeResultRecord,
    "dead-end-constraint.schema.json": DeadEndConstraintRecord,
    "research-checkpoint.schema.json": ResearchCheckpointRecord,
    "chat-import-preview.schema.json": ChatImportPreviewRecord,
    "plugin-run.schema.json": PluginRunRecord,
    "plugin-manifest.schema.json": PluginManifestRecord,
    "project-plugin.schema.json": ProjectPluginRecord,
    "plugin-health.schema.json": PluginHealthRecord,
    "model-session.schema.json": ModelSessionRecord,
    "handoff-artifact.schema.json": HandoffArtifactRecord,
    "arena-recipe.schema.json": ArenaRecipeRecord,
    "historical-search-hit.schema.json": HistoricalSearchHit,
    "import-preflight.schema.json": ImportPreflightReport,
    "epistemic-delta.schema.json": EpistemicDeltaSummary,
    "canvas-snapshot.schema.json": CanvasSnapshotRecord,
    "artifact.schema.json": ArtifactRecord,
    "event.schema.json": EventRecord,
}


def main() -> int:
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    for filename, model in MODELS.items():
        schema = model.model_json_schema(mode="validation")
        schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
        schema["$id"] = f"https://schemamath.org/schemas/runtime/{filename}"
        (SCHEMA_DIR / filename).write_text(
            json.dumps(schema, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"Exported {len(MODELS)} runtime schemas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
