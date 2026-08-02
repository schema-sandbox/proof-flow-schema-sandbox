from __future__ import annotations

import os
from pathlib import Path

from schemamath_api.config import Settings
from schemamath_api.domain import (
    Actor,
    ActorType,
    BranchCreate,
    BranchState,
    BridgeResultCreate,
    ChallengeCreate,
    ChallengeType,
    ChatImportConfirmRequest,
    ChatImportSelection,
    DeadEndConstraintCreate,
    DeadEndStrength,
    HumanNoteCreate,
    ImportDisposition,
    ProblemContract,
    ProjectCreate,
    PythonPluginRunRequest,
    ResearchCheckpointCreate,
    ResearchPacketRequest,
    RouteCreate,
    RouteMergeRequest,
    RouteSplitChild,
    RouteSplitRequest,
    RouteState,
    RouteStateChange,
)
from schemamath_api.service import SchemaMathService


def main() -> None:
    root = Path(
        os.environ.get(
            "SCHEMAMATH_WORKSPACE",
            str(Path.cwd() / ".schemamath-workspace"),
        )
    ).resolve()
    plugin_root = Path(
        os.environ.get(
            "SCHEMAMATH_PLUGIN_ROOT",
            str(Path.cwd() / ".schemamath-plugins"),
        )
    ).resolve()
    service = SchemaMathService(Settings.from_environment(root, plugin_root))
    human = Actor(
        type=ActorType.HUMAN,
        id="demo-researcher",
        display_name="Demo Researcher",
    )
    project = service.create_project(
        ProjectCreate(
            title="Demo: unresolved combinatorial exploration",
            description=(
                "A deliberately unresolved Alpha.2 project exercising branches, "
                "challenges, bridge results, chat import, and an optional Python experiment."
            ),
            problem=ProblemContract(
                source_text=(
                    "Given a finite family of subsets with a specified intersection pattern, "
                    "determine whether a stronger extremal bound should hold."
                ),
                author_notes=(
                    "Synthetic prompt. The goal is to test the research sandbox, not to "
                    "claim a theorem."
                ),
                definitions=["A route is a mechanism-level line of attack."],
                assumptions=["No completeness claim is required."],
            ),
            actor=human,
        )
    )
    route_a = service.create_route(
        project.project_id,
        RouteCreate(
            title="Small-case counterexample search",
            description="Enumerate small structures and look for a minimal obstruction.",
            initial_state=RouteState.ACTIVE,
            actor=human,
        ),
    )
    route_b = service.create_route(
        project.project_id,
        RouteCreate(
            title="Compression / entropy route",
            description="Try to encode the family and derive an information inequality.",
            initial_state=RouteState.SEED,
            revival_conditions=["A useful encoding or invariant is found."],
            actor=human,
        ),
    )
    branch = service.create_branch(
        project.project_id,
        BranchCreate(
            route_id=route_a.route_id,
            title="Enumerate n <= 10",
            description="A bounded branch used to expose parity and boundary effects.",
            parameters={"n_max": 10},
            initial_state=BranchState.ACTIVE,
            actor=human,
        ),
    )
    service.create_challenge(
        project.project_id,
        ChallengeCreate(
            route_id=route_a.route_id,
            branch_id=branch.branch_id,
            challenge_type=ChallengeType.BOUNDARY_CASE,
            statement="The candidate inequality may fail for the empty family.",
            test_plan="Include empty and singleton families in the exact enumeration.",
            actor=human,
        ),
    )
    service.add_human_note(
        project.project_id,
        HumanNoteCreate(
            content=(
                "The small cases may reveal a parity obstruction; do not discard this "
                "route if n <= 10 is inconclusive."
            ),
            route_id=route_a.route_id,
            branch_id=branch.branch_id,
            note_type="INTUITION",
            actor=human,
        ),
    )
    service.create_dead_end_constraint(
        project.project_id,
        DeadEndConstraintCreate(
            title="Naive averaging loses the intersection constraint",
            description=(
                "Previous attempts average over sets before preserving the local "
                "intersection pattern. Deprioritize this exact reduction."
            ),
            route_id=route_b.route_id,
            strength=DeadEndStrength.OBSERVED,
            reopen_conditions=["A weighted average preserves the local constraint."],
            actor=human,
        ),
    )
    service.create_bridge_result(
        project.project_id,
        BridgeResultCreate(
            route_id=route_a.route_id,
            branch_id=branch.branch_id,
            title="Parity classification for the smallest cases",
            summary=(
                "The enumeration does not settle the conjecture, but it separates two "
                "parity classes that can guide a later invariant."
            ),
            enabled_route_ids=[route_b.route_id],
            retained_value=["parity split", "boundary examples"],
            actor=human,
        ),
    )
    split = service.split_route(
        project.project_id,
        route_a.route_id,
        RouteSplitRequest(
            children=[
                RouteSplitChild(
                    title="Even-parity obstruction route",
                    description="Track the small-case obstruction in the even class.",
                    initial_state=RouteState.ACTIVE,
                ),
                RouteSplitChild(
                    title="Odd-parity construction route",
                    description="Search for a construction compatible with the odd class.",
                    initial_state=RouteState.SEED,
                ),
            ],
            reason="The bridge result separates two mechanisms that should not be conflated.",
            actor=human,
        ),
    )
    merged = service.merge_routes(
        project.project_id,
        RouteMergeRequest(
            source_route_ids=[split.created_routes[0].route_id, route_b.route_id],
            title="Signed parity synthesis",
            description=(
                "A synthesis route connecting the even-parity obstruction to a weighted "
                "incidence encoding."
            ),
            reason="Test whether the computational split can seed a structural invariant.",
            supersede_sources=False,
            actor=human,
        ),
    )
    service.create_checkpoint(
        project.project_id,
        ResearchCheckpointCreate(
            current_target="Find an invariant consistent with the small parity split.",
            route_id=route_a.route_id,
            branch_id=branch.branch_id,
            intended_move="Export the parity classes to the compression route.",
            observed_failure_or_gain="No theorem yet; a reusable classification emerged.",
            unresolved_obligations=["prove the classification beyond n=10"],
            next_route_suggestions=["weighted encoding", "search for a minimal counterexample"],
            actor=human,
        ),
    )
    service.change_route_state(
        project.project_id,
        route_b.route_id,
        RouteStateChange(
            new_state=RouteState.DORMANT,
            reason="No useful encoding yet; preserve the route for later revival.",
            actor=human,
        ),
    )

    markdown = b"""# User\nCan the parity split be encoded as a signed sum?\n\n# Assistant\nAlternative approach: define a signed incidence vector and compare its squared norm.\n\n# Assistant\nObjection: the empty family makes the normalization undefined; test the boundary separately.\n"""
    preview = service.preview_chat_import(
        project_id=project.project_id,
        filename="demo-chat.md",
        content=markdown,
        media_type="text/markdown",
        actor=human,
    )
    service.confirm_chat_import(
        project.project_id,
        preview.import_id,
        ChatImportConfirmRequest(
            selections=[
                ChatImportSelection(
                    candidate_id=preview.candidates[1].candidate_id,
                    disposition=ImportDisposition.NEW_BRANCH,
                    route_id=route_b.route_id,
                    title="Signed incidence vector",
                ),
                ChatImportSelection(
                    candidate_id=preview.candidates[2].candidate_id,
                    disposition=ImportDisposition.CHALLENGE,
                    route_id=route_b.route_id,
                    structured_payload={"test_plan": "Check empty and singleton families."},
                ),
            ],
            actor=human,
        ),
    )

    service.enable_plugin(project.project_id, "python.local", human)
    service.run_python_plugin(
        project.project_id,
        PythonPluginRunRequest(
            source_code=(
                "from pathlib import Path\n"
                "import os\n"
                "values = [(-1)**n for n in range(10)]\n"
                "print(values)\n"
                "Path(os.environ['SCHEMAMATH_OUTPUT_DIR'], 'parity.json').write_text("
                "__import__('json').dumps(values), encoding='utf-8')\n"
            ),
            route_id=route_a.route_id,
            branch_id=branch.branch_id,
            timeout_seconds=10,
            actor=human,
        ),
    )

    packet = service.build_research_packet(
        project.project_id,
        ResearchPacketRequest(
            route_ids=[route_a.route_id, route_b.route_id, merged.merged_route.route_id],
            purpose="Generate non-equivalent next moves without forcing a solution.",
        ),
    )
    packet_path = service.project_dir(project.project_id) / "exports" / "demo_research_packet.md"
    packet_path.write_text(packet.markdown, encoding="utf-8")
    export_path = service.export_project_zip(project.project_id)
    print(f"Created demo project: {project.project_id}")
    print(f"Workspace: {service.project_dir(project.project_id)}")
    print(f"Research packet: {packet_path}")
    print(f"Export: {export_path}")


if __name__ == "__main__":
    main()
