"""
Node implementations for quantum Bayesian networks.

This module provides different types of nodes that can be used in quantum-classical
hybrid probabilistic graphical models, including pure quantum nodes, classical
stochastic nodes, and hybrid nodes that combine both paradigms.
"""

import numpy as np
from abc import ABC, abstractmethod
from typing import (
    List, Dict, Any, Optional, Union, Set, Tuple, 
    Callable, Type
)
from dataclasses import dataclass, field
from enum import Enum
import uuid

from .operators import (
    QuantumState, QuantumOperator, UnitaryOperator, 
    MeasurementOperator, ComputationalBasisMeasurement
)
from .exceptions import QuantumStateError, NetworkTopologyError


class NodeType(Enum):
    """Enumeration of different node types."""
    QUANTUM = "quantum"
    STOCHASTIC = "stochastic" 
    HYBRID = "hybrid"
    DETERMINISTIC = "deterministic"


@dataclass
class ConditionalProbabilityTable:
    """Classical conditional probability table."""
    
    variables: List[str]
    table: Dict[Tuple, np.ndarray]
    
    def __post_init__(self) -> None:
        """Validate CPT after initialization."""
        self._validate_cpt()
    
    def _validate_cpt(self) -> None:
        """Validate that CPT is properly normalized."""
        for key, probs in self.table.items():
            if not np.isclose(np.sum(probs), 1.0):
                raise NetworkTopologyError(
                    f"CPT probabilities must sum to 1, got {np.sum(probs)}",
                    details={"key": key, "probabilities": probs.tolist()}
                )
    
    def get_probability(self, child_value: Any, parent_values: Dict[str, Any]) -> float:
        """Get conditional probability P(child=value|parents)."""
        parent_tuple = tuple(parent_values[var] for var in self.variables[:-1])
        child_idx = self._get_value_index(child_value)
        
        if parent_tuple not in self.table:
            raise NetworkTopologyError(
                f"Parent configuration {parent_tuple} not found in CPT"
            )
        
        return float(self.table[parent_tuple][child_idx])
    
    def _get_value_index(self, value: Any) -> int:
        """Get index of value in outcome space."""
        # This is a simplified implementation
        # In practice, you'd maintain a mapping of values to indices
        if isinstance(value, int):
            return value
        elif isinstance(value, str):
            return hash(value) % len(list(self.table.values())[0])
        else:
            return 0


@dataclass
class QuantumConditionalOperator:
    """Quantum analog of conditional probability tables."""
    
    parent_nodes: List[str]
    conditional_operators: Dict[Tuple, QuantumOperator]
    
    def get_operator(self, parent_values: Dict[str, Any]) -> QuantumOperator:
        """Get quantum operator conditioned on parent values."""
        parent_tuple = tuple(parent_values[node] for node in self.parent_nodes)
        
        if parent_tuple not in self.conditional_operators:
            raise NetworkTopologyError(
                f"No conditional operator for parent configuration {parent_tuple}"
            )
        
        return self.conditional_operators[parent_tuple]


class BaseNode(ABC):
    """Abstract base class for all node types in quantum Bayesian networks."""
    
    def __init__(
        self,
        node_id: str,
        name: str,
        node_type: NodeType,
        outcome_space: List[Any]
    ) -> None:
        self.node_id = node_id
        self.name = name
        self.node_type = node_type
        self.outcome_space = outcome_space
        self.parents: Set[str] = set()
        self.children: Set[str] = set()
        self.metadata: Dict[str, Any] = {}
        
        # Evidence and observation tracking
        self.observed_value: Optional[Any] = None
        self.is_evidence = False
    
    @abstractmethod
    def sample(self, parent_values: Optional[Dict[str, Any]] = None) -> Any:
        """Sample a value from this node."""
        pass
    
    @abstractmethod
    def log_probability(
        self, 
        value: Any, 
        parent_values: Optional[Dict[str, Any]] = None
    ) -> float:
        """Compute log probability of value given parents."""
        pass
    
    def add_parent(self, parent_id: str) -> None:
        """Add a parent node."""
        self.parents.add(parent_id)
    
    def remove_parent(self, parent_id: str) -> None:
        """Remove a parent node."""
        self.parents.discard(parent_id)
    
    def add_child(self, child_id: str) -> None:
        """Add a child node."""
        self.children.add(child_id)
    
    def remove_child(self, child_id: str) -> None:
        """Remove a child node."""
        self.children.discard(child_id)
    
    def set_evidence(self, value: Any) -> None:
        """Set evidence for this node."""
        if value not in self.outcome_space:
            raise NetworkTopologyError(
                f"Evidence value {value} not in outcome space {self.outcome_space}",
                node_id=self.node_id
            )
        self.observed_value = value
        self.is_evidence = True
    
    def clear_evidence(self) -> None:
        """Clear evidence from this node."""
        self.observed_value = None
        self.is_evidence = False


class QuantumNode(BaseNode):
    """Node representing a quantum random variable with amplitude-based states."""
    
    def __init__(
        self,
        node_id: str,
        name: str,
        outcome_space: List[Any],
        initial_state: Optional[QuantumState] = None,
        conditional_operators: Optional[QuantumConditionalOperator] = None
    ) -> None:
        super().__init__(node_id, name, NodeType.QUANTUM, outcome_space)
        
        # Initialize quantum state
        if initial_state is None:
            # Create uniform superposition as default
            n_states = len(outcome_space)
            amplitudes = np.ones(n_states, dtype=complex) / np.sqrt(n_states)
            basis_labels = [str(outcome) for outcome in outcome_space]
            self.quantum_state = QuantumState(amplitudes, basis_labels)
        else:
            self.quantum_state = initial_state
        
        self.conditional_operators = conditional_operators
        self.measurement_operator = ComputationalBasisMeasurement(len(outcome_space))
        
        # Quantum-specific properties
        self.entangled_with: Set[str] = set()
        self.coherence_time: Optional[float] = None
    
    def sample(self, parent_values: Optional[Dict[str, Any]] = None) -> Any:
        """Sample from quantum state by performing measurement."""
        if self.is_evidence:
            return self.observed_value
        
        # Apply conditional operations if parents exist
        current_state = self.quantum_state
        if parent_values and self.conditional_operators:
            operator = self.conditional_operators.get_operator(parent_values)
            current_state = operator.apply(current_state)
        
        # Perform measurement
        collapsed_state = self.measurement_operator.apply(current_state)
        probabilities = collapsed_state.probabilities()
        
        # Sample outcome based on quantum probabilities
        outcomes = list(probabilities.keys())
        probs = list(probabilities.values())
        
        sampled_basis = np.random.choice(outcomes, p=probs)
        
        # Map basis state back to outcome space
        basis_idx = collapsed_state.basis_labels.index(sampled_basis)
        return self.outcome_space[basis_idx]
    
    def log_probability(
        self, 
        value: Any, 
        parent_values: Optional[Dict[str, Any]] = None
    ) -> float:
        """Compute log probability using Born rule."""
        if value not in self.outcome_space:
            return -np.inf
        
        current_state = self.quantum_state
        if parent_values and self.conditional_operators:
            operator = self.conditional_operators.get_operator(parent_values)
            current_state = operator.apply(current_state)
        
        probabilities = current_state.probabilities()
        value_idx = self.outcome_space.index(value)
        basis_label = current_state.basis_labels[value_idx]
        
        prob = probabilities.get(basis_label, 0.0)
        return np.log(max(prob, 1e-12))  # Avoid log(0)
    
    def apply_unitary(self, unitary: UnitaryOperator) -> None:
        """Apply unitary transformation to quantum state."""
        self.quantum_state = unitary.apply(self.quantum_state)
    
    def get_amplitude(self, outcome: Any) -> complex:
        """Get quantum amplitude for specific outcome."""
        if outcome not in self.outcome_space:
            return 0.0
        
        outcome_idx = self.outcome_space.index(outcome)
        return self.quantum_state.amplitudes[outcome_idx]
    
    def set_amplitude(self, outcome: Any, amplitude: complex) -> None:
        """Set quantum amplitude for specific outcome."""
        if outcome not in self.outcome_space:
            raise QuantumStateError(f"Outcome {outcome} not in space")
        
        outcome_idx = self.outcome_space.index(outcome)
        self.quantum_state.amplitudes[outcome_idx] = amplitude
        self.quantum_state.normalize()
    
    def entangle_with(self, other_node_id: str) -> None:
        """Mark this node as entangled with another."""
        self.entangled_with.add(other_node_id)
    
    def is_entangled(self) -> bool:
        """Check if node is entangled with others."""
        return len(self.entangled_with) > 0


class StochasticNode(BaseNode):
    """Classical probabilistic node with conditional probability tables."""
    
    def __init__(
        self,
        node_id: str,
        name: str,
        outcome_space: List[Any],
        cpt: Optional[ConditionalProbabilityTable] = None,
        prior_distribution: Optional[np.ndarray] = None
    ) -> None:
        super().__init__(node_id, name, NodeType.STOCHASTIC, outcome_space)
        
        self.cpt = cpt
        
        # Set prior distribution
        if prior_distribution is None:
            n_outcomes = len(outcome_space)
            self.prior_distribution = np.ones(n_outcomes) / n_outcomes
        else:
            if not np.isclose(np.sum(prior_distribution), 1.0):
                raise NetworkTopologyError(
                    "Prior distribution must sum to 1",
                    node_id=node_id
                )
            self.prior_distribution = prior_distribution
    
    def sample(self, parent_values: Optional[Dict[str, Any]] = None) -> Any:
        """Sample from conditional or prior distribution."""
        if self.is_evidence:
            return self.observed_value
        
        if parent_values and self.cpt:
            # Sample from conditional distribution
            probabilities = self._get_conditional_distribution(parent_values)
        else:
            # Sample from prior distribution
            probabilities = self.prior_distribution
        
        sampled_idx = np.random.choice(len(self.outcome_space), p=probabilities)
        return self.outcome_space[sampled_idx]
    
    def log_probability(
        self, 
        value: Any, 
        parent_values: Optional[Dict[str, Any]] = None
    ) -> float:
        """Compute log probability from CPT or prior."""
        if value not in self.outcome_space:
            return -np.inf
        
        value_idx = self.outcome_space.index(value)
        
        if parent_values and self.cpt:
            prob = self.cpt.get_probability(value, parent_values)
        else:
            prob = self.prior_distribution[value_idx]
        
        return np.log(max(prob, 1e-12))
    
    def _get_conditional_distribution(self, parent_values: Dict[str, Any]) -> np.ndarray:
        """Get conditional probability distribution given parent values."""
        if not self.cpt:
            return self.prior_distribution
        
        parent_tuple = tuple(parent_values[var] for var in self.cpt.variables[:-1])
        
        if parent_tuple not in self.cpt.table:
            # Fallback to prior if parent configuration not found
            return self.prior_distribution
        
        return self.cpt.table[parent_tuple]
    
    def update_cpt(self, cpt: ConditionalProbabilityTable) -> None:
        """Update the conditional probability table."""
        self.cpt = cpt


class HybridNode(BaseNode):
    """Node that combines quantum and classical probabilistic elements."""
    
    def __init__(
        self,
        node_id: str,
        name: str,
        outcome_space: List[Any],
        quantum_component: Optional[QuantumNode] = None,
        classical_component: Optional[StochasticNode] = None,
        mixing_parameter: float = 0.5
    ) -> None:
        super().__init__(node_id, name, NodeType.HYBRID, outcome_space)
        
        # Initialize components
        if quantum_component is None:
            quantum_component = QuantumNode(
                f"{node_id}_quantum", f"{name}_quantum", outcome_space
            )
        if classical_component is None:
            classical_component = StochasticNode(
                f"{node_id}_classical", f"{name}_classical", outcome_space
            )
        
        self.quantum_component = quantum_component
        self.classical_component = classical_component
        self.mixing_parameter = mixing_parameter  # λ ∈ [0,1]
        
        # Validate mixing parameter
        if not 0 <= mixing_parameter <= 1:
            raise NetworkTopologyError(
                "Mixing parameter must be between 0 and 1",
                node_id=node_id,
                details={"mixing_parameter": mixing_parameter}
            )
    
    def sample(self, parent_values: Optional[Dict[str, Any]] = None) -> Any:
        """Sample using mixture of quantum and classical components."""
        if self.is_evidence:
            return self.observed_value
        
        # Decide which component to use based on mixing parameter
        use_quantum = np.random.random() < self.mixing_parameter
        
        if use_quantum:
            return self.quantum_component.sample(parent_values)
        else:
            return self.classical_component.sample(parent_values)
    
    def log_probability(
        self, 
        value: Any, 
        parent_values: Optional[Dict[str, Any]] = None
    ) -> float:
        """Compute mixture log probability."""
        if value not in self.outcome_space:
            return -np.inf
        
        # P_hybrid(X) = λ * P_quantum(X) + (1-λ) * P_classical(X)
        quantum_log_prob = self.quantum_component.log_probability(value, parent_values)
        classical_log_prob = self.classical_component.log_probability(value, parent_values)
        
        quantum_prob = np.exp(quantum_log_prob)
        classical_prob = np.exp(classical_log_prob)
        
        mixture_prob = (
            self.mixing_parameter * quantum_prob +
            (1 - self.mixing_parameter) * classical_prob
        )
        
        return np.log(max(mixture_prob, 1e-12))
    
    def update_mixing_parameter(self, new_lambda: float) -> None:
        """Update the quantum-classical mixing parameter."""
        if not 0 <= new_lambda <= 1:
            raise NetworkTopologyError(
                "Mixing parameter must be between 0 and 1",
                details={"new_lambda": new_lambda}
            )
        self.mixing_parameter = new_lambda
    
    def get_quantum_probability(
        self, 
        value: Any, 
        parent_values: Optional[Dict[str, Any]] = None
    ) -> float:
        """Get probability from quantum component only."""
        return np.exp(self.quantum_component.log_probability(value, parent_values))
    
    def get_classical_probability(
        self, 
        value: Any, 
        parent_values: Optional[Dict[str, Any]] = None
    ) -> float:
        """Get probability from classical component only."""
        return np.exp(self.classical_component.log_probability(value, parent_values))


class DeterministicNode(BaseNode):
    """Node with deterministic relationship to parents."""
    
    def __init__(
        self,
        node_id: str,
        name: str,
        outcome_space: List[Any],
        function: Callable[[Dict[str, Any]], Any]
    ) -> None:
        super().__init__(node_id, name, NodeType.DETERMINISTIC, outcome_space)
        self.function = function
    
    def sample(self, parent_values: Optional[Dict[str, Any]] = None) -> Any:
        """Deterministically compute value from parent values."""
        if self.is_evidence:
            return self.observed_value
        
        if parent_values is None:
            raise NetworkTopologyError(
                "Deterministic node requires parent values",
                node_id=self.node_id
            )
        
        result = self.function(parent_values)
        
        if result not in self.outcome_space:
            raise NetworkTopologyError(
                f"Function result {result} not in outcome space",
                node_id=self.node_id
            )
        
        return result
    
    def log_probability(
        self, 
        value: Any, 
        parent_values: Optional[Dict[str, Any]] = None
    ) -> float:
        """Log probability is 0 for correct value, -inf otherwise."""
        if parent_values is None:
            return -np.inf
        
        correct_value = self.function(parent_values)
        return 0.0 if value == correct_value else -np.inf


def create_node(
    node_type: Union[NodeType, str],
    node_id: str,
    name: str,
    outcome_space: List[Any],
    **kwargs
) -> BaseNode:
    """Factory function to create nodes of different types."""
    
    if isinstance(node_type, str):
        node_type = NodeType(node_type)
    
    if node_type == NodeType.QUANTUM:
        return QuantumNode(node_id, name, outcome_space, **kwargs)
    elif node_type == NodeType.STOCHASTIC:
        return StochasticNode(node_id, name, outcome_space, **kwargs)
    elif node_type == NodeType.HYBRID:
        return HybridNode(node_id, name, outcome_space, **kwargs)
    elif node_type == NodeType.DETERMINISTIC:
        if 'function' not in kwargs:
            raise ValueError("Deterministic node requires 'function' parameter")
        return DeterministicNode(node_id, name, outcome_space, kwargs['function'])
    else:
        raise ValueError(f"Unknown node type: {node_type}")
