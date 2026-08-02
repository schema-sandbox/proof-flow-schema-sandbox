"""
Tests for ProofFlow v29.0 (Bio-Molecular Folding & 3D Protein Structure Formal Proof Translator)

Covers:
    - PdbStructureParser (PDB atomic coordinate parsing)
    - RamachandranPlotEvaluator (Steric clash evaluation)
    - Lean4BioGeometryBridge (Lean4 structural code translation)
    - EnergyLandscapeOptimizer (CHARMM/AMBER potential energy computation)
"""

from __future__ import annotations

import pytest

from schemamath_api.biomath_translator import (
    EnergyLandscapeOptimizer,
    Lean4BioGeometryBridge,
    PdbStructureParser,
    RamachandranPlotEvaluator,
)


class TestBiomathTranslator:
    def test_pdb_parse_and_ramachandran_eval(self):
        parser = PdbStructureParser()
        pdb = "ATOM 1 CA ALA A 1 10.0 12.0 15.0\nATOM 2 CA GLY A 2 12.0 14.0 17.0"
        angles = parser.parse_backbone_angles(pdb)
        assert len(angles) == 2

        evaluator = RamachandranPlotEvaluator()
        assessment = evaluator.evaluate_angles(angles)
        assert assessment.is_structurally_valid is True
        assert assessment.favored_region_count == 2

        bridge = Lean4BioGeometryBridge()
        lean_code = bridge.translate_structure("1ubq", assessment)
        assert "theorem 1ubq_validity" in lean_code

    def test_energy_optimizer(self):
        opt = EnergyLandscapeOptimizer()
        res = opt.compute_potential_energy("1ubq", atom_count=50)
        assert res.potential_energy_kcal_mol < 0.0
        assert res.is_at_local_minimum is True
