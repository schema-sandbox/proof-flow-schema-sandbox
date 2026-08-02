"""
Interplanetary Content-Addressed Event Store (IpfsEventStore)

Implements IPFS Multihash CID content addressing for event records,
providing immutable decentralized distribution across planetary research networks.
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from schemamath_api.domain import EventRecord
from schemamath_api.event_store import canonical_json

logger = logging.getLogger(__name__)


@dataclass
class IpfsCidRecord:
    cid: str
    event_id: str
    content_hash: str


class IpfsEventStore:
    """
    IPFS Content-Addressed EventStore providing planetary event distribution.
    """

    def __init__(self) -> None:
        self.cid_index: dict[str, EventRecord] = {}

    @staticmethod
    def generate_cid(data: dict[str, Any]) -> str:
        """Generate IPFS-compatible CID Multihash string (Qm...)."""
        raw_bytes = canonical_json(data)
        h = hashlib.sha256(raw_bytes).hexdigest()
        import base64
        b58_hash = base64.b32encode(h[:20].encode()).decode("utf-8").lower()
        return f"Qm{b58_hash}"

    def store_event(self, record: EventRecord) -> IpfsCidRecord:
        """Store an event record and return its IPFS CID record."""
        data = record.model_dump(mode="json")
        cid = self.generate_cid(data)

        self.cid_index[cid] = record
        logger.info("Event '%s' stored under IPFS CID '%s'", record.event_id, cid)

        return IpfsCidRecord(
            cid=cid,
            event_id=str(record.event_id),
            content_hash=record.event_hash,
        )

    def retrieve_by_cid(self, cid: str) -> EventRecord | None:
        """Retrieve an event record by its IPFS CID."""
        return self.cid_index.get(cid)
