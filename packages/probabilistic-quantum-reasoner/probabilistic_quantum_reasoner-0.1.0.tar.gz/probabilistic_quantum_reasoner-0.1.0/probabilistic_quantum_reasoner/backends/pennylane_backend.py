"""
PennyLane backend implementation for quantum machine learning.

This module provides integration with PennyLane for quantum machine learning
and variational quantum algorithms.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Union, Callable
import logging

try:
    import pennylane as qml
    from pennylane import numpy as pnp
    PENNYLANE_AVAILABLE = True
except ImportError:
    PENNYLANE_AVAILABLE = False

from .simulator import Backend
from ..core.exceptions import BackendError
from ..core.operators import QuantumState, UnitaryOperator

logger = logging.getLogger(__name__)


class PennyLaneBackend(Backend):
    """
    PennyLane backend for quantum machine learning.
    
    Provides integration with PennyLane for variational quantum algorithms,
    quantum machine learning, and automatic differentiation.
    """
    
    def __init__(
        self,
        device_name: str = "default.qubit",
        n_qubits: int = 4,
        shots: Optional[int] = None,
        **device_kwargs
    ) -> None:
        """
        Initialize PennyLane backend.
        
        Args:
            device_name: PennyLane device name
            n_qubits: Number of qubits
            shots: Number of shots (None for exact simulation)
            **device_kwargs: Additional device arguments
        """
        if not PENNYLANE_AVAILABLE:
            raise BackendError("PennyLane not available. Install with: pip install pennylane")
        
        self.device_name = device_name
        self.n_qubits = n_qubits
        self.shots = shots
        
        # Create PennyLane device
        try:
            device_args = {"wires": n_qubits}
            if shots is not None:
                device_args["shots"] = shots
            device_args.update(device_kwargs)
            
            self.device = qml.device(device_name, **device_args)
        except Exception as e:
            raise BackendError(f"Failed to create PennyLane device: {e}")
        
        # Store quantum nodes
        self.qnodes: Dict[str, qml.QNode] = {}
        
        logger.info(f"Initialized PennyLane backend: {device_name} with {n_qubits} qubits")
    
    def create_qnode(self, circuit_func: Callable, name: str = "qnode") -> qml.QNode:
        """
        Create a quantum node (QNode) from circuit function.
        
        Args:
            circuit_func: Circuit function
            name: Name for the QNode
            
        Returns:
            PennyLane QNode
        """
        qnode = qml.QNode(circuit_func, self.device)
        self.qnodes[name] = qnode
        return qnode
    
    def apply_unitary_circuit(
        self,
        unitary: UnitaryOperator,
        qubits: List[int],
        parameters: Optional[np.ndarray] = None
    ) -> Callable:
        """
        Create circuit function that applies unitary operator.
        
        Args:
            unitary: Unitary operator to apply
            qubits: Target qubits
            parameters: Optional parameters for parametric unitaries
            
        Returns:
            Circuit function
        """
        def circuit():
            # Apply unitary matrix
            matrix = unitary.matrix_representation()
            qml.QubitUnitary(matrix, wires=qubits)
            return qml.state()
        
        return circuit
    
    def create_variational_circuit(
        self,
        n_layers: int = 3,
        template: str = "StronglyEntanglingLayers"
    ) -> Callable:
        """
        Create variational quantum circuit.
        
        Args:
            n_layers: Number of variational layers
            template: PennyLane template to use
            
        Returns:
            Variational circuit function
        """
        def circuit(params):
            # Initialize with Hadamard gates
            for wire in range(self.n_qubits):
                qml.Hadamard(wires=wire)
            
            # Apply variational template
            if template == "StronglyEntanglingLayers":
                qml.StronglyEntanglingLayers(params, wires=range(self.n_qubits))
            elif template == "BasicEntanglerLayers":
                qml.BasicEntanglerLayers(params, wires=range(self.n_qubits))
            elif template == "RandomLayers":
                qml.RandomLayers(params, wires=range(self.n_qubits))
            else:
                # Custom template
                self._apply_custom_template(params, n_layers)
            
            return qml.state()
        
        return circuit
    
    def _apply_custom_template(self, params: np.ndarray, n_layers: int) -> None:
        """Apply custom variational template."""
        param_idx = 0
        
        for layer in range(n_layers):
            # Rotation layers
            for wire in range(self.n_qubits):
                if param_idx < len(params):
                    qml.RX(params[param_idx], wires=wire)
                    param_idx += 1
                if param_idx < len(params):
                    qml.RY(params[param_idx], wires=wire)
                    param_idx += 1
                if param_idx < len(params):
                    qml.RZ(params[param_idx], wires=wire)
                    param_idx += 1
            
            # Entangling layer
            for wire in range(self.n_qubits - 1):
                qml.CNOT(wires=[wire, wire + 1])
            
            # Circular entanglement
            if self.n_qubits > 2:
                qml.CNOT(wires=[self.n_qubits - 1, 0])
    
    def create_bell_circuit(self, qubits: List[int]) -> Callable:
        """
        Create Bell state circuit.
        
        Args:
            qubits: Two qubits to entangle
            
        Returns:
            Bell state circuit function
        """
        if len(qubits) != 2:
            raise ValueError("Bell state requires exactly 2 qubits")
        
        def circuit():
            qml.Hadamard(wires=qubits[0])
            qml.CNOT(wires=qubits)
            return qml.state()
        
        return circuit
    
    def create_ghz_circuit(self, qubits: List[int]) -> Callable:
        """
        Create GHZ state circuit.
        
        Args:
            qubits: Qubits to entangle
            
        Returns:
            GHZ state circuit function
        """
        if len(qubits) < 3:
            raise ValueError("GHZ state requires at least 3 qubits")
        
        def circuit():
            qml.Hadamard(wires=qubits[0])
            for i in range(1, len(qubits)):
                qml.CNOT(wires=[qubits[0], qubits[i]])
            return qml.state()
        
        return circuit
    
    def execute_circuit(self, circuit_func: Callable, shots: int = 1024) -> Dict[str, int]:
        """
        Execute circuit and return measurement counts.
        
        Args:
            circuit_func: Circuit function to execute
            shots: Number of measurement shots
            
        Returns:
            Dictionary mapping measurement outcomes to counts
        """
        try:
            # Create QNode for measurement
            def measurement_circuit():
                circuit_func()
                # Add measurements
                return [qml.sample(qml.PauliZ(wire)) for wire in range(self.n_qubits)]
            
            # Create device with shots if needed
            if self.shots is None and shots > 0:
                temp_device = qml.device(self.device_name, wires=self.n_qubits, shots=shots)
                qnode = qml.QNode(measurement_circuit, temp_device)
            else:
                qnode = qml.QNode(measurement_circuit, self.device)
            
            # Execute and collect samples
            samples = qnode()
            
            # Convert samples to counts
            if isinstance(samples, list) and len(samples) > 0:
                # Multiple measurements
                counts = {}
                for shot_idx in range(shots):
                    outcome = ""
                    for wire_samples in samples:
                        # Convert -1/1 to 0/1
                        bit = 0 if wire_samples[shot_idx] == -1 else 1
                        outcome += str(bit)
                    
                    counts[outcome] = counts.get(outcome, 0) + 1
                
                return counts
            else:
                # Single measurement or no shots
                return {"0" * self.n_qubits: 1}
                
        except Exception as e:
            raise BackendError(f"Circuit execution failed: {e}")
    
    def get_statevector(self, circuit_func: Callable) -> np.ndarray:
        """
        Get state vector from circuit.
        
        Args:
            circuit_func: Circuit function
            
        Returns:
            State vector as numpy array
        """
        try:
            # Create QNode for statevector
            qnode = qml.QNode(circuit_func, self.device)
            state = qnode()
            
            # Convert to numpy array
            if hasattr(state, 'numpy'):
                return state.numpy()
            else:
                return np.array(state)
                
        except Exception as e:
            raise BackendError(f"Statevector computation failed: {e}")
    
    def compute_expectation(self, circuit_func: Callable, observable: Any) -> float:
        """
        Compute expectation value of observable.
        
        Args:
            circuit_func: Circuit function
            observable: Observable (PennyLane observable or matrix)
            
        Returns:
            Expectation value
        """
        try:
            def expectation_circuit():
                circuit_func()
                if isinstance(observable, np.ndarray):
                    # Convert matrix to PennyLane observable
                    return qml.expval(qml.Hermitian(observable, wires=range(self.n_qubits)))
                else:
                    return qml.expval(observable)
            
            qnode = qml.QNode(expectation_circuit, self.device)
            return float(qnode())
            
        except Exception as e:
            raise BackendError(f"Expectation value computation failed: {e}")
    
    def compute_gradient(
        self,
        circuit_func: Callable,
        parameters: np.ndarray,
        cost_function: Optional[Callable] = None
    ) -> np.ndarray:
        """
        Compute gradient of circuit with respect to parameters.
        
        Args:
            circuit_func: Parametric circuit function
            parameters: Circuit parameters
            cost_function: Cost function (defaults to expectation of PauliZ)
            
        Returns:
            Gradient array
        """
        try:
            if cost_function is None:
                # Default cost function
                def cost_function(params):
                    def circuit():
                        circuit_func(params)
                        return qml.expval(qml.PauliZ(0))
                    
                    qnode = qml.QNode(circuit, self.device)
                    return qnode()
            
            # Compute gradient using PennyLane's automatic differentiation
            grad_func = qml.grad(cost_function)
            return grad_func(parameters)
            
        except Exception as e:
            raise BackendError(f"Gradient computation failed: {e}")
    
    def optimize_circuit(
        self,
        circuit_func: Callable,
        initial_params: np.ndarray,
        cost_function: Callable,
        optimizer: str = "AdamOptimizer",
        max_iterations: int = 100,
        learning_rate: float = 0.1
    ) -> Dict[str, Any]:
        """
        Optimize circuit parameters.
        
        Args:
            circuit_func: Parametric circuit function
            initial_params: Initial parameters
            cost_function: Cost function to minimize
            optimizer: Optimizer name
            max_iterations: Maximum optimization iterations
            learning_rate: Learning rate
            
        Returns:
            Optimization results
        """
        try:
            # Create optimizer
            if optimizer == "AdamOptimizer":
                opt = qml.AdamOptimizer(stepsize=learning_rate)
            elif optimizer == "GradientDescentOptimizer":
                opt = qml.GradientDescentOptimizer(stepsize=learning_rate)
            elif optimizer == "NesterovMomentumOptimizer":
                opt = qml.NesterovMomentumOptimizer(stepsize=learning_rate)
            else:
                opt = qml.GradientDescentOptimizer(stepsize=learning_rate)
            
            # Optimization loop
            params = initial_params.copy()
            cost_history = []
            
            for iteration in range(max_iterations):
                cost = cost_function(params)
                cost_history.append(cost)
                
                params = opt.step(cost_function, params)
                
                # Check convergence
                if iteration > 0:
                    cost_change = abs(cost_history[-1] - cost_history[-2])
                    if cost_change < 1e-6:
                        break
            
            return {
                "optimized_params": params,
                "final_cost": cost_history[-1],
                "cost_history": cost_history,
                "iterations": len(cost_history),
                "converged": len(cost_history) < max_iterations
            }
            
        except Exception as e:
            raise BackendError(f"Circuit optimization failed: {e}")
    
    def create_quantum_state(self, amplitudes: np.ndarray, basis_labels: List[str]) -> QuantumState:
        """
        Create QuantumState from amplitudes.
        
        Args:
            amplitudes: State amplitudes
            basis_labels: Basis state labels
            
        Returns:
            QuantumState instance
        """
        return QuantumState(amplitudes, basis_labels)
    
    def prepare_state(self, target_state: np.ndarray) -> Callable:
        """
        Create circuit to prepare target quantum state.
        
        Args:
            target_state: Target state vector
            
        Returns:
            State preparation circuit function
        """
        def circuit():
            qml.QubitStateVector(target_state, wires=range(self.n_qubits))
            return qml.state()
        
        return circuit
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get device information and capabilities."""
        info = {
            "name": self.device_name,
            "type": "pennylane",
            "n_qubits": self.n_qubits,
            "shots": self.shots,
            "supports_gradients": True,
            "supports_optimization": True,
            "supports_quantum_ml": True,
        }
        
        # Add device-specific information
        if hasattr(self.device, 'capabilities'):
            capabilities = self.device.capabilities()
            info.update({
                "supports_finite_shots": capabilities.get("supports_finite_shots", False),
                "supports_tensor_observables": capabilities.get("supports_tensor_observables", False),
                "returns_state": capabilities.get("returns_state", False),
            })
        
        return info
    
    def create_quantum_neural_network(
        self,
        n_layers: int = 3,
        input_encoding: str = "angle"
    ) -> Callable:
        """
        Create quantum neural network circuit.
        
        Args:
            n_layers: Number of layers
            input_encoding: Input encoding method
            
        Returns:
            QNN circuit function
        """
        def qnn_circuit(inputs, weights):
            # Input encoding
            if input_encoding == "angle":
                for i, inp in enumerate(inputs):
                    if i < self.n_qubits:
                        qml.RY(inp, wires=i)
            elif input_encoding == "amplitude":
                # Amplitude encoding (simplified)
                qml.QubitStateVector(inputs, wires=range(len(inputs)))
            
            # Variational layers
            for layer in range(n_layers):
                # Parameterized rotation gates
                for wire in range(self.n_qubits):
                    param_idx = layer * self.n_qubits * 3 + wire * 3
                    if param_idx < len(weights):
                        qml.RX(weights[param_idx], wires=wire)
                    if param_idx + 1 < len(weights):
                        qml.RY(weights[param_idx + 1], wires=wire)
                    if param_idx + 2 < len(weights):
                        qml.RZ(weights[param_idx + 2], wires=wire)
                
                # Entangling gates
                for wire in range(self.n_qubits - 1):
                    qml.CNOT(wires=[wire, wire + 1])
            
            # Output measurement
            return qml.expval(qml.PauliZ(0))
        
        return qnn_circuit
    
    def tensor_network_contraction(self, tensors: List[np.ndarray]) -> np.ndarray:
        """
        Perform tensor network contraction (if supported by device).
        
        Args:
            tensors: List of tensors to contract
            
        Returns:
            Contracted tensor
        """
        # This would require specialized tensor network backend
        # For now, provide basic implementation
        result = tensors[0]
        for tensor in tensors[1:]:
            result = np.tensordot(result, tensor, axes=1)
        return result
