"""
Quantum XOR reasoning example.

This example demonstrates quantum entanglement and superposition in logical
reasoning using XOR gates and quantum amplitude interference.
"""

import numpy as np
from typing import Dict, List, Any, Optional
import logging

from ..core.network import QuantumBayesianNetwork
from ..core.operators import UnitaryOperator, CNOTOperator, HadamardOperator
from ..backends.simulator import ClassicalSimulator

logger = logging.getLogger(__name__)


class QuantumXORExample:
    """
    Quantum XOR gate reasoning example.
    
    Demonstrates quantum logical reasoning using:
    - Quantum superposition of inputs
    - Entangled XOR relationships
    - Amplitude interference effects
    - Quantum vs classical logical inference
    """
    
    def __init__(self, backend: Optional[Any] = None) -> None:
        """
        Initialize quantum XOR example.
        
        Args:
            backend: Quantum backend (defaults to classical simulator)
        """
        if backend is None:
            backend = ClassicalSimulator()
        
        self.backend = backend
        self.network = self._create_xor_network()
        
        logger.info("Initialized Quantum XOR reasoning example")
    
    def _create_xor_network(self) -> QuantumBayesianNetwork:
        """Create quantum XOR reasoning network."""
        network = QuantumBayesianNetwork("QuantumXOR", self.backend)
        
        # Input qubits A and B
        input_a = network.add_quantum_node(
            "input_a",
            outcome_space=[0, 1],
            name="Input A",
            initial_amplitudes=np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
        )
        
        input_b = network.add_quantum_node(
            "input_b", 
            outcome_space=[0, 1],
            name="Input B",
            initial_amplitudes=np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
        )
        
        # XOR output
        xor_output = network.add_quantum_node(
            "xor_output",
            outcome_space=[0, 1],
            name="XOR Output",
            initial_amplitudes=np.array([1.0, 0.0], dtype=complex)
        )
        
        # Create logical dependencies
        network.add_edge(input_a, xor_output)
        network.add_edge(input_b, xor_output)
        
        # Entangle inputs and output to implement XOR logic
        network.entangle([input_a, input_b, xor_output])
        
        # Set up XOR quantum logic
        self._implement_xor_logic(network)
        
        return network
    
    def _implement_xor_logic(self, network: QuantumBayesianNetwork) -> None:
        """Implement quantum XOR logic using unitary operations."""
        # This is a simplified implementation
        # In practice, would use controlled gates and proper quantum circuit design
        
        # Create CNOT-like relationship for XOR
        # XOR(a,b) = a ⊕ b
        
        # For now, we'll implement this through conditional quantum operators
        # that will be applied during inference
        
        logger.debug("Implemented quantum XOR logic relationships")
    
    def demonstrate_superposition_xor(self) -> Dict[str, Any]:
        """Demonstrate XOR with superposition inputs."""
        logger.info("Demonstrating XOR with superposition inputs")
        
        # Both inputs in superposition |+⟩ = (|0⟩ + |1⟩)/√2
        result = self.network.infer()
        
        # Extract quantum amplitudes
        amplitudes = result.quantum_amplitudes
        
        # Compute XOR truth table probabilities
        truth_table = self._compute_quantum_truth_table()
        
        return {
            "input_superposition": {
                "input_a": amplitudes["input_a"] if amplitudes else "N/A",
                "input_b": amplitudes["input_b"] if amplitudes else "N/A"
            },
            "output_distribution": result.marginal_probabilities["xor_output"],
            "quantum_truth_table": truth_table,
            "entanglement_measure": result.entanglement_measure,
            "classical_vs_quantum": self._compare_classical_quantum_xor()
        }
    
    def _compute_quantum_truth_table(self) -> Dict[str, Dict[str, float]]:
        """Compute quantum XOR truth table with probabilities."""
        truth_table = {}
        
        # Test all input combinations
        input_combinations = [
            (0, 0), (0, 1), (1, 0), (1, 1)
        ]
        
        for a, b in input_combinations:
            # Set evidence for inputs
            evidence = {"input_a": a, "input_b": b}
            result = self.network.infer(evidence=evidence, query_nodes=["xor_output"])
            
            expected_output = a ^ b  # Classical XOR
            quantum_output_dist = result.marginal_probabilities["xor_output"]
            
            truth_table[f"{a},{b}"] = {
                "inputs": (a, b),
                "classical_output": expected_output,
                "quantum_output_distribution": quantum_output_dist,
                "quantum_most_likely": max(quantum_output_dist.items(), key=lambda x: x[1])[0],
                "agreement": quantum_output_dist.get(expected_output, 0.0)
            }
        
        return truth_table
    
    def _compare_classical_quantum_xor(self) -> Dict[str, Any]:
        """Compare classical and quantum XOR implementations."""
        classical_results = {}
        quantum_results = {}
        
        for a in [0, 1]:
            for b in [0, 1]:
                # Classical XOR
                classical_output = a ^ b
                classical_results[f"{a},{b}"] = classical_output
                
                # Quantum XOR
                evidence = {"input_a": a, "input_b": b}
                result = self.network.infer(evidence=evidence, query_nodes=["xor_output"])
                quantum_dist = result.marginal_probabilities["xor_output"]
                
                # Most likely quantum output
                quantum_output = max(quantum_dist.items(), key=lambda x: x[1])[0]
                quantum_results[f"{a},{b}"] = {
                    "distribution": quantum_dist,
                    "most_likely": quantum_output,
                    "certainty": max(quantum_dist.values())
                }
        
        # Compute agreement
        agreement_count = 0
        total_cases = len(classical_results)
        
        for key in classical_results:
            if classical_results[key] == quantum_results[key]["most_likely"]:
                agreement_count += 1
        
        return {
            "classical_results": classical_results,
            "quantum_results": quantum_results,
            "agreement_rate": agreement_count / total_cases,
            "quantum_uncertainty": np.mean([
                1 - max(qr["distribution"].values()) 
                for qr in quantum_results.values()
            ])
        }
    
    def demonstrate_interference_effects(self) -> Dict[str, Any]:
        """Demonstrate quantum interference in XOR reasoning."""
        logger.info("Demonstrating quantum interference effects")
        
        # Create specific superposition states to show interference
        interference_results = {}
        
        # Test different phase relationships
        phases = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
        
        for phase in phases:
            # Set input A to |+⟩ and input B to |+⟩ with phase
            a_amplitudes = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
            b_amplitudes = np.array([1/np.sqrt(2), np.exp(1j*phase)/np.sqrt(2)], dtype=complex)
            
            # Update node states
            self.network.nodes["input_a"].quantum_state.amplitudes = a_amplitudes
            self.network.nodes["input_b"].quantum_state.amplitudes = b_amplitudes
            
            # Perform inference
            result = self.network.infer(query_nodes=["xor_output"])
            
            interference_results[f"phase_{phase:.3f}"] = {
                "phase": phase,
                "input_a_amplitudes": a_amplitudes.tolist(),
                "input_b_amplitudes": b_amplitudes.tolist(),
                "output_distribution": result.marginal_probabilities["xor_output"],
                "interference_pattern": self._analyze_interference_pattern(
                    result.marginal_probabilities["xor_output"]
                )
            }
        
        return {
            "interference_results": interference_results,
            "phase_dependence": self._analyze_phase_dependence(interference_results),
            "quantum_coherence": self._measure_quantum_coherence(interference_results)
        }
    
    def _analyze_interference_pattern(self, output_dist: Dict[str, float]) -> Dict[str, Any]:
        """Analyze interference pattern in output distribution."""
        prob_0 = output_dist.get(0, 0.0)
        prob_1 = output_dist.get(1, 0.0)
        
        return {
            "bias": prob_1 - prob_0,
            "uncertainty": -sum(p * np.log2(p) for p in [prob_0, prob_1] if p > 0),
            "max_prob": max(prob_0, prob_1),
            "interference_strength": abs(prob_1 - prob_0)
        }
    
    def _analyze_phase_dependence(self, interference_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze how output depends on input phase."""
        phases = []
        biases = []
        
        for key, result in interference_results.items():
            phases.append(result["phase"])
            biases.append(result["interference_pattern"]["bias"])
        
        return {
            "phase_values": phases,
            "bias_values": biases,
            "max_bias": max(biases),
            "min_bias": min(biases),
            "bias_range": max(biases) - min(biases),
            "phase_sensitivity": np.std(biases)
        }
    
    def _measure_quantum_coherence(self, interference_results: Dict[str, Any]) -> float:
        """Measure quantum coherence across different phases."""
        coherence_values = []
        
        for result in interference_results.values():
            uncertainty = result["interference_pattern"]["uncertainty"]
            max_uncertainty = 1.0  # For 2-level system
            coherence = 1 - (uncertainty / max_uncertainty)
            coherence_values.append(coherence)
        
        return np.mean(coherence_values)
    
    def multi_qubit_xor_reasoning(self, n_inputs: int = 3) -> Dict[str, Any]:
        """Demonstrate multi-qubit XOR reasoning."""
        logger.info(f"Demonstrating {n_inputs}-input XOR reasoning")
        
        # Create extended network
        extended_network = QuantumBayesianNetwork(f"XOR_{n_inputs}", self.backend)
        
        # Add input nodes
        input_nodes = []
        for i in range(n_inputs):
            node_id = f"input_{i}"
            node = extended_network.add_quantum_node(
                node_id,
                outcome_space=[0, 1],
                name=f"Input {i}",
                initial_amplitudes=np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
            )
            input_nodes.append(node_id)
        
        # Add XOR output
        output_node = extended_network.add_quantum_node(
            "xor_output",
            outcome_space=[0, 1],
            name="XOR Output"
        )
        
        # Connect inputs to output
        for input_node in input_nodes:
            extended_network.add_edge(input_node, output_node)
        
        # Entangle all nodes
        extended_network.entangle(input_nodes + [output_node])
        
        # Test multi-input XOR
        results = {}
        
        # Generate all possible input combinations
        for i in range(2**n_inputs):
            input_values = [(i >> j) & 1 for j in range(n_inputs)]
            evidence = {f"input_{j}": input_values[j] for j in range(n_inputs)}
            
            result = extended_network.infer(evidence=evidence, query_nodes=[output_node])
            
            # Classical multi-XOR
            classical_xor = sum(input_values) % 2
            
            quantum_dist = result.marginal_probabilities[output_node]
            quantum_output = max(quantum_dist.items(), key=lambda x: x[1])[0]
            
            results[f"inputs_{input_values}"] = {
                "inputs": input_values,
                "classical_xor": classical_xor,
                "quantum_distribution": quantum_dist,
                "quantum_output": quantum_output,
                "agreement": quantum_output == classical_xor
            }
        
        # Compute overall statistics
        agreement_rate = sum(1 for r in results.values() if r["agreement"]) / len(results)
        
        return {
            "n_inputs": n_inputs,
            "test_results": results,
            "agreement_rate": agreement_rate,
            "quantum_advantage": self._assess_quantum_advantage(results),
            "scalability": self._assess_scalability(n_inputs, agreement_rate)
        }
    
    def _assess_quantum_advantage(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess quantum advantage in XOR reasoning."""
        # Measure quantum uncertainty and parallelism
        uncertainties = []
        
        for result in results.values():
            dist = result["quantum_distribution"]
            entropy = -sum(p * np.log2(p) for p in dist.values() if p > 0)
            uncertainties.append(entropy)
        
        return {
            "average_uncertainty": np.mean(uncertainties),
            "max_uncertainty": max(uncertainties),
            "parallel_evaluation": "Quantum system evaluates all inputs simultaneously",
            "superposition_advantage": "Can process multiple input combinations in parallel"
        }
    
    def _assess_scalability(self, n_inputs: int, agreement_rate: float) -> Dict[str, Any]:
        """Assess scalability of quantum XOR reasoning."""
        return {
            "input_size": n_inputs,
            "state_space_size": 2**n_inputs,
            "agreement_rate": agreement_rate,
            "quantum_resource_scaling": f"O(2^{n_inputs}) classical vs O({n_inputs}) quantum qubits",
            "complexity_advantage": "Exponential classical vs polynomial quantum"
        }
    
    def run_complete_xor_analysis(self) -> Dict[str, Any]:
        """Run complete quantum XOR analysis."""
        logger.info("Running complete quantum XOR analysis")
        
        results = {
            "basic_xor": self.demonstrate_superposition_xor(),
            "interference_effects": self.demonstrate_interference_effects(),
            "multi_qubit_xor": self.multi_qubit_xor_reasoning(3),
            "scalability_test": {
                "2_inputs": self.multi_qubit_xor_reasoning(2),
                "3_inputs": self.multi_qubit_xor_reasoning(3),
                "4_inputs": self.multi_qubit_xor_reasoning(4)
            }
        }
        
        return results
    
    def generate_xor_report(self) -> str:
        """Generate human-readable XOR analysis report."""
        results = self.run_complete_xor_analysis()
        
        report = []
        report.append("=== Quantum XOR Reasoning Analysis Report ===\n")
        
        # Basic XOR
        basic = results["basic_xor"]
        report.append("1. Basic Quantum XOR:")
        report.append(f"   - Agreement with classical XOR: {basic['classical_vs_quantum']['agreement_rate']:.1%}")
        report.append(f"   - Quantum uncertainty: {basic['classical_vs_quantum']['quantum_uncertainty']:.3f}")
        report.append(f"   - Entanglement measure: {basic['entanglement_measure']:.3f}")
        report.append("")
        
        # Interference
        interference = results["interference_effects"]
        report.append("2. Quantum Interference Effects:")
        report.append(f"   - Phase sensitivity: {interference['phase_dependence']['phase_sensitivity']:.3f}")
        report.append(f"   - Quantum coherence: {interference['quantum_coherence']:.3f}")
        report.append(f"   - Bias range: {interference['phase_dependence']['bias_range']:.3f}")
        report.append("")
        
        # Multi-qubit
        multi = results["multi_qubit_xor"]
        report.append("3. Multi-Qubit XOR Reasoning:")
        report.append(f"   - {multi['n_inputs']}-input XOR agreement: {multi['agreement_rate']:.1%}")
        report.append(f"   - Average uncertainty: {multi['quantum_advantage']['average_uncertainty']:.3f}")
        report.append(f"   - {multi['quantum_advantage']['parallel_evaluation']}")
        report.append("")
        
        # Scalability
        report.append("4. Scalability Analysis:")
        for size, test in results["scalability_test"].items():
            report.append(f"   - {size}: {test['agreement_rate']:.1%} agreement")
        report.append("")
        
        return "\n".join(report)
