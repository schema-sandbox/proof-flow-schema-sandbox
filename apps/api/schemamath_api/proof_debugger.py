"""
Interactive Time-Traveling Proof Debugger (ProofDebugger)

Enables precise single-step time travel backward/forward through 100,000+ step
epistemic event DAGs with breakpoint suspension and state snapshot inspection.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from schemamath_api.domain import EventRecord

logger = logging.getLogger(__name__)


@dataclass
class DebuggerState:
    current_offset: int = 0
    total_events: int = 0
    current_event: EventRecord | None = None
    breakpoints: set[str] = None

    def __post_init__(self) -> None:
        if self.breakpoints is None:
            self.breakpoints = set()


class ProofDebugger:
    """
    Time-travel debugger for stepping through ProofFlow event logs.
    """

    def __init__(self, events: list[EventRecord]) -> None:
        self.events = events
        self.state = DebuggerState(total_events=len(events))
        if events:
            self.state.current_event = events[0]

    def set_breakpoint(self, event_type: str) -> None:
        """Add a breakpoint on event_type."""
        self.state.breakpoints.add(event_type.upper())

    def step_forward(self) -> EventRecord | None:
        """Advance one step in time."""
        if self.state.current_offset + 1 < len(self.events):
            self.state.current_offset += 1
            self.state.current_event = self.events[self.state.current_offset]
            return self.state.current_event
        return None

    def step_backward(self) -> EventRecord | None:
        """Rewind one step in time."""
        if self.state.current_offset > 0:
            self.state.current_offset -= 1
            self.state.current_event = self.events[self.state.current_offset]
            return self.state.current_event
        return None

    def jump_to_offset(self, offset: int) -> EventRecord | None:
        """Jump directly to a specified offset."""
        if 0 <= offset < len(self.events):
            self.state.current_offset = offset
            self.state.current_event = self.events[offset]
            return self.state.current_event
        return None
