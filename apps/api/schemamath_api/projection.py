from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from .domain import (
    ArenaRecipeRecord,
    ArtifactRecord,
    AttemptRecord,
    BenchmarkBindingRecord,
    BranchRecord,
    BridgeResultRecord,
    CanvasSnapshotRecord,
    ChallengeRecord,
    ChatImportPreviewRecord,
    ClaimAtomRecord,
    ClaimRelationRecord,
    ContinuationContractRecord,
    CostVectorRecord,
    DeadEndConstraintRecord,
    EventRecord,
    EvidenceCardRecord,
    FormalCoverageBindingRecord,
    HandoffArtifactRecord,
    HandoffPacketStatus,
    HandoffPacketV2Record,
    HandoffReceipt,
    MicroFalsificationPlanRecord,
    ModelSessionRecord,
    PluginRunRecord,
    ProjectPluginRecord,
    QuestionAgendaRecord,
    RepairLineageRecord,
    RepositorySnapshotRecord,
    ResearchCheckpointRecord,
    ResearchEpisodeDossierV2Record,
    ResearchHierarchyNodeRecord,
    ResearchStateTransitionRecord,
    ReviewLineageRecord,
    RouteRecord,
    TransitionProposalRecord,
    VerificationExecutionManifestRecord,
    VerificationMutationSetRecord,
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
    event_hash TEXT NOT NULL UNIQUE,
    revision INTEGER,
    batch_id TEXT,
    idempotency_key TEXT,
    command_id TEXT
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
    objections_json TEXT NOT NULL DEFAULT '[]',
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

CREATE TABLE IF NOT EXISTS transition_proposals (
    proposal_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    status TEXT NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS research_state_transitions (
    transition_id TEXT PRIMARY KEY,
    proposal_id TEXT NOT NULL,
    project_id TEXT NOT NULL,
    accepted INTEGER NOT NULL,
    from_revision INTEGER NOT NULL,
    to_revision INTEGER NOT NULL,
    record_json TEXT NOT NULL,
    accepted_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS continuation_contracts (
    contract_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    decision TEXT NOT NULL,
    status TEXT NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS handoff_packets_v2 (
    packet_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    status TEXT NOT NULL,
    packet_hash TEXT NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS handoff_receipts (
    receipt_id TEXT PRIMARY KEY,
    packet_id TEXT NOT NULL,
    project_id TEXT NOT NULL,
    accepted INTEGER NOT NULL,
    record_json TEXT NOT NULL,
    accepted_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS claim_atoms (
    claim_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    state TEXT NOT NULL,
    record_json TEXT NOT NULL,
    as_of TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS claim_relations (
    relation_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    source_claim_id TEXT NOT NULL,
    target_claim_id TEXT NOT NULL,
    relation TEXT NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS review_lineage (
    lineage_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS evidence_cards (
    card_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    claim_id TEXT NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS verification_execution_manifests (
    execution_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    status TEXT NOT NULL,
    manifest_sha256 TEXT NOT NULL,
    record_json TEXT NOT NULL,
    executed_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS formal_coverage_bindings (
    binding_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    challenge_id TEXT NOT NULL,
    status TEXT NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS repository_snapshots (
    snapshot_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    commit_ref TEXT NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS repair_lineage (
    repair_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    repair_type TEXT NOT NULL,
    repair_sha256 TEXT NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS research_hierarchy_nodes (
    node_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    node_type TEXT NOT NULL,
    label TEXT NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS attempt_records (
    attempt_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    target_ref TEXT NOT NULL,
    outcome TEXT NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cost_vectors (
    cost_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    scope_ref TEXT NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS micro_falsification_plans (
    plan_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    target_ref TEXT NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS benchmark_bindings (
    binding_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    benchmark_ref TEXT NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dossier_v2 (
    dossier_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    episode_ref TEXT NOT NULL,
    dossier_sha256 TEXT NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS verification_mutation_sets (
    mutation_set_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    execution_id TEXT NOT NULL,
    all_expected_failures INTEGER NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS question_agendas (
    agenda_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    episode_ref TEXT NOT NULL,
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
CREATE INDEX IF NOT EXISTS idx_events_idempotency ON events(idempotency_key);
CREATE INDEX IF NOT EXISTS idx_transition_proposals_project ON transition_proposals(project_id, created_at);
CREATE INDEX IF NOT EXISTS idx_state_transitions_project ON research_state_transitions(project_id, accepted_at);
CREATE INDEX IF NOT EXISTS idx_continuation_contracts_project ON continuation_contracts(project_id, created_at);
CREATE INDEX IF NOT EXISTS idx_handoff_packets_v2_project ON handoff_packets_v2(project_id, created_at);
CREATE INDEX IF NOT EXISTS idx_claim_atoms_project ON claim_atoms(project_id, as_of);
CREATE INDEX IF NOT EXISTS idx_claim_relations_project ON claim_relations(project_id, created_at);
CREATE INDEX IF NOT EXISTS idx_evidence_cards_claim ON evidence_cards(project_id, claim_id, created_at);
CREATE INDEX IF NOT EXISTS idx_verification_manifests_project ON verification_execution_manifests(project_id, executed_at);
CREATE INDEX IF NOT EXISTS idx_coverage_bindings_project ON formal_coverage_bindings(project_id, challenge_id);
CREATE INDEX IF NOT EXISTS idx_repository_snapshots_project ON repository_snapshots(project_id, created_at);
CREATE INDEX IF NOT EXISTS idx_repair_lineage_project ON repair_lineage(project_id, created_at);
CREATE INDEX IF NOT EXISTS idx_hierarchy_nodes_project ON research_hierarchy_nodes(project_id, created_at);
CREATE INDEX IF NOT EXISTS idx_attempt_records_project ON attempt_records(project_id, created_at);
CREATE INDEX IF NOT EXISTS idx_cost_vectors_project ON cost_vectors(project_id, created_at);
CREATE INDEX IF NOT EXISTS idx_falsification_plans_project ON micro_falsification_plans(project_id, created_at);
CREATE INDEX IF NOT EXISTS idx_benchmark_bindings_project ON benchmark_bindings(project_id, created_at);
CREATE INDEX IF NOT EXISTS idx_dossier_v2_project ON dossier_v2(project_id, created_at);
CREATE INDEX IF NOT EXISTS idx_mutation_sets_project ON verification_mutation_sets(project_id, created_at);
CREATE INDEX IF NOT EXISTS idx_question_agendas_project ON question_agendas(project_id, created_at);
"""


class ProjectionStore:
    CURRENT_SCHEMA_VERSION = 7
    MIGRATIONS: tuple[tuple[int, str], ...] = (
        (1, "event-branch-and-artifact-references"),
        (2, "epistemic-delta-columns"),
        (3, "project-plugin-record"),
        (4, "alpha3-record-projections"),
        (5, "alpha5-transition-records-and-event-provenance"),
        (6, "alpha5-evidence-verification-and-dossier-projections"),
        (7, "branch-objection-projections"),
    )

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
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
            elif version == 4:
                # alpha3-record-projections: the alpha3 tables are created by
                # SCHEMA_SQL (IF NOT EXISTS), which runs before migrations on
                # every initialize(), so a database predating alpha3 gets them
                # here; no column additions to pre-existing tables are needed.
                pass
            elif version == 5:
                self._ensure_column(connection, "events", "revision", "INTEGER")
                self._ensure_column(connection, "events", "batch_id", "TEXT")
                self._ensure_column(connection, "events", "idempotency_key", "TEXT")
                self._ensure_column(connection, "events", "command_id", "TEXT")
            elif version == 6:
                # alpha5-evidence-verification-and-dossier-projections: the new
                # tables (evidence_cards, verification_execution_manifests,
                # dossier_v2, ...) are likewise covered by SCHEMA_SQL; the only
                # pre-existing-table columns alpha5 added are in migration 5.
                pass
            elif version == 7:
                self._ensure_column(
                    connection, "branches", "objections_json", "TEXT NOT NULL DEFAULT '[]'"
                )
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
                    artifact_refs_json, payload_json, event_hash, revision,
                    batch_id, idempotency_key, command_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    event.revision,
                    str(event.batch_id) if event.batch_id else None,
                    event.idempotency_key,
                    event.command_id,
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
        elif kind == "OBJECTION_ADDED":
            content = event.payload["content"]
            if event.route_id is not None:
                row = connection.execute(
                    "SELECT objections_json FROM routes WHERE route_id = ?",
                    (str(event.route_id),),
                ).fetchone()
                if row:
                    objections = json.loads(row["objections_json"])
                    objections.append(content)
                    connection.execute(
                        "UPDATE routes SET objections_json = ?, updated_at = ? WHERE route_id = ?",
                        (
                            json.dumps(objections, ensure_ascii=False),
                            event.timestamp.isoformat(),
                            str(event.route_id),
                        ),
                    )
            if event.branch_id is not None:
                row = connection.execute(
                    "SELECT objections_json FROM branches WHERE branch_id = ?",
                    (str(event.branch_id),),
                ).fetchone()
                if row:
                    objections = json.loads(row["objections_json"])
                    objections.append(content)
                    connection.execute(
                        "UPDATE branches SET objections_json = ?, updated_at = ? WHERE branch_id = ?",
                        (
                            json.dumps(objections, ensure_ascii=False),
                            event.timestamp.isoformat(),
                            str(event.branch_id),
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
        elif kind == "RESEARCH_STATE_TRANSITION_PROPOSED":
            record = TransitionProposalRecord.model_validate(event.payload["proposal"])
            connection.execute(
                """
                INSERT OR REPLACE INTO transition_proposals (
                    proposal_id, project_id, status, record_json, created_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    str(record.proposal_id),
                    str(record.project_id),
                    record.status.value,
                    record.model_dump_json(),
                    record.created_at.isoformat(),
                ),
            )
        elif kind in {
            "RESEARCH_STATE_TRANSITION_ACCEPTED",
            "RESEARCH_STATE_TRANSITION_REJECTED",
        }:
            record = ResearchStateTransitionRecord.model_validate(event.payload["transition"])
            connection.execute(
                """
                INSERT OR REPLACE INTO research_state_transitions (
                    transition_id, proposal_id, project_id, accepted,
                    from_revision, to_revision, record_json, accepted_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(record.transition_id),
                    str(record.proposal_id),
                    str(record.project_id),
                    int(record.accepted),
                    record.from_revision,
                    record.to_revision,
                    record.model_dump_json(),
                    record.accepted_at.isoformat(),
                ),
            )
            connection.execute(
                "UPDATE transition_proposals SET status = ?, record_json = ? WHERE proposal_id = ?",
                (
                    "ACCEPTED" if record.accepted else "REJECTED",
                    json.dumps(
                        {
                            **json.loads(
                                connection.execute(
                                    "SELECT record_json FROM transition_proposals WHERE proposal_id = ?",
                                    (str(record.proposal_id),),
                                ).fetchone()["record_json"]
                            ),
                            "status": "ACCEPTED" if record.accepted else "REJECTED",
                        },
                        ensure_ascii=False,
                    ),
                    str(record.proposal_id),
                ),
            )
            if record.accepted:
                for claim_payload in record.accepted_delta.get("claim", {}).get("atoms", {}).values():
                    claim = ClaimAtomRecord.model_validate(claim_payload)
                    connection.execute(
                        """
                        INSERT OR REPLACE INTO claim_atoms (
                            claim_id, project_id, version, state, record_json, as_of
                        ) VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            str(claim.claim_id),
                            str(claim.project_id),
                            claim.version,
                            claim.state.value,
                            claim.model_dump_json(),
                            claim.as_of.isoformat(),
                        ),
                    )
        elif kind == "CONTINUATION_CONTRACT_RECORDED":
            record = ContinuationContractRecord.model_validate(event.payload["contract"])
            connection.execute(
                """
                INSERT OR REPLACE INTO continuation_contracts (
                    contract_id, project_id, decision, status, record_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(record.contract_id),
                    str(record.project_id),
                    record.decision.value,
                    record.status.value,
                    record.model_dump_json(),
                    record.created_at.isoformat(),
                ),
            )
        elif kind == "HANDOFF_PACKET_V2_CREATED":
            record = HandoffPacketV2Record.model_validate(event.payload["packet"])
            connection.execute(
                """
                INSERT OR REPLACE INTO handoff_packets_v2 (
                    packet_id, project_id, status, packet_hash, record_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(record.packet_id),
                    str(record.project_id),
                    record.status.value,
                    record.packet_hash,
                    record.model_dump_json(),
                    record.created_at.isoformat(),
                ),
            )
        elif kind in {"HANDOFF_ACCEPTED", "HANDOFF_REJECTED"}:
            receipt = HandoffReceipt.model_validate(event.payload["receipt"])
            connection.execute(
                """
                INSERT OR REPLACE INTO handoff_receipts (
                    receipt_id, packet_id, project_id, accepted, record_json, accepted_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(receipt.receipt_id),
                    str(receipt.packet_id),
                    str(receipt.project_id),
                    int(receipt.accepted),
                    receipt.model_dump_json(),
                    receipt.accepted_at.isoformat(),
                ),
            )
            packet_row = connection.execute(
                "SELECT record_json FROM handoff_packets_v2 WHERE packet_id = ?",
                (str(receipt.packet_id),),
            ).fetchone()
            if packet_row:
                packet = HandoffPacketV2Record.model_validate_json(packet_row["record_json"])
                packet = packet.model_copy(
                    update={
                        "status": (
                            HandoffPacketStatus.ACCEPTED
                            if receipt.accepted
                            else HandoffPacketStatus.REJECTED
                        )
                    }
                )
                connection.execute(
                    "UPDATE handoff_packets_v2 SET status = ?, record_json = ? WHERE packet_id = ?",
                    (
                        packet.status.value,
                        packet.model_dump_json(),
                        str(receipt.packet_id),
                    ),
                )
        elif kind == "CLAIM_RELATION_CREATED":
            relation = ClaimRelationRecord.model_validate(event.payload["relation"])
            connection.execute(
                """
                INSERT OR REPLACE INTO claim_relations (
                    relation_id, project_id, source_claim_id, target_claim_id,
                    relation, record_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(relation.relation_id),
                    str(relation.project_id),
                    str(relation.source_claim_id),
                    str(relation.target_claim_id),
                    relation.relation.value,
                    relation.model_dump_json(),
                    relation.created_at.isoformat(),
                ),
            )
        elif kind == "REVIEW_LINEAGE_CREATED":
            lineage = ReviewLineageRecord.model_validate(event.payload["lineage"])
            connection.execute(
                """
                INSERT OR REPLACE INTO review_lineage (
                    lineage_id, project_id, record_json, created_at
                ) VALUES (?, ?, ?, ?)
                """,
                (
                    str(lineage.lineage_id),
                    str(lineage.project_id),
                    lineage.model_dump_json(),
                    lineage.created_at.isoformat(),
                ),
            )
        elif kind == "EVIDENCE_CARD_CREATED":
            card = EvidenceCardRecord.model_validate(event.payload["evidence_card"])
            connection.execute(
                """
                INSERT OR REPLACE INTO evidence_cards (
                    card_id, project_id, claim_id, record_json, created_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    str(card.card_id),
                    str(card.project_id),
                    str(card.claim_id),
                    card.model_dump_json(),
                    card.created_at.isoformat(),
                ),
            )
        elif kind == "VERIFICATION_EXECUTION_MANIFEST_RECORDED":
            manifest = VerificationExecutionManifestRecord.model_validate(
                event.payload["manifest"]
            )
            connection.execute(
                """
                INSERT OR REPLACE INTO verification_execution_manifests (
                    execution_id, project_id, status, manifest_sha256, record_json, executed_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(manifest.execution_id),
                    str(manifest.project_id),
                    manifest.status.value,
                    manifest.manifest_sha256,
                    manifest.model_dump_json(),
                    manifest.executed_at.isoformat(),
                ),
            )
        elif kind == "FORMAL_COVERAGE_BINDING_RECORDED":
            binding = FormalCoverageBindingRecord.model_validate(event.payload["binding"])
            connection.execute(
                """
                INSERT OR REPLACE INTO formal_coverage_bindings (
                    binding_id, project_id, challenge_id, status, record_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(binding.binding_id),
                    str(binding.project_id),
                    binding.challenge_id,
                    binding.status.value,
                    binding.model_dump_json(),
                    binding.created_at.isoformat(),
                ),
            )
        elif kind == "REPOSITORY_SNAPSHOT_RECORDED":
            snapshot = RepositorySnapshotRecord.model_validate(event.payload["snapshot"])
            connection.execute(
                """
                INSERT OR REPLACE INTO repository_snapshots (
                    snapshot_id, project_id, commit_ref, record_json, created_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    str(snapshot.snapshot_id),
                    str(snapshot.project_id),
                    snapshot.commit,
                    snapshot.model_dump_json(),
                    snapshot.created_at.isoformat(),
                ),
            )
        elif kind == "REPAIR_LINEAGE_RECORDED":
            repair = RepairLineageRecord.model_validate(event.payload["repair"])
            connection.execute(
                """
                INSERT OR REPLACE INTO repair_lineage (
                    repair_id, project_id, repair_type, repair_sha256, record_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(repair.repair_id),
                    str(repair.project_id),
                    repair.repair_type.value,
                    repair.repair_sha256,
                    repair.model_dump_json(),
                    repair.created_at.isoformat(),
                ),
            )
        elif kind == "RESEARCH_HIERARCHY_NODE_RECORDED":
            node = ResearchHierarchyNodeRecord.model_validate(event.payload["node"])
            connection.execute(
                """
                INSERT OR REPLACE INTO research_hierarchy_nodes (
                    node_id, project_id, node_type, label, record_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(node.node_id),
                    str(node.project_id),
                    node.node_type.value,
                    node.label,
                    node.model_dump_json(),
                    node.created_at.isoformat(),
                ),
            )
        elif kind == "ATTEMPT_RECORDED":
            attempt = AttemptRecord.model_validate(event.payload["attempt"])
            connection.execute(
                """
                INSERT OR REPLACE INTO attempt_records (
                    attempt_id, project_id, target_ref, outcome, record_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(attempt.attempt_id),
                    str(attempt.project_id),
                    attempt.target_ref,
                    attempt.outcome.value,
                    attempt.model_dump_json(),
                    attempt.created_at.isoformat(),
                ),
            )
        elif kind == "COST_VECTOR_RECORDED":
            cost = CostVectorRecord.model_validate(event.payload["cost"])
            connection.execute(
                """
                INSERT OR REPLACE INTO cost_vectors (
                    cost_id, project_id, scope_ref, record_json, created_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    str(cost.cost_id),
                    str(cost.project_id),
                    cost.scope_ref,
                    cost.model_dump_json(),
                    cost.created_at.isoformat(),
                ),
            )
        elif kind == "MICRO_FALSIFICATION_PLAN_RECORDED":
            plan = MicroFalsificationPlanRecord.model_validate(event.payload["plan"])
            connection.execute(
                """
                INSERT OR REPLACE INTO micro_falsification_plans (
                    plan_id, project_id, target_ref, record_json, created_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    str(plan.plan_id),
                    str(plan.project_id),
                    plan.target_ref,
                    plan.model_dump_json(),
                    plan.created_at.isoformat(),
                ),
            )
        elif kind == "BENCHMARK_BINDING_RECORDED":
            binding = BenchmarkBindingRecord.model_validate(event.payload["binding"])
            connection.execute(
                """
                INSERT OR REPLACE INTO benchmark_bindings (
                    binding_id, project_id, benchmark_ref, record_json, created_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    str(binding.binding_id),
                    str(binding.project_id),
                    binding.benchmark_ref,
                    binding.model_dump_json(),
                    binding.created_at.isoformat(),
                ),
            )
        elif kind == "DOSSIER_V2_RECORDED":
            dossier = ResearchEpisodeDossierV2Record.model_validate(event.payload["dossier"])
            connection.execute(
                """
                INSERT OR REPLACE INTO dossier_v2 (
                    dossier_id, project_id, episode_ref, dossier_sha256, record_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(dossier.dossier_id),
                    str(dossier.project_id),
                    dossier.episode_ref,
                    dossier.dossier_sha256,
                    dossier.model_dump_json(),
                    dossier.created_at.isoformat(),
                ),
            )
        elif kind == "VERIFICATION_MUTATION_SET_RECORDED":
            mutation_set = VerificationMutationSetRecord.model_validate(
                event.payload["mutation_set"]
            )
            connection.execute(
                """
                INSERT OR REPLACE INTO verification_mutation_sets (
                    mutation_set_id, project_id, execution_id,
                    all_expected_failures, record_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(mutation_set.mutation_set_id),
                    str(mutation_set.project_id),
                    str(mutation_set.execution_id),
                    int(mutation_set.all_expected_failures),
                    mutation_set.model_dump_json(),
                    mutation_set.created_at.isoformat(),
                ),
            )
        elif kind == "QUESTION_AGENDA_RECORDED":
            agenda = QuestionAgendaRecord.model_validate(event.payload["agenda"])
            connection.execute(
                """
                INSERT OR REPLACE INTO question_agendas (
                    agenda_id, project_id, episode_ref, record_json, created_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    str(agenda.agenda_id),
                    str(agenda.project_id),
                    agenda.episode_ref,
                    agenda.model_dump_json(),
                    agenda.created_at.isoformat(),
                ),
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
                description, assumptions_json, parameters_json, objections_json,
                state, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                json.dumps(branch.objections, ensure_ascii=False),
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

    def list_continuation_contracts(self) -> list[ContinuationContractRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM continuation_contracts ORDER BY created_at"
            ).fetchall()
        return [ContinuationContractRecord.model_validate_json(row["record_json"]) for row in rows]

    def list_handoff_packets_v2(self) -> list[HandoffPacketV2Record]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM handoff_packets_v2 ORDER BY created_at"
            ).fetchall()
        return [HandoffPacketV2Record.model_validate_json(row["record_json"]) for row in rows]

    def list_handoff_receipts(self) -> list[HandoffReceipt]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM handoff_receipts ORDER BY accepted_at"
            ).fetchall()
        return [HandoffReceipt.model_validate_json(row["record_json"]) for row in rows]

    def list_claim_atoms(self) -> list[ClaimAtomRecord]:
        with self.connect() as connection:
            rows = connection.execute("SELECT record_json FROM claim_atoms ORDER BY as_of").fetchall()
        return [ClaimAtomRecord.model_validate_json(row["record_json"]) for row in rows]

    def get_claim_atom(self, claim_id: str) -> ClaimAtomRecord | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT record_json FROM claim_atoms WHERE claim_id = ?", (claim_id,)
            ).fetchone()
        return ClaimAtomRecord.model_validate_json(row["record_json"]) if row else None

    def list_claim_relations(self) -> list[ClaimRelationRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM claim_relations ORDER BY created_at"
            ).fetchall()
        return [ClaimRelationRecord.model_validate_json(row["record_json"]) for row in rows]

    def list_review_lineage(self) -> list[ReviewLineageRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM review_lineage ORDER BY created_at"
            ).fetchall()
        return [ReviewLineageRecord.model_validate_json(row["record_json"]) for row in rows]

    def list_evidence_cards(self) -> list[EvidenceCardRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM evidence_cards ORDER BY created_at"
            ).fetchall()
        return [EvidenceCardRecord.model_validate_json(row["record_json"]) for row in rows]

    def list_verification_manifests(self) -> list[VerificationExecutionManifestRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM verification_execution_manifests ORDER BY executed_at"
            ).fetchall()
        return [
            VerificationExecutionManifestRecord.model_validate_json(row["record_json"])
            for row in rows
        ]

    def list_coverage_bindings(self) -> list[FormalCoverageBindingRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM formal_coverage_bindings ORDER BY created_at"
            ).fetchall()
        return [FormalCoverageBindingRecord.model_validate_json(row["record_json"]) for row in rows]

    def list_repository_snapshots(self) -> list[RepositorySnapshotRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM repository_snapshots ORDER BY created_at"
            ).fetchall()
        return [RepositorySnapshotRecord.model_validate_json(row["record_json"]) for row in rows]

    def list_repair_lineage(self) -> list[RepairLineageRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM repair_lineage ORDER BY created_at"
            ).fetchall()
        return [RepairLineageRecord.model_validate_json(row["record_json"]) for row in rows]

    def list_hierarchy_nodes(self) -> list[ResearchHierarchyNodeRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM research_hierarchy_nodes ORDER BY created_at"
            ).fetchall()
        return [ResearchHierarchyNodeRecord.model_validate_json(row["record_json"]) for row in rows]

    def list_attempt_records(self) -> list[AttemptRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM attempt_records ORDER BY created_at"
            ).fetchall()
        return [AttemptRecord.model_validate_json(row["record_json"]) for row in rows]

    def list_cost_vectors(self) -> list[CostVectorRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM cost_vectors ORDER BY created_at"
            ).fetchall()
        return [CostVectorRecord.model_validate_json(row["record_json"]) for row in rows]

    def list_falsification_plans(self) -> list[MicroFalsificationPlanRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM micro_falsification_plans ORDER BY created_at"
            ).fetchall()
        return [MicroFalsificationPlanRecord.model_validate_json(row["record_json"]) for row in rows]

    def list_benchmark_bindings(self) -> list[BenchmarkBindingRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM benchmark_bindings ORDER BY created_at"
            ).fetchall()
        return [BenchmarkBindingRecord.model_validate_json(row["record_json"]) for row in rows]

    def list_dossiers_v2(self) -> list[ResearchEpisodeDossierV2Record]:
        with self.connect() as connection:
            rows = connection.execute("SELECT record_json FROM dossier_v2 ORDER BY created_at").fetchall()
        return [ResearchEpisodeDossierV2Record.model_validate_json(row["record_json"]) for row in rows]

    def list_mutation_sets(self) -> list[VerificationMutationSetRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM verification_mutation_sets ORDER BY created_at"
            ).fetchall()
        return [VerificationMutationSetRecord.model_validate_json(row["record_json"]) for row in rows]

    def list_question_agendas(self) -> list[QuestionAgendaRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT record_json FROM question_agendas ORDER BY created_at"
            ).fetchall()
        return [QuestionAgendaRecord.model_validate_json(row["record_json"]) for row in rows]

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
                "objections": json.loads(row["objections_json"]),
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
