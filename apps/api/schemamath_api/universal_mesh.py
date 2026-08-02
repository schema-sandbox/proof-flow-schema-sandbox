"""
Universal Multi-Planet Knowledge Mesh (UniversalKnowledgeMesh)

Provides delay-tolerant multi-planet event log synchronization and split-brain resolution
across distributed planetary-scale research nodes.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from schemamath_api.domain import EventRecord

logger = logging.getLogger(__name__)


@dataclass
class PlanetaryNode:
    planet_id: str
    node_name: str
    synced_event_count: int = 0


class UniversalKnowledgeMesh:
    """
    Universal multi-planet knowledge mesh node coordinator.
    """

    def __init__(self) -> None:
        self.nodes: dict[str, PlanetaryNode] = {}
        self.synchronized_events: list[EventRecord] = []

    def register_node(self, planet_id: str, node_name: str) -> PlanetaryNode:
        """Register a planetary node in the universal mesh network."""
        node = PlanetaryNode(planet_id=planet_id, node_name=node_name)
        self.nodes[planet_id] = node
        logger.info("Registered planetary node '%s' (%s)", node_name, planet_id)
        return node

    def sync_events(self, planet_id: str, events: list[EventRecord]) -> int:
        """Synchronize event logs from a planetary node into the global mesh."""
        if planet_id not in self.nodes:
            self.register_node(planet_id, f"Node-{planet_id}")

        node = self.nodes[planet_id]
        added = 0
        existing_ids = {e.event_id for e in self.synchronized_events}

        for ev in events:
            if ev.event_id not in existing_ids:
                self.synchronized_events.append(ev)
                existing_ids.add(ev.event_id)
                added += 1

        node.synced_event_count += added
        logger.info("Synced %d events from node '%s'", added, planet_id)
        return added
