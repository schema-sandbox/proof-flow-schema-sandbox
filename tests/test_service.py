from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest
from schemamath_api.domain import (
    DOSSIER_V2_FIELD_NAMES,
    Actor,
    ActorType,
    ArtifactOrigin,
    ArtifactType,
    AttemptOutcome,
    AttemptRecordCreate,
    BenchmarkBindingCreate,
    BranchCreate,
    BranchState,
    ClaimAtomCreate,
    ClaimSourceClass,
    ContinuationContractCreate,
    ContinuationDecision,
    CostVector,
    CostVectorCreate,
    CoverageStatus,
    DossierField,
    EvidenceCardCreate,
    EvidenceDimension,
    EvidenceDimensionName,
    EvidenceDimensionStatus,
    FormalCoverageBindingCreate,
    HandoffDecisionCreate,
    HandoffPacketV2Create,
    HumanNoteCreate,
    InterpretationStatus,
    MicroFalsificationPlanCreate,
    MutationObservation,
    ProblemContract,
    ProjectCreate,
    QuestionAgendaCreate,
    RepairLineageCreate,
    RepairLineageType,
    RepositorySnapshotCreate,
    ResearchEpisodeDossierV2Create,
    ResearchHierarchyNodeCreate,
    ResearchPacketRequest,
    ReviewLineageCreate,
    RouteCreate,
    RouteState,
    RouteStateChange,
    TransitionAcceptanceCreate,
    TransitionProposalCreate,
    TransitionTriggerClass,
    TransitionVisibility,
    VerificationExecutionManifestCreate,
    VerificationExecutionStatus,
    VerificationMutationSetCreate,
    utc_now,
)
from schemamath_api.projection import ProjectionStore
from schemamath_api.service import ConflictError, NotFoundError, SchemaMathService


def make_project(service: SchemaMathService):
    return service.create_project(
        ProjectCreate(
            title="Test project",
            description="Event-store test",
            problem=ProblemContract(
                source_text="Determine whether the test statement is true.",
                author_notes="No solution is required.",
            ),
        )
    )


def test_project_route_event_chain_and_rebuild(service: SchemaMathService) -> None:
    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="First route", initial_state=RouteState.ACTIVE),
    )
    service.add_human_note(
        project.project_id,
        HumanNoteCreate(
            route_id=route.route_id,
            note_type="INTUITION",
            content="Try a parity invariant.",
        ),
    )
    changed = service.change_route_state(
        project.project_id,
        route.route_id,
        RouteStateChange(
            new_state=RouteState.DORMANT,
            reason="No progress yet; preserve for later.",
        ),
    )
    assert changed.state == RouteState.DORMANT

    report = service.integrity_report(project.project_id)
    assert report.valid is True
    assert report.event_count == 4

    database_path = service.project_dir(project.project_id) / "database" / "projections.sqlite3"
    database_path.unlink()
    replayed = service.rebuild_projection(project.project_id)
    assert replayed == 4
    routes = service.list_routes(project.project_id)
    assert routes[0].state == RouteState.DORMANT


def test_alpha5_transition_proposal_acceptance_and_projection(
    service: SchemaMathService,
) -> None:
    project = make_project(service)
    proposal = service.create_transition_proposal(
        project.project_id,
        TransitionProposalCreate(
            expected_revision=1,
            idempotency_key="proposal-alpha5-1",
            trigger_class=TransitionTriggerClass.OBSERVATION,
            trigger_evidence_refs=["artifact:observation-1"],
            accepted_delta={"claim": {"status": "candidate", "confidence": 0.4}},
            next_obligation_refs=["obligation:verify-1"],
            visibility=TransitionVisibility.DIRECT_OBSERVATION,
            proposal_actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    assert proposal.status.value == "PROPOSED"
    assert service.list_transition_proposals(project.project_id)[0].proposal_id == proposal.proposal_id

    transition = service.accept_transition_proposal(
        project.project_id,
        proposal.proposal_id,
        TransitionAcceptanceCreate(
            expected_revision=2,
            idempotency_key="accept-alpha5-1",
            acceptance_actor=Actor(type=ActorType.HUMAN, id="reviewer"),
            acceptance_mechanism="manual-review",
        ),
    )
    assert transition.accepted is True
    assert transition.from_revision == 2
    assert transition.to_revision == 3
    state = service.research_state(project.project_id)
    assert state.revision == 3
    assert state.claim["status"] == "candidate"
    assert service.list_transition_proposals(project.project_id)[0].status.value == "ACCEPTED"
    receipts = service.list_command_receipts(project.project_id)
    assert receipts[-1].event_ids
    assert receipts[-1].to_revision == 3

    with ProjectionStore(
        service.project_dir(project.project_id) / "database" / "projections.sqlite3"
    ).connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM transition_proposals").fetchone()[0] == 1
        assert (
            connection.execute("SELECT COUNT(*) FROM research_state_transitions").fetchone()[0]
            == 1
        )
        provenance = connection.execute(
            "SELECT revision, idempotency_key FROM events "
            "WHERE event_type = 'RESEARCH_STATE_TRANSITION_ACCEPTED'"
        ).fetchone()
        assert provenance["revision"] == 3
        assert provenance["idempotency_key"] == "accept-alpha5-1"

    replayed = service.rebuild_projection(project.project_id)
    assert replayed == 3
    assert service.research_state(project.project_id).claim["status"] == "candidate"


def test_alpha5_typed_continuation_and_handoff_v2(service: SchemaMathService) -> None:
    project = make_project(service)
    with pytest.raises(ValueError, match="RUN_NEXT requires explicit human confirmation"):
        ContinuationContractCreate(
            expected_revision=1,
            idempotency_key="continuation-invalid",
            decision=ContinuationDecision.RUN_NEXT,
            scope="next proof search",
            actor=Actor(type=ActorType.MODEL, id="planner"),
        )

    continuation = service.create_continuation_contract(
        project.project_id,
        ContinuationContractCreate(
            expected_revision=1,
            idempotency_key="continuation-1",
            decision=ContinuationDecision.NO_CHANGE,
            scope="retain unresolved route",
            obligation_refs=["obligation:next"],
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    assert continuation.status.value == "RECORDED"

    packet = service.create_handoff_packet_v2(
        project.project_id,
        HandoffPacketV2Create(
            expected_revision=2,
            idempotency_key="handoff-v2-1",
            scope="parity route",
            tool_hashes=["sha256:tool-1"],
            fact_evidence_refs=["artifact:fact-1"],
            failure_evidence_refs=["artifact:failure-1"],
            revival_conditions=["try odd modulus"],
            obligation_refs=["obligation:verify"],
            next_receiver_refs=["session:next"],
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    assert len(packet.packet_hash) == 64
    receipt = service.accept_handoff_packet_v2(
        project.project_id,
        packet.packet_id,
        HandoffDecisionCreate(
            expected_revision=3,
            idempotency_key="handoff-receipt-1",
            accepted=True,
            acceptance_actor=Actor(type=ActorType.HUMAN, id="receiver"),
        ),
    )
    assert receipt.accepted is True
    assert service.list_handoff_packets_v2(project.project_id)[0].status.value == "ACCEPTED"
    assert service.integrity_report(project.project_id).valid is True


def test_alpha5_claim_atom_and_six_dimension_evidence(service: SchemaMathService) -> None:
    project = make_project(service)
    claim_proposal = service.propose_claim_atom(
        project.project_id,
        ClaimAtomCreate(
            expected_revision=1,
            idempotency_key="claim-proposal-1",
            statement="The parity invariant persists under the tested move.",
            source_refs=["artifact:claim-source"],
            source_class=ClaimSourceClass.AUTHOR_REPORTED,
            definitions={"move": "the permitted transformation"},
            quantifiers=["for every tested move"],
            scope={"domain": "finite examples"},
            open_obligation_refs=["obligation:formalize"],
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    accepted = service.accept_transition_proposal(
        project.project_id,
        claim_proposal.proposal_id,
        TransitionAcceptanceCreate(
            expected_revision=2,
            idempotency_key="claim-accept-1",
            acceptance_actor=Actor(type=ActorType.HUMAN, id="reviewer"),
            acceptance_mechanism="manual-review",
        ),
    )
    assert accepted.accepted is True
    claim = service.list_claim_atoms(project.project_id)[0]
    assert claim.state.value == "UNRESOLVED"

    lineage = service.create_review_lineage(
        project.project_id,
        ReviewLineageCreate(
            expected_revision=3,
            idempotency_key="lineage-1",
            reviewer_family="human-review",
            organization="local",
            source_material_refs=["artifact:claim-source"],
            checker="manual-check",
            scope="claim wording only",
            unchecked_items=["formal kernel reproduction"],
            actor=Actor(type=ActorType.HUMAN, id="reviewer"),
        ),
    )
    dimensions = {
        name: EvidenceDimension(
            evidence_refs=[f"artifact:{name.value}"],
            status=(
                EvidenceDimensionStatus.PARTIAL
                if name is EvidenceDimensionName.INDEPENDENT_REPRODUCTION
                else EvidenceDimensionStatus.SUPPORTED
            ),
            evaluator_ref="reviewer",
        )
        for name in EvidenceDimensionName
    }
    card = service.create_evidence_card(
        project.project_id,
        EvidenceCardCreate(
            expected_revision=4,
            idempotency_key="evidence-card-1",
            claim_id=claim.claim_id,
            dimensions=dimensions,
            review_lineage_ref=lineage.lineage_id,
            actor=Actor(type=ActorType.HUMAN, id="reviewer"),
        ),
    )
    assert set(card.dimensions) == set(EvidenceDimensionName)
    assert not hasattr(card, "total")
    assert (
        service.list_evidence_cards(project.project_id)[0]
        .dimensions[EvidenceDimensionName.INDEPENDENT_REPRODUCTION]
        .status
        is EvidenceDimensionStatus.PARTIAL
    )


def test_alpha5_verification_manifest_coverage_repository_and_repair(
    service: SchemaMathService,
) -> None:
    project = make_project(service)
    manifest = service.create_verification_manifest(
        project.project_id,
        VerificationExecutionManifestCreate(
            expected_revision=1,
            idempotency_key="manifest-1",
            command=["lake", "env", "lean", "Main.lean"],
            working_directory="proofs",
            environment_fingerprint={"lean": "4.32.0", "lake": "sha256:lake"},
            dependency_lock_refs=["artifact:lake-manifest"],
            exit_status=0,
            verification_check_ids=["check:headline", "check:no-sorry"],
            axiom_ceiling=["propext", "Classical.choice", "Quot.sound"],
            target_scope="headline theorem only",
            status=VerificationExecutionStatus.SUCCEEDED,
            actor=Actor(type=ActorType.TOOL, id="lean"),
        ),
    )
    assert manifest.manifest_sha256

    binding = service.create_coverage_binding(
        project.project_id,
        FormalCoverageBindingCreate(
            expected_revision=2,
            idempotency_key="coverage-1",
            challenge_id="challenge-1",
            headline_statement_ref="theorem:headline",
            covered_declaration_refs=["theorem:headline"],
            missing_declaration_refs=["lemma:boundary"],
            status=CoverageStatus.PARTIAL,
            actor=Actor(type=ActorType.HUMAN, id="reviewer"),
        ),
    )
    assert binding.status is CoverageStatus.PARTIAL

    snapshot = service.create_repository_snapshot(
        project.project_id,
        RepositorySnapshotCreate(
            expected_revision=3,
            idempotency_key="repo-snapshot-1",
            repository_url="https://example.invalid/repo",
            ref="refs/heads/main",
            commit="a" * 40,
            observed_at=utc_now(),
            actor=Actor(type=ActorType.RUNTIME, id="audit"),
        ),
    )
    assert snapshot.commit == "a" * 40

    repair = service.create_repair_lineage(
        project.project_id,
        RepairLineageCreate(
            expected_revision=4,
            idempotency_key="repair-1",
            repair_type=RepairLineageType.REPAIR,
            input_refs=["artifact:broken-proof"],
            output_refs=["artifact:repaired-proof"],
            affected_claim_refs=["claim:headline"],
            downstream_reopen_obligations=["obligation:recheck-boundary"],
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    assert len(repair.repair_sha256) == 64
    assert service.list_verification_manifests(project.project_id)[0].execution_id == manifest.execution_id
    assert service.list_coverage_bindings(project.project_id)[0].binding_id == binding.binding_id
    assert service.list_repository_snapshots(project.project_id)[0].snapshot_id == snapshot.snapshot_id
    assert service.list_repair_lineage(project.project_id)[0].repair_id == repair.repair_id


def test_alpha5_hierarchy_attempt_cost_falsification_benchmark_dossier(
    service: SchemaMathService,
) -> None:
    project = make_project(service)
    node = service.create_hierarchy_node(
        project.project_id,
        ResearchHierarchyNodeCreate(
            expected_revision=1,
            idempotency_key="hierarchy-1",
            node_type="EPISODE",
            label="Episode E1",
            source_refs=["event:1"],
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    attempt = service.create_attempt_record(
        project.project_id,
        AttemptRecordCreate(
            expected_revision=2,
            idempotency_key="attempt-1",
            target_ref=str(node.node_id),
            method_ref="search:parity",
            outcome=AttemptOutcome.NO_CHANGE,
            started_at=utc_now(),
            no_change_reason="search space unchanged",
            actor=Actor(type=ActorType.TOOL, id="searcher"),
        ),
    )
    assert attempt.outcome is AttemptOutcome.NO_CHANGE
    cost = service.create_cost_vector(
        project.project_id,
        CostVectorCreate(
            expected_revision=3,
            idempotency_key="cost-1",
            scope_ref=str(node.node_id),
            vector=CostVector(discovery=1.5, failed_attempts=0.5, human_review=2),
            source_refs=[str(attempt.attempt_id)],
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    assert cost.vector.human_review == 2
    plan = service.create_falsification_plan(
        project.project_id,
        MicroFalsificationPlanCreate(
            expected_revision=4,
            idempotency_key="micro-1",
            target_ref=str(node.node_id),
            hypotheses=["parity breaks at the boundary"],
            tests=["enumerate n <= 20"],
            stopping_conditions=["counterexample found or all cases checked"],
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    assert plan.tests == ["enumerate n <= 20"]
    benchmark = service.create_benchmark_binding(
        project.project_id,
        BenchmarkBindingCreate(
            expected_revision=5,
            idempotency_key="benchmark-1",
            benchmark_ref="benchmark:parity-v1",
            target_refs=[str(node.node_id)],
            metric_definition="counterexamples found per minute",
            result_refs=[str(attempt.attempt_id)],
            actor=Actor(type=ActorType.TOOL, id="benchmark"),
        ),
    )
    assert benchmark.benchmark_ref == "benchmark:parity-v1"

    fields = {
        name: DossierField(
            value=("unknown" if name in {"kernel_execution", "independent_reproduction"} else None),
            source_class="RAW_EVENT" if name == "episode_identity" else "UNKNOWN",
            source_refs=[str(node.node_id)] if name == "episode_identity" else [],
        )
        for name in DOSSIER_V2_FIELD_NAMES
    }
    dossier = service.create_dossier_v2(
        project.project_id,
        ResearchEpisodeDossierV2Create(
            expected_revision=6,
            idempotency_key="dossier-v2-1",
            episode_ref=str(node.node_id),
            fields=fields,
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    assert len(dossier.fields) == 27
    assert len(dossier.dossier_sha256) == 64
    assert service.list_dossiers_v2(project.project_id)[0].dossier_id == dossier.dossier_id


def test_alpha5_command_receipt_mutation_set_and_question_agenda(
    service: SchemaMathService,
) -> None:
    project = make_project(service)
    manifest = service.create_verification_manifest(
        project.project_id,
        VerificationExecutionManifestCreate(
            expected_revision=1,
            idempotency_key="receipt-manifest-1",
            command=["lean", "Main.lean"],
            status=VerificationExecutionStatus.EXECUTED,
            actor=Actor(type=ActorType.TOOL, id="lean"),
        ),
    )
    mutation_set = service.create_mutation_set(
        project.project_id,
        VerificationMutationSetCreate(
            expected_revision=2,
            idempotency_key="mutation-set-1",
            execution_id=manifest.execution_id,
            mutations=[
                MutationObservation(
                    mutation_id="remove-headline",
                    expected="FAIL",
                    observed="FAIL",
                    passed=False,
                )
            ],
            actor=Actor(type=ActorType.HUMAN, id="reviewer"),
        ),
    )
    assert mutation_set.all_expected_failures is True
    agenda = service.create_question_agenda(
        project.project_id,
        QuestionAgendaCreate(
            expected_revision=3,
            idempotency_key="agenda-1",
            episode_ref="episode-1",
            target_specification="a bounded target",
            questions=[{"question_id": "q1", "category": "prior_art"}],
            parent_child_edges=[],
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    assert agenda.coverage_score == 0.2
    assert service.list_command_receipts(project.project_id)[-1].event_ids


def test_certified_close_requires_human_and_evidence(service: SchemaMathService) -> None:
    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="Closable route", initial_state=RouteState.ACTIVE),
    )
    with pytest.raises(ConflictError):
        service.change_route_state(
            project.project_id,
            route.route_id,
            RouteStateChange(
                new_state=RouteState.CERTIFIED_CLOSED,
                reason="A model says it is impossible.",
                actor=Actor(type=ActorType.MODEL, id="critic"),
            ),
        )

    closed = service.change_route_state(
        project.project_id,
        route.route_id,
        RouteStateChange(
            new_state=RouteState.CERTIFIED_CLOSED,
            reason="A finite exhaustive certificate was checked and accepted by the researcher.",
            evidence_refs=["artifact:certificate-1"],
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    assert closed.state == RouteState.CERTIFIED_CLOSED
    assert closed.closure_evidence_refs == ["artifact:certificate-1"]


def test_generic_event_cannot_forge_certified_close(service: SchemaMathService) -> None:
    from schemamath_api.domain import GenericEventCreate

    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="Guarded route", initial_state=RouteState.ACTIVE),
    )
    with pytest.raises(ValueError, match="dedicated endpoint"):
        service.append_generic_event(
            project.project_id,
            GenericEventCreate(
                event_type="ROUTE_STATE_CHANGED",
                actor=Actor(type=ActorType.MODEL, id="forger"),
                route_id=route.route_id,
                payload={"new_state": "CERTIFIED_CLOSED", "closure_evidence_refs": []},
            ),
        )
    assert service.list_routes(project.project_id)[0].state == RouteState.ACTIVE
    assert service.integrity_report(project.project_id).valid is True


def test_generic_event_cannot_forge_internal_event_types(
    service: SchemaMathService,
) -> None:
    from schemamath_api.domain import GenericEventCreate

    project = make_project(service)
    for event_type in ("ROUTE_CREATED", "BRANCH_STATE_CHANGED", "CHALLENGE_STATUS_CHANGED"):
        with pytest.raises(ValueError, match="dedicated endpoint"):
            service.append_generic_event(
                project.project_id,
                GenericEventCreate(
                    event_type=event_type,
                    actor=Actor(type=ActorType.MODEL, id="forger"),
                    payload={"anything": True},
                ),
            )


def test_generic_event_accepts_arbitrary_research_annotation(
    service: SchemaMathService,
) -> None:
    from schemamath_api.domain import GenericEventCreate

    project = make_project(service)
    event = service.append_generic_event(
        project.project_id,
        GenericEventCreate(
            event_type="EXPERIMENT_NOTE",
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
            payload={"label": "sporadic-observation"},
            epistemic_delta="A new experimental observation was recorded.",
        ),
    )
    assert event.event_type == "EXPERIMENT_NOTE"
    events = service.list_events(project.project_id)
    assert any(item.event_type == "EXPERIMENT_NOTE" for item in events)
    assert service.integrity_report(project.project_id).valid is True


def test_content_addressed_artifact_and_packet(service: SchemaMathService) -> None:
    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="Artifact route", initial_state=RouteState.ACTIVE),
    )
    content = b"candidate computation\n"
    artifact = service.add_artifact(
        project_id=project.project_id,
        filename="candidate.txt",
        content=content,
        artifact_type=ArtifactType.TEXT,
        origin=ArtifactOrigin.HUMAN,
        media_type="text/plain",
        interpretation_status=InterpretationStatus.RAW,
        actor=Actor(type=ActorType.HUMAN, id="researcher"),
    )
    stored = service.project_dir(project.project_id) / artifact.blob_relpath
    assert stored.read_bytes() == content

    packet = service.build_research_packet(
        project.project_id,
        ResearchPacketRequest(route_ids=[route.route_id]),
    )
    assert "Do not force a complete solution" in packet.markdown
    assert "Artifact route" in packet.markdown


def test_export_zip_contains_event_source(service: SchemaMathService) -> None:
    project = make_project(service)
    destination = service.export_project_zip(project.project_id)
    assert destination.exists()
    with zipfile.ZipFile(destination) as archive:
        names = set(archive.namelist())
    assert "project.json" in names
    assert "events/events.jsonl" in names


def test_branch_challenge_bridge_dead_end_checkpoint_and_rebuild(
    service: SchemaMathService,
) -> None:
    from schemamath_api.domain import (
        BranchCreate,
        BranchState,
        BranchStateChange,
        BridgeResultCreate,
        ChallengeCreate,
        ChallengeStatus,
        ChallengeStatusChange,
        ChallengeType,
        DeadEndConstraintCreate,
        DeadEndStrength,
        ResearchCheckpointCreate,
    )

    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="Generating-function route", initial_state=RouteState.ACTIVE),
    )
    branch = service.create_branch(
        project.project_id,
        BranchCreate(
            route_id=route.route_id,
            title="Small-parameter branch",
            description="Test n <= 30 before committing to the asymptotic route.",
            assumptions=["n is positive"],
            parameters={"n_max": 30},
            initial_state=BranchState.ACTIVE,
        ),
    )
    challenge = service.create_challenge(
        project.project_id,
        ChallengeCreate(
            route_id=route.route_id,
            branch_id=branch.branch_id,
            challenge_type=ChallengeType.BOUNDARY_CASE,
            statement="The claimed recurrence may fail at n=1.",
            test_plan="Enumerate n=1..30 exactly.",
        ),
    )
    assert challenge.status == ChallengeStatus.OPEN
    resolved = service.change_challenge_status(
        project.project_id,
        challenge.challenge_id,
        ChallengeStatusChange(
            new_status=ChallengeStatus.RESOLVED,
            resolution_summary="The n=1 case was separated and the recurrence was repaired.",
            evidence_refs=["artifact:table-1"],
        ),
    )
    assert resolved.status == ChallengeStatus.RESOLVED

    bridge = service.create_bridge_result(
        project.project_id,
        BridgeResultCreate(
            route_id=route.route_id,
            branch_id=branch.branch_id,
            title="Finite recurrence lemma",
            summary="A finite lemma survives even if the asymptotic route is replaced.",
            retained_value=["recurrence", "boundary classification"],
        ),
    )
    assert bridge.branch_id == branch.branch_id

    dead_end = service.create_dead_end_constraint(
        project.project_id,
        DeadEndConstraintCreate(
            title="Do not assume coefficient positivity",
            description="Repeated attempts used positivity that fails at n=7.",
            route_id=route.route_id,
            branch_id=branch.branch_id,
            applicability_scope=["this recurrence representation"],
            strength=DeadEndStrength.REPEATED,
            reopen_conditions=["a different normalization proves positivity"],
        ),
    )
    assert dead_end.strength == DeadEndStrength.REPEATED

    checkpoint = service.create_checkpoint(
        project.project_id,
        ResearchCheckpointCreate(
            current_target="Classify the valid recurrence range.",
            route_id=route.route_id,
            branch_id=branch.branch_id,
            intended_move="Separate boundary cases from the asymptotic step.",
            assumptions_used=["n >= 2"],
            observed_failure_or_gain="The n=1 obstruction is now explicit.",
            unresolved_obligations=["prove recurrence for all n >= 2"],
            next_route_suggestions=["formalize the recurrence", "search for a bijection"],
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    assert checkpoint.branch_id == branch.branch_id

    changed = service.change_branch_state(
        project.project_id,
        branch.branch_id,
        BranchStateChange(
            new_state=BranchState.BRIDGE_RESULT,
            reason="The branch produced a reusable finite lemma.",
        ),
    )
    assert changed.state == BranchState.BRIDGE_RESULT

    database_path = service.project_dir(project.project_id) / "database" / "projections.sqlite3"
    database_path.unlink()
    replayed = service.rebuild_projection(project.project_id)
    assert replayed >= 9
    assert service.list_branches(project.project_id)[0].state == BranchState.BRIDGE_RESULT
    assert service.list_challenges(project.project_id)[0].status == ChallengeStatus.RESOLVED
    assert service.list_bridge_results(project.project_id)[0].title == "Finite recurrence lemma"
    assert service.list_dead_end_constraints(project.project_id)[0].title.startswith("Do not")
    assert service.list_checkpoints(project.project_id)[0].current_target.startswith("Classify")


def test_chat_import_confirmation_does_not_partially_commit(
    service: SchemaMathService,
) -> None:
    """A bad selection reference must be rejected before any event is written."""
    from uuid import uuid4

    from schemamath_api.domain import (
        ChatImportConfirmRequest,
        ChatImportSelection,
        ImportDisposition,
    )

    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="Host", initial_state=RouteState.ACTIVE),
    )
    preview = service.preview_chat_import(
        project_id=project.project_id,
        filename="conversation.md",
        content=b"# Assistant\nA note to import.\n",
        media_type="text/markdown",
        actor=Actor(type=ActorType.HUMAN, id="researcher"),
    )
    candidate = preview.candidates[0]
    with pytest.raises(NotFoundError):
        service.confirm_chat_import(
            project.project_id,
            preview.import_id,
            ChatImportConfirmRequest(
                selections=[
                    ChatImportSelection(
                        candidate_id=candidate.candidate_id,
                        disposition=ImportDisposition.MODEL_NOTE,
                        route_id=route.route_id,
                    ),
                    ChatImportSelection(
                        candidate_id=candidate.candidate_id,
                        disposition=ImportDisposition.NEW_BRANCH,
                        route_id=uuid4(),
                        title="Bad branch",
                    ),
                ],
                actor=Actor(type=ActorType.HUMAN, id="researcher"),
            ),
        )
    event_types = [event.event_type for event in service.list_events(project.project_id)]
    assert "MODEL_NOTE_IMPORTED" not in event_types
    assert service.list_chat_imports(project.project_id)[0].confirmed_at is None


def test_chat_import_requires_human_confirmation(service: SchemaMathService) -> None:
    from schemamath_api.domain import (
        ChatImportConfirmRequest,
        ChatImportSelection,
        ImportDisposition,
    )

    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="Imported ideas", initial_state=RouteState.ACTIVE),
    )
    markdown = b"""# User\nCan this be attacked by parity?\n\n# Assistant\nAlternative approach: split into even and odd cases.\n\n# Assistant\nObjection: the odd case fails at n=3. Test n <= 20.\n"""
    preview = service.preview_chat_import(
        project_id=project.project_id,
        filename="conversation.md",
        content=markdown,
        media_type="text/markdown",
        actor=Actor(type=ActorType.HUMAN, id="researcher"),
    )
    assert len(preview.candidates) == 3
    assert service.list_branches(project.project_id) == []
    assert service.list_challenges(project.project_id) == []

    first_assistant = preview.candidates[1]
    second_assistant = preview.candidates[2]
    confirmation = service.confirm_chat_import(
        project.project_id,
        preview.import_id,
        ChatImportConfirmRequest(
            selections=[
                ChatImportSelection(
                    candidate_id=first_assistant.candidate_id,
                    disposition=ImportDisposition.NEW_BRANCH,
                    route_id=route.route_id,
                    title="Parity split",
                ),
                ChatImportSelection(
                    candidate_id=second_assistant.candidate_id,
                    disposition=ImportDisposition.CHALLENGE,
                    route_id=route.route_id,
                    structured_payload={"test_plan": "Enumerate n <= 20."},
                ),
            ],
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    assert confirmation.ignored_count == 0
    assert len(service.list_branches(project.project_id)) == 1
    assert len(service.list_challenges(project.project_id)) == 1
    imports = service.list_chat_imports(project.project_id)
    assert imports[0].confirmed_at is not None


def test_python_plugin_success_and_failure_are_recorded(service: SchemaMathService) -> None:
    from schemamath_api.domain import PythonPluginRunRequest

    project = make_project(service)
    service.enable_plugin(
        project.project_id,
        "python.local",
        Actor(type=ActorType.HUMAN, id="researcher"),
    )
    success = service.run_python_plugin(
        project.project_id,
        PythonPluginRunRequest(
            source_code=(
                "from pathlib import Path\n"
                "import os\n"
                "out = Path(os.environ['SCHEMAMATH_OUTPUT_DIR']) / 'result.txt'\n"
                "out.write_text('42', encoding='utf-8')\n"
                "print('experiment ok')\n"
            ),
            timeout_seconds=10,
        ),
    )
    assert success.status.value == "SUCCEEDED"
    assert success.exit_code == 0
    assert success.stdout_artifact_ref is not None
    assert success.produced_artifact_refs

    failed = service.run_python_plugin(
        project.project_id,
        PythonPluginRunRequest(
            source_code="raise RuntimeError('deliberate failure')\n",
            timeout_seconds=10,
        ),
    )
    assert failed.status.value == "FAILED"
    assert failed.exit_code != 0
    assert failed.stderr_artifact_ref is not None
    assert len(service.list_plugin_runs(project.project_id)) == 2
    event_types = [event.event_type for event in service.list_events(project.project_id)]
    assert event_types.count("PLUGIN_RUN_STARTED") == 2
    assert event_types.count("PLUGIN_RUN_COMPLETED") == 2
    assert service.integrity_report(project.project_id).valid is True


def test_route_split_and_merge_preserve_lineage(service: SchemaMathService) -> None:
    from schemamath_api.domain import (
        RouteMergeRequest,
        RouteSplitChild,
        RouteSplitRequest,
    )

    project = make_project(service)
    source = service.create_route(
        project.project_id,
        RouteCreate(
            title="Source route",
            description="A broad representation that should be decomposed.",
            initial_state=RouteState.ACTIVE,
        ),
    )
    split = service.split_route(
        project.project_id,
        source.route_id,
        RouteSplitRequest(
            children=[
                RouteSplitChild(title="Algebraic child", initial_state=RouteState.ACTIVE),
                RouteSplitChild(title="Combinatorial child", initial_state=RouteState.SEED),
            ],
            reason="The source route contains two genuinely different mechanisms.",
        ),
    )
    assert len(split.created_routes) == 2
    assert all(item.parent_route_id == source.route_id for item in split.created_routes)
    assert service._require_route(project.project_id, source.route_id).state == RouteState.ACTIVE

    merged = service.merge_routes(
        project.project_id,
        RouteMergeRequest(
            source_route_ids=[item.route_id for item in split.created_routes],
            title="Synthesis route",
            description="Combine the invariant from one child with the construction from the other.",
            reason="The two child routes supplied complementary components.",
        ),
    )
    assert merged.merged_route.state == RouteState.ACTIVE
    source_states = {
        service._require_route(project.project_id, item.route_id).state
        for item in split.created_routes
    }
    assert source_states == {RouteState.SUPERSEDED}
    event_types = [event.event_type for event in service.list_events(project.project_id)]
    assert "ROUTE_SPLIT" in event_types
    assert "ROUTES_MERGED" in event_types
    assert service.integrity_report(project.project_id).valid is True


def test_chat_import_model_cannot_confirm(service: SchemaMathService) -> None:
    from schemamath_api.domain import (
        ChatImportConfirmRequest,
        ChatImportSelection,
        ImportDisposition,
    )

    project = make_project(service)
    preview = service.preview_chat_import(
        project_id=project.project_id,
        filename="model-output.md",
        content=b"# Assistant\nA candidate route.",
        media_type="text/markdown",
        actor=Actor(type=ActorType.HUMAN, id="researcher"),
    )
    with pytest.raises(ConflictError):
        service.confirm_chat_import(
            project.project_id,
            preview.import_id,
            ChatImportConfirmRequest(
                selections=[
                    ChatImportSelection(
                        candidate_id=preview.candidates[0].candidate_id,
                        disposition=ImportDisposition.MODEL_NOTE,
                    )
                ],
                actor=Actor(type=ActorType.MODEL, id="self-confirming-model"),
            ),
        )


def test_export_import_retains_alpha2_objects_and_plugin_runs(
    service: SchemaMathService, tmp_path: Path
) -> None:
    from schemamath_api.config import Settings
    from schemamath_api.domain import (
        BranchCreate,
        BridgeResultCreate,
        ChallengeCreate,
        ChallengeType,
        DeadEndConstraintCreate,
        PythonPluginRunRequest,
        ResearchCheckpointCreate,
    )

    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="Portable route", initial_state=RouteState.ACTIVE),
    )
    branch = service.create_branch(
        project.project_id,
        BranchCreate(route_id=route.route_id, title="Portable branch"),
    )
    service.create_challenge(
        project.project_id,
        ChallengeCreate(
            route_id=route.route_id,
            branch_id=branch.branch_id,
            challenge_type=ChallengeType.OBJECTION,
            statement="Preserve this objection across export/import.",
        ),
    )
    service.create_bridge_result(
        project.project_id,
        BridgeResultCreate(
            route_id=route.route_id,
            branch_id=branch.branch_id,
            title="Portable bridge",
            summary="A bridge result that should survive replay.",
        ),
    )
    service.create_dead_end_constraint(
        project.project_id,
        DeadEndConstraintCreate(
            route_id=route.route_id,
            branch_id=branch.branch_id,
            title="Portable dead end",
            description="Do not repeat the naive reduction.",
        ),
    )
    service.create_checkpoint(
        project.project_id,
        ResearchCheckpointCreate(
            current_target="Portable checkpoint",
            route_id=route.route_id,
            branch_id=branch.branch_id,
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    service.enable_plugin(
        project.project_id,
        "python.local",
        Actor(type=ActorType.HUMAN, id="researcher"),
    )
    service.run_python_plugin(
        project.project_id,
        PythonPluginRunRequest(source_code="print('portable')", timeout_seconds=10),
    )
    archive = service.export_project_zip(project.project_id)

    imported_service = SchemaMathService(
        Settings.from_environment(tmp_path / "imported-workspaces", tmp_path / "imported-plugins")
    )
    imported = imported_service.import_project_zip(archive)
    assert imported.project_id == project.project_id
    assert imported_service.integrity_report(project.project_id).valid is True
    assert imported_service.list_branches(project.project_id)[0].title == "Portable branch"
    assert imported_service.list_challenges(project.project_id)[0].statement.startswith("Preserve")
    assert imported_service.list_bridge_results(project.project_id)[0].title == "Portable bridge"
    assert (
        imported_service.list_dead_end_constraints(project.project_id)[0].title
        == "Portable dead end"
    )
    assert (
        imported_service.list_checkpoints(project.project_id)[0].current_target
        == "Portable checkpoint"
    )
    assert imported_service.list_plugin_runs(project.project_id)[0].status.value == "SUCCEEDED"


def test_route_split_merge_preserves_source_history(service: SchemaMathService) -> None:
    from schemamath_api.domain import (
        RouteMergeRequest,
        RouteSplitChild,
        RouteSplitRequest,
    )

    project = make_project(service)
    source = service.create_route(
        project.project_id,
        RouteCreate(title="Ambiguous route", initial_state=RouteState.ACTIVE),
    )
    split = service.split_route(
        project.project_id,
        source.route_id,
        RouteSplitRequest(
            children=[
                RouteSplitChild(title="Algebraic child", initial_state=RouteState.ACTIVE),
                RouteSplitChild(title="Combinatorial child", initial_state=RouteState.ACTIVE),
            ],
            reason="The original route contains two genuinely different mechanisms.",
        ),
    )
    assert len(split.created_routes) == 2
    assert service._require_route(project.project_id, source.route_id).state == RouteState.ACTIVE

    merged = service.merge_routes(
        project.project_id,
        RouteMergeRequest(
            source_route_ids=[item.route_id for item in split.created_routes],
            title="Synthesis route",
            description="Use the invariant from one route inside the construction from the other.",
            reason="A bridge was found.",
            supersede_sources=True,
        ),
    )
    assert merged.merged_route.state == RouteState.ACTIVE
    routes = {route.route_id: route for route in service.list_routes(project.project_id)}
    for source_id in merged.source_route_ids:
        assert routes[source_id].state == RouteState.SUPERSEDED
    assert routes[source.route_id].state == RouteState.ACTIVE
    assert service.integrity_report(project.project_id).valid is True


def test_certified_dead_end_requires_human_evidence(service: SchemaMathService) -> None:
    from schemamath_api.domain import DeadEndConstraintCreate, DeadEndStrength

    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="Potential dead end", initial_state=RouteState.ACTIVE),
    )
    with pytest.raises(ConflictError):
        service.create_dead_end_constraint(
            project.project_id,
            DeadEndConstraintCreate(
                route_id=route.route_id,
                title="Premature closure",
                description="A model disliked the route.",
                strength=DeadEndStrength.CERTIFIED,
                actor=Actor(type=ActorType.MODEL, id="critic"),
            ),
        )
    certified = service.create_dead_end_constraint(
        project.project_id,
        DeadEndConstraintCreate(
            route_id=route.route_id,
            title="Bounded impossibility",
            description="A human accepted a finite exhaustive obstruction in the stated scope.",
            strength=DeadEndStrength.CERTIFIED,
            evidence_refs=["artifact:finite-certificate"],
            applicability_scope=["n <= 12"],
            reopen_conditions=["the scope is enlarged or the encoding changes"],
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    assert certified.strength == DeadEndStrength.CERTIFIED


def test_python_plugin_timeout_is_preserved(service: SchemaMathService) -> None:
    from schemamath_api.domain import PythonPluginRunRequest

    project = make_project(service)
    service.enable_plugin(
        project.project_id,
        "python.local",
        Actor(type=ActorType.HUMAN, id="researcher"),
    )
    timed_out = service.run_python_plugin(
        project.project_id,
        PythonPluginRunRequest(
            source_code="import time\ntime.sleep(5)\n",
            timeout_seconds=1,
        ),
    )
    assert timed_out.status.value == "TIMED_OUT"
    assert timed_out.error and "timeout" in timed_out.error
    assert timed_out.stdout_artifact_ref is not None
    assert timed_out.stderr_artifact_ref is not None
    assert service.integrity_report(project.project_id).valid is True


def test_chat_import_parses_html_and_json() -> None:
    from schemamath_api.chat_importer import parse_chat

    html = b"""<html><body><div data-message-author-role="user">Question</div><div data-message-author-role="assistant">Try parity.</div></body></html>"""
    parsed_html = parse_chat("chat.html", "text/html", html)
    assert parsed_html.messages == [("user", "Question"), ("assistant", "Try parity.")]

    json_payload = json.dumps(
        {"messages": [{"role": "user", "content": "Q"}, {"role": "assistant", "content": "A"}]}
    ).encode()
    parsed_json = parse_chat("chat.json", "application/json", json_payload)
    assert parsed_json.messages == [("user", "Q"), ("assistant", "A")]


def test_python_plugin_must_be_enabled(service: SchemaMathService) -> None:
    from schemamath_api.domain import PythonPluginRunRequest

    project = make_project(service)
    with pytest.raises(ConflictError):
        service.run_python_plugin(
            project.project_id,
            PythonPluginRunRequest(source_code="print('not enabled')", timeout_seconds=5),
        )


def test_import_rejects_path_traversal(service: SchemaMathService, tmp_path: Path) -> None:
    archive = tmp_path / "unsafe.smath.zip"
    with zipfile.ZipFile(archive, "w") as handle:
        handle.writestr("../escape.txt", "bad")
        handle.writestr("project.json", "{}")
    with pytest.raises(ConflictError):
        service.import_project_zip(archive)


def test_import_preflight_is_read_only_and_accepts_alpha2_package(
    service: SchemaMathService,
) -> None:
    archive = (
        Path(__file__).resolve().parents[1]
        / "examples"
        / "demo_open_research_project_alpha2.smath.zip"
    )
    report = service.preflight_project_zip(archive)
    assert report.can_import is True
    assert report.schema_version == "0.2"
    assert report.event_chain_valid is True
    assert report.event_count > 0
    assert report.missing_artifact_paths == []
    assert list(service.settings.workspace_root.iterdir()) == []


def test_import_preflight_reports_tampered_chain_and_unsafe_paths(
    service: SchemaMathService, tmp_path: Path
) -> None:
    source = (
        Path(__file__).resolve().parents[1]
        / "examples"
        / "demo_open_research_project_alpha2.smath.zip"
    )
    tampered = tmp_path / "tampered.smath.zip"
    with zipfile.ZipFile(source) as original, zipfile.ZipFile(tampered, "w") as replacement:
        for member in original.infolist():
            content = original.read(member.filename)
            if member.filename == "events/events.jsonl":
                lines = content.decode("utf-8").splitlines()
                event = json.loads(lines[0])
                event["event_type"] = "TAMPERED_EVENT"
                lines[0] = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
                content = ("\n".join(lines) + "\n").encode("utf-8")
            replacement.writestr(member, content)
    report = service.preflight_project_zip(tampered)
    assert report.can_import is False
    assert report.event_chain_valid is False
    assert "event hash chain is invalid" in report.errors

    unsafe = tmp_path / "unsafe-preflight.smath.zip"
    with zipfile.ZipFile(unsafe, "w") as archive:
        archive.writestr("../escape.txt", "bad")
        archive.writestr("project.json", "{}")
    unsafe_report = service.preflight_project_zip(unsafe)
    assert unsafe_report.can_import is False
    assert any("unsafe path" in error for error in unsafe_report.errors)


def test_import_rejects_tampered_chain_even_when_manifest_points_elsewhere(
    service: SchemaMathService, tmp_path: Path
) -> None:
    """Preflight inspects manifest.event_stream, but import replays events.jsonl."""
    project = make_project(service)
    service.create_route(
        project.project_id,
        RouteCreate(title="R", initial_state=RouteState.ACTIVE),
    )
    archive = service.export_project_zip(project.project_id)

    bypass = tmp_path / "bypass.smath.zip"
    with zipfile.ZipFile(archive) as source, zipfile.ZipFile(bypass, "w") as replacement:
        for member in source.infolist():
            if member.filename in {"project.json", "events/events.jsonl"}:
                continue
            replacement.writestr(member, source.read(member.filename))
        chain = source.read("events/events.jsonl").decode("utf-8")
        # A valid, self-consistent copy that preflight will inspect.
        replacement.writestr("events/backup.jsonl", chain)
        # The canonical stream import actually replays, with its chain broken.
        lines = chain.splitlines()
        event = json.loads(lines[0])
        event["event_type"] = "TAMPERED_EVENT"
        lines[0] = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
        replacement.writestr("events/events.jsonl", ("\n".join(lines) + "\n"))
        # Point the manifest at the clean copy so preflight approves the archive.
        manifest = json.loads(source.read("project.json"))
        manifest["event_stream"] = "events/backup.jsonl"
        replacement.writestr(
            "project.json", json.dumps(manifest, ensure_ascii=False, sort_keys=True)
        )

    report = service.preflight_project_zip(bypass)
    assert report.can_import is True
    from schemamath_api.config import Settings

    imported_service = SchemaMathService(
        Settings.from_environment(tmp_path / "imported-workspaces", tmp_path / "imported-plugins")
    )
    with pytest.raises(ConflictError, match="event chain is invalid"):
        imported_service.import_project_zip(bypass)


def test_corrupt_event_history_is_reported_by_integrity_check(service: SchemaMathService) -> None:
    project = make_project(service)
    event_path = service.project_dir(project.project_id) / "events" / "events.jsonl"
    records = event_path.read_text(encoding="utf-8").splitlines()
    record = json.loads(records[0])
    record["event_type"] = "TAMPERED_EVENT"
    records[0] = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
    event_path.write_text("\n".join(records) + "\n", encoding="utf-8")

    report = service.integrity_report(project.project_id)
    assert report.valid is False


def test_corrupt_event_tail_locks_project_against_new_writes(
    service: SchemaMathService,
) -> None:
    project = make_project(service)
    event_path = service.project_dir(project.project_id) / "events" / "events.jsonl"
    records = event_path.read_text(encoding="utf-8").splitlines()
    record = json.loads(records[-1])
    record["event_type"] = "TAMPERED_TAIL"
    records[-1] = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
    event_path.write_text("\n".join(records) + "\n", encoding="utf-8")

    report = service.integrity_report(project.project_id)
    assert report.valid is False
    with pytest.raises(ValueError, match="read-only until recovery"):
        service.create_route(
            project.project_id,
            RouteCreate(
                title="Must not append to a corrupt history", initial_state=RouteState.ACTIVE
            ),
        )


def test_corrupt_event_history_blocks_middle_event_tampering(
    service: SchemaMathService,
) -> None:
    """A non-tail (early) tamper must also refuse further appends.

    Regression for a bug where only the tail record was checked on append: an
    attacker/process that altered an earlier event could keep writing even though
    the chain was already invalid.
    """
    project = make_project(service)
    event_path = service.project_dir(project.project_id) / "events" / "events.jsonl"
    records = event_path.read_text(encoding="utf-8").splitlines()
    record = json.loads(records[0])
    record["event_type"] = "EARLY_TAMPERED_EVENT"
    records[0] = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
    event_path.write_text("\n".join(records) + "\n", encoding="utf-8")

    report = service.integrity_report(project.project_id)
    assert report.valid is False
    with pytest.raises(ValueError, match="read-only until recovery"):
        service.create_route(
            project.project_id,
            RouteCreate(
                title="Must not append after early corruption", initial_state=RouteState.ACTIVE
            ),
        )


def test_initial_state_cannot_bypass_certified_closure_gate(
    service: SchemaMathService,
) -> None:
    """CERTIFIED_CLOSED/COMPLETED must not be reachable via initial_state."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError, match="CERTIFIED_CLOSED cannot be an initial state"):
        RouteCreate(title="Sneaky", initial_state=RouteState.CERTIFIED_CLOSED)

    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="Host", initial_state=RouteState.ACTIVE),
    )
    with pytest.raises(ValidationError, match="COMPLETED cannot be an initial state"):
        BranchCreate(
            route_id=route.route_id,
            title="Sneaky branch",
            initial_state=BranchState.COMPLETED,
        )


def test_branch_only_objection_is_projected(service: SchemaMathService) -> None:
    from schemamath_api.domain import HumanNoteCreate

    project = make_project(service)
    route = service.create_route(
        project.project_id,
        RouteCreate(title="Host route", initial_state=RouteState.ACTIVE),
    )
    branch = service.create_branch(
        project.project_id,
        BranchCreate(route_id=route.route_id, title="Leaf branch"),
    )
    service.add_human_note(
        project.project_id,
        HumanNoteCreate(
            branch_id=branch.branch_id,
            note_type="COUNTEREXAMPLE",
            content="The construction fails at n=3.",
            actor=Actor(type=ActorType.HUMAN, id="researcher"),
        ),
    )
    projected = service.list_branches(project.project_id)[0]
    assert "The construction fails at n=3." in projected.objections


def test_projection_migrations_upgrade_legacy_database(tmp_path: Path) -> None:
    database_path = tmp_path / "legacy.sqlite3"
    import sqlite3

    with sqlite3.connect(database_path) as connection:
        connection.execute(
            "CREATE TABLE events (sequence INTEGER PRIMARY KEY, event_id TEXT NOT NULL, route_id TEXT)"
        )
        connection.execute(
            "CREATE TABLE project_plugins (plugin_id TEXT PRIMARY KEY, version TEXT, enabled INTEGER)"
        )
    projection = ProjectionStore(database_path)
    assert projection.schema_version() == ProjectionStore.CURRENT_SCHEMA_VERSION
    with projection.connect() as connection:
        event_columns = {row["name"] for row in connection.execute("PRAGMA table_info(events)")}
        plugin_columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(project_plugins)")
        }
    assert {"branch_id", "artifact_refs_json", "epistemic_delta_type"} <= event_columns
    assert "record_json" in plugin_columns
