"""
Tests for ProofFlow v23.0 (Advanced Algebraic Topology & Persistent Homology Analytics Suite)

Covers:
    - VietorisRipsComplexBuilder (Point cloud filtration building)
    - PersistentDiagramEngine (Persistence barcode report generation)
    - BottleneckDistanceCalculator (Bottleneck distance computation)
    - TopologicalDataAnalyzer (TDA landscape vector extraction)
"""

from __future__ import annotations

from schemamath_api.persistent_homology import (
    BottleneckDistanceCalculator,
    PersistentDiagramEngine,
    TopologicalDataAnalyzer,
    VietorisRipsComplexBuilder,
)


class TestPersistentHomology:
    def test_build_filtration_and_diagram(self):
        builder = VietorisRipsComplexBuilder()
        pts = [[0.0, 0.0], [1.0, 0.0], [0.5, 0.866]]
        pairs = builder.build_filtration(pts, max_radius=1.5)

        assert len(pairs) >= 3
        assert pairs[0].persistence > 0

        engine = PersistentDiagramEngine()
        report = engine.generate_diagram(pairs)
        assert report.total_pairs == len(pairs)
        assert report.betti_numbers[0] == 3

    def test_bottleneck_distance_and_tda(self):
        builder = VietorisRipsComplexBuilder()
        pts1 = [[0.0, 0.0], [1.0, 0.0]]
        pts2 = [[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]]

        pairs1 = builder.build_filtration(pts1)
        pairs2 = builder.build_filtration(pts2)

        calc = BottleneckDistanceCalculator()
        dist = calc.compute_bottleneck_distance(pairs1, pairs2)
        assert dist >= 0.0

        tda = TopologicalDataAnalyzer()
        engine = PersistentDiagramEngine()
        landscape = tda.compute_landscape_vector(engine.generate_diagram(pairs1))
        assert len(landscape) == len(pairs1)
