"""
Self-Replicating Autonomic Epistemic Organism (AutonomicOrganism)

Monitors system compute load and verification debt; autonomously clones and spawns
child sandbox instances when load exceeds safe thresholds.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from schemamath_api.sip import ComposedSandbox, compose, createFence, createGate, createPartition

logger = logging.getLogger(__name__)


@dataclass
class OrganismState:
    generation: int
    child_sandbox_count: int
    load_factor: float
    is_split_recommended: bool


class AutonomicOrganism:
    """
    Autonomic self-replicating organism for dynamic load shedding and sandbox spawning.
    """

    def __init__(self, generation: int = 1) -> None:
        self.generation = generation
        self.children: list[ComposedSandbox] = []

    def inspect_load(self, active_tasks: int, verification_debt: int) -> OrganismState:
        """Inspect current compute load and verification debt."""
        load_factor = round((active_tasks * 0.1) + (verification_debt * 0.05), 2)
        should_split = load_factor > 0.7

        return OrganismState(
            generation=self.generation,
            child_sandbox_count=len(self.children),
            load_factor=load_factor,
            is_split_recommended=should_split,
        )

    def spawn_child_sandbox(self, allowed_path: str = "/tmp") -> ComposedSandbox:
        """Replicate and spawn a child sandbox node."""
        child = compose(
            createGate(input={"type": "object"}),
            createFence(fs=[allowed_path]),
            createPartition(mode="PROCESS"),
        )
        self.children.append(child)
        logger.info("Organism gen-%d spawned child sandbox #%d", self.generation, len(self.children))
        return child
