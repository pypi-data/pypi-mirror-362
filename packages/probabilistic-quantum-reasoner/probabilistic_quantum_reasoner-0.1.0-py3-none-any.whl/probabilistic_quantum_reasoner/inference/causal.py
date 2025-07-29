"""
Causal inference for quantum Bayesian networks.

This module implements quantum analogs of causal inference methods,
including do-calculus for quantum interventions and counterfactual reasoning.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Set
import logging
from copy import deepcopy

from ..core.network import InferenceResult
from ..core.nodes import BaseNode, QuantumNode, StochasticNode, HybridNode
from ..core.operators import UnitaryOperator, QuantumState
from ..core.exceptions import CausalInferenceError, NetworkTopologyError

logger = logging.getLogger(__name__)


class QuantumCausalInference:
    """
    Quantum causal inference engine.
    
    Implements quantum analogs of Pearl's causal hierarchy:
    1. Association (observation): P(Y|X)
    2. Intervention (action): P(Y|do(X))
    3. Counterfactuals: P(Y_x|X',Y')
    """
    
    def __init__(self, network: Any, backend: Optional[Any] = None) -> None:
        """
        Initialize quantum causal inference engine.
        
        Args:
            network: QuantumBayesianNetwork instance
            backend: Quantum computing backend
        """
        self.network = network
        self.backend = backend
        
        # Causal structure analysis
        self.causal_graph = None
        self.confounders: Dict[Tuple[str, str], Set[str]] = {}
        self.colliders: Set[str] = set()
        
        self._analyze_causal_structure()
    
    def do_calculus(
        self,
        interventions: Dict[str, Any],
        query_nodes: Optional[List[str]] = None,
        **kwargs
    ) -> InferenceResult:
        """
        Perform quantum do-calculus intervention.
        
        Args:
            interventions: Dictionary of node_id -> intervention_value
            query_nodes: Nodes to query after intervention
            **kwargs: Additional parameters
            
        Returns:
            InferenceResult after intervention
        """
        logger.info(f"Performing do-calculus intervention: {interventions}")
        
        if query_nodes is None:
            query_nodes = [
                node_id for node_id in self.network.nodes.keys()
                if node_id not in interventions
            ]
        
        # Create interventional network
        interventional_network = self._create_interventional_network(interventions)
        
        # Perform inference on interventional network
        from .engine import QuantumInferenceEngine
        engine = QuantumInferenceEngine(interventional_network, self.backend)
        
        result = engine.infer(query_nodes, **kwargs)
        
        # Add causal metadata
        if result.convergence_info is None:
            result.convergence_info = {}
        
        result.convergence_info.update({
            "causal_intervention": True,
            "interventions": interventions,
            "intervention_type": "do_calculus"
        })
        
        return result
    
    def counterfactual_query(
        self,
        factual_evidence: Dict[str, Any],
        counterfactual_interventions: Dict[str, Any],
        query_nodes: List[str],
        **kwargs
    ) -> InferenceResult:
        """
        Perform counterfactual query: P(Y_x | X', Y').
        
        Args:
            factual_evidence: Observed evidence in actual world
            counterfactual_interventions: Interventions in counterfactual world
            query_nodes: Nodes to query in counterfactual world
            
        Returns:
            Counterfactual inference result
        """
        logger.info(f"Counterfactual query with evidence {factual_evidence} and interventions {counterfactual_interventions}")
        
        # Step 1: Abduction - infer latent variables from evidence
        latent_distribution = self._abduction_step(factual_evidence)
        
        # Step 2: Action - apply interventions
        interventional_network = self._create_interventional_network(counterfactual_interventions)
        
        # Step 3: Prediction - predict in counterfactual world
        counterfactual_results = []
        
        for latent_config, prob in latent_distribution.items():
            # Set latent configuration
            self._set_latent_configuration(interventional_network, latent_config)
            
            # Perform inference
            from .engine import QuantumInferenceEngine
            engine = QuantumInferenceEngine(interventional_network, self.backend)
            result = engine.infer(query_nodes, **kwargs)
            
            counterfactual_results.append((result, prob))
        
        # Aggregate counterfactual results
        aggregated_result = self._aggregate_counterfactual_results(
            counterfactual_results, query_nodes
        )
        
        # Add counterfactual metadata
        if aggregated_result.convergence_info is None:
            aggregated_result.convergence_info = {}
        
        aggregated_result.convergence_info.update({
            "counterfactual_query": True,
            "factual_evidence": factual_evidence,
            "counterfactual_interventions": counterfactual_interventions,
            "n_latent_configurations": len(latent_distribution)
        })
        
        return aggregated_result
    
    def estimate_causal_effect(
        self,
        treatment: str,
        outcome: str,
        confounders: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Estimate causal effect of treatment on outcome.
        
        Args:
            treatment: Treatment variable
            outcome: Outcome variable
            confounders: List of confounding variables
            
        Returns:
            Dictionary with causal effect estimates
        """
        if confounders is None:
            confounders = self._identify_confounders(treatment, outcome)
        
        treatment_node = self.network.nodes[treatment]
        
        results = {}
        
        # Compute effect for each treatment value
        for treatment_value in treatment_node.outcome_space:
            # Interventional distribution
            interventional_result = self.do_calculus({treatment: treatment_value}, [outcome])
            
            results[f"P({outcome}|do({treatment}={treatment_value}))"] = \
                interventional_result.marginal_probabilities[outcome]
        
        # Compute average treatment effect if binary treatment
        if len(treatment_node.outcome_space) == 2:
            treat_0, treat_1 = treatment_node.outcome_space
            
            prob_0 = results[f"P({outcome}|do({treatment}={treat_0}))"]
            prob_1 = results[f"P({outcome}|do({treatment}={treat_1}))"]
            
            # Compute difference for each outcome value
            ate = {}
            for outcome_value in self.network.nodes[outcome].outcome_space:
                ate[outcome_value] = prob_1[outcome_value] - prob_0[outcome_value]
            
            results["average_treatment_effect"] = ate
        
        return results
    
    def _create_interventional_network(self, interventions: Dict[str, Any]) -> Any:
        """Create a copy of network with interventions applied."""
        # Create deep copy of network
        interventional_network = deepcopy(self.network)
        
        for node_id, intervention_value in interventions.items():
            if node_id not in interventional_network.nodes:
                raise CausalInferenceError(
                    f"Intervention node {node_id} not found",
                    intervention={node_id: intervention_value}
                )
            
            node = interventional_network.nodes[node_id]
            
            # Remove incoming edges (graphical surgery)
            parents = list(interventional_network.graph.predecessors(node_id))
            for parent in parents:
                interventional_network.remove_edge(parent, node_id)
            
            # Set intervention value as evidence
            if isinstance(node, QuantumNode):
                # For quantum nodes, create deterministic state
                intervention_idx = node.outcome_space.index(intervention_value)
                n_outcomes = len(node.outcome_space)
                
                new_amplitudes = np.zeros(n_outcomes, dtype=complex)
                new_amplitudes[intervention_idx] = 1.0
                
                node.quantum_state.amplitudes = new_amplitudes
                node.quantum_state.is_normalized = True
            
            # Set as evidence
            node.set_evidence(intervention_value)
        
        return interventional_network
    
    def _analyze_causal_structure(self) -> None:
        """Analyze causal structure of the network."""
        import networkx as nx
        
        # Identify colliders (nodes with multiple parents)
        for node_id in self.network.nodes:
            parents = list(self.network.graph.predecessors(node_id))
            if len(parents) > 1:
                self.colliders.add(node_id)
        
        # Identify confounders for each pair of nodes
        for node1 in self.network.nodes:
            for node2 in self.network.nodes:
                if node1 != node2:
                    confounders = self._find_confounders(node1, node2)
                    if confounders:
                        self.confounders[(node1, node2)] = confounders
    
    def _find_confounders(self, node1: str, node2: str) -> Set[str]:
        """Find confounders between two nodes."""
        import networkx as nx
        
        confounders = set()
        
        # A confounder has paths to both nodes
        for candidate in self.network.nodes:
            if candidate in {node1, node2}:
                continue
            
            try:
                # Check if there are paths to both nodes
                has_path_to_1 = nx.has_path(self.network.graph, candidate, node1)
                has_path_to_2 = nx.has_path(self.network.graph, candidate, node2)
                
                if has_path_to_1 and has_path_to_2:
                    confounders.add(candidate)
            except nx.NetworkXNoPath:
                continue
        
        return confounders
    
    def _identify_confounders(self, treatment: str, outcome: str) -> List[str]:
        """Identify confounders for causal effect estimation."""
        confounders = self.confounders.get((treatment, outcome), set())
        return list(confounders)
    
    def _abduction_step(self, evidence: Dict[str, Any]) -> Dict[tuple, float]:
        """
        Abduction step for counterfactual reasoning.
        
        Infer distribution over latent (unobserved) variables given evidence.
        """
        # Simplified abduction - in practice would use more sophisticated methods
        
        # Set evidence
        original_evidence = self.network.evidence.copy()
        self.network.set_evidence(evidence)
        
        # Identify latent variables (nodes without evidence)
        latent_nodes = [
            node_id for node_id in self.network.nodes.keys()
            if node_id not in evidence
        ]
        
        # Generate possible latent configurations
        latent_configs = self._enumerate_latent_configurations(latent_nodes)
        
        # Compute posterior distribution over latent configurations
        latent_distribution = {}
        
        for config in latent_configs:
            # Compute probability of this latent configuration given evidence
            full_config = {**evidence, **config}
            joint_prob = self._compute_joint_probability(full_config)
            
            if joint_prob > 0:
                latent_distribution[tuple(config.items())] = joint_prob
        
        # Normalize
        total_prob = sum(latent_distribution.values())
        if total_prob > 0:
            latent_distribution = {
                k: v / total_prob for k, v in latent_distribution.items()
            }
        
        # Restore original evidence
        self.network.clear_evidence()
        self.network.set_evidence(original_evidence)
        
        return latent_distribution
    
    def _enumerate_latent_configurations(self, latent_nodes: List[str]) -> List[Dict[str, Any]]:
        """Enumerate possible configurations of latent variables."""
        if not latent_nodes:
            return [{}]
        
        configs = []
        
        def backtrack(idx: int, current_config: Dict[str, Any]) -> None:
            if idx == len(latent_nodes):
                configs.append(current_config.copy())
                return
            
            node_id = latent_nodes[idx]
            node = self.network.nodes[node_id]
            
            for outcome in node.outcome_space:
                current_config[node_id] = outcome
                backtrack(idx + 1, current_config)
                del current_config[node_id]
        
        backtrack(0, {})
        return configs
    
    def _compute_joint_probability(self, configuration: Dict[str, Any]) -> float:
        """Compute joint probability of configuration."""
        # Reuse implementation from inference engine
        from .engine import QuantumInferenceEngine
        engine = QuantumInferenceEngine(self.network, self.backend)
        return engine._compute_joint_probability(configuration)
    
    def _set_latent_configuration(self, network: Any, latent_config: tuple) -> None:
        """Set latent variable configuration in network."""
        config_dict = dict(latent_config)
        
        for node_id, value in config_dict.items():
            if node_id in network.nodes:
                network.nodes[node_id].set_evidence(value)
    
    def _aggregate_counterfactual_results(
        self,
        results: List[Tuple[InferenceResult, float]],
        query_nodes: List[str]
    ) -> InferenceResult:
        """Aggregate results from multiple counterfactual worlds."""
        # Initialize aggregated marginals
        aggregated_marginals = {}
        
        for node_id in query_nodes:
            aggregated_marginals[node_id] = {}
        
        # Weighted average over counterfactual worlds
        for result, weight in results:
            for node_id in query_nodes:
                if node_id in result.marginal_probabilities:
                    node_marginals = result.marginal_probabilities[node_id]
                    
                    for outcome, prob in node_marginals.items():
                        if outcome not in aggregated_marginals[node_id]:
                            aggregated_marginals[node_id][outcome] = 0.0
                        
                        aggregated_marginals[node_id][outcome] += weight * prob
        
        # Create aggregated result
        return InferenceResult(
            marginal_probabilities=aggregated_marginals,
            joint_probability=None,
            quantum_amplitudes=None,
            entanglement_measure=None,
            convergence_info={"aggregated_counterfactual": True}
        )
    
    def is_identifiable(self, treatment: str, outcome: str) -> bool:
        """Check if causal effect is identifiable from observational data."""
        # Simplified identifiability check
        # In practice, would implement back-door criterion, front-door criterion, etc.
        
        confounders = self._identify_confounders(treatment, outcome)
        
        # If we can observe all confounders, effect is identifiable
        return len(confounders) == 0 or all(
            confounder not in self.network.evidence for confounder in confounders
        )
