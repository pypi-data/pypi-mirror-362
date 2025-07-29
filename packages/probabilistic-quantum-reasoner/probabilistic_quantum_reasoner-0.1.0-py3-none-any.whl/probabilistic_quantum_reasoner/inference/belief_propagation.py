"""
Quantum belief propagation for inference in quantum Bayesian networks.

This module implements quantum belief propagation algorithm that extends
classical belief propagation to handle quantum amplitudes and entanglement.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
import logging
from collections import defaultdict

from ..core.nodes import BaseNode, QuantumNode, StochasticNode, HybridNode
from ..core.operators import QuantumState, UnitaryOperator
from ..core.exceptions import InferenceError

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """Message passed between nodes in belief propagation."""
    
    sender: str
    receiver: str
    data: Dict[Any, complex]  # outcome -> amplitude/probability
    is_quantum: bool
    iteration: int
    
    def normalize(self) -> None:
        """Normalize message data."""
        if self.is_quantum:
            # Normalize amplitudes
            total_amplitude_squared = sum(abs(amp) ** 2 for amp in self.data.values())
            if total_amplitude_squared > 0:
                norm_factor = np.sqrt(total_amplitude_squared)
                self.data = {k: v / norm_factor for k, v in self.data.items()}
        else:
            # Normalize probabilities
            total_prob = sum(abs(p) for p in self.data.values())
            if total_prob > 0:
                self.data = {k: abs(v) / total_prob for k, v in self.data.items()}
    
    def to_probabilities(self) -> Dict[Any, float]:
        """Convert message to probability distribution."""
        if self.is_quantum:
            return {k: abs(v) ** 2 for k, v in self.data.items()}
        else:
            return {k: abs(v) for k, v in self.data.items()}


class QuantumBeliefPropagation:
    """
    Quantum belief propagation algorithm for inference.
    
    Extends classical belief propagation to handle quantum amplitudes,
    superposition, and entanglement in hybrid probabilistic networks.
    """
    
    def __init__(self, network: Any, max_iterations: int = 100, tolerance: float = 1e-6) -> None:
        """
        Initialize quantum belief propagation.
        
        Args:
            network: QuantumBayesianNetwork instance
            max_iterations: Maximum number of iterations
            tolerance: Convergence tolerance
        """
        self.network = network
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        
        # Message storage
        self.messages: Dict[Tuple[str, str], Message] = {}
        self.beliefs: Dict[str, Dict[Any, complex]] = {}
        
        # Convergence tracking
        self.iteration = 0
        self.converged = False
        self.convergence_history: List[float] = []
    
    def run_inference(
        self,
        query_nodes: Optional[List[str]] = None,
        evidence: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Dict[Any, float]]:
        """
        Run quantum belief propagation inference.
        
        Args:
            query_nodes: Nodes to compute beliefs for
            evidence: Evidence to condition on
            
        Returns:
            Dictionary mapping node IDs to probability distributions
        """
        if query_nodes is None:
            query_nodes = list(self.network.nodes.keys())
        
        if evidence:
            self.network.set_evidence(evidence)
        
        logger.info(f"Starting quantum belief propagation for {len(query_nodes)} query nodes")
        
        # Initialize messages
        self._initialize_messages()
        
        # Run iterative message passing
        for self.iteration in range(self.max_iterations):
            logger.debug(f"Belief propagation iteration {self.iteration + 1}")
            
            old_messages = self._copy_messages()
            self._update_messages()
            
            # Check convergence
            convergence_error = self._compute_convergence_error(old_messages)
            self.convergence_history.append(convergence_error)
            
            if convergence_error < self.tolerance:
                self.converged = True
                logger.info(f"Converged after {self.iteration + 1} iterations")
                break
        else:
            logger.warning(f"Did not converge after {self.max_iterations} iterations")
        
        # Compute final beliefs
        self._compute_beliefs()
        
        # Convert to probability distributions
        result = {}
        for node_id in query_nodes:
            if node_id in self.beliefs:
                if self._is_quantum_node(node_id):
                    # Convert amplitudes to probabilities (Born rule)
                    probs = {k: abs(v) ** 2 for k, v in self.beliefs[node_id].items()}
                else:
                    # Already probabilities
                    probs = {k: abs(v) for k, v in self.beliefs[node_id].items()}
                
                # Normalize
                total = sum(probs.values())
                if total > 0:
                    probs = {k: v / total for k, v in probs.items()}
                
                result[node_id] = probs
        
        return result
    
    def _initialize_messages(self) -> None:
        """Initialize all messages in the network."""
        self.messages.clear()
        
        for edge in self.network.graph.edges():
            parent_id, child_id = edge
            
            # Initialize parent -> child message
            self._initialize_message(parent_id, child_id)
            
            # Initialize child -> parent message (for undirected communication)
            self._initialize_message(child_id, parent_id)
    
    def _initialize_message(self, sender: str, receiver: str) -> None:
        """Initialize a single message."""
        sender_node = self.network.nodes[sender]
        is_quantum = isinstance(sender_node, (QuantumNode, HybridNode))
        
        # Initialize uniform message
        outcome_space = sender_node.outcome_space
        
        if is_quantum:
            # Initialize with uniform amplitudes
            n_outcomes = len(outcome_space)
            uniform_amplitude = 1.0 / np.sqrt(n_outcomes)
            data = {outcome: uniform_amplitude for outcome in outcome_space}
        else:
            # Initialize with uniform probabilities
            uniform_prob = 1.0 / len(outcome_space)
            data = {outcome: uniform_prob for outcome in outcome_space}
        
        message = Message(
            sender=sender,
            receiver=receiver,
            data=data,
            is_quantum=is_quantum,
            iteration=0
        )
        
        self.messages[(sender, receiver)] = message
    
    def _update_messages(self) -> None:
        """Update all messages in one iteration."""
        # Update messages in random order to avoid bias
        edges = list(self.network.graph.edges())
        np.random.shuffle(edges)
        
        for parent_id, child_id in edges:
            self._update_message(parent_id, child_id)
            self._update_message(child_id, parent_id)
    
    def _update_message(self, sender: str, receiver: str) -> None:
        """Update a single message from sender to receiver."""
        sender_node = self.network.nodes[sender]
        receiver_node = self.network.nodes[receiver]
        
        # Collect incoming messages to sender (except from receiver)
        incoming_messages = []
        for neighbor in self.network.graph.neighbors(sender):
            if neighbor != receiver and (neighbor, sender) in self.messages:
                incoming_messages.append(self.messages[(neighbor, sender)])
        
        # Compute new message
        new_data = {}
        
        for outcome in sender_node.outcome_space:
            if sender_node.is_evidence and outcome != sender_node.observed_value:
                # Evidence constraint
                new_data[outcome] = 0.0
                continue
            
            # Aggregate incoming messages
            incoming_factor = 1.0
            for msg in incoming_messages:
                if outcome in msg.data:
                    incoming_factor *= msg.data[outcome]
            
            # Apply node's local factor
            if isinstance(sender_node, QuantumNode):
                # Quantum amplitude
                amplitude = sender_node.get_amplitude(outcome)
                new_data[outcome] = amplitude * incoming_factor
            elif isinstance(sender_node, StochasticNode):
                # Classical probability
                if not sender_node.parents:  # Root node
                    prob = sender_node.prior_distribution[sender_node.outcome_space.index(outcome)]
                else:
                    # Would need parent values - simplified for now
                    prob = 1.0 / len(sender_node.outcome_space)
                new_data[outcome] = prob * incoming_factor
            elif isinstance(sender_node, HybridNode):
                # Hybrid: combine quantum and classical
                quantum_amp = sender_node.quantum_component.get_amplitude(outcome)
                classical_prob = 1.0 / len(sender_node.outcome_space)  # Simplified
                
                mixed_value = (
                    sender_node.mixing_parameter * quantum_amp +
                    (1 - sender_node.mixing_parameter) * classical_prob
                )
                new_data[outcome] = mixed_value * incoming_factor
        
        # Create and normalize new message
        is_quantum = isinstance(sender_node, (QuantumNode, HybridNode))
        new_message = Message(
            sender=sender,
            receiver=receiver,
            data=new_data,
            is_quantum=is_quantum,
            iteration=self.iteration
        )
        new_message.normalize()
        
        self.messages[(sender, receiver)] = new_message
    
    def _compute_beliefs(self) -> None:
        """Compute final beliefs for all nodes."""
        self.beliefs.clear()
        
        for node_id, node in self.network.nodes.items():
            if node.is_evidence:
                # Evidence node has deterministic belief
                self.beliefs[node_id] = {
                    outcome: 1.0 if outcome == node.observed_value else 0.0
                    for outcome in node.outcome_space
                }
                continue
            
            # Aggregate all incoming messages
            belief_data = {}
            
            for outcome in node.outcome_space:
                # Start with local factor
                if isinstance(node, QuantumNode):
                    local_factor = node.get_amplitude(outcome)
                elif isinstance(node, StochasticNode):
                    if not node.parents:
                        local_factor = node.prior_distribution[node.outcome_space.index(outcome)]
                    else:
                        local_factor = 1.0 / len(node.outcome_space)  # Simplified
                elif isinstance(node, HybridNode):
                    quantum_comp = node.quantum_component.get_amplitude(outcome)
                    classical_comp = 1.0 / len(node.outcome_space)  # Simplified
                    local_factor = (
                        node.mixing_parameter * quantum_comp +
                        (1 - node.mixing_parameter) * classical_comp
                    )
                else:
                    local_factor = 1.0
                
                # Multiply by all incoming messages
                for neighbor in self.network.graph.neighbors(node_id):
                    if (neighbor, node_id) in self.messages:
                        msg = self.messages[(neighbor, node_id)]
                        if outcome in msg.data:
                            local_factor *= msg.data[outcome]
                
                belief_data[outcome] = local_factor
            
            self.beliefs[node_id] = belief_data
    
    def _compute_convergence_error(self, old_messages: Dict) -> float:
        """Compute convergence error between message sets."""
        total_error = 0.0
        count = 0
        
        for key, new_msg in self.messages.items():
            if key in old_messages:
                old_msg = old_messages[key]
                
                for outcome in new_msg.data:
                    if outcome in old_msg.data:
                        error = abs(new_msg.data[outcome] - old_msg.data[outcome])
                        total_error += error
                        count += 1
        
        return total_error / max(count, 1)
    
    def _copy_messages(self) -> Dict:
        """Create a deep copy of current messages."""
        return {
            key: Message(
                sender=msg.sender,
                receiver=msg.receiver,
                data=msg.data.copy(),
                is_quantum=msg.is_quantum,
                iteration=msg.iteration
            )
            for key, msg in self.messages.items()
        }
    
    def _is_quantum_node(self, node_id: str) -> bool:
        """Check if node is quantum."""
        node = self.network.nodes[node_id]
        return isinstance(node, (QuantumNode, HybridNode))
    
    def get_convergence_info(self) -> Dict[str, Any]:
        """Get information about convergence."""
        return {
            "converged": self.converged,
            "iterations": self.iteration + 1,
            "final_error": self.convergence_history[-1] if self.convergence_history else None,
            "convergence_history": self.convergence_history,
            "tolerance": self.tolerance
        }
