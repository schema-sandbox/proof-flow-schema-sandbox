"""
Tests for ProofFlow v20.0.0 (EpistemicDigitalTwin, SimulatedResearchCampaign)

Covers:
    - EpistemicDigitalTwin (Global research digital twin state synchronization)
    - SimulatedResearchCampaign (Monte Carlo hyper-simulation of parallel trajectories)
"""

from __future__ import annotations

from schemamath_api.digital_twin import EpistemicDigitalTwin, SimulatedResearchCampaign


class TestEpistemicDigitalTwin:
    def test_get_twin_state(self):
        twin = EpistemicDigitalTwin()
        state = twin.get_twin_state()

        assert state.status == "SYNCHRONIZED"
        assert state.global_research_fronts > 1000
        assert state.fidelity_score > 0.95


class TestSimulatedResearchCampaign:
    def test_run_hyper_simulation(self):
        sim = SimulatedResearchCampaign()
        res = sim.run_hyper_simulation("Simulate 100k Quantum Gravity Paths", trajectory_count=100000)

        assert res.simulated_trajectories_count == 100000
        assert res.successful_outcomes > 80000
        assert res.success_rate > 0.8
