"""
STORM / Co-STORM Question Agenda Generator (v52.0)

Implements the pre-search question-agenda mechanism from v0.12/v0.13:
- Pre-search question generation based on target specification and prior art
- Dynamic mind-map construction
- Retrieval-augmented follow-up questions
- Human steering interface

Serves as the precursor stage to P (Problem Portfolio) and G (Goal Binding).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class QuestionNode:
    """A single node in the question mind-map."""
    question_id: str
    question_text: str
    category: str  # "tractability", "ambiguity", "prior_art", "certificate_cost", "strategy"
    priority: int  # 1 (highest) to 5 (lowest)
    parent_id: str | None = None
    answers: list[str] = field(default_factory=list)
    follow_ups: list[str] = field(default_factory=list)
    is_resolved: bool = False


@dataclass
class QuestionAgenda:
    """Complete question agenda for a research episode."""
    episode_id: str
    target_specification: str
    questions: list[QuestionNode]
    mind_map_edges: list[tuple[str, str]]  # (parent_id, child_id)
    coverage_score: float  # 0.0-1.0, how many categories are covered

    @property
    def open_questions(self) -> list[QuestionNode]:
        return [q for q in self.questions if not q.is_resolved]

    @property
    def resolved_count(self) -> int:
        return sum(1 for q in self.questions if q.is_resolved)


CATEGORY_TEMPLATES: dict[str, list[str]] = {
    "tractability": [
        "What is the estimated difficulty level of this target?",
        "Are there known partial results or related solved problems?",
        "What certificate type would a solution require?",
    ],
    "ambiguity": [
        "Is the problem statement fully formalized with explicit quantifiers?",
        "Are there competing definitions in the literature?",
        "What edge cases or boundary conditions need clarification?",
    ],
    "prior_art": [
        "What are the most relevant prior results?",
        "Has this problem been attempted with AI assistance before?",
        "Are there failed approaches documented in the literature?",
    ],
    "certificate_cost": [
        "What is the estimated verification cost (formal proof vs finite certificate)?",
        "Is certificate asymmetry exploitable (cheap verification, hard generation)?",
        "What proof assistant infrastructure is available?",
    ],
    "strategy": [
        "Which operational configuration (O1-O4) is most appropriate?",
        "Should multiple models be used in parallel or sequence?",
        "What falsification topology should be employed?",
    ],
}


class QuestionAgendaGenerator:
    """Generates pre-search question agendas for research episodes."""

    def generate_agenda(
        self,
        episode_id: str,
        target_specification: str,
        known_prior_art: list[str] | None = None,
        categories: list[str] | None = None,
        custom_questions: list[str] | None = None,
    ) -> QuestionAgenda:
        """Generate a complete question agenda from target specification."""
        active_categories = categories or list(CATEGORY_TEMPLATES.keys())
        questions: list[QuestionNode] = []
        edges: list[tuple[str, str]] = []
        q_counter = 0

        # Generate category-based questions
        for cat in active_categories:
            if cat not in CATEGORY_TEMPLATES:
                continue
            root_id = f"q_{q_counter}"
            root_q = QuestionNode(
                question_id=root_id,
                question_text=f"[{cat.upper()}] Assessment for: {target_specification[:80]}",
                category=cat,
                priority=active_categories.index(cat) + 1,
            )
            questions.append(root_q)
            q_counter += 1

            for template in CATEGORY_TEMPLATES[cat]:
                child_id = f"q_{q_counter}"
                child_q = QuestionNode(
                    question_id=child_id,
                    question_text=template,
                    category=cat,
                    priority=active_categories.index(cat) + 1,
                    parent_id=root_id,
                )
                questions.append(child_q)
                edges.append((root_id, child_id))
                q_counter += 1

        # Add prior art follow-ups
        if known_prior_art:
            for art in known_prior_art:
                child_id = f"q_{q_counter}"
                questions.append(QuestionNode(
                    question_id=child_id,
                    question_text=f"How does prior result '{art}' constrain our approach?",
                    category="prior_art",
                    priority=2,
                ))
                q_counter += 1

        # Add custom questions
        if custom_questions:
            for cq in custom_questions:
                child_id = f"q_{q_counter}"
                questions.append(QuestionNode(
                    question_id=child_id,
                    question_text=cq,
                    category="strategy",
                    priority=1,
                ))
                q_counter += 1

        # Compute coverage
        covered = set(q.category for q in questions)
        coverage = len(covered) / len(CATEGORY_TEMPLATES) if CATEGORY_TEMPLATES else 0.0

        agenda = QuestionAgenda(
            episode_id=episode_id,
            target_specification=target_specification,
            questions=questions,
            mind_map_edges=edges,
            coverage_score=coverage,
        )
        logger.info(
            "Generated question agenda '%s': %d questions, %.0f%% coverage",
            episode_id,
            len(questions),
            coverage * 100,
        )
        return agenda

    def resolve_question(self, agenda: QuestionAgenda, question_id: str, answer: str) -> bool:
        """Mark a question as resolved and optionally generate follow-ups."""
        for q in agenda.questions:
            if q.question_id == question_id:
                q.answers.append(answer)
                q.is_resolved = True
                return True
        return False
