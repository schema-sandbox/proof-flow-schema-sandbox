"""
Tests for ProofFlow v11.0.0 (AutonomicOrganism, QuantumLatticeMesh, TournamentBenchmarkEngine)

Covers:
    - AutonomicOrganism (load inspection & child sandbox self-replication)
    - QuantumLatticeMesh (post-quantum lattice KEM handshake & key exchange)
    - TournamentBenchmarkEngine (model benchmark competition & leaderboard generation)
"""

from __future__ import annotations

from schemamath_api.benchmark_engine import TournamentBenchmarkEngine
from schemamath_api.organism import AutonomicOrganism
from schemamath_api.quantum_mesh import QuantumLatticeMesh


class TestAutonomicOrganism:
    def test_inspect_load_and_spawn_child(self, tmp_path):
        organism = AutonomicOrganism(generation=1)
        state = organism.inspect_load(active_tasks=5, verification_debt=8)

        assert state.load_factor > 0.7
        assert state.is_split_recommended is True

        ws = tmp_path / "ws"
        ws.mkdir()
        child = organism.spawn_child_sandbox(allowed_path=str(ws))
        assert child is not None
        assert len(organism.children) == 1

        res = child.run("organism_step", input_data={"requested_fs": str(ws / "data.txt")})
        assert res.success is True


class TestQuantumLatticeMesh:
    def test_perform_lattice_handshake(self):
        qmesh = QuantumLatticeMesh()
        handshake = qmesh.perform_lattice_handshake("peer_alpha")

        assert handshake.is_quantum_secure is True
        assert handshake.public_key_kem.startswith("kyber_pk_")
        assert len(handshake.shared_secret_hash) > 0


class TestTournamentBenchmarkEngine:
    def test_run_benchmark_tournament(self):
        engine = TournamentBenchmarkEngine()
        models = ["GPT-4o", "Claude-3.5-Sonnet", "DeepSeek-R1"]

        leaderboard = engine.run_benchmark_tournament(
            tournament_name="Grand Math Tournament 2026",
            models=models,
            problem_count=10,
        )

        assert leaderboard.tournament_name == "Grand Math Tournament 2026"
        assert len(leaderboard.rankings) == 3
        assert leaderboard.rankings[0].accuracy_rate >= leaderboard.rankings[1].accuracy_rate
