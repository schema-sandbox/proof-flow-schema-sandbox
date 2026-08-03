"""
Tests for ProofFlow v1.2.0 Ecosystem Features

Covers:
    - PostgresEventStore (relational event store with SHA-256 hash chaining)
    - AuthMiddleware (API Key & HMAC token validation)
    - WasiPluginRunner (WASI / WebAssembly micro-sandbox runner)
    - DeepSeekR1Importer (<think> reasoning trace parser and project importer)
"""

from __future__ import annotations

from uuid import uuid4

from schemamath_api.auth import AuthMiddleware
from schemamath_api.config import Settings
from schemamath_api.deepseek_importer import DeepSeekR1Importer
from schemamath_api.domain import Actor, ActorType
from schemamath_api.postgres_event_store import PostgresEventStore
from schemamath_api.service import SchemaMathService
from schemamath_api.wasi_runner import WasiPluginRunner


class TestPostgresEventStore:
    def test_append_and_hash_chain_verification(self):
        store = PostgresEventStore(":memory:")
        project_id = uuid4()

        rec1 = store.append(
            project_id=project_id,
            event_type="STEP_1",
            actor=Actor(type=ActorType.HUMAN, id="user1"),
            payload={"key": "val1"},
        )
        rec2 = store.append(
            project_id=project_id,
            event_type="STEP_2",
            actor=Actor(type=ActorType.MODEL, id="gpt4"),
            payload={"key": "val2"},
        )

        assert rec1.previous_hash is None
        assert rec2.previous_hash == rec1.event_hash

        valid, bad_idx, err = store.verify_chain()
        assert valid is True
        assert bad_idx is None

        records = store.read_all()
        assert len(records) == 2


class TestAuthMiddleware:
    def test_api_key_validation(self):
        auth = AuthMiddleware(valid_api_keys=["key123"])
        assert auth.validate_api_key("key123") is True
        assert auth.validate_api_key("wrongkey") is False

    def test_token_creation_and_verification(self):
        auth = AuthMiddleware(secret_key="test_secret")
        token = auth.create_token(user_id="user_admin", roles=["admin", "user"])
        user = auth.verify_token(token)

        assert user is not None
        assert user.user_id == "user_admin"
        assert user.is_admin is True

    def test_tampered_token_rejected(self):
        auth = AuthMiddleware(secret_key="test_secret")
        token = auth.create_token(user_id="user1")
        tampered_token = token[:-4] + "bad"
        assert auth.verify_token(tampered_token) is None


class TestWasiRunner:
    def test_wasi_runner_graceful_fallback(self, tmp_path):
        runner = WasiPluginRunner(wasm_runtime="/nonexistent/wasmtime")
        res = runner.run_wasm(tmp_path / "app.wasm")
        assert res.success is False
        assert "WASI runtime binary not found" in res.stderr


class TestDeepSeekR1Importer:
    def test_parse_reasoning_text(self):
        raw = """<think>
First, assume that n is an even integer.
Let n = 2k for some integer k.

However, if n is odd, a counterexample may exist.
Let us analyze 3n + 1.
</think>

The Collatz sequence reaches 1 for all tested small integers.
"""
        parsed = DeepSeekR1Importer.parse_reasoning_text(raw)
        assert len(parsed.steps) == 2
        assert "Collatz sequence" in parsed.final_answer
        assert parsed.steps[0].is_assumption is True
        assert parsed.steps[1].is_objection is True

    def test_import_into_service(self, tmp_path):
        service = SchemaMathService(Settings.from_environment(workspace_root=tmp_path / "ws"))
        importer = DeepSeekR1Importer()

        raw = "<think>Suppose x = 2.</think>Conclusion x=2 is valid."
        project_id = importer.import_into_service(service, "DeepSeek Collatz Test", raw)

        manifest = service.get_project(project_id)
        assert manifest.title == "DeepSeek Collatz Test"
        assert "DeepSeek R1 reasoning trace" in manifest.description
