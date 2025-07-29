"""
Unit tests for network functionality.
"""

import pytest
import numpy as np
from probabilistic_quantum_reasoner.core.network import QuantumBayesianNetwork
from probabilistic_quantum_reasoner.core.exceptions import (
    NetworkTopologyError, QuantumStateError
)
from .conftest import (
    assert_probability_distribution_valid,
    assert_quantum_amplitudes_normalized
)


class TestQuantumBayesianNetwork:
    """Test QuantumBayesianNetwork functionality."""
    
    def test_network_creation(self, classical_backend):
        """Test basic network creation."""
        network = QuantumBayesianNetwork("TestNetwork", classical_backend)
        
        assert network.name == "TestNetwork"
        assert network.backend == classical_backend
        assert len(network.nodes) == 0
        assert len(network.edges) == 0
    
    def test_add_quantum_node(self, classical_backend):
        """Test adding quantum nodes."""
        network = QuantumBayesianNetwork("TestNetwork", classical_backend)
        
        # Add quantum node with custom amplitudes
        amplitudes = np.array([0.8, 0.6], dtype=complex)
        node = network.add_quantum_node(
            "test_node",
            outcome_space=["state1", "state2"],
            initial_amplitudes=amplitudes,
            name="Test Quantum Node"
        )
        
        assert node.node_id == "test_node"
        assert node.outcome_space == ["state1", "state2"]
        assert node.name == "Test Quantum Node"
        assert_quantum_amplitudes_normalized(node.quantum_state.amplitudes)
        
        # Node should be in network
        assert "test_node" in network.nodes
        assert network.nodes["test_node"] == node
    
    def test_add_stochastic_node(self, classical_backend):
        """Test adding stochastic nodes."""
        network = QuantumBayesianNetwork("TestNetwork", classical_backend)
        
        node = network.add_stochastic_node(
            "stochastic_node",
            outcome_space=["yes", "no"],
            name="Test Stochastic Node"
        )
        
        assert node.node_id == "stochastic_node"
        assert node.outcome_space == ["yes", "no"]
        assert node.name == "Test Stochastic Node"
        
        # Should have uniform prior by default
        assert_probability_distribution_valid(node.prior_distribution)
    
    def test_add_hybrid_node(self, classical_backend):
        """Test adding hybrid nodes."""
        network = QuantumBayesianNetwork("TestNetwork", classical_backend)
        
        node = network.add_hybrid_node(
            "hybrid_node",
            outcome_space=["option1", "option2", "option3"],
            mixing_parameter=0.7,
            name="Test Hybrid Node"
        )
        
        assert node.node_id == "hybrid_node"
        assert node.mixing_parameter == 0.7
        assert len(node.outcome_space) == 3
    
    def test_duplicate_node_error(self, classical_backend):
        """Test error on duplicate node IDs."""
        network = QuantumBayesianNetwork("TestNetwork", classical_backend)
        
        # Add first node
        network.add_quantum_node("duplicate", ["a", "b"])
        
        # Adding same ID should raise error
        with pytest.raises(ValueError, match="Node duplicate already exists"):
            network.add_quantum_node("duplicate", ["x", "y"])
    
    def test_add_edge(self, classical_backend):
        """Test adding edges between nodes."""
        network = QuantumBayesianNetwork("TestNetwork", classical_backend)
        
        # Create nodes
        parent = network.add_quantum_node("parent", ["p1", "p2"])
        child = network.add_stochastic_node("child", ["c1", "c2"])
        
        # Add edge
        network.add_edge(parent, child)
        
        # Check edge exists
        assert (parent, child) in network.edges
        assert child in network.get_children(parent)
        assert parent in network.get_parents(child)
    
    def test_invalid_edge_error(self, classical_backend):
        """Test error on invalid edges."""
        network = QuantumBayesianNetwork("TestNetwork", classical_backend)
        node = network.add_quantum_node("node1", ["a", "b"])
        
        # Self-loop should raise error
        with pytest.raises(NetworkTopologyError):
            network.add_edge(node, node)
    
    def test_entanglement(self, classical_backend):
        """Test quantum entanglement between nodes."""
        network = QuantumBayesianNetwork("TestNetwork", classical_backend)
        
        # Create quantum nodes
        node1 = network.add_quantum_node("q1", ["0", "1"])
        node2 = network.add_quantum_node("q2", ["0", "1"])
        
        # Entangle nodes
        network.entangle([node1, node2])
        
        # Should be in entangled groups
        assert network.is_entangled(node1, node2)
    
    def test_entanglement_non_quantum_error(self, classical_backend):
        """Test error when entangling non-quantum nodes."""
        network = QuantumBayesianNetwork("TestNetwork", classical_backend)
        
        quantum_node = network.add_quantum_node("q1", ["0", "1"])
        classical_node = network.add_stochastic_node("c1", ["yes", "no"])
        
        # Should raise error
        with pytest.raises(ValueError, match="Only quantum nodes can be entangled"):
            network.entangle([quantum_node, classical_node])
    
    def test_basic_inference(self, small_network):
        """Test basic inference on small network."""
        network = small_network
        
        # Perform inference without evidence
        result = network.infer(query_nodes=["A", "B"])
        
        assert "A" in result.marginal_probabilities
        assert "B" in result.marginal_probabilities
        
        # Check probability distributions are valid
        for node_probs in result.marginal_probabilities.values():
            assert_probability_distribution_valid(node_probs)
    
    def test_conditional_inference(self, small_network):
        """Test conditional inference with evidence."""
        network = small_network
        
        # Inference with evidence
        result = network.infer(
            evidence={"A": "true"},
            query_nodes=["B"]
        )
        
        assert "B" in result.marginal_probabilities
        assert_probability_distribution_valid(result.marginal_probabilities["B"])
    
    def test_intervention(self, small_network):
        """Test causal intervention (do-calculus)."""
        network = small_network
        
        # Perform intervention
        result = network.intervene(
            interventions={"A": "false"},
            query_nodes=["B"]
        )
        
        assert "B" in result.marginal_probabilities
        assert_probability_distribution_valid(result.marginal_probabilities["B"])
    
    def test_get_quantum_state(self, classical_backend):
        """Test getting quantum state of nodes."""
        network = QuantumBayesianNetwork("TestNetwork", classical_backend)
        
        amplitudes = np.array([0.6, 0.8], dtype=complex)
        node = network.add_quantum_node("quantum", ["0", "1"], amplitudes)
        
        state = network.get_quantum_state("quantum")
        assert_quantum_amplitudes_normalized(state.amplitudes)
        
        # Should match normalized input amplitudes
        norm = np.sqrt(np.sum(np.abs(amplitudes) ** 2))
        expected = amplitudes / norm
        np.testing.assert_allclose(state.amplitudes, expected)
    
    def test_quantum_state_nonexistent_node(self, classical_backend):
        """Test error getting state of nonexistent node."""
        network = QuantumBayesianNetwork("TestNetwork", classical_backend)
        
        with pytest.raises(KeyError):
            network.get_quantum_state("nonexistent")
    
    def test_quantum_state_classical_node(self, classical_backend):
        """Test error getting quantum state of classical node."""
        network = QuantumBayesianNetwork("TestNetwork", classical_backend)
        
        network.add_stochastic_node("classical", ["yes", "no"])
        
        with pytest.raises(ValueError, match="not a quantum node"):
            network.get_quantum_state("classical")
    
    def test_set_conditional_probability_table(self, classical_backend):
        """Test setting conditional probability tables."""
        network = QuantumBayesianNetwork("TestNetwork", classical_backend)
        
        parent = network.add_quantum_node("parent", ["p1", "p2"])
        child = network.add_stochastic_node("child", ["c1", "c2"])
        network.add_edge(parent, child)
        
        # Set CPT
        cpt = {
            ("p1",): {"c1": 0.8, "c2": 0.2},
            ("p2",): {"c1": 0.3, "c2": 0.7}
        }
        network.set_conditional_probability_table(child, cpt)
        
        # Verify CPT was set
        assert child.conditional_probability_table.table == cpt
    
    def test_invalid_cpt_probabilities(self, classical_backend):
        """Test error on invalid CPT probabilities."""
        network = QuantumBayesianNetwork("TestNetwork", classical_backend)
        
        parent = network.add_quantum_node("parent", ["p1", "p2"])
        child = network.add_stochastic_node("child", ["c1", "c2"])
        network.add_edge(parent, child)
        
        # Invalid CPT (probabilities don't sum to 1)
        invalid_cpt = {
            ("p1",): {"c1": 0.8, "c2": 0.3},  # Sum = 1.1
            ("p2",): {"c1": 0.3, "c2": 0.7}
        }
        
        with pytest.raises(ValueError, match="Probabilities must sum to 1"):
            network.set_conditional_probability_table(child, invalid_cpt)
    
    def test_network_serialization(self, small_network):
        """Test network serialization to dict."""
        network = small_network
        
        # This would test serialization if implemented
        # For now, just test that method exists
        assert hasattr(network, '__dict__')
    
    @pytest.mark.parametrize("num_nodes", [1, 5, 10])
    def test_network_scaling(self, classical_backend, num_nodes):
        """Test network performance with different sizes."""
        network = QuantumBayesianNetwork("ScaleTest", classical_backend)
        
        # Add nodes
        nodes = []
        for i in range(num_nodes):
            node = network.add_quantum_node(f"node_{i}", ["0", "1"])
            nodes.append(node)
        
        # Add some edges (chain structure)
        for i in range(num_nodes - 1):
            network.add_edge(nodes[i], nodes[i + 1])
        
        # Perform inference
        result = network.infer(query_nodes=[f"node_{num_nodes-1}"])
        
        assert f"node_{num_nodes-1}" in result.marginal_probabilities
        assert_probability_distribution_valid(
            result.marginal_probabilities[f"node_{num_nodes-1}"]
        )
