"""Seed a complete English demonstration project into ProofFlow workspace."""
from __future__ import annotations

import sys
from pathlib import Path

# Add apps/api to path
ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "apps" / "api"
if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))

from schemamath_api.config import Settings  # noqa: E402
from schemamath_api.domain import (  # noqa: E402
    Actor,
    ActorType,
    BranchCreate,
    BranchState,
    BridgeResultCreate,
    ChallengeCreate,
    ChallengeType,
    ProblemContract,
    ProjectCreate,
    ResearchCheckpointCreate,
    RouteCreate,
    RouteState,
)
from schemamath_api.service import SchemaMathService  # noqa: E402

HUMAN = Actor(type=ActorType.HUMAN, id="lead-mathematician", display_name="Lead Researcher")


def seed_english_project() -> None:
    settings = Settings.from_environment()
    service = SchemaMathService(settings)

    project = service.create_project(
        ProjectCreate(
            title="Twin Prime Conjecture Exploration",
            description="Investigation of sieve methods, spectral obstructions, and bounded prime gaps.",
            problem=ProblemContract(
                source_text="Are there infinitely many prime pairs (p, p+2)?",
                author_notes="Exploratory workspace evaluating Goldston-Pintz-Yildirim weights, Zhang's bounded gaps, and obstruction revival conditions.",
                definitions=[
                    "Twin Primes: Pair (p, p+2) where both p and p+2 are prime.",
                    "Parity Barrier: Sieve methods cannot distinguish integers with an odd number of prime factors from those with an even number.",
                ],
                assumptions=[
                    "Generalized Riemann Hypothesis (provisional)",
                    "Elliott-Halberstam Conjecture (conditional branch)",
                ],
            ),
            actor=HUMAN,
        )
    )

    pid = project.project_id
    print(f"Created English Project: {project.title} (ID: {pid})")

    # 1. Sieve Theory Route
    route_sieve = service.create_route(
        pid,
        RouteCreate(
            title="Sieve Theory Route",
            description="Parity barrier analysis, Selberg sieve variants, and smooth weight optimizations.",
            initial_state=RouteState.ACTIVE,
            actor=HUMAN,
        ),
    )

    # Branches for Sieve Route
    _branch_gpy = service.create_branch(
        pid,
        BranchCreate(
            route_id=route_sieve.route_id,
            title="GPY Sieve Construction",
            description="Approximation of prime tuples via smooth short-interval weights.",
            initial_state=BranchState.ACTIVE,
            actor=HUMAN,
        ),
    )

    branch_maynard = service.create_branch(
        pid,
        BranchCreate(
            route_id=route_sieve.route_id,
            title="Maynard-Tao Multidimensional Sieve",
            description="Higher-dimensional weight functions bypassing classical single-variable parity obstruction.",
            initial_state=BranchState.ACTIVE,
            actor=HUMAN,
        ),
    )

    # 2. Analytic Number Theory Route
    route_analytic = service.create_route(
        pid,
        RouteCreate(
            title="Analytic Number Theory Route",
            description="Distribution of primes in arithmetic progressions to large moduli beyond square-root threshold.",
            initial_state=RouteState.CHALLENGED,
            actor=HUMAN,
        ),
    )

    branch_bv = service.create_branch(
        pid,
        BranchCreate(
            route_id=route_analytic.route_id,
            title="Bombieri-Vinogradov Extension",
            description="Investigation of distribution level theta > 1/2 for smooth factorable moduli.",
            initial_state=BranchState.ACTIVE,
            actor=HUMAN,
        ),
    )

    # 3. Spectral Obstruction Route
    _route_spectral = service.create_route(
        pid,
        RouteCreate(
            title="Spectral & Automorphic Route",
            description="Selberg eigenvalue conjecture and spectral gaps on arithmetic surfaces.",
            initial_state=RouteState.DORMANT,
            revival_conditions=[
                "A sharper exceptional eigenvalue bound lambda_1 >= 1/4 - eps is proved.",
                "Kloosterman sum bilinear estimates yield level of distribution theta >= 0.55.",
            ],
            actor=HUMAN,
        ),
    )

    # Challenges
    service.create_challenge(
        pid,
        ChallengeCreate(
            route_id=route_analytic.route_id,
            challenge_type=ChallengeType.OBJECTION,
            statement="Parity barrier fundamentally obstructs isolating prime pairs without bilinear forms.",
            test_plan="Verify if bilinear Kloosterman estimates break the parity symmetry.",
            branch_id=branch_bv.branch_id,
            actor=HUMAN,
        ),
    )

    # Bridge Results
    service.create_bridge_result(
        pid,
        BridgeResultCreate(
            route_id=route_sieve.route_id,
            title="Zhang Bounded Prime Gaps (2013)",
            summary="Proved liminf (p_{n+1} - p_n) <= 70,000,000 using smooth factorable moduli of distribution level 1/2 + 1/1168.",
            retained_value=[
                "Established existence of finite bounded gap between consecutive primes.",
                "Bypassed full Elliott-Halberstam requirement using factorable moduli.",
            ],
            branch_id=branch_maynard.branch_id,
            actor=HUMAN,
        ),
    )

    # Checkpoint
    service.create_checkpoint(
        pid,
        ResearchCheckpointCreate(
            current_target="Evaluate Maynard-Tao variational integrals for k=50 prime tuples.",
            intended_move="Run numerical quadratic form optimization on simplex polynomials.",
            observed_failure_or_gain="Unconditional gap bound reduced to 246; gap bounded by 6 under Generalized Elliott-Halberstam.",
            unresolved_obligations=[
                "Construct Lean 4 verification artifact for the multidimensional sieve weight positivity.",
                "Derive numerical bound for k=100 tuple weights.",
            ],
            route_id=route_sieve.route_id,
            branch_id=branch_maynard.branch_id,
            actor=HUMAN,
        ),
    )

    print("Successfully populated English demonstration project with routes, branches, challenges, and bridge results!")


if __name__ == "__main__":
    seed_english_project()
