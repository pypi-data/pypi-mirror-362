"""
Classical simulator backend for quantum operations.

This module provides a classical simulation backend that uses NumPy and SciPy
to simulate quantum operations without requiring actual quantum hardware.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Union, Tuple
import logging
from abc import ABC, abstractmethod

from ..core.operators import QuantumState, QuantumOperator, UnitaryOperator
from ..core.exceptions import BackendError, QuantumStateError

logger = logging.getLogger(__name__)


class Backend(ABC):
    """Abstract base class for quantum backends."""
    
    @abstractmethod
    def execute_circuit(self, circuit: Any, shots: int = 1024) -> Dict[str, int]:
        """Execute quantum circuit and return measurement counts."""
        pass
    
    @abstractmethod
    def get_statevector(self, circuit: Any) -> np.ndarray:
        """Get the state vector from a quantum circuit."""
        pass
    
    @abstractmethod
    def compute_expectation(self, circuit: Any, observable: Any) -> float:
        """Compute expectation value of observable."""
        pass


class ClassicalSimulator(Backend):
    """
    Classical simulation backend for quantum operations.
    
    Provides quantum circuit simulation using classical linear algebra
    operations. Suitable for small to medium-sized quantum circuits.
    """
    
    def __init__(self, max_qubits: int = 20, noise_model: Optional[Any] = None) -> None:
        """
        Initialize classical simulator.
        
        Args:
            max_qubits: Maximum number of qubits to simulate
            noise_model: Optional noise model for realistic simulation
        """
        self.max_qubits = max_qubits
        self.noise_model = noise_model
        self.name = "ClassicalSimulator"
        
        # State management
        self.current_state: Optional[np.ndarray] = None
        self.n_qubits: int = 0
        
        # Statistics
        self.execution_count = 0
        self.total_shots = 0
        
        logger.info(f"Initialized {self.name} with max {max_qubits} qubits")
    
    def initialize_state(self, n_qubits: int, initial_state: Optional[np.ndarray] = None) -> None:
        """
        Initialize quantum state.
        
        Args:
            n_qubits: Number of qubits
            initial_state: Initial state vector (defaults to |0...0⟩)
        """
        if n_qubits > self.max_qubits:
            raise BackendError(
                f"Requested {n_qubits} qubits exceeds maximum {self.max_qubits}",
                backend_name=self.name
            )
        
        self.n_qubits = n_qubits
        
        if initial_state is None:
            # Initialize to |0...0⟩ state
            state_size = 2 ** n_qubits
            self.current_state = np.zeros(state_size, dtype=complex)
            self.current_state[0] = 1.0
        else:
            if len(initial_state) != 2 ** n_qubits:
                raise QuantumStateError(
                    f"Initial state size {len(initial_state)} doesn't match {n_qubits} qubits"
                )
            self.current_state = initial_state.copy()
        
        logger.debug(f"Initialized {n_qubits}-qubit state")
    
    def apply_unitary(self, unitary: np.ndarray, qubits: List[int]) -> None:
        """
        Apply unitary operation to specified qubits.
        
        Args:
            unitary: Unitary matrix
            qubits: List of qubit indices to apply operation to
        """
        if self.current_state is None:
            raise BackendError("No quantum state initialized")
        
        if len(qubits) == 1:
            self._apply_single_qubit_unitary(unitary, qubits[0])
        elif len(qubits) == 2:
            self._apply_two_qubit_unitary(unitary, qubits[0], qubits[1])
        else:
            self._apply_multi_qubit_unitary(unitary, qubits)
    
    def _apply_single_qubit_unitary(self, unitary: np.ndarray, qubit: int) -> None:
        """Apply single-qubit unitary operation."""
        if unitary.shape != (2, 2):
            raise QuantumStateError("Single-qubit unitary must be 2x2")
        
        # Create full system unitary
        full_unitary = self._tensor_product_unitary(unitary, [qubit])
        
        # Apply to state
        self.current_state = full_unitary @ self.current_state
    
    def _apply_two_qubit_unitary(self, unitary: np.ndarray, qubit1: int, qubit2: int) -> None:
        """Apply two-qubit unitary operation."""
        if unitary.shape != (4, 4):
            raise QuantumStateError("Two-qubit unitary must be 4x4")
        
        # Create full system unitary
        full_unitary = self._tensor_product_unitary(unitary, [qubit1, qubit2])
        
        # Apply to state
        self.current_state = full_unitary @ self.current_state
    
    def _apply_multi_qubit_unitary(self, unitary: np.ndarray, qubits: List[int]) -> None:
        """Apply multi-qubit unitary operation."""
        expected_size = 2 ** len(qubits)
        if unitary.shape != (expected_size, expected_size):
            raise QuantumStateError(
                f"Multi-qubit unitary must be {expected_size}x{expected_size}"
            )
        
        # Create full system unitary
        full_unitary = self._tensor_product_unitary(unitary, qubits)
        
        # Apply to state
        self.current_state = full_unitary @ self.current_state
    
    def _tensor_product_unitary(self, unitary: np.ndarray, target_qubits: List[int]) -> np.ndarray:
        """Create full system unitary from local unitary and target qubits."""
        n_target = len(target_qubits)
        target_size = 2 ** n_target
        
        if unitary.shape != (target_size, target_size):
            raise QuantumStateError("Unitary size doesn't match number of target qubits")
        
        # Create identity for non-target qubits
        full_size = 2 ** self.n_qubits
        full_unitary = np.eye(full_size, dtype=complex)
        
        # For each basis state, apply the unitary to target qubits
        for i in range(full_size):
            for j in range(full_size):
                # Extract target qubit states
                i_target = self._extract_target_state(i, target_qubits)
                j_target = self._extract_target_state(j, target_qubits)
                
                # Check if non-target qubits are the same
                i_others = self._extract_other_state(i, target_qubits)
                j_others = self._extract_other_state(j, target_qubits)
                
                if i_others == j_others:
                    full_unitary[i, j] = unitary[i_target, j_target]
                else:
                    full_unitary[i, j] = 0.0
        
        return full_unitary
    
    def _extract_target_state(self, state_index: int, target_qubits: List[int]) -> int:
        """Extract target qubit states from full state index."""
        target_state = 0
        for i, qubit in enumerate(target_qubits):
            if (state_index >> qubit) & 1:
                target_state |= (1 << i)
        return target_state
    
    def _extract_other_state(self, state_index: int, target_qubits: List[int]) -> int:
        """Extract non-target qubit states from full state index."""
        other_state = 0
        bit_pos = 0
        
        for qubit in range(self.n_qubits):
            if qubit not in target_qubits:
                if (state_index >> qubit) & 1:
                    other_state |= (1 << bit_pos)
                bit_pos += 1
        
        return other_state
    
    def measure(self, qubits: Optional[List[int]] = None, shots: int = 1024) -> Dict[str, int]:
        """
        Perform measurement on specified qubits.
        
        Args:
            qubits: Qubits to measure (all if None)
            shots: Number of measurement shots
            
        Returns:
            Dictionary mapping measurement outcomes to counts
        """
        if self.current_state is None:
            raise BackendError("No quantum state to measure")
        
        if qubits is None:
            qubits = list(range(self.n_qubits))
        
        # Compute measurement probabilities
        probabilities = np.abs(self.current_state) ** 2
        
        # Generate measurement outcomes
        outcomes = {}
        
        for _ in range(shots):
            # Sample state based on probabilities
            state_idx = np.random.choice(len(probabilities), p=probabilities)
            
            # Extract measurement result for specified qubits
            measurement_string = ""
            for qubit in qubits:
                bit = (state_idx >> qubit) & 1
                measurement_string += str(bit)
            
            # Reverse to match standard qubit ordering (MSB first)
            measurement_string = measurement_string[::-1]
            
            outcomes[measurement_string] = outcomes.get(measurement_string, 0) + 1
        
        # Apply noise if noise model is present
        if self.noise_model:
            outcomes = self._apply_measurement_noise(outcomes, qubits)
        
        self.execution_count += 1
        self.total_shots += shots
        
        return outcomes
    
    def get_statevector(self) -> np.ndarray:
        """Get current quantum state vector."""
        if self.current_state is None:
            raise BackendError("No quantum state initialized")
        
        return self.current_state.copy()
    
    def get_probabilities(self, qubits: Optional[List[int]] = None) -> Dict[str, float]:
        """
        Get measurement probabilities for specified qubits.
        
        Args:
            qubits: Qubits to get probabilities for (all if None)
            
        Returns:
            Dictionary mapping measurement outcomes to probabilities
        """
        if self.current_state is None:
            raise BackendError("No quantum state initialized")
        
        if qubits is None:
            qubits = list(range(self.n_qubits))
        
        probabilities = {}
        state_probs = np.abs(self.current_state) ** 2
        
        for state_idx, prob in enumerate(state_probs):
            if prob > 1e-12:  # Only include non-negligible probabilities
                measurement_string = ""
                for qubit in qubits:
                    bit = (state_idx >> qubit) & 1
                    measurement_string += str(bit)
                
                measurement_string = measurement_string[::-1]
                probabilities[measurement_string] = probabilities.get(measurement_string, 0) + prob
        
        return probabilities
    
    def compute_expectation_value(self, observable: np.ndarray) -> float:
        """
        Compute expectation value of observable.
        
        Args:
            observable: Observable operator matrix
            
        Returns:
            Expectation value ⟨ψ|O|ψ⟩
        """
        if self.current_state is None:
            raise BackendError("No quantum state initialized")
        
        expected_size = 2 ** self.n_qubits
        if observable.shape != (expected_size, expected_size):
            raise QuantumStateError(
                f"Observable size {observable.shape} doesn't match state size {expected_size}"
            )
        
        # ⟨ψ|O|ψ⟩ = ψ†Oψ
        expectation = np.real(
            np.conj(self.current_state).T @ observable @ self.current_state
        )
        
        return float(expectation)
    
    def reset(self) -> None:
        """Reset simulator to initial state."""
        if self.n_qubits > 0:
            self.initialize_state(self.n_qubits)
    
    def _apply_measurement_noise(self, outcomes: Dict[str, int], qubits: List[int]) -> Dict[str, int]:
        """Apply measurement noise model (simplified)."""
        if not self.noise_model:
            return outcomes
        
        # Simple bit-flip noise model
        noise_rate = getattr(self.noise_model, 'measurement_error', 0.01)
        
        noisy_outcomes = {}
        
        for outcome, count in outcomes.items():
            for _ in range(count):
                noisy_outcome = ""
                
                for i, bit in enumerate(outcome):
                    if np.random.random() < noise_rate:
                        # Flip bit
                        noisy_bit = "1" if bit == "0" else "0"
                        noisy_outcome += noisy_bit
                    else:
                        noisy_outcome += bit
                
                noisy_outcomes[noisy_outcome] = noisy_outcomes.get(noisy_outcome, 0) + 1
        
        return noisy_outcomes
    
    def execute_circuit(self, circuit: Any, shots: int = 1024) -> Dict[str, int]:
        """Execute a quantum circuit (simplified interface)."""
        # This is a simplified interface for circuit execution
        # In practice, would parse circuit and apply operations sequentially
        
        if hasattr(circuit, 'operations'):
            # Apply each operation in the circuit
            for operation in circuit.operations:
                self._apply_operation(operation)
        
        # Perform measurement
        return self.measure(shots=shots)
    
    def _apply_operation(self, operation: Any) -> None:
        """Apply a single quantum operation."""
        # Simplified operation application
        # Would need more sophisticated parsing in practice
        
        if hasattr(operation, 'matrix') and hasattr(operation, 'qubits'):
            self.apply_unitary(operation.matrix, operation.qubits)
    
    def get_backend_info(self) -> Dict[str, Any]:
        """Get backend information and statistics."""
        return {
            "name": self.name,
            "type": "classical_simulator",
            "max_qubits": self.max_qubits,
            "current_qubits": self.n_qubits,
            "has_noise_model": self.noise_model is not None,
            "execution_count": self.execution_count,
            "total_shots": self.total_shots,
            "state_initialized": self.current_state is not None
        }


class NoiseModel:
    """Simple noise model for classical simulation."""
    
    def __init__(
        self,
        measurement_error: float = 0.01,
        gate_error: float = 0.001,
        decoherence_time: Optional[float] = None
    ) -> None:
        """
        Initialize noise model.
        
        Args:
            measurement_error: Probability of measurement bit flip
            gate_error: Probability of gate error
            decoherence_time: T2 decoherence time (microseconds)
        """
        self.measurement_error = measurement_error
        self.gate_error = gate_error
        self.decoherence_time = decoherence_time
    
    def apply_gate_noise(self, state: np.ndarray, gate_time: float = 0.1) -> np.ndarray:
        """Apply gate noise to quantum state."""
        # Simplified noise application
        if self.decoherence_time and gate_time > 0:
            # Apply dephasing
            decoherence_factor = np.exp(-gate_time / self.decoherence_time)
            
            # Simple dephasing model (loses off-diagonal elements)
            noisy_state = state.copy()
            for i in range(len(state)):
                if i > 0:  # Keep |0⟩ state, decohere superpositions
                    noisy_state[i] *= decoherence_factor
            
            # Renormalize
            norm = np.linalg.norm(noisy_state)
            if norm > 0:
                noisy_state /= norm
            
            return noisy_state
        
        return state
