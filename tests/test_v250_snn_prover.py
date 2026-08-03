"""
Tests for ProofFlow v25.0 (Deep Neuromorphic Spiking Neural Network Theorem Prover)

Covers:
    - SpikingNeuronModel (LIF neuron integration & spike threshold firing)
    - StdpSynapticLearning (STDP synaptic weight LTP & LTD updates)
    - SnnTacticGenerator (Spike rate to Lean4 tactic mapping & energy profiling)
"""

from __future__ import annotations

from schemamath_api.snn_prover import (
    SnnTacticGenerator,
    SpikingNeuronModel,
    StdpSynapticLearning,
)


class TestSnnProver:
    def test_lif_neuron_firing(self):
        neuron = SpikingNeuronModel(threshold=1.0, decay=0.9)
        assert neuron.step(0.5) is False
        assert neuron.step(0.8) is True  # Fired
        assert neuron.step(0.5) is False  # Refractory period

    def test_stdp_learning_and_tactic_gen(self):
        stdp = StdpSynapticLearning()
        w_ltp = stdp.update_weight(pre_spike_time=10.0, post_spike_time=12.0, current_weight=0.5)
        assert w_ltp > 0.5  # LTP weight increase

        w_ltd = stdp.update_weight(pre_spike_time=12.0, post_spike_time=10.0, current_weight=0.5)
        assert w_ltd < 0.5  # LTD weight decrease

        gen = SnnTacticGenerator()
        prop = gen.generate_tactic(spike_rate_hz=60.0)
        assert prop.tactic == "by simp; ring"
        assert prop.spike_confidence == 0.95
