"""
Tests for ProofFlow v2.0.0 (Autonomous Swarm, Meta-Sandbox, Paper Synthesizer)

Covers:
    - ResearchSwarmCoordinator (autonomous loop execution & bottleneck detection)
    - MetaSandboxEngine (rule amendment evaluation & K0 invariant protection)
    - PaperSynthesizer (LaTeX paper generation & .tex export)
"""

from __future__ import annotations

from schemamath_api.config import Settings
from schemamath_api.domain import Actor, ActorType, ProblemContract, ProjectCreate
from schemamath_api.meta_sandbox import MetaSandboxEngine, RuleAmendmentProposal
from schemamath_api.paper_synthesizer import PaperSynthesizer
from schemamath_api.service import SchemaMathService
from schemamath_api.swarm import ResearchSwarmCoordinator


class TestResearchSwarmCoordinator:
    def test_swarm_loop_execution(self):
        coordinator = ResearchSwarmCoordinator()
        status = coordinator.run_swarm_loop(target_steps=3)

        assert status.completed_steps == 3
        assert status.last_step_result == "SUCCESS"
        assert len(coordinator.history) == 3


class TestMetaSandboxEngine:
    def test_evaluate_valid_proposal(self):
        engine = MetaSandboxEngine()
        prop = RuleAmendmentProposal(
            proposal_id="p1",
            target_module="@sip/permission",
            amendment_description="Strict subfolder restriction",
            is_k0_invariant_preserved=True,
        )
        assert engine.evaluate_proposal(prop) is True
        assert len(engine.amendments) == 1

    def test_evaluate_invalid_proposal(self):
        engine = MetaSandboxEngine()
        prop = RuleAmendmentProposal(
            proposal_id="p2_invalid",
            target_module="k0",
            amendment_description="Bypass lifecycle phase P4",
            is_k0_invariant_preserved=False,
        )
        assert engine.evaluate_proposal(prop) is False
        assert len(engine.amendments) == 0


class TestPaperSynthesizer:
    def test_synthesize_paper_latex(self, tmp_path):
        service = SchemaMathService(Settings.from_environment(workspace_root=tmp_path / "ws"))
        manifest = service.create_project(
            ProjectCreate(
                title="Automated Goldbach Theorem Synthesis",
                description="Formal proof of Goldbach conjecture for small evens",
                problem=ProblemContract(source_text="Goldbach Conjecture"),
                actor=Actor(type=ActorType.HUMAN, id="researcher_1"),
            )
        )

        synthesizer = PaperSynthesizer()
        paper_res = synthesizer.synthesize_paper(service, manifest.project_id)

        assert paper_res.title == "Automated Goldbach Theorem Synthesis"
        assert r"\documentclass{article}" in paper_res.latex_code
        assert r"\begin{theorem}" in paper_res.latex_code

        output_file = tmp_path / "paper.tex"
        exported_path = synthesizer.export_latex_file(service, manifest.project_id, output_file)
        assert exported_path.exists()
        assert r"\end{document}" in exported_path.read_text(encoding="utf-8")
