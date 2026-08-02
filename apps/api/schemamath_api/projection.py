from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from .domain import (
    ArenaRecipeRecord,
    ArtifactRecord,
    BranchRecord,
    BridgeResultRecord,
    CanvasSnapshotRecord,
    ChallengeRecord,
    ChatImportPreviewRecord,
    DeadEndConstraintRecord,
    EventRecord,
    HandoffArtifactRecord,
    ModelSessionRecord,
    PluginRunRecord,
    ProjectPluginRecord,
    ResearchCheckpointRecord,
    RouteRecord,
)

SCHEMA_SQL = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS events (
    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL UNIQUE,
    event_type TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    actor_type TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    route_id TEXT,
    branch_id TEXT,
    epistemic_delta TEXT,
    epistemic_delta_type TEXT,
    artifact_refs_json TEXT NOT NULL DEFAULT '[]',
    payload_json TEXT NOT NULL,
    event_hash TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS routes (
    route_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    parent_route_id TEXT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    state TEXT NOT NULL,
    objections_json TEXT NOT NULL,
    revival_conditions_json TEXT NOT NULL,
    closure_evidence_refs_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS branches (
    branch_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    route_id TEXT NOT NULL,
    parent_branch_id TEXT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    assumptions_json TEXT NOT NULL,
    parameters_json TEXT NOT NULL,
    state TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS challenges (
    challenge_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    route_id TEXT,
    branch_id TEXT,
    challenge_type TEXT NOT NULL,
    status TEXT NOT NULL,
    statement TEXT NOT NULL,
    test_plan TEXT NOT NULL,
    evidence_refs_json TEXT NOT NULL,
    resolution_summary TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bridge_results (
    bridge_result_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    route_id TEXT NOT NULL,
    branch_id TEXT,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    enabled_route_ids_json TEXT NOT NULL,
    artifact_refs_json TEXT NOT NULL,
    retained_value_json TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dead_end_constraints (
    dead_end_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    route_id TEXT,
    branch_id TEXT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    applicability_scope_json TEXT NOT NULL,
    prior_attempt_refs_json TEXT NOT NULL,
    evidence_refs_json TEXT NOT NULL,
    strength TEXT NOT NULL,
    reopen_conditions_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS checkpoints (
    checkpoint_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    current_target TEXT NOT NULL,
    route_id TEXT,
    branch_id TEXT,
    intended_move TEXT NOT NULL,
    assumptions_used_json TEXT NOT NULL,
    expected_result TEXT NOT NULL,
    produced_artifact_refs_json TEXT NOT NULL,
    observed_failure_or_gain TEXT NOT NULL,
    confidence TEXT NOT NULL,
    unresolved_obligations_json TEXT NOT NULL,
    next_route_suggestions_json TEXT NOT NULL,
    source_session_ref TEXT,
    actor_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS artifacts (
    artifact_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    media_type TEXT NOT NULL,
    size_bytes INTEGER NOT NULL,
    origin TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    blob_relpath TEXT NOT NULL,
    source_ref TEXT,
    interpretation_status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chat_imports (
    import_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    artifact_id TEXT NOT NULL,
    source_filename TEXT NOT NULL,
    import_format TEXT NOT NULL,
    parser_name TEXT NOT NULL,
    candidates_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    confirmed_at TEXT
);

CREATE TABLE IF NOT EXISTS project_plugins (
    plugin_id TEXT PRIMARY KEY,
    version TEXT NOT NULL,
    enabled INTEGER NOT NULL,
    enabled_at TEXT,
    record_json TEXT
);

CREATE TABLE IF NOT EXISTS plugin_runs (
    run_id TEXT PRIMARY KEY,
    record_json TEXT NOT NULL,
    started_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS model_sessions (
    session_id TEXT PRIMARY KEY,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS handoff_artifacts (
    handoff_id TEXT PRIMARY KEY,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS arena_recipes (
    recipe_id TEXT PRIMARY KEY,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS visual_artifacts (
    visual_id TEXT PRIMARY KEY,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projection_migrations (
    version INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

"""

INDEX_SQL = """
CREATE INDEX IF NOT EXISTS idx_events_route ON events(route_id);
CREATE INDEX IF NOT EXISTS idx_events_branch ON events(branch_id);
CREATE INDEX IF NOT EXISTS idx_branches_route ON branches(route_id);
CREATE INDEX IF NOT EXISTS idx_challenges_route ON challenges(route_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_sha ON artifacts(sha256);
CREATE INDEX IF NOT EXISTS idx_chat_imports_created ON chat_imports(created_at);
CREATE INDEX IF NOT EXISTS idx_plugin_runs_started ON plugin_runs(started_at);
CREATE INDEX IF NOT EXISTS idx_model_sessions_created ON model_sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_handoffs_created ON handoff_artifacts(created_at);
CREATE INDEX IF NOT EXISTS idx_arena_recipes_created ON arena_recipes(created_at);
CREATE INDEX IF NOT EXISTS idx_visual_artifacts_created ON visual_artifacts(created_at);
"""


class ProjectionStore:
    CURRENT_SCHEMA_VERSION = 4
    MIGRATIONS: tuple[tuple[int, str], ...] = (
        (1, "event-branch-and-artifact-references"),
        (2, "epistemic-delta-columns"),
        (3, "project-plugin-record"),
        (4, "alpha3-record-projections"),
    )

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path, timeout=5.0)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout=5000")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(SCHEMA_SQL)
            self._apply_migrations(connection)
            connection.executescript(INDEX_SQL)

    def _apply_migrations(self, connection: sqlite3.Connection) -> None:
        applied = {
            int(row["version"])
            for row in connection.execute("SELECT version FROM projection_migrations")
        }
        for version, name in self.MIGRATIONS:
            if version in applied:
                continue
            if version == 1:
                self._ensure_column(connection, "events", "branch_id", "TEXT")
                self._ensure_column(
                    connection, "events", "artifact_refs_json", "TEXT NOT NULL DEFAULT '[]'"
                )
            elif version == 2:
                self._ensure_column(connection, "events", "epistemic_delta", "TEXT")
                self._ensure_column(connection, "events", "epistemic_delta_type", "TEXT")
            elif version == 3:
                self._ensure_column(connection, "project_plugins", "record_json", "TEXT")
            connection.execute(
                "INSERT INTO projection_migrations (version, name) VALUES (?, ?)",
                (version, name),
            )

    def schema_version(self) -> int:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT MAX(version) AS version FROM projection_migrations"
            ).fetchone()
        return int(row["version"] or 0)

    @staticmethod
    def _ensure_column(
        connection: sqlite3.Connection, table: str, column: str, declaration: str
    ) -> None:
        columns = {row["name"] for row in connection.execute(f"PRAGMA table_info({table})")}
        if column not in columns:
            connection.execute(f"ALTER TABLE {table} ADD COLUMN {column} {declaration}")

    def reset(self) -> None:
        if self.database_path.exists():
            self.database_path.unlink()
        self.initialize()

    def apply(self, event: EventRecord) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO events (
                    event_id, event_type, timestamp, actor_type, actor_id,
                    route_id, branch_id, epistemic_delta, epistemic_delta_type,
                    artifact_refs_json, payload_json, event_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(event.event_id),
                    event.event_type,
                    event.timestamp.isoformat(),
                    event.actor.type.value,
                    event.actor.id,
                    str(event.route_id) if event.route_id else None,
                    str(event.branch_id) if event.branch_id else None,
                    event.epistemic_delta,
                    (event.epistemic_delta_type.value if event.epistemic_delta_type else None),
                    json.dumps(event.artifact_refs, ensure_ascii=False),
                    json.dumps(event.payload, ensure_ascii=False, sort_keys=True),
                    event.event_hash,
                ),
            )
            self._apply_domain_event(connection, event)

    def _apply_domain_event(self, connection: sqlite3.Connection, event: EventRecord) -> None:
        kind = event.event_type
        if kind == "ROUTE_CREATED":
            self._insert_route(connection, RouteRecord.model_validate(event.payload["route"]))
        elif kind == "ROUTE_STATE_CHANGED":
            connection.execute(
                """
                UPDATE routes SET state = ?, closure_evidence_refs_json = ?, updated_at = ?
                WHERE route_id = ?
                """,
                (
                    event.payload["new_state"],
                    json.dumps(event.payload.get("closure_evidence_refs", []), ensure_ascii=False),
                    event.timestamp.isoformat(),
                    str(event.route_id),
                ),
            )
        elif kind == "OBJECTION_ADDED" and event.route_id is not None:
            row = connection.execute(
                "SELECT objections_json FROM routes WHERE route_id = ?",
                (str(event.route_id),),
            ).fetchone()
            if row:
                objections = json.loads(row["objections_json"])
                objections.append(event.payload["content"])
                connection.execute(
                    "UPDATE routes SET objections_json = ?, updated_at = ? WHERE route_id = ?",
                    (
                        json.dumps(objections, ensure_ascii=False),
                        event.timestamp.isoformat(),
                        str(event.route_id),
                    ),
                )
        elif kind == "BRANCH_CREATED":
            self._insert_branch(connection, BranchRecord.model_validate(event.payload["branch"]))
        elif kind == "BRANCH_STATE_CHANGED":
            connection.execute(
                "UPDATE branches SET state = ?, updated_at = ? WHERE branch_id = ?",
                (
                    event.payload["new_state"],
                    event.timestamp.isoformat(),
                    str(event.branch_id),
                ),
            )
        elif kind == "CHALLENGE_CREATED":
            self._insert_challenge(
                connection, ChallengeRecord.model_validate(event.payload["challenge"])
            )
        elif kind == "CHALLENGE_STATUS_CHANGED":
            connection.execute(
                """
                UPDATE challenges SET status = ?, resolution_summary = ?,
                    evidence_refs_json = ?, updated_at = ?
                WHERE challenge_id = ?
                """,
                (
                    event.payload["new_status"],
                    event.payload.get("resolution_summary", ""),
                    json.dumps(event.payload.get("evidence_refs", []), ensure_ascii=False),
                    event.timestamp.isoformat(),
                    event.payload["challenge_id"],
                ),
            )
        elif kind == "BRIDGE_RESULT_CREATED":
            self._insert_bridge_result(
                connection,
                BridgeResultRecord.model_validate(event.payload["bridge_result"]),
            )
        elif kind == "DEAD_END_CONSTRAINT_CREATED":
            payload = event.payload.get("dead_end_constraint") or event.payload.get("dead_end")
            if payload is None:
                raise KeyError("dead_end_constraint")
            self._insert_dead_end(
                connection,
                DeadEndConstraintRecord.model_validate(payload),
            )
        elif kind == "RESEARCH_CHECKPOINT_CREATED":
            self._insert_checkpoint(
                connection,
                ResearchCheckpointRecord.model_validate(event.payload["checkpoint"]),
            )
        elif kind == "ARTIFACT_ADDED":
            self._insert_artifact(
                connection, ArtifactRecord.model_validate(event.payload["artifact"])
            )
        elif kind == "CHAT_IMPORT_PREVIEW_CREATED":
            preview = ChatImportPreviewRecord.model_validate(event.payload["preview"])
            connection.execute(
                """
                INSERT INTO chat_imports (
                    import_id, project_id, artifact_id, source_filename,
                    import_format, parser_name, candidates_json, created_at, confirmed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(preview.import_id),
                    str(preview.project_id),
                    str(preview.artifact_id),
                    preview.source_filename,
                    preview.import_format.value,
                    preview.parser_name,
                    json.dumps(
                        [candidate.model_dump(mode="json") for candidate in preview.candidates],
                        ensure_ascii=False,
                    ),
                    preview.created_at.isoformat(),
                    preview.confirmed_at.isoformat() if preview.confirmed_at else None,
                ),
            )
        elif kind == "CHAT_IMPORT_CONFIRMED":
            connection.execute(
                "UPDATE chat_imports SET confirmed_at = ? WHERE import_id = ?",
                (event.timestamp.isoformat(), event.payload["import_id"]),
            )
        elif kind == "PLUGIN_ENABLED":
            plugin = ProjectPluginRecord.model_validate(event.payload["plugin"])
            connection.execute(
                """
                INSERT OR REPLACE INTO project_plugins (
                    plugin_id, version, enabled, enabled_at, record_json
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    plugin.plugin_id,
                    plugin.version,
                    int(plugin.enabled),
                    plugin.enabled_at.isoformat() if plugin.enabled_at else None,
                    plugin.model_dump_json(),
                ),
            )
        elif kind == "PLUGIN_DISABLED":
            plugin_payload = event.payload.get("plugin")
            if plugin_payload:
                plugin = ProjectPluginRecord.model_validate(plugin_payload)
                connection.execute(
                    """
                    INSERT OR REPLACE INTO project_plugins (
                        plugin_id, version, enabled, enabled_at, record_json
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        plugin.plugin_id,
                        plugin.version,
                        int(plugin.enabled),
                        plugin.enabled_at.isoformat() if plugin.enabled_at else None,
                        plugin.model_dump_json(),
                    ),
                )
            else:
                connection.execute(
                    "UPDATE project_plugins SET enabled = 0 WHERE plugin_id = ?",
                    (event.payload["plugin_id"],),
                )
        elif kind in {"PLUGIN_INSTALLED", "PLUGIN_HEALTH_CHECKED", "PLUGIN_UNINSTALLED"}:
            plugin = ProjectPluginRecord.model_validate(event.payload["plugin"])
            connection.execute(
                """
                INSERT OR REPLACE INTO project_plugins (
                    plugin_id, version, enabled, enabled_at, record_json
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    plugin.plugin_id,
                    plugin.version,
                    int(plugin.enabled),
                    plugin.enabled_at.isoformat() if plugin.enabled_at else None,
                    plugin.model_dump_json(),
                ),
            )
        elif kind == "PLUGIN_RUN_COMPLETED":
            record = PluginRunRecord.model_validate(event.payload["plugin_run"])
            connection.execute(
                "INSERT INTO plugin_runs (run_id, record_json, started_at) VALUES (?, ?, ?)",
                (
                    str(record.run_id),
                    record.model_dump_json(),
                    record.started_at.isoformat(),
                ),
            )
        elif kind == "MODEL_SESSION_CREATED":
            record = ModelSessionRecord.model_validate(event.payload["model_session"])
            connection.execute(
                "INSERT INTO model_sessions (session_id, record_json, created_at) VALUES (?, ?, ?)",
                (str(record.session_id), record.model_dump_json(), record.created_at.isoformat()),
            )
        elif kind == "HANDOFF_CREATED":
            record = HandoffArtifactRecord.model_validate(event.payload["handoff"])
            connection.execute(
                "INSERT INTO handoff_artifacts (handoff_id, record_json, created_at) VALUES (?, ?, ?)",
                (str(record.handoff_id), record.model_dump_json(), record.created_at.isoformat()),
            )
        elif kind == "ARENA_RECIPE_CREATED":
            record = ArenaRecipeRecord.model_validate(event.payload["arena_recipe"])
            connection.execute(
                "INSERT INTO arena_recipes (recipe_id, record_json, created_at) VALUES (?, ?, ?)",
                (str(record.recipe_id), record.model_dump_json(), record.created_at.isoformat()),
            )
        elif kind == "VISUAL_CANVAS_SNAPSHOT_CREATED":
            record = CanvasSnapshotRecord.model_validate(event.payload["visual_artifact"])
            connection.execute(
                "INSERT INTO visual_artifacts (visual_id, record_json, created_at) VALUES (?, ?, ?)",
                (str(record.visual_id), record.model_dump_json(), record.created_at.isoformat()),
            )

    @staticmethod
    def _insert_route(connection: sqlite3.Connection, route: RouteRecord) -> None:
        connection.execute(
            """
            INSERT INTO routes (
                route_id, project_id, parent_route_id, title, description,
                state, objections_json, revival_conditions_json,
                closure_evidence_refs_json, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(route.route_id),
                str(route.project_id),
                str(route.parent_route_id) if route.parent_route_id else None,
                route.title,
                route.description,
                route.state.value,
                json.dumps(route.objections, ensure_ascii=False),
                json.dumps(route.revival_conditions, ensure_ascii=False),
                json.dumps(route.closure_evidence_refs, ensure_ascii=False),
                route.created_at.isoformat(),
                route.updated_at.isoformat(),
            ),
        )

    @staticmethod
    def _insert_branch(connection: sqlite3.Connection, branch: BranchRecord) -> None:
        connection.execute(
            """
            INSERT INTO branches (
                branch_id, project_id, route_id, parent_branch_id, title,
                description, assumptions_json, parameters_json, state,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(branch.branch_id),
                str(branch.project_id),
                str(branch.route_id),
                str(branch.parent_branch_id) if branch.parent_branch_id else None,
                branch.title,
                branch.description,
                json.dumps(branch.assumptions, ensure_ascii=False),
                json.dumps(branch.parameters, ensure_ascii=False, sort_keys=True),
                branch.state.value,
                branch.created_at.isoformat(),
                branch.updated_at.isoformat(),
            ),
        )

    @staticmethod
    def _insert_challenge(connection: sqlite3.Connection, item: ChallengeRecord) -> None:
        connection.execute(
            """
            INSERT INTO challenges (
                challenge_id, project_id, route_id, branch_id, challenge_type,
                status, statement, test_plan, evidence_refs_json,
                resolution_summary, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(item.challenge_id),
                str(item.project_id),
                str(item.route_id) if item.route_id else None,
                str(item.branch_id) if item.branch_id else None,
                item.challenge_type.value,
                item.status.value,
                item.statement,
                item.test_plan,
                json.dumps(item.evidence_refs, ensure_ascii=False),
                item.resolution_summary,
                item.created_at.isoformat(),
                item.updated_at.isoformat(),
            ),
        )

    @staticmethod
    def _insert_bridge_result(connection: sqlite3.Connection, item: BridgeResultRecord) -> None:
        connection.execute(
            """
            INSERT INTO bridge_results (
                bridge_result_id, project_id, route_id, branch_id, title,
                summary, enabled_route_ids_json, artifact_refs_json,
                retained_value_json, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(item.bridge_result_id),
                str(item.project_id),
                str(item.route_id),
                str(item.branch_id) if item.branch_id else None,
                item.title,
                item.summary,
                json.dumps([str(value) for value in item.enabled_route_ids]),
                json.dumps(item.artifact_refs, ensure_ascii=False),
                json.dumps(item.retained_value, ensure_ascii=False),
                item.status.value,
                item.created_at.isoformat(),
                item.updated_at.isoformat(),
            ),
        )

    @staticmethod
    def _insert_dead_end(connection: sqlite3.Connection, item: DeadEndConstraintRecord) -> None:
        connection.execute(
            """
            INSERT INTO dead_end_constraints (
                dead_end_id, project_id, route_id, branch_id, title, description,
                applicability_scope_json, prior_attempt_refs_json,
                evidence_refs_json, strength, reopen_conditions_json,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(item.dead_end_id),
                str(item.project_id),
                str(item.route_id) if item.route_id else None,
                str(item.branch_id) if item.branch_id else None,
                item.title,
                item.description,
                json.dumps(item.applicability_scope, ensure_ascii=False),
                json.dumps(item.prior_attempt_refs, ensure_ascii=False),
                json.dumps(item.evidence_refs, ensure_ascii=False),
                item.strength.value,
                json.dumps(item.reopen_conditions, ensure_ascii=False),
                item.created_at.isoformat(),
                item.updated_at.isoformat(),
            ),
        )

    @staticmethod
    def _insert_checkpoint(connection: sqlite3.Connection, item: ResearchCheckpointRecord) -> None:
        connection.execute(
            """
            INSERT INTO checkpoints (
                checkpoint_id, project_id, current_target, route_id, branch_id,
                intended_move, assumptions_used_json, expected_result,
                produced_artifact_refs_json, observed_failure_or_gain,
                confidence, unresolved_obligations_json,
                next_route_suggestions_json, source_session_ref, actor_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(item.checkpoint_id),
                str(item.project_id),
                item.current_target,
                str(item.route_id) if item.route_id else None,
                str(item.branch_id) if item.branch_id else None,
                item.intended_move,
                json.dumps(item.assumptions_used, ensure_ascii=False),
                item.expected_result,
                json.dumps(item.produced_artifact_refs, ensure_ascii=False),
                item.observed_failure_or_gain,
                item.confidence.value,
                json.dumps(item.unresolved_obligations, ensure_ascii=False),
                json.dumps(item.next_route_suggestions, ensure_ascii=False),
                item.source_session_ref,
                json.dumps(item.actor.model_dump(mode="json"), ensure_ascii=False),
                item.created_at.isoformat(),
            ),
        )

    @staticmethod
    def _insert_artifact(connection: sqlite3.Connection, item: ArtifactRecord) -> None:
        connection.execute(
            """
            INSERT INTO artifacts (
                artifact_id, project_id, artifact_type, sha256, media_type,
                size_bytes, origin, original_filename, blob_relpath,
                source_ref, interpretation_status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(item.artifact_id),
                str(item.project_id),
                item.artifact_type.value,
                item.sha256,
                item.media_type,
                item.size_bytes,
                item.origin.value,
                item.original_filename,
                item.blob_relpath,
                item.source_ref,
                item.interpretation_status.value,
                item.created_at.isoformat(),
            ),
        )

    def list_routes(self) -> list[RouteRecord]:
        with self.connect() as connection:
            rows = connection.execute("SELECT * FROM routes ORDER BY created_at").fetchall()
        return [self._route_from_row(row) for row in rows]

    def get_route(self, route_id: str) -> RouteRecord | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM routes WHERE route_id = ?", (route_id,)
            ).fetchone()
        return self._route_from_row(row) if row else None

    def list_branches(self, route_id: str | None = None) -> list[BranchRecord]:
        sql = "SELECT * FROM branches"
        params: tuple[str, ...] = ()
        if route_id:
            sql += " WHERE route_id = ?"
            params = (route_id,)
        sql += " ORDER BY created_at"
        with self.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [self._branch_from_row(row) for row in rows]

    def get_branch(self, branch_id: str) -> BranchRecord | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM branches WHERE branch_id = ?", (branch_id,)
            ).fetchone()
        return self._branch_from_row(row) if row else None

    def list_challenges(self) -> list[ChallengeRecord]:
        with self.connect() as connection:
            rows = connection.execute("SELECT * FROM challenges ORDER BY created_at").fetchall()
        return [self._challenge_from_row(row) for row in rows]

    def get_challenge(self, challenge_id: str) -> ChallengeRecord | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM challenges WHERE challenge_id = ?", (challenge_id,)
            ).fetchone()
        return self._challenge_from_row(row) if row else None

    def list_bridge_results(self) -> list[BridgeResultRecord]:
        with self.connect() as connection:
            rows = connection.execute("SELECT * FROM bridge_results ORDER BY created_at").fetchall()
        return [self._bridge_from_row(row) for row in rows]

    def list_dead_end_constraints(self) -> list[DeadEndConstraintRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT * FROM dead_end_constraints ORDER BY created_at"
            ).fetchall()
        return [self._dead_end_from_row(row) for row in rows]

    def list_checkpoints(self, limit: int | None = None) -> list[ResearchCheckpointRecord]:
        params: tuple[int, ...] = ()
        if limit is None:
            sql = "SELECT * FROM checkpoints ORDER BY created_at"
        else:
            sql = (
                "SELECT * FROM (SELECT * FROM checkpoints ORDER BY created_at DESC LIMIT ?) "
                "ORDER BY created_at"
            )
            params = (limit,)
        with self.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [self._checkpoint_from_row(row) for row in rows]

    # Backward-compatible alias for early alpha callers.
    def list_dead_ends(self) -> list[DeadEndConstraintRecord]:
        return self.list_dead_end_constraints()

    def list_artifacts(self) -> list[ArtifactRecord]:
        with self.connect() as connection:
            rows = connection.execute("SELECT * FROM artifacts ORDER BY created_at DESC").fetchall()
        return [ArtifactRecord.model_validate(dict(row)) for row in rows]

    def get_artifact(self, artifact_id: str) -> ArtifactRecord | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM artifacts WHERE artifact_id = ?", (artifact_id,)
            ).fetchone()
        return ArtifactRecord.model_validate(dict(row)) if row else None

    def list_chat_imports(self) -> list[ChatImportPreviewRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT * FROM chat_imports ORDER BY created_at DESC"
            ).fetchall()
        return [self._chat_import_from_row(row) for row in rows]

    def get_chat_import(self, import_id: str) -> ChatImportPreviewRecord | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM chat_imports WHERE import_id = ?", (import_id,)
            ).fetchone()
        return self._chat_import_from_row(row) if row else None

    def list_project_plugins(self) -> list[ProjectPluginRecord]:
        with self.connect() as connection:
            rows = connection.execute("SELECT * FROM project_plugins ORDER BY plugin_id").fetchall()
        return [self._project_plugin_from_row(row) for row in rows]

    def get_project_plugin(self, plugin_id: str) -> ProjectPluginRecord | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM project_plugins WHERE plugin_id = ?", (plugin_id,)
            ).fetchone()
        if not row:
            return None
        return self._project_plugin_from_row(row)

    def list_plugin_runs(self) -> list[PluginRunRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM plugin_runs ORDER BY started_at DESC"
            ).fetchall()
        return [PluginRunRecord.model_validate_json(row["record_json"]) for row in rows]

    def list_model_sessions(self) -> list[ModelSessionRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM model_sessions ORDER BY created_at"
            ).fetchall()
        return [ModelSessionRecord.model_validate_json(row["record_json"]) for row in rows]

    def get_model_session(self, session_id: str) -> ModelSessionRecord | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT record_json FROM model_sessions WHERE session_id = ?", (session_id,)
            ).fetchone()
        return ModelSessionRecord.model_validate_json(row["record_json"]) if row else None

    def list_handoff_artifacts(self) -> list[HandoffArtifactRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM handoff_artifacts ORDER BY created_at"
            ).fetchall()
        return [HandoffArtifactRecord.model_validate_json(row["record_json"]) for row in rows]

    def list_arena_recipes(self) -> list[ArenaRecipeRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM arena_recipes ORDER BY created_at"
            ).fetchall()
        return [ArenaRecipeRecord.model_validate_json(row["record_json"]) for row in rows]

    def get_arena_recipe(self, recipe_id: str) -> ArenaRecipeRecord | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT record_json FROM arena_recipes WHERE recipe_id = ?", (recipe_id,)
            ).fetchone()
        return ArenaRecipeRecord.model_validate_json(row["record_json"]) if row else None

    def list_visual_artifacts(self) -> list[CanvasSnapshotRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM visual_artifacts ORDER BY created_at"
            ).fetchall()
        return [CanvasSnapshotRecord.model_validate_json(row["record_json"]) for row in rows]

    @staticmethod
    def _project_plugin_from_row(row: sqlite3.Row) -> ProjectPluginRecord:
        if row["record_json"]:
            return ProjectPluginRecord.model_validate_json(row["record_json"])
        return ProjectPluginRecord.model_validate(
            {
                "plugin_id": row["plugin_id"],
                "version": row["version"],
                "enabled": bool(row["enabled"]),
                "enabled_at": row["enabled_at"],
            }
        )

    @staticmethod
    def _route_from_row(row: sqlite3.Row) -> RouteRecord:
        return RouteRecord.model_validate(
            {
                "route_id": row["route_id"],
                "project_id": row["project_id"],
                "parent_route_id": row["parent_route_id"],
                "title": row["title"],
                "description": row["description"],
                "state": row["state"],
                "objections": json.loads(row["objections_json"]),
                "revival_conditions": json.loads(row["revival_conditions_json"]),
                "closure_evidence_refs": json.loads(row["closure_evidence_refs_json"]),
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
        )

    @staticmethod
    def _branch_from_row(row: sqlite3.Row) -> BranchRecord:
        return BranchRecord.model_validate(
            {
                "branch_id": row["branch_id"],
                "project_id": row["project_id"],
                "route_id": row["route_id"],
                "parent_branch_id": row["parent_branch_id"],
                "title": row["title"],
                "description": row["description"],
                "assumptions": json.loads(row["assumptions_json"]),
                "parameters": json.loads(row["parameters_json"]),
                "state": row["state"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
        )

    @staticmethod
    def _challenge_from_row(row: sqlite3.Row) -> ChallengeRecord:
        return ChallengeRecord.model_validate(
            {
                "challenge_id": row["challenge_id"],
                "project_id": row["project_id"],
                "route_id": row["route_id"],
                "branch_id": row["branch_id"],
                "challenge_type": row["challenge_type"],
                "status": row["status"],
                "statement": row["statement"],
                "test_plan": row["test_plan"],
                "evidence_refs": json.loads(row["evidence_refs_json"]),
                "resolution_summary": row["resolution_summary"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
        )

    @staticmethod
    def _bridge_from_row(row: sqlite3.Row) -> BridgeResultRecord:
        return BridgeResultRecord.model_validate(
            {
                "bridge_result_id": row["bridge_result_id"],
                "project_id": row["project_id"],
                "route_id": row["route_id"],
                "branch_id": row["branch_id"],
                "title": row["title"],
                "summary": row["summary"],
                "enabled_route_ids": json.loads(row["enabled_route_ids_json"]),
                "artifact_refs": json.loads(row["artifact_refs_json"]),
                "retained_value": json.loads(row["retained_value_json"]),
                "status": row["status"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
        )

    @staticmethod
    def _dead_end_from_row(row: sqlite3.Row) -> DeadEndConstraintRecord:
        return DeadEndConstraintRecord.model_validate(
            {
                "dead_end_id": row["dead_end_id"],
                "project_id": row["project_id"],
                "route_id": row["route_id"],
                "branch_id": row["branch_id"],
                "title": row["title"],
                "description": row["description"],
                "applicability_scope": json.loads(row["applicability_scope_json"]),
                "prior_attempt_refs": json.loads(row["prior_attempt_refs_json"]),
                "evidence_refs": json.loads(row["evidence_refs_json"]),
                "strength": row["strength"],
                "reopen_conditions": json.loads(row["reopen_conditions_json"]),
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
        )

    @staticmethod
    def _checkpoint_from_row(row: sqlite3.Row) -> ResearchCheckpointRecord:
        return ResearchCheckpointRecord.model_validate(
            {
                "checkpoint_id": row["checkpoint_id"],
                "project_id": row["project_id"],
                "current_target": row["current_target"],
                "route_id": row["route_id"],
                "branch_id": row["branch_id"],
                "intended_move": row["intended_move"],
                "assumptions_used": json.loads(row["assumptions_used_json"]),
                "expected_result": row["expected_result"],
                "produced_artifact_refs": json.loads(row["produced_artifact_refs_json"]),
                "observed_failure_or_gain": row["observed_failure_or_gain"],
                "confidence": row["confidence"],
                "unresolved_obligations": json.loads(row["unresolved_obligations_json"]),
                "next_route_suggestions": json.loads(row["next_route_suggestions_json"]),
                "source_session_ref": row["source_session_ref"],
                "actor": json.loads(row["actor_json"]),
                "created_at": row["created_at"],
            }
        )

    @staticmethod
    def _chat_import_from_row(row: sqlite3.Row) -> ChatImportPreviewRecord:
        return ChatImportPreviewRecord.model_validate(
            {
                "import_id": row["import_id"],
                "project_id": row["project_id"],
                "artifact_id": row["artifact_id"],
                "source_filename": row["source_filename"],
                "import_format": row["import_format"],
                "parser_name": row["parser_name"],
                "candidates": json.loads(row["candidates_json"]),
                "created_at": row["created_at"],
                "confirmed_at": row["confirmed_at"],
            }
        )
