"""
DeepSeek R1 Reasoning Chain Parser and Importer (DeepSeekR1Importer)

Parses DeepSeek R1 reasoning trace tags (`<think> ... </think>` and `reasoning_content`),
extracts step-by-step thinking traces, and projects them into ProofFlow research routes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from uuid import UUID

from schemamath_api.domain import Actor, ActorType, ProblemContract, ProjectCreate
from schemamath_api.service import SchemaMathService


@dataclass
class DeepSeekReasoningStep:
    step_index: int
    content: str
    is_objection: bool = False
    is_assumption: bool = False


@dataclass
class ParsedDeepSeekChain:
    thinking_trace: str
    final_answer: str
    steps: list[DeepSeekReasoningStep] = field(default_factory=list)


class DeepSeekR1Importer:
    """
    Parses DeepSeek R1 output containing reasoning chains and converts them into ProofFlow projects.
    """

    @staticmethod
    def parse_reasoning_text(raw_text: str) -> ParsedDeepSeekChain:
        """Parse raw text containing <think> ... </think> tags."""
        think_match = re.search(r"<think>(.*?)</think>", raw_text, re.DOTALL | re.IGNORECASE)

        if think_match:
            thinking_trace = think_match.group(1).strip()
            final_answer = raw_text[think_match.end() :].strip()
        else:
            thinking_trace = ""
            final_answer = raw_text.strip()

        # Split thinking trace into individual reasoning steps
        raw_paragraphs = [p.strip() for p in thinking_trace.split("\n\n") if p.strip()]
        steps: list[DeepSeekReasoningStep] = []

        for idx, paragraph in enumerate(raw_paragraphs, start=1):
            is_obj = any(k in paragraph.lower() for k in ["however", "but", "wait", "objection", "counterexample", "non-goal", "fail"])
            is_ass = any(k in paragraph.lower() for k in ["assume", "suppose", "let ", "given ", "hypothesis"])

            steps.append(
                DeepSeekReasoningStep(
                    step_index=idx,
                    content=paragraph,
                    is_objection=is_obj,
                    is_assumption=is_ass,
                )
            )

        return ParsedDeepSeekChain(
            thinking_trace=thinking_trace,
            final_answer=final_answer,
            steps=steps,
        )

    def import_into_service(
        self,
        service: SchemaMathService,
        title: str,
        raw_deepseek_text: str,
        actor_id: str = "deepseek_r1",
    ) -> UUID:
        """Parse DeepSeek output and import into a new ProofFlow project."""
        parsed = self.parse_reasoning_text(raw_deepseek_text)

        manifest = service.create_project(
            ProjectCreate(
                title=title,
                description=f"Imported from DeepSeek R1 reasoning trace ({len(parsed.steps)} thinking steps)",
                problem=ProblemContract(
                    source_text=parsed.final_answer or "DeepSeek R1 Reasoning Target",
                    author_notes=f"Thinking Trace length: {len(parsed.thinking_trace)} chars",
                ),
                actor=Actor(type=ActorType.MODEL, id=actor_id),
            )
        )

        return manifest.project_id
