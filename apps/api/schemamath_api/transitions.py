from __future__ import annotations

from .domain import (
    ActorType,
    BranchState,
    BranchStateChange,
    ChallengeStatus,
    ChallengeStatusChange,
    RouteState,
    RouteStateChange,
)

ALLOWED_TRANSITIONS: dict[RouteState, set[RouteState]] = {
    RouteState.SEED: {
        RouteState.ACTIVE,
        RouteState.CHALLENGED,
        RouteState.DORMANT,
        RouteState.BRIDGE_RESULT,
        RouteState.SUPERSEDED,
    },
    RouteState.ACTIVE: {
        RouteState.CHALLENGED,
        RouteState.CONDITIONAL,
        RouteState.DORMANT,
        RouteState.BRIDGE_RESULT,
        RouteState.SUPERSEDED,
        RouteState.CERTIFIED_CLOSED,
    },
    RouteState.CHALLENGED: {
        RouteState.ACTIVE,
        RouteState.CONDITIONAL,
        RouteState.DORMANT,
        RouteState.BRIDGE_RESULT,
        RouteState.SUPERSEDED,
        RouteState.CERTIFIED_CLOSED,
    },
    RouteState.CONDITIONAL: {
        RouteState.ACTIVE,
        RouteState.DORMANT,
        RouteState.BRIDGE_RESULT,
        RouteState.SUPERSEDED,
        RouteState.CERTIFIED_CLOSED,
    },
    RouteState.DORMANT: {
        RouteState.REVIVED,
        RouteState.SUPERSEDED,
        RouteState.CERTIFIED_CLOSED,
    },
    RouteState.REVIVED: {
        RouteState.ACTIVE,
        RouteState.CHALLENGED,
        RouteState.CONDITIONAL,
        RouteState.DORMANT,
        RouteState.BRIDGE_RESULT,
        RouteState.SUPERSEDED,
    },
    RouteState.BRIDGE_RESULT: {
        RouteState.ACTIVE,
        RouteState.DORMANT,
        RouteState.SUPERSEDED,
    },
    RouteState.SUPERSEDED: {RouteState.REVIVED},
    RouteState.CERTIFIED_CLOSED: {RouteState.REVIVED},
}


ALLOWED_BRANCH_TRANSITIONS: dict[BranchState, set[BranchState]] = {
    BranchState.SEED: {
        BranchState.ACTIVE,
        BranchState.CHALLENGED,
        BranchState.DORMANT,
        BranchState.BRIDGE_RESULT,
        BranchState.SUPERSEDED,
    },
    BranchState.ACTIVE: {
        BranchState.CHALLENGED,
        BranchState.DORMANT,
        BranchState.BRIDGE_RESULT,
        BranchState.SUPERSEDED,
        BranchState.COMPLETED,
    },
    BranchState.CHALLENGED: {
        BranchState.ACTIVE,
        BranchState.DORMANT,
        BranchState.BRIDGE_RESULT,
        BranchState.SUPERSEDED,
        BranchState.COMPLETED,
    },
    BranchState.DORMANT: {BranchState.REVIVED, BranchState.SUPERSEDED},
    BranchState.REVIVED: {
        BranchState.ACTIVE,
        BranchState.CHALLENGED,
        BranchState.DORMANT,
        BranchState.BRIDGE_RESULT,
        BranchState.SUPERSEDED,
    },
    BranchState.BRIDGE_RESULT: {
        BranchState.ACTIVE,
        BranchState.DORMANT,
        BranchState.SUPERSEDED,
        BranchState.COMPLETED,
    },
    BranchState.SUPERSEDED: {BranchState.REVIVED},
    BranchState.COMPLETED: {BranchState.REVIVED},
}


ALLOWED_CHALLENGE_TRANSITIONS: dict[ChallengeStatus, set[ChallengeStatus]] = {
    ChallengeStatus.OPEN: {
        ChallengeStatus.TESTING,
        ChallengeStatus.RESOLVED,
        ChallengeStatus.DEFERRED,
        ChallengeStatus.WITHDRAWN,
    },
    ChallengeStatus.TESTING: {
        ChallengeStatus.OPEN,
        ChallengeStatus.RESOLVED,
        ChallengeStatus.DEFERRED,
        ChallengeStatus.WITHDRAWN,
    },
    ChallengeStatus.DEFERRED: {
        ChallengeStatus.OPEN,
        ChallengeStatus.TESTING,
        ChallengeStatus.RESOLVED,
        ChallengeStatus.WITHDRAWN,
    },
    ChallengeStatus.RESOLVED: {ChallengeStatus.OPEN},
    ChallengeStatus.WITHDRAWN: {ChallengeStatus.OPEN},
}


class InvalidTransition(ValueError):
    pass


def validate_transition(current: RouteState, request: RouteStateChange) -> None:
    if request.new_state == current:
        raise InvalidTransition(f"route is already in state {current}")
    if request.new_state not in ALLOWED_TRANSITIONS.get(current, set()):
        raise InvalidTransition(f"transition {current} -> {request.new_state} is not allowed")
    if request.new_state == RouteState.CERTIFIED_CLOSED:
        if request.actor.type != ActorType.HUMAN and not request.human_confirmed:
            raise InvalidTransition(
                "CERTIFIED_CLOSED requires a human actor or explicit human confirmation"
            )
        if not request.evidence_refs:
            raise InvalidTransition(
                "CERTIFIED_CLOSED requires at least one closure evidence reference"
            )
    if current == RouteState.CERTIFIED_CLOSED and request.new_state == RouteState.REVIVED:
        if request.actor.type != ActorType.HUMAN and not request.human_confirmed:
            raise InvalidTransition("reviving a certified-closed route requires human confirmation")


def validate_branch_transition(current: BranchState, request: BranchStateChange) -> None:
    if request.new_state == current:
        raise InvalidTransition(f"branch is already in state {current}")
    if request.new_state not in ALLOWED_BRANCH_TRANSITIONS.get(current, set()):
        raise InvalidTransition(
            f"branch transition {current} -> {request.new_state} is not allowed"
        )


def validate_challenge_transition(current: ChallengeStatus, request: ChallengeStatusChange) -> None:
    if request.new_status == current:
        raise InvalidTransition(f"challenge is already in status {current}")
    if request.new_status not in ALLOWED_CHALLENGE_TRANSITIONS.get(current, set()):
        raise InvalidTransition(
            f"challenge transition {current} -> {request.new_status} is not allowed"
        )
    if request.new_status == ChallengeStatus.RESOLVED and not request.resolution_summary:
        raise InvalidTransition("resolving a challenge requires a resolution summary")


# Explicit alias used by the service layer.
def validate_route_transition(current: RouteState, request: RouteStateChange) -> None:
    validate_transition(current, request)
