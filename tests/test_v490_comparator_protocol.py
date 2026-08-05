"""Tests for Comparator Protocol (v49.0)."""

from schemamath_api.comparator_protocol import (
    DEFAULT_AXIOM_CEILING,
    ComparatorProtocol,
)


class TestComparatorVerify:
    def test_matching_statements_pass(self):
        cp = ComparatorProtocol(primary_kernel_runner=lambda _code: True)
        result = cp.verify(
            challenge_id="challenge_1",
            challenge_statement="theorem foo : ∀ n, n + 0 = n",
            candidate_id="solution_1",
            candidate_code="theorem foo : ∀ n, n + 0 = n := by omega",
            candidate_statement="theorem foo : ∀ n, n + 0 = n",
        )
        assert result.statement_match
        assert result.overall_verdict == "PASS"
        assert result.is_verified

    def test_mismatched_statements_fail(self):
        cp = ComparatorProtocol()
        result = cp.verify(
            challenge_id="c1",
            challenge_statement="theorem foo : True",
            candidate_id="s1",
            candidate_code="theorem bar : False := sorry",
            candidate_statement="theorem bar : False",
        )
        assert not result.statement_match
        assert result.overall_verdict == "FAIL"

    def test_sorry_causes_fail(self):
        cp = ComparatorProtocol()
        result = cp.verify(
            challenge_id="c2",
            challenge_statement="theorem x : True",
            candidate_id="s2",
            candidate_code="theorem x : True := sorry",
            candidate_statement="theorem x : True",
        )
        assert result.sorry_count == 1
        assert result.overall_verdict == "FAIL"

    def test_forbidden_axiom_fails(self):
        cp = ComparatorProtocol()
        result = cp.verify(
            challenge_id="c3",
            challenge_statement="theorem x : True",
            candidate_id="s3",
            candidate_code="theorem x : True := trivial",
            candidate_statement="theorem x : True",
            axioms_declared=["propext", "unsafeAxiom"],
        )
        assert not result.axiom_ceiling_respected
        assert result.overall_verdict == "FAIL"

    def test_permitted_axioms_pass(self):
        cp = ComparatorProtocol(primary_kernel_runner=lambda _code: True)
        result = cp.verify(
            challenge_id="c4",
            challenge_statement="theorem x : True",
            candidate_id="s4",
            candidate_code="theorem x : True := trivial",
            candidate_statement="theorem x : True",
            axioms_declared=["propext", "Classical.choice"],
        )
        assert result.axiom_ceiling_respected
        assert result.overall_verdict == "PASS"

    def test_definition_hole_gives_provisional(self):
        cp = ComparatorProtocol(primary_kernel_runner=lambda _code: True)
        code = "opaque myDef : Nat := 42\ntheorem x : True := trivial"
        result = cp.verify(
            challenge_id="c5",
            challenge_statement="theorem x : True",
            candidate_id="s5",
            candidate_code=code,
            candidate_statement="theorem x : True",
        )
        assert len(result.definition_holes) == 1
        assert result.overall_verdict == "PROVISIONAL"

    def test_sorry_def_hole_detected(self):
        cp = ComparatorProtocol()
        code = "def helper : Nat := sorry\ntheorem x : True := trivial"
        result = cp.verify(
            challenge_id="c6",
            challenge_statement="theorem x : True",
            candidate_id="s6",
            candidate_code=code,
            candidate_statement="theorem x : True",
        )
        # sorry in code triggers FAIL regardless of holes
        assert result.sorry_count >= 1
        assert result.overall_verdict == "FAIL"

    def test_secondary_kernel_is_none(self):
        cp = ComparatorProtocol()
        result = cp.verify(
            challenge_id="c7",
            challenge_statement="theorem x : True",
            candidate_id="s7",
            candidate_code="theorem x : True := trivial",
            candidate_statement="theorem x : True",
        )
        assert result.secondary_kernel_accepts is None
        assert result.overall_verdict == "UNAVAILABLE"
        assert not result.primary_kernel_executed

    def test_static_text_cannot_claim_kernel_success(self):
        cp = ComparatorProtocol()
        result = cp.verify(
            challenge_id="c_static",
            challenge_statement="theorem x : True",
            candidate_id="s_static",
            candidate_code="theorem x : True := by definitely_not_a_lean_tactic",
            candidate_statement="theorem x : True",
        )
        assert result.overall_verdict == "UNAVAILABLE"
        assert not result.is_verified

    def test_explicit_kernel_execution_can_pass(self):
        cp = ComparatorProtocol()
        result = cp.verify(
            challenge_id="c_exec",
            challenge_statement="theorem x : True",
            candidate_id="s_exec",
            candidate_code="theorem x : True := trivial",
            candidate_statement="theorem x : True",
            primary_kernel_accepts=True,
            independent_reproduction_status="NOT_CONFIGURED",
        )
        assert result.overall_verdict == "PASS"
        assert result.primary_kernel_executed

    def test_custom_axiom_ceiling(self):
        cp = ComparatorProtocol(axiom_ceiling=frozenset({"propext"}))
        result = cp.verify(
            challenge_id="c8",
            challenge_statement="theorem x : True",
            candidate_id="s8",
            candidate_code="theorem x : True := trivial",
            candidate_statement="theorem x : True",
            axioms_declared=["Classical.choice"],
        )
        assert not result.axiom_ceiling_respected

    def test_statement_normalization(self):
        cp = ComparatorProtocol()
        result = cp.verify(
            challenge_id="c9",
            challenge_statement="theorem   foo :  True",
            candidate_id="s9",
            candidate_code="theorem foo : True := trivial",
            candidate_statement="theorem foo : True",
        )
        assert result.statement_match

    def test_extract_statement_from_code(self):
        cp = ComparatorProtocol()
        result = cp.verify(
            challenge_id="c10",
            challenge_statement="theorem myThm : Nat = Nat := rfl",
            candidate_id="s10",
            candidate_code="import Mathlib\n\ntheorem myThm : Nat = Nat := rfl",
        )
        assert result.statement_match

    def test_axiom_scanning(self):
        cp = ComparatorProtocol()
        axioms = cp._scan_axioms("uses propext and Classical.choice here")
        assert "propext" in axioms
        assert "Classical.choice" in axioms

    def test_default_axiom_ceiling_contents(self):
        assert "propext" in DEFAULT_AXIOM_CEILING
        assert "Classical.choice" in DEFAULT_AXIOM_CEILING
        assert "Quot.sound" in DEFAULT_AXIOM_CEILING
        assert len(DEFAULT_AXIOM_CEILING) == 3
