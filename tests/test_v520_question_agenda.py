"""Tests for Question Agenda Generator (v52.0)."""

import pytest
from schemamath_api.question_agenda import (
    QuestionAgendaGenerator, CATEGORY_TEMPLATES, QuestionAgenda,
)


class TestQuestionAgendaGenerator:
    def test_default_agenda(self):
        gen = QuestionAgendaGenerator()
        agenda = gen.generate_agenda("ep1", "Erdős conjecture #536")
        assert agenda.episode_id == "ep1"
        assert len(agenda.questions) > 0
        assert agenda.coverage_score == 1.0

    def test_all_categories_covered(self):
        gen = QuestionAgendaGenerator()
        agenda = gen.generate_agenda("ep2", "test target")
        cats = {q.category for q in agenda.questions}
        assert cats == set(CATEGORY_TEMPLATES.keys())

    def test_selective_categories(self):
        gen = QuestionAgendaGenerator()
        agenda = gen.generate_agenda(
            "ep3", "test", categories=["tractability", "prior_art"],
        )
        cats = {q.category for q in agenda.questions}
        assert "tractability" in cats
        assert "prior_art" in cats
        assert "strategy" not in cats

    def test_coverage_partial(self):
        gen = QuestionAgendaGenerator()
        agenda = gen.generate_agenda(
            "ep4", "test", categories=["tractability"],
        )
        assert agenda.coverage_score == 1.0 / len(CATEGORY_TEMPLATES)

    def test_custom_questions_added(self):
        gen = QuestionAgendaGenerator()
        agenda = gen.generate_agenda(
            "ep5", "test",
            custom_questions=["Is there a Lean 4 formalization available?"],
        )
        texts = [q.question_text for q in agenda.questions]
        assert any("Lean 4" in t for t in texts)

    def test_prior_art_follow_ups(self):
        gen = QuestionAgendaGenerator()
        agenda = gen.generate_agenda(
            "ep6", "test",
            known_prior_art=["Smith 2024", "Jones 2025"],
        )
        texts = [q.question_text for q in agenda.questions]
        assert any("Smith 2024" in t for t in texts)
        assert any("Jones 2025" in t for t in texts)

    def test_mind_map_edges(self):
        gen = QuestionAgendaGenerator()
        agenda = gen.generate_agenda("ep7", "test")
        assert len(agenda.mind_map_edges) > 0
        for parent, child in agenda.mind_map_edges:
            assert parent != child

    def test_open_questions(self):
        gen = QuestionAgendaGenerator()
        agenda = gen.generate_agenda("ep8", "test")
        assert len(agenda.open_questions) == len(agenda.questions)
        assert agenda.resolved_count == 0

    def test_resolve_question(self):
        gen = QuestionAgendaGenerator()
        agenda = gen.generate_agenda("ep9", "test")
        first_q = agenda.questions[0]
        result = gen.resolve_question(agenda, first_q.question_id, "Yes, tractable")
        assert result is True
        assert first_q.is_resolved
        assert "Yes, tractable" in first_q.answers
        assert agenda.resolved_count == 1

    def test_resolve_nonexistent_question(self):
        gen = QuestionAgendaGenerator()
        agenda = gen.generate_agenda("ep10", "test")
        result = gen.resolve_question(agenda, "nonexistent_id", "answer")
        assert result is False

    def test_question_priorities(self):
        gen = QuestionAgendaGenerator()
        agenda = gen.generate_agenda("ep11", "test")
        priorities = {q.priority for q in agenda.questions}
        assert len(priorities) > 1  # Different categories have different priorities

    def test_parent_child_relationship(self):
        gen = QuestionAgendaGenerator()
        agenda = gen.generate_agenda("ep12", "test", categories=["tractability"])
        children = [q for q in agenda.questions if q.parent_id is not None]
        assert len(children) > 0
        parent_ids = {q.question_id for q in agenda.questions if q.parent_id is None}
        for child in children:
            assert child.parent_id in parent_ids
