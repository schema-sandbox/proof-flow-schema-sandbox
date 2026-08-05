"""Tests for Schema Migrator (v46.0)."""

import json

import pytest
from schemamath_api.schema_migrator import SchemaMigrator


class TestMigrateRecord:
    def test_already_at_target_is_noop(self):
        rec = {"schema_version": "0.5", "data": "test"}
        m = SchemaMigrator()
        result = m.migrate_record(rec, "0.5")
        assert result["schema_version"] == "0.5"

    def test_v04_to_v05_upgrades_version(self):
        rec = {"schema_version": "0.4", "payload": {}}
        m = SchemaMigrator()
        result = m.migrate_record(rec, "0.5")
        assert result["schema_version"] == "0.5"

    def test_v04_to_v05_adds_trace_class(self):
        rec = {"schema_version": "0.4", "payload": {}}
        m = SchemaMigrator()
        result = m.migrate_record(rec, "0.5")
        assert result["payload"]["trace_class"] == "FINAL_ONLY_ARTIFACT"

    def test_v04_to_v05_adds_artifact_correlations(self):
        rec = {"schema_version": "0.4", "payload": {}}
        m = SchemaMigrator()
        result = m.migrate_record(rec, "0.5")
        assert result["payload"]["artifact_correlations"] == []

    def test_v04_to_v05_preserves_existing_payload(self):
        rec = {"schema_version": "0.4", "payload": {"existing": "data"}}
        m = SchemaMigrator()
        result = m.migrate_record(rec, "0.5")
        assert result["payload"]["existing"] == "data"
        assert result["payload"]["trace_class"] == "FINAL_ONLY_ARTIFACT"

    def test_v05_to_v06_adds_control_plane_metadata_without_rewriting_payload(self):
        rec = {"schema_version": "0.5", "payload": {"claim": "legacy"}}
        result = SchemaMigrator().migrate_record(rec, "0.6")
        assert result["schema_version"] == "0.6"
        assert result["payload"]["claim"] == "legacy"
        assert result["revision"] is None
        assert result["idempotency_key"] is None

    def test_v03_to_v05_chain(self):
        rec = {"schema_version": "0.3", "payload": {}}
        m = SchemaMigrator()
        result = m.migrate_record(rec, "0.5")
        assert result["schema_version"] == "0.5"

    def test_invalid_path_raises(self):
        rec = {"schema_version": "9.9", "payload": {}}
        m = SchemaMigrator()
        with pytest.raises(ValueError, match="No migration path"):
            m.migrate_record(rec, "0.5")


class TestMigrateRecords:
    def test_batch_migration(self):
        records = [
            {"schema_version": "0.4", "payload": {}},
            {"schema_version": "0.5", "payload": {}},
            {"schema_version": "0.4", "payload": {"x": 1}},
        ]
        m = SchemaMigrator()
        result = m.migrate_records(records, "0.5")
        assert result.records_migrated == 2
        assert result.records_skipped == 1
        assert result.success

    def test_batch_with_errors(self):
        records = [
            {"schema_version": "0.4", "payload": {}},
            {"schema_version": "9.9", "payload": {}},
        ]
        m = SchemaMigrator()
        result = m.migrate_records(records, "0.5")
        assert result.records_migrated == 1
        assert len(result.errors) == 1
        assert not result.success


class TestMigrateJsonlFile:
    def test_file_migration(self, tmp_path):
        source = tmp_path / "events.jsonl"
        lines = [
            json.dumps({"schema_version": "0.4", "payload": {}}),
            json.dumps({"schema_version": "0.4", "payload": {"key": "val"}}),
        ]
        source.write_text("\n".join(lines) + "\n", encoding="utf-8")

        m = SchemaMigrator()
        result = m.migrate_jsonl_file(source)
        assert result.success
        assert result.records_migrated == 2

        migrated = [json.loads(line) for line in source.read_text().strip().splitlines()]
        assert all(r["schema_version"] == "0.5" for r in migrated)

    def test_file_to_new_target(self, tmp_path):
        source = tmp_path / "old.jsonl"
        target = tmp_path / "new.jsonl"
        source.write_text(json.dumps({"schema_version": "0.4", "payload": {}}) + "\n")

        m = SchemaMigrator()
        result = m.migrate_jsonl_file(source, target)
        assert result.success
        assert target.exists()


class TestBuildChain:
    def test_direct_step(self):
        m = SchemaMigrator()
        chain = m._build_chain("0.4", "0.5")
        assert chain == [("0.4", "0.5")]

    def test_multi_step(self):
        m = SchemaMigrator()
        chain = m._build_chain("0.2", "0.5")
        assert len(chain) == 3
        assert chain[0] == ("0.2", "0.3")
        assert chain[-1] == ("0.4", "0.5")

    def test_full_chain(self):
        m = SchemaMigrator()
        chain = m._build_chain("0.1", "0.5")
        assert len(chain) == 4
