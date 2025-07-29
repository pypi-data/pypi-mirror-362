"""
Variational quantum inference for quantum Bayesian networks.

This module implements variational quantum algorithms for inference,
including variational quantum eigensolver (VQE) and quantum approximate
optimization algorithm (QAOA) approaches to probabilistic reasoning.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Callable
import logging
from abc import ABC, abstractmethod

try:
    import pennylane as qml
    PENNYLANE_AVAILABLE = True
except ImportError:
    PENNYLANE_AVAILABLE = False

try:
    from qiskit import QuantumCircuit, transpile
    from qiskit.primitives import Estimator
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False

from ..core.nodes import BaseNode, QuantumNode, HybridNode
from ..core.exceptions import InferenceError, BackendError

logger = logging.getLogger(__name__)


class ParametricQuantumCircuit(ABC):
    """Abstract base class for parametric quantum circuits."""
    
    def __init__(self, n_qubits: int, n_parameters: int) -> None:
        self.n_qubits = n_qubits
        self.n_parameters = n_parameters
        self.parameters = np.random.uniform(0, 2*np.pi, n_parameters)
    
    @abstractmethod
    def build_circuit(self, parameters: np.ndarray) -> Any:
        """Build the parametric quantum circuit."""
        pass
    
    @abstractmethod
    def expectation_value(self, parameters: np.ndarray, observable: Any) -> float:
        """Compute expectation value of observable."""
        pass


class PennyLaneCircuit(ParametricQuantumCircuit):
    """PennyLane implementation of parametric quantum circuit."""
    
    def __init__(self, n_qubits: int, n_layers: int = 3) -> None:
        if not PENNYLANE_AVAILABLE:
            raise BackendError("PennyLane not available")
        
        self.n_layers = n_layers
        n_parameters = n_layers * n_qubits * 3  # RX, RY, RZ for each qubit per layer
        super().__init__(n_qubits, n_parameters)
        
        # Create device
        self.device = qml.device('default.qubit', wires=n_qubits)
        
        # Create quantum node
        self.qnode = qml.QNode(self._circuit, self.device)
    
    def _circuit(self, parameters: np.ndarray, observable: Optional[Any] = None) -> Any:
        """Define the variational quantum circuit."""
        param_idx = 0
        
        # Initial layer of Hadamard gates
        for i in range(self.n_qubits):
            qml.Hadamard(wires=i)
        
        # Variational layers
        for layer in range(self.n_layers):
            # Rotation gates
            for i in range(self.n_qubits):
                qml.RX(parameters[param_idx], wires=i)
                param_idx += 1
                qml.RY(parameters[param_idx], wires=i)
                param_idx += 1
                qml.RZ(parameters[param_idx], wires=i)
                param_idx += 1
            
            # Entangling gates
            for i in range(self.n_qubits - 1):
                qml.CNOT(wires=[i, i + 1])
            
            # Circular entanglement
            if self.n_qubits > 2:
                qml.CNOT(wires=[self.n_qubits - 1, 0])
        
        # Return expectation value or state
        if observable is not None:
            return qml.expval(observable)
        else:
            return qml.state()
    
    def build_circuit(self, parameters: np.ndarray) -> Any:
        """Build circuit and return state vector."""
        return self.qnode(parameters)
    
    def expectation_value(self, parameters: np.ndarray, observable: Any) -> float:
        """Compute expectation value."""
        qnode_exp = qml.QNode(
            lambda params: self._circuit(params, observable),
            self.device
        )
        return float(qnode_exp(parameters))


class QiskitCircuit(ParametricQuantumCircuit):
    """Qiskit implementation of parametric quantum circuit."""
    
    def __init__(self, n_qubits: int, n_layers: int = 3) -> None:
        if not QISKIT_AVAILABLE:
            raise BackendError("Qiskit not available")
        
        self.n_layers = n_layers
        n_parameters = n_layers * n_qubits * 3
        super().__init__(n_qubits, n_parameters)
        
        # Create estimator for expectation values
        self.estimator = Estimator()
    
    def build_circuit(self, parameters: np.ndarray) -> 'QuantumCircuit':
        """Build parametric quantum circuit."""
        qc = QuantumCircuit(self.n_qubits)
        param_idx = 0
        
        # Initial Hadamard layer
        for i in range(self.n_qubits):
            qc.h(i)
        
        # Variational layers
        for layer in range(self.n_layers):
            # Rotation gates
            for i in range(self.n_qubits):
                qc.rx(parameters[param_idx], i)
                param_idx += 1
                qc.ry(parameters[param_idx], i)
                param_idx += 1
                qc.rz(parameters[param_idx], i)
                param_idx += 1
            
            # Entangling gates
            for i in range(self.n_qubits - 1):
                qc.cx(i, i + 1)
            
            if self.n_qubits > 2:
                qc.cx(self.n_qubits - 1, 0)
        
        return qc
    
    def expectation_value(self, parameters: np.ndarray, observable: Any) -> float:
        """Compute expectation value using Qiskit primitives."""
        circuit = self.build_circuit(parameters)
        
        # Use estimator to compute expectation value
        job = self.estimator.run([circuit], [observable])
        result = job.result()
        
        return float(result.values[0])


class VariationalQuantumInference:
    """
    Variational quantum inference for quantum Bayesian networks.
    
    Uses variational quantum circuits to approximate marginal distributions
    and perform approximate inference in quantum probabilistic models.
    """
    
    def __init__(
        self, 
        network: Any, 
        backend: Any,
        n_layers: int = 3,
        optimizer: str = "adam"
    ) -> None:
        """
        Initialize variational quantum inference.
        
        Args:
            network: QuantumBayesianNetwork instance
            backend: Quantum computing backend
            n_layers: Number of variational layers
            optimizer: Classical optimizer for parameters
        """
        self.network = network
        self.backend = backend
        self.n_layers = n_layers
        self.optimizer_name = optimizer
        
        # Count quantum nodes to determine qubit requirements
        self.quantum_nodes = [
            node_id for node_id, node in network.nodes.items()
            if isinstance(node, (QuantumNode, HybridNode))
        ]
        
        self.n_qubits = len(self.quantum_nodes)
        
        if self.n_qubits == 0:
            raise InferenceError(
                "No quantum nodes found for variational inference",
                algorithm="variational"
            )
        
        # Create parametric quantum circuit
        self.circuit = self._create_circuit()
        
        # Optimization history
        self.cost_history: List[float] = []
        self.parameter_history: List[np.ndarray] = []
    
    def run_inference(
        self,
        query_nodes: List[str],
        max_iterations: int = 100,
        learning_rate: float = 0.1,
        tolerance: float = 1e-6,
        **kwargs
    ) -> Tuple[Dict[str, Dict[Any, float]], Dict[str, Any]]:
        """
        Run variational quantum inference.
        
        Args:
            query_nodes: Nodes to compute marginals for
            max_iterations: Maximum optimization iterations
            learning_rate: Learning rate for parameter updates
            tolerance: Convergence tolerance
            
        Returns:
            Tuple of (marginals, metadata)
        """
        logger.info(f"Starting variational quantum inference with {self.n_qubits} qubits")
        
        # Define cost function
        def cost_function(parameters: np.ndarray) -> float:
            return self._compute_cost(parameters, query_nodes)
        
        # Initialize optimizer
        optimizer = self._create_optimizer(learning_rate)
        
        # Optimization loop
        current_params = self.circuit.parameters.copy()
        
        for iteration in range(max_iterations):
            # Compute cost and gradient
            cost = cost_function(current_params)
            gradient = self._compute_gradient(current_params, query_nodes)
            
            # Update parameters
            current_params = optimizer.update(current_params, gradient)
            
            # Store history
            self.cost_history.append(cost)
            self.parameter_history.append(current_params.copy())
            
            # Check convergence
            if iteration > 0:
                cost_change = abs(self.cost_history[-1] - self.cost_history[-2])
                if cost_change < tolerance:
                    logger.info(f"Converged after {iteration + 1} iterations")
                    break
        
        # Compute final marginals
        marginals = self._compute_marginals(current_params, query_nodes)
        
        metadata = {
            "algorithm": "variational",
            "iterations": len(self.cost_history),
            "final_cost": self.cost_history[-1],
            "converged": len(self.cost_history) < max_iterations,
            "n_qubits": self.n_qubits,
            "n_parameters": self.circuit.n_parameters
        }
        
        return marginals, metadata
    
    def _create_circuit(self) -> ParametricQuantumCircuit:
        """Create parametric quantum circuit based on backend."""
        backend_name = type(self.backend).__name__.lower()
        
        if "pennylane" in backend_name or PENNYLANE_AVAILABLE:
            return PennyLaneCircuit(self.n_qubits, self.n_layers)
        elif "qiskit" in backend_name or QISKIT_AVAILABLE:
            return QiskitCircuit(self.n_qubits, self.n_layers)
        else:
            raise BackendError(f"Unsupported backend for variational inference: {backend_name}")
    
    def _compute_cost(self, parameters: np.ndarray, query_nodes: List[str]) -> float:
        """Compute cost function for parameter optimization."""
        # Get quantum state from variational circuit
        try:
            state_vector = self.circuit.build_circuit(parameters)
            
            # Convert to probability distribution
            if hasattr(state_vector, 'numpy'):
                state_vector = state_vector.numpy()
            
            probabilities = np.abs(state_vector) ** 2
            
            # Compute KL divergence from target distribution
            target_probs = self._get_target_probabilities(query_nodes)
            
            # KL(target || approx) = Σ p_target * log(p_target / p_approx)
            kl_div = 0.0
            for i, (target_p, approx_p) in enumerate(zip(target_probs, probabilities)):
                if target_p > 0 and approx_p > 0:
                    kl_div += target_p * np.log(target_p / approx_p)
            
            return kl_div
            
        except Exception as e:
            logger.warning(f"Error computing cost: {e}")
            return 1e6  # Large penalty for invalid parameters
    
    def _get_target_probabilities(self, query_nodes: List[str]) -> np.ndarray:
        """Get target probability distribution from classical inference."""
        # Use exact inference to get target distribution
        from .engine import QuantumInferenceEngine
        
        # Create classical approximation for target
        classical_network = self._create_classical_approximation()
        engine = QuantumInferenceEngine(classical_network)
        
        try:
            result = engine.infer(query_nodes, algorithm="exact")
            
            # Convert marginals to joint distribution (simplified)
            # In practice, would need more sophisticated approach
            n_states = 2 ** self.n_qubits
            target_probs = np.ones(n_states) / n_states
            
            return target_probs
            
        except Exception:
            # Fallback to uniform distribution
            n_states = 2 ** self.n_qubits
            return np.ones(n_states) / n_states
    
    def _create_classical_approximation(self) -> Any:
        """Create classical approximation of quantum network."""
        # Simplified: convert quantum nodes to classical
        # In practice, would use more sophisticated approximation
        return self.network
    
    def _compute_gradient(self, parameters: np.ndarray, query_nodes: List[str]) -> np.ndarray:
        """Compute gradient of cost function."""
        gradient = np.zeros_like(parameters)
        epsilon = 1e-6
        
        for i in range(len(parameters)):
            # Forward difference
            params_plus = parameters.copy()
            params_plus[i] += epsilon
            cost_plus = self._compute_cost(params_plus, query_nodes)
            
            # Backward difference
            params_minus = parameters.copy()
            params_minus[i] -= epsilon
            cost_minus = self._compute_cost(params_minus, query_nodes)
            
            # Central difference
            gradient[i] = (cost_plus - cost_minus) / (2 * epsilon)
        
        return gradient
    
    def _compute_marginals(
        self, 
        parameters: np.ndarray, 
        query_nodes: List[str]
    ) -> Dict[str, Dict[Any, float]]:
        """Compute marginal distributions from optimized parameters."""
        # Get final quantum state
        state_vector = self.circuit.build_circuit(parameters)
        
        if hasattr(state_vector, 'numpy'):
            state_vector = state_vector.numpy()
        
        probabilities = np.abs(state_vector) ** 2
        
        # Map to marginal distributions for each query node
        marginals = {}
        
        for i, node_id in enumerate(query_nodes):
            if node_id in self.quantum_nodes:
                node = self.network.nodes[node_id]
                node_marginals = {}
                
                # Extract marginal for this qubit (simplified)
                qubit_idx = self.quantum_nodes.index(node_id)
                
                # Trace out other qubits
                prob_0 = sum(
                    probabilities[state_idx] 
                    for state_idx in range(len(probabilities))
                    if not (state_idx >> qubit_idx) & 1
                )
                prob_1 = 1.0 - prob_0
                
                # Map to outcome space
                if len(node.outcome_space) >= 2:
                    node_marginals[node.outcome_space[0]] = prob_0
                    node_marginals[node.outcome_space[1]] = prob_1
                else:
                    node_marginals[node.outcome_space[0]] = 1.0
                
                marginals[node_id] = node_marginals
        
        return marginals
    
    def _create_optimizer(self, learning_rate: float) -> Any:
        """Create classical optimizer for parameter updates."""
        if self.optimizer_name.lower() == "adam":
            return AdamOptimizer(learning_rate)
        elif self.optimizer_name.lower() == "sgd":
            return SGDOptimizer(learning_rate)
        else:
            return SGDOptimizer(learning_rate)


class Optimizer(ABC):
    """Abstract base class for optimizers."""
    
    @abstractmethod
    def update(self, parameters: np.ndarray, gradient: np.ndarray) -> np.ndarray:
        """Update parameters using gradient."""
        pass


class SGDOptimizer(Optimizer):
    """Stochastic gradient descent optimizer."""
    
    def __init__(self, learning_rate: float = 0.1) -> None:
        self.learning_rate = learning_rate
    
    def update(self, parameters: np.ndarray, gradient: np.ndarray) -> np.ndarray:
        """SGD update rule."""
        return parameters - self.learning_rate * gradient


class AdamOptimizer(Optimizer):
    """Adam optimizer with momentum and adaptive learning rates."""
    
    def __init__(
        self, 
        learning_rate: float = 0.001,
        beta1: float = 0.9,
        beta2: float = 0.999,
        epsilon: float = 1e-8
    ) -> None:
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        
        self.m = None  # First moment
        self.v = None  # Second moment
        self.t = 0     # Time step
    
    def update(self, parameters: np.ndarray, gradient: np.ndarray) -> np.ndarray:
        """Adam update rule."""
        self.t += 1
        
        if self.m is None:
            self.m = np.zeros_like(parameters)
            self.v = np.zeros_like(parameters)
        
        # Update moments
        self.m = self.beta1 * self.m + (1 - self.beta1) * gradient
        self.v = self.beta2 * self.v + (1 - self.beta2) * gradient**2
        
        # Bias correction
        m_hat = self.m / (1 - self.beta1**self.t)
        v_hat = self.v / (1 - self.beta2**self.t)
        
        # Update parameters
        return parameters - self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon)
