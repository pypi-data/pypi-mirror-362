"""
Quantum Bayesian Network implementation.

This module provides the main QuantumBayesianNetwork class that combines
quantum and classical probabilistic reasoning in a unified graph structure.
"""

import numpy as np
import networkx as nx
from typing import (
    Dict, List, Any, Optional, Set, Tuple, Union, 
    Callable, Type, Iterator
)
from collections import defaultdict, deque
import logging
from dataclasses import dataclass
import uuid

from .nodes import (
    BaseNode, QuantumNode, StochasticNode, HybridNode, 
    DeterministicNode, NodeType, create_node
)
from .operators import (
    QuantumState, UnitaryOperator, CNOTOperator, HadamardOperator,
    ComputationalBasisMeasurement
)
from .exceptions import (
    NetworkTopologyError, QuantumStateError, InferenceError
)

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class InferenceResult:
    """Results from quantum-classical inference."""
    
    marginal_probabilities: Dict[str, Dict[Any, float]]
    joint_probability: Optional[float] = None
    quantum_amplitudes: Optional[Dict[str, Dict[Any, complex]]] = None
    entanglement_measure: Optional[float] = None
    convergence_info: Optional[Dict[str, Any]] = None
    inference_time: Optional[float] = None


@dataclass
class NetworkStatistics:
    """Statistics about the quantum Bayesian network."""
    
    total_nodes: int
    quantum_nodes: int
    classical_nodes: int
    hybrid_nodes: int
    deterministic_nodes: int
    total_edges: int
    entangled_pairs: int
    max_parents: int
    max_children: int
    is_dag: bool
    has_cycles: bool


class QuantumBayesianNetwork:
    """
    A quantum-classical hybrid Bayesian network for probabilistic reasoning.
    
    This class implements a graph structure that combines quantum nodes
    (with amplitudes and superposition) and classical nodes (with probability
    distributions) to enable sophisticated uncertainty modeling and inference.
    """
    
    def __init__(
        self,
        name: str = "QuantumBayesianNetwork",
        backend: Optional[Any] = None
    ) -> None:
        """
        Initialize a quantum Bayesian network.
        
        Args:
            name: Name identifier for the network
            backend: Quantum computing backend (Qiskit, PennyLane, etc.)
        """
        self.name = name
        self.backend = backend
        
        # Graph structure
        self.graph = nx.DiGraph()
        self.nodes: Dict[str, BaseNode] = {}
        
        # Entanglement tracking
        self.entangled_groups: List[Set[str]] = []
        self.entanglement_matrix: Optional[np.ndarray] = None
        
        # Evidence and queries
        self.evidence: Dict[str, Any] = {}
        self.query_cache: Dict[str, InferenceResult] = {}
        
        # Network metadata
        self.metadata: Dict[str, Any] = {}
        self.creation_time = None
        self.last_modified = None
        
        logger.info(f"Initialized {self.name} with backend {type(backend).__name__ if backend else 'None'}")
    
    def add_node(
        self,
        node_id: str,
        node_type: Union[NodeType, str],
        name: Optional[str] = None,
        outcome_space: Optional[List[Any]] = None,
        **kwargs
    ) -> str:
        """
        Add a node to the network.
        
        Args:
            node_id: Unique identifier for the node
            node_type: Type of node (quantum, stochastic, hybrid, deterministic)
            name: Human-readable name for the node
            outcome_space: Possible outcomes for the random variable
            **kwargs: Additional parameters for node creation
            
        Returns:
            The node ID
            
        Raises:
            NetworkTopologyError: If node_id already exists or invalid parameters
        """
        if node_id in self.nodes:
            raise NetworkTopologyError(
                f"Node {node_id} already exists in network",
                node_id=node_id
            )
        
        if name is None:
            name = node_id
        
        if outcome_space is None:
            outcome_space = [0, 1]  # Binary by default
        
        # Create node
        node = create_node(node_type, node_id, name, outcome_space, **kwargs)
        
        # Add to network
        self.nodes[node_id] = node
        self.graph.add_node(node_id, node_type=node_type, **kwargs)
        
        # Clear cache since network structure changed
        self.query_cache.clear()
        
        logger.debug(f"Added {node_type} node {node_id} with outcomes {outcome_space}")
        return node_id
    
    def add_quantum_node(
        self,
        node_id: str,
        outcome_space: List[Any],
        name: Optional[str] = None,
        initial_amplitudes: Optional[np.ndarray] = None,
        **kwargs
    ) -> str:
        """Convenience method to add a quantum node."""
        if initial_amplitudes is not None:
            basis_labels = [str(outcome) for outcome in outcome_space]
            initial_state = QuantumState(initial_amplitudes, basis_labels)
            kwargs['initial_state'] = initial_state
        
        return self.add_node(node_id, NodeType.QUANTUM, name, outcome_space, **kwargs)
    
    def add_stochastic_node(
        self,
        node_id: str,
        outcome_space: List[Any],
        name: Optional[str] = None,
        prior_probabilities: Optional[np.ndarray] = None,
        **kwargs
    ) -> str:
        """Convenience method to add a classical stochastic node."""
        if prior_probabilities is not None:
            kwargs['prior_distribution'] = prior_probabilities
        
        return self.add_node(node_id, NodeType.STOCHASTIC, name, outcome_space, **kwargs)
    
    def add_hybrid_node(
        self,
        node_id: str,
        outcome_space: List[Any],
        name: Optional[str] = None,
        mixing_parameter: float = 0.5,
        **kwargs
    ) -> str:
        """Convenience method to add a hybrid quantum-classical node."""
        kwargs['mixing_parameter'] = mixing_parameter
        return self.add_node(node_id, NodeType.HYBRID, name, outcome_space, **kwargs)
    
    def remove_node(self, node_id: str) -> None:
        """
        Remove a node from the network.
        
        Args:
            node_id: ID of node to remove
            
        Raises:
            NetworkTopologyError: If node doesn't exist
        """
        if node_id not in self.nodes:
            raise NetworkTopologyError(
                f"Node {node_id} not found in network",
                node_id=node_id
            )
        
        # Remove from entanglement groups
        self._remove_from_entanglement_groups(node_id)
        
        # Remove edges
        parents = list(self.graph.predecessors(node_id))
        children = list(self.graph.successors(node_id))
        
        for parent in parents:
            self.remove_edge(parent, node_id)
        for child in children:
            self.remove_edge(node_id, child)
        
        # Remove node
        del self.nodes[node_id]
        self.graph.remove_node(node_id)
        
        # Clear evidence if set
        if node_id in self.evidence:
            del self.evidence[node_id]
        
        self.query_cache.clear()
        logger.debug(f"Removed node {node_id}")
    
    def add_edge(self, parent_id: str, child_id: str, **edge_attrs) -> None:
        """
        Add a directed edge (causal relationship) between nodes.
        
        Args:
            parent_id: ID of parent node
            child_id: ID of child node
            **edge_attrs: Additional edge attributes
            
        Raises:
            NetworkTopologyError: If nodes don't exist or edge creates cycle
        """
        if parent_id not in self.nodes:
            raise NetworkTopologyError(
                f"Parent node {parent_id} not found",
                node_id=parent_id
            )
        if child_id not in self.nodes:
            raise NetworkTopologyError(
                f"Child node {child_id} not found",
                node_id=child_id
            )
        
        # Check if edge would create cycle
        if self._would_create_cycle(parent_id, child_id):
            raise NetworkTopologyError(
                f"Adding edge {parent_id} -> {child_id} would create cycle",
                edge_info=(parent_id, child_id)
            )
        
        # Add edge to graph
        self.graph.add_edge(parent_id, child_id, **edge_attrs)
        
        # Update node parent/child relationships
        self.nodes[parent_id].add_child(child_id)
        self.nodes[child_id].add_parent(parent_id)
        
        self.query_cache.clear()
        logger.debug(f"Added edge {parent_id} -> {child_id}")
    
    def remove_edge(self, parent_id: str, child_id: str) -> None:
        """Remove edge between nodes."""
        if not self.graph.has_edge(parent_id, child_id):
            raise NetworkTopologyError(
                f"Edge {parent_id} -> {child_id} does not exist",
                edge_info=(parent_id, child_id)
            )
        
        self.graph.remove_edge(parent_id, child_id)
        self.nodes[parent_id].remove_child(child_id)
        self.nodes[child_id].remove_parent(parent_id)
        
        self.query_cache.clear()
        logger.debug(f"Removed edge {parent_id} -> {child_id}")
    
    def entangle(self, node_ids: List[str]) -> None:
        """
        Create quantum entanglement between specified nodes.
        
        Args:
            node_ids: List of node IDs to entangle
            
        Raises:
            NetworkTopologyError: If nodes are not quantum nodes
        """
        if len(node_ids) < 2:
            raise NetworkTopologyError("Need at least 2 nodes for entanglement")
        
        # Verify all nodes are quantum or hybrid
        for node_id in node_ids:
            if node_id not in self.nodes:
                raise NetworkTopologyError(f"Node {node_id} not found")
            
            node = self.nodes[node_id]
            if not isinstance(node, (QuantumNode, HybridNode)):
                raise NetworkTopologyError(
                    f"Node {node_id} is not a quantum node",
                    node_id=node_id
                )
        
        # Create entanglement group
        entangled_set = set(node_ids)
        
        # Merge with existing entanglement groups if overlap
        groups_to_merge = []
        for i, group in enumerate(self.entangled_groups):
            if group.intersection(entangled_set):
                groups_to_merge.append(i)
        
        # Merge groups
        if groups_to_merge:
            merged_group = entangled_set
            for i in sorted(groups_to_merge, reverse=True):
                merged_group.update(self.entangled_groups.pop(i))
            self.entangled_groups.append(merged_group)
        else:
            self.entangled_groups.append(entangled_set)
        
        # Update individual node entanglement info
        for node_id in node_ids:
            node = self.nodes[node_id]
            if isinstance(node, QuantumNode):
                for other_id in node_ids:
                    if other_id != node_id:
                        node.entangle_with(other_id)
        
        self.query_cache.clear()
        logger.info(f"Entangled nodes: {node_ids}")
    
    def set_evidence(self, evidence: Dict[str, Any]) -> None:
        """
        Set evidence (observations) for nodes.
        
        Args:
            evidence: Dictionary mapping node IDs to observed values
        """
        for node_id, value in evidence.items():
            if node_id not in self.nodes:
                raise NetworkTopologyError(f"Node {node_id} not found")
            
            self.nodes[node_id].set_evidence(value)
            self.evidence[node_id] = value
        
        self.query_cache.clear()
        logger.debug(f"Set evidence: {evidence}")
    
    def clear_evidence(self, node_ids: Optional[List[str]] = None) -> None:
        """Clear evidence from specified nodes or all nodes."""
        if node_ids is None:
            node_ids = list(self.evidence.keys())
        
        for node_id in node_ids:
            if node_id in self.nodes:
                self.nodes[node_id].clear_evidence()
            if node_id in self.evidence:
                del self.evidence[node_id]
        
        self.query_cache.clear()
    
    def infer(
        self,
        query_nodes: Optional[List[str]] = None,
        evidence: Optional[Dict[str, Any]] = None,
        algorithm: str = "belief_propagation",
        **kwargs
    ) -> InferenceResult:
        """
        Perform probabilistic inference on the network.
        
        Args:
            query_nodes: Nodes to compute marginals for (all if None)
            evidence: Evidence to condition on
            algorithm: Inference algorithm to use
            **kwargs: Algorithm-specific parameters
            
        Returns:
            InferenceResult with marginal probabilities and metadata
        """
        # Set evidence if provided
        if evidence:
            self.set_evidence(evidence)
        
        if query_nodes is None:
            query_nodes = list(self.nodes.keys())
        
        # Create cache key
        cache_key = self._create_cache_key(query_nodes, self.evidence, algorithm)
        
        if cache_key in self.query_cache:
            logger.debug("Returning cached inference result")
            return self.query_cache[cache_key]
        
        # Import inference engine (avoid circular import)
        from ..inference.engine import QuantumInferenceEngine
        
        # Create inference engine
        engine = QuantumInferenceEngine(self, backend=self.backend)
        
        # Perform inference
        try:
            result = engine.infer(query_nodes, algorithm, **kwargs)
            self.query_cache[cache_key] = result
            return result
        except Exception as e:
            raise InferenceError(
                f"Inference failed: {str(e)}",
                algorithm=algorithm,
                query_nodes=query_nodes
            )
    
    def intervene(
        self,
        interventions: Dict[str, Any],
        query_nodes: Optional[List[str]] = None,
        **kwargs
    ) -> InferenceResult:
        """
        Perform causal intervention (do-calculus).
        
        Args:
            interventions: Dictionary of node_id -> intervention_value
            query_nodes: Nodes to query after intervention
            **kwargs: Additional parameters
            
        Returns:
            InferenceResult after intervention
        """
        # Import causal inference engine
        from ..inference.causal import QuantumCausalInference
        
        causal_engine = QuantumCausalInference(self, backend=self.backend)
        return causal_engine.do_calculus(interventions, query_nodes, **kwargs)
    
    def sample(
        self,
        n_samples: int = 1000,
        evidence: Optional[Dict[str, Any]] = None,
        method: str = "forward"
    ) -> List[Dict[str, Any]]:
        """
        Generate samples from the network.
        
        Args:
            n_samples: Number of samples to generate
            evidence: Evidence to condition on
            method: Sampling method ('forward', 'gibbs', 'quantum')
            
        Returns:
            List of sample dictionaries
        """
        if evidence:
            self.set_evidence(evidence)
        
        samples = []
        
        for _ in range(n_samples):
            sample = {}
            
            # Topological ordering for forward sampling
            if method == "forward":
                for node_id in nx.topological_sort(self.graph):
                    node = self.nodes[node_id]
                    
                    if node.is_evidence:
                        sample[node_id] = node.observed_value
                    else:
                        parent_values = {pid: sample[pid] for pid in node.parents if pid in sample}
                        sample[node_id] = node.sample(parent_values)
            
            samples.append(sample)
        
        return samples
    
    def collapse(self, node_id: str) -> Any:
        """
        Collapse a quantum node by measurement.
        
        Args:
            node_id: ID of quantum node to collapse
            
        Returns:
            Measured value
        """
        if node_id not in self.nodes:
            raise NetworkTopologyError(f"Node {node_id} not found")
        
        node = self.nodes[node_id]
        if not isinstance(node, (QuantumNode, HybridNode)):
            raise NetworkTopologyError(f"Node {node_id} is not quantum")
        
        # Perform measurement
        measured_value = node.sample()
        
        # Set as evidence
        self.set_evidence({node_id: measured_value})
        
        logger.info(f"Collapsed node {node_id} to value {measured_value}")
        return measured_value
    
    def get_statistics(self) -> NetworkStatistics:
        """Get network statistics."""
        node_counts = defaultdict(int)
        for node in self.nodes.values():
            node_counts[node.node_type] += 1
        
        return NetworkStatistics(
            total_nodes=len(self.nodes),
            quantum_nodes=node_counts[NodeType.QUANTUM],
            classical_nodes=node_counts[NodeType.STOCHASTIC],
            hybrid_nodes=node_counts[NodeType.HYBRID],
            deterministic_nodes=node_counts[NodeType.DETERMINISTIC],
            total_edges=len(self.graph.edges),
            entangled_pairs=sum(len(group) * (len(group) - 1) // 2 for group in self.entangled_groups),
            max_parents=max((len(node.parents) for node in self.nodes.values()), default=0),
            max_children=max((len(node.children) for node in self.nodes.values()), default=0),
            is_dag=nx.is_directed_acyclic_graph(self.graph),
            has_cycles=not nx.is_directed_acyclic_graph(self.graph)
        )
    
    def validate(self) -> List[str]:
        """
        Validate network structure and return list of issues.
        
        Returns:
            List of validation issues (empty if valid)
        """
        issues = []
        
        # Check DAG property
        if not nx.is_directed_acyclic_graph(self.graph):
            issues.append("Network contains cycles")
        
        # Check node consistency
        for node_id, node in self.nodes.items():
            # Check parent consistency
            graph_parents = set(self.graph.predecessors(node_id))
            node_parents = node.parents
            if graph_parents != node_parents:
                issues.append(f"Node {node_id} parent mismatch")
            
            # Check child consistency
            graph_children = set(self.graph.successors(node_id))
            node_children = node.children
            if graph_children != node_children:
                issues.append(f"Node {node_id} child mismatch")
        
        # Check entanglement consistency
        for group in self.entangled_groups:
            for node_id in group:
                if node_id not in self.nodes:
                    issues.append(f"Entangled node {node_id} not in network")
                elif not isinstance(self.nodes[node_id], (QuantumNode, HybridNode)):
                    issues.append(f"Non-quantum node {node_id} in entanglement group")
        
        return issues
    
    def explain_pathway(
        self,
        source: str,
        target: str,
        evidence: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Explain reasoning pathway from source to target node.
        
        Args:
            source: Source node ID
            target: Target node ID
            evidence: Evidence context
            
        Returns:
            Explanation dictionary with pathway information
        """
        if evidence:
            self.set_evidence(evidence)
        
        # Find all paths
        try:
            paths = list(nx.all_simple_paths(self.graph, source, target))
        except nx.NetworkXNoPath:
            paths = []
        
        explanation = {
            "source": source,
            "target": target,
            "direct_connection": self.graph.has_edge(source, target),
            "paths": paths,
            "path_count": len(paths),
            "evidence": self.evidence.copy(),
            "entanglement_groups": [
                list(group) for group in self.entangled_groups
                if source in group or target in group
            ]
        }
        
        # Add influence analysis
        if paths:
            explanation["shortest_path"] = min(paths, key=len)
            explanation["longest_path"] = max(paths, key=len)
        
        return explanation
    
    def _would_create_cycle(self, parent_id: str, child_id: str) -> bool:
        """Check if adding edge would create cycle."""
        # Temporarily add edge and check for cycles
        temp_graph = self.graph.copy()
        temp_graph.add_edge(parent_id, child_id)
        return not nx.is_directed_acyclic_graph(temp_graph)
    
    def _remove_from_entanglement_groups(self, node_id: str) -> None:
        """Remove node from entanglement groups."""
        groups_to_remove = []
        for i, group in enumerate(self.entangled_groups):
            if node_id in group:
                group.remove(node_id)
                if len(group) < 2:
                    groups_to_remove.append(i)
        
        for i in sorted(groups_to_remove, reverse=True):
            del self.entangled_groups[i]
    
    def _create_cache_key(
        self,
        query_nodes: List[str],
        evidence: Dict[str, Any],
        algorithm: str
    ) -> str:
        """Create cache key for inference results."""
        key_parts = [
            f"query:{','.join(sorted(query_nodes))}",
            f"evidence:{','.join(f'{k}={v}' for k, v in sorted(evidence.items()))}",
            f"algorithm:{algorithm}"
        ]
        return "|".join(key_parts)
    
    def __repr__(self) -> str:
        stats = self.get_statistics()
        return (
            f"QuantumBayesianNetwork(name='{self.name}', "
            f"nodes={stats.total_nodes}, edges={stats.total_edges}, "
            f"quantum={stats.quantum_nodes}, classical={stats.classical_nodes})"
        )
