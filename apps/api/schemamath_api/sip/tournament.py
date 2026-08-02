"""
@sip/schema-tournament (O4: Competitive Schema Framework Competitions)

Evaluates competing schema proposals under equal-budget execution conditions,
tracks framework overthrow events, and accommodates meta-sandbox updates.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, Field

from schemamath_api.k0.decision import Decision, ModuleDecision
from schemamath_api.k0.lifecycle import (
    HookType,
    LifecycleContext,
    LifecyclePhase,
    LifecycleScheduler,
)
from schemamath_api.k0.manifest import (
    CapabilityDeclaration,
    LifecycleHook,
    ModuleKind,
)
from schemamath_api.sip.core import SipModule

logger = logging.getLogger(__name__)


class SchemaProposal(BaseModel):
    proposal_id: str
    author_role: str
    framework_name: str
    schema_definition: dict[str, Any]
    score: float = 0.0
    evaluation_count: int = 0


class TournamentModule(SipModule):
    """
    O4: @sip/schema-tournament module.

    Runs equal-budget competitive evaluation of schema proposals in P7_ASSERTION_EVALUATION.
    """

    def __init__(self) -> None:
        super().__init__(
            name="@sip/schema-tournament",
            version="1.1.0",
            kind=ModuleKind.SCHEDULER,
            description="Competitive Schema Proposals and Equal-Budget Framework Tournament",
            provides=[CapabilityDeclaration(name="schema_tournament", version="1.1")],
        )

        self.proposals: dict[str, SchemaProposal] = {}
        self.leading_proposal_id: str | None = None

        self._manifest.lifecycle_hooks = [
            LifecycleHook(
                phase=LifecyclePhase.P7_ASSERTION_EVALUATION,
                hook_type=HookType.PRE,
                priority=20,
                description="Evaluate competitive schema proposals in tournament arena",
            ),
        ]

    def bind_hooks(self, scheduler: LifecycleScheduler) -> None:
        scheduler.register_hook(
            self.name,
            LifecyclePhase.P7_ASSERTION_EVALUATION,
            HookType.PRE,
            20,
            self.evaluate_tournament,
        )

    def submit_proposal(
        self, proposal_id: str, framework_name: str, schema_def: dict[str, Any], author: str = "builder"
    ) -> SchemaProposal:
        """Submit a new competitive schema proposal."""
        prop = SchemaProposal(
            proposal_id=proposal_id,
            author_role=author,
            framework_name=framework_name,
            schema_definition=schema_def,
        )
        self.proposals[proposal_id] = prop
        if self.leading_proposal_id is None:
            self.leading_proposal_id = proposal_id
        return prop

    def evaluate_tournament(self, ctx: LifecycleContext) -> ModuleDecision:
        """Evaluate submitted proposals against task assertions."""
        prop_id = ctx.input_data.get("tournament_proposal_id")
        score_delta = ctx.input_data.get("evaluation_score_delta", 0.0)

        if prop_id and prop_id in self.proposals:
            prop = self.proposals[prop_id]
            prop.score += score_delta
            prop.evaluation_count += 1

            # Update leading proposal if score exceeds current leader
            if self.leading_proposal_id and prop_id != self.leading_proposal_id:
                leader = self.proposals[self.leading_proposal_id]
                if prop.score > leader.score:
                    logger.info("Framework Overthrow: '%s' surpassed '%s'", prop.framework_name, leader.framework_name)
                    self.leading_proposal_id = prop_id
                    ctx.propose_event({
                        "event_type": "FRAMEWORK_OVERTHROWN",
                        "payload": {
                            "new_leader": prop.framework_name,
                            "previous_leader": leader.framework_name,
                            "winning_score": prop.score,
                        },
                    })

        return ModuleDecision(
            source_module=self.name,
            approval=Decision.ALLOW,
            capabilities={"schema_tournament"},
            metadata={"leading_framework": self.leading_proposal_id},
        )


def createTournament() -> TournamentModule:
    """Helper factory matching JS-style createTournament()."""
    return TournamentModule()
