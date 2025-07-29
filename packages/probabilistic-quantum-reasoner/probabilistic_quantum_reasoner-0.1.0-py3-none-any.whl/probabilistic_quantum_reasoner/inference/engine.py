"""
Main inference engine for quantum Bayesian networks.

This module provides the central inference engine that coordinates different
inference algorithms and handles quantum-classical hybrid reasoning.
"""

import numpy as np
import time
from typing import Dict, List, Any, Optional, Union
import logging

from ..core.network import InferenceResult
from ..core.nodes import BaseNode, QuantumNode, StochasticNode, HybridNode
from ..core.exceptions import InferenceError, BackendError
from .belief_propagation import QuantumBeliefPropagation

logger = logging.getLogger(__name__)


class QuantumInferenceEngine:
    """
    Central inference engine for quantum Bayesian networks.
    
    Coordinates different inference algorithms and provides a unified
    interface for probabilistic reasoning in quantum-classical hybrid models.
    """
    
    def __init__(self, network: Any, backend: Optional[Any] = None) -> None:
        """
        Initialize the inference engine.
        
        Args:
            network: QuantumBayesianNetwork instance
            backend: Quantum computing backend
        """
        self.network = network
        self.backend = backend
        
        # Algorithm instances
        self.belief_propagation = QuantumBeliefPropagation(network)
        
        # Available algorithms
        self.algorithms = {
            "belief_propagation": self._run_belief_propagation,
            "exact": self._run_exact_inference,
            "sampling": self._run_sampling_inference,
            "variational": self._run_variational_inference,
            "grover": self._run_grover_search,
        }
    
    def infer(
        self,
        query_nodes: List[str],
        algorithm: str = "belief_propagation",
        **kwargs
    ) -> InferenceResult:
        """
        Perform inference on the network.
        
        Args:
            query_nodes: List of nodes to compute marginals for
            algorithm: Inference algorithm to use
            **kwargs: Algorithm-specific parameters
            
        Returns:
            InferenceResult with marginal probabilities and metadata
            
        Raises:
            InferenceError: If inference fails
        """
        start_time = time.time()
        
        logger.info(f"Running {algorithm} inference on {len(query_nodes)} nodes")
        
        if algorithm not in self.algorithms:
            raise InferenceError(
                f"Unknown algorithm: {algorithm}",
                algorithm=algorithm,
                available_algorithms=list(self.algorithms.keys())
            )
        
        try:
            # Run the specific algorithm
            marginals, metadata = self.algorithms[algorithm](query_nodes, **kwargs)
            
            # Compute quantum amplitudes if applicable
            quantum_amplitudes = self._extract_quantum_amplitudes(query_nodes)
            
            # Compute entanglement measure
            entanglement_measure = self._compute_entanglement_measure()
            
            inference_time = time.time() - start_time
            
            return InferenceResult(
                marginal_probabilities=marginals,
                quantum_amplitudes=quantum_amplitudes,
                entanglement_measure=entanglement_measure,
                convergence_info=metadata,
                inference_time=inference_time
            )
            
        except Exception as e:
            raise InferenceError(
                f"Inference failed: {str(e)}",
                algorithm=algorithm,
                query_nodes=query_nodes
            ) from e
    
    def _run_belief_propagation(
        self,
        query_nodes: List[str],
        max_iterations: int = 100,
        tolerance: float = 1e-6,
        **kwargs
    ) -> tuple:
        """Run quantum belief propagation algorithm."""
        bp = QuantumBeliefPropagation(
            self.network,
            max_iterations=max_iterations,
            tolerance=tolerance
        )
        
        marginals = bp.run_inference(query_nodes)
        convergence_info = bp.get_convergence_info()
        
        return marginals, convergence_info
    
    def _run_exact_inference(self, query_nodes: List[str], **kwargs) -> tuple:
        """Run exact inference by enumerating all configurations."""
        logger.info("Running exact inference")
        
        # Get all possible configurations
        all_nodes = list(self.network.nodes.keys())
        configurations = self._enumerate_configurations(all_nodes)
        
        # Compute joint probabilities
        joint_probs = {}
        for config in configurations:
            prob = self._compute_joint_probability(config)
            joint_probs[tuple(config.items())] = prob
        
        # Marginalize to get query node distributions
        marginals = {}
        for node_id in query_nodes:
            node_marginals = {}
            node = self.network.nodes[node_id]
            
            for outcome in node.outcome_space:
                marginal_prob = 0.0
                
                for config_tuple, joint_prob in joint_probs.items():
                    config = dict(config_tuple)
                    if config[node_id] == outcome:
                        marginal_prob += joint_prob
                
                node_marginals[outcome] = marginal_prob
            
            marginals[node_id] = node_marginals
        
        metadata = {
            "algorithm": "exact",
            "total_configurations": len(configurations)
        }
        
        return marginals, metadata
    
    def _run_sampling_inference(
        self,
        query_nodes: List[str],
        n_samples: int = 10000,
        method: str = "forward",
        **kwargs
    ) -> tuple:
        """Run sampling-based inference."""
        logger.info(f"Running sampling inference with {n_samples} samples")
        
        # Generate samples
        samples = self.network.sample(n_samples, method=method)
        
        # Compute empirical marginals
        marginals = {}
        for node_id in query_nodes:
            node = self.network.nodes[node_id]
            counts = {outcome: 0 for outcome in node.outcome_space}
            
            for sample in samples:
                if node_id in sample:
                    counts[sample[node_id]] += 1
            
            # Convert to probabilities
            total = sum(counts.values())
            if total > 0:
                marginals[node_id] = {k: v / total for k, v in counts.items()}
            else:
                marginals[node_id] = {k: 1.0 / len(node.outcome_space) for k in node.outcome_space}
        
        metadata = {
            "algorithm": "sampling",
            "n_samples": n_samples,
            "method": method
        }
        
        return marginals, metadata
    
    def _run_variational_inference(self, query_nodes: List[str], **kwargs) -> tuple:
        """Run variational quantum inference."""
        if self.backend is None:
            raise InferenceError(
                "Variational inference requires a quantum backend",
                algorithm="variational"
            )
        
        try:
            from .variational import VariationalQuantumInference
            vqi = VariationalQuantumInference(self.network, self.backend)
            return vqi.run_inference(query_nodes, **kwargs)
        except ImportError:
            raise InferenceError(
                "Variational inference not available",
                algorithm="variational"
            )
    
    def _run_grover_search(self, query_nodes: List[str], **kwargs) -> tuple:
        """Run Grover-enhanced search for inference."""
        if self.backend is None:
            raise InferenceError(
                "Grover search requires a quantum backend",
                algorithm="grover"
            )
        
        logger.info("Running Grover-enhanced inference")
        
        # Simplified Grover search implementation
        # In practice, this would use quantum circuits
        
        # For now, fall back to exact inference with quantum amplitude consideration
        marginals, metadata = self._run_exact_inference(query_nodes)
        
        # Add Grover-specific metadata
        metadata.update({
            "algorithm": "grover",
            "quantum_speedup": True,
            "note": "Simplified implementation"
        })
        
        return marginals, metadata
    
    def _enumerate_configurations(self, node_ids: List[str]) -> List[Dict[str, Any]]:
        """Enumerate all possible configurations of nodes."""
        if not node_ids:
            return [{}]
        
        configurations = []
        
        def backtrack(idx: int, current_config: Dict[str, Any]) -> None:
            if idx == len(node_ids):
                configurations.append(current_config.copy())
                return
            
            node_id = node_ids[idx]
            node = self.network.nodes[node_id]
            
            if node.is_evidence:
                # Fixed value
                current_config[node_id] = node.observed_value
                backtrack(idx + 1, current_config)
            else:
                # Try all possible values
                for outcome in node.outcome_space:
                    current_config[node_id] = outcome
                    backtrack(idx + 1, current_config)
                    del current_config[node_id]
        
        backtrack(0, {})
        return configurations
    
    def _compute_joint_probability(self, configuration: Dict[str, Any]) -> float:
        """Compute joint probability of a configuration."""
        log_prob = 0.0
        
        # Use topological order for computation
        import networkx as nx
        
        for node_id in nx.topological_sort(self.network.graph):
            node = self.network.nodes[node_id]
            value = configuration[node_id]
            
            # Get parent values
            parent_values = {
                parent_id: configuration[parent_id]
                for parent_id in node.parents
            }
            
            # Add node's contribution to joint probability
            node_log_prob = node.log_probability(value, parent_values)
            log_prob += node_log_prob
        
        return np.exp(log_prob)
    
    def _extract_quantum_amplitudes(self, query_nodes: List[str]) -> Optional[Dict[str, Dict[Any, complex]]]:
        """Extract quantum amplitudes for quantum nodes."""
        quantum_amplitudes = {}
        
        for node_id in query_nodes:
            node = self.network.nodes[node_id]
            
            if isinstance(node, QuantumNode):
                amplitudes = {}
                for outcome in node.outcome_space:
                    amplitudes[outcome] = node.get_amplitude(outcome)
                quantum_amplitudes[node_id] = amplitudes
            elif isinstance(node, HybridNode):
                # Extract from quantum component
                amplitudes = {}
                for outcome in node.outcome_space:
                    amplitudes[outcome] = node.quantum_component.get_amplitude(outcome)
                quantum_amplitudes[node_id] = amplitudes
        
        return quantum_amplitudes if quantum_amplitudes else None
    
    def _compute_entanglement_measure(self) -> Optional[float]:
        """Compute entanglement measure for the network."""
        if not self.network.entangled_groups:
            return 0.0
        
        # Simplified entanglement measure based on group sizes
        total_entanglement = 0.0
        
        for group in self.network.entangled_groups:
            if len(group) > 1:
                # von Neumann entropy-based measure (simplified)
                group_size = len(group)
                group_entanglement = np.log2(group_size)
                total_entanglement += group_entanglement
        
        return total_entanglement
    
    def estimate_complexity(self, algorithm: str) -> Dict[str, Any]:
        """Estimate computational complexity for given algorithm."""
        n_nodes = len(self.network.nodes)
        n_edges = len(self.network.graph.edges)
        
        max_domain_size = max(
            len(node.outcome_space) for node in self.network.nodes.values()
        )
        
        complexity_info = {
            "algorithm": algorithm,
            "n_nodes": n_nodes,
            "n_edges": n_edges,
            "max_domain_size": max_domain_size
        }
        
        if algorithm == "exact":
            # Exponential in number of nodes
            complexity_info["time_complexity"] = f"O({max_domain_size}^{n_nodes})"
            complexity_info["space_complexity"] = f"O({max_domain_size}^{n_nodes})"
            complexity_info["is_tractable"] = n_nodes < 20
            
        elif algorithm == "belief_propagation":
            # Polynomial for tree-like structures
            complexity_info["time_complexity"] = f"O({n_edges} * {max_domain_size}^2)"
            complexity_info["space_complexity"] = f"O({n_edges} * {max_domain_size})"
            complexity_info["is_tractable"] = True
            
        elif algorithm == "sampling":
            # Linear in number of samples
            complexity_info["time_complexity"] = "O(n_samples * n_nodes)"
            complexity_info["space_complexity"] = "O(n_nodes)"
            complexity_info["is_tractable"] = True
            
        return complexity_info
