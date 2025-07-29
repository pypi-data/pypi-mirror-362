"""
Quantum operators for the probabilistic quantum reasoner.

This module provides quantum operators used in quantum Bayesian networks,
including unitary operations, measurement operators, and Kraus operators
for implementing quantum inference algorithms.
"""

import numpy as np
from abc import ABC, abstractmethod
from typing import Union, List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
import sympy as sp
from scipy.linalg import expm

from .exceptions import QuantumStateError, MeasurementError


@dataclass
class QuantumState:
    """Represents a quantum state with amplitudes and basis."""
    
    amplitudes: np.ndarray
    basis_labels: List[str]
    is_normalized: bool = True
    
    def __post_init__(self) -> None:
        """Validate quantum state after initialization."""
        if not self.is_normalized:
            self.normalize()
        self._validate_state()
    
    def normalize(self) -> None:
        """Normalize the quantum state amplitudes."""
        norm = np.linalg.norm(self.amplitudes)
        if norm > 0:
            self.amplitudes = self.amplitudes / norm
            self.is_normalized = True
    
    def _validate_state(self) -> None:
        """Validate quantum state properties."""
        if len(self.amplitudes) != len(self.basis_labels):
            raise QuantumStateError(
                "Amplitudes and basis labels must have same length",
                state_info={
                    "amplitudes_len": len(self.amplitudes),
                    "basis_len": len(self.basis_labels)
                }
            )
        
        if not np.isclose(np.linalg.norm(self.amplitudes), 1.0):
            raise QuantumStateError(
                "Quantum state must be normalized",
                state_info={"norm": np.linalg.norm(self.amplitudes)}
            )
    
    def probabilities(self) -> Dict[str, float]:
        """Get measurement probabilities for each basis state."""
        return {
            label: float(np.abs(amp) ** 2)
            for label, amp in zip(self.basis_labels, self.amplitudes)
        }
    
    def density_matrix(self) -> np.ndarray:
        """Compute the density matrix representation."""
        state_vector = self.amplitudes.reshape(-1, 1)
        return state_vector @ state_vector.conj().T


class QuantumOperator(ABC):
    """Abstract base class for quantum operators."""
    
    def __init__(self, name: str, dimension: int) -> None:
        self.name = name
        self.dimension = dimension
        self.matrix: Optional[np.ndarray] = None
    
    @abstractmethod
    def apply(self, state: QuantumState) -> QuantumState:
        """Apply the operator to a quantum state."""
        pass
    
    @abstractmethod
    def matrix_representation(self) -> np.ndarray:
        """Get the matrix representation of the operator."""
        pass
    
    def is_unitary(self) -> bool:
        """Check if the operator is unitary."""
        if self.matrix is None:
            matrix = self.matrix_representation()
        else:
            matrix = self.matrix
        
        return np.allclose(
            matrix @ matrix.conj().T,
            np.eye(self.dimension),
            rtol=1e-10
        )
    
    def is_hermitian(self) -> bool:
        """Check if the operator is Hermitian."""
        if self.matrix is None:
            matrix = self.matrix_representation()
        else:
            matrix = self.matrix
        
        return np.allclose(matrix, matrix.conj().T, rtol=1e-10)


class UnitaryOperator(QuantumOperator):
    """Unitary quantum operator for reversible quantum operations."""
    
    def __init__(
        self, 
        name: str, 
        matrix: Optional[np.ndarray] = None,
        generator: Optional[np.ndarray] = None,
        angle: float = 0.0
    ) -> None:
        if matrix is not None:
            self.matrix = matrix
            dimension = matrix.shape[0]
        elif generator is not None:
            self.generator = generator
            dimension = generator.shape[0]
            self.angle = angle
            self.matrix = expm(-1j * angle * generator)
        else:
            raise ValueError("Either matrix or generator must be provided")
        
        super().__init__(name, dimension)
        
        if not self.is_unitary():
            raise QuantumStateError(
                f"Matrix for {name} is not unitary",
                state_info={"matrix_shape": self.matrix.shape}
            )
    
    def apply(self, state: QuantumState) -> QuantumState:
        """Apply unitary transformation to quantum state."""
        if len(state.amplitudes) != self.dimension:
            raise QuantumStateError(
                "State dimension doesn't match operator dimension",
                state_info={
                    "state_dim": len(state.amplitudes),
                    "operator_dim": self.dimension
                }
            )
        
        new_amplitudes = self.matrix @ state.amplitudes
        return QuantumState(
            amplitudes=new_amplitudes,
            basis_labels=state.basis_labels,
            is_normalized=True
        )
    
    def matrix_representation(self) -> np.ndarray:
        """Get the unitary matrix representation."""
        return self.matrix
    
    def inverse(self) -> "UnitaryOperator":
        """Get the inverse (adjoint) of the unitary operator."""
        return UnitaryOperator(
            name=f"{self.name}_inv",
            matrix=self.matrix.conj().T
        )


class MeasurementOperator(QuantumOperator):
    """Measurement operator for quantum state collapse."""
    
    def __init__(
        self,
        name: str,
        projectors: List[np.ndarray],
        outcome_labels: List[str]
    ) -> None:
        if len(projectors) != len(outcome_labels):
            raise MeasurementError(
                "Number of projectors must match number of outcome labels",
                measurement_basis=name
            )
        
        self.projectors = projectors
        self.outcome_labels = outcome_labels
        dimension = projectors[0].shape[0]
        super().__init__(name, dimension)
        
        # Validate completeness relation
        total_projector = sum(projectors)
        if not np.allclose(total_projector, np.eye(dimension)):
            raise MeasurementError(
                "Projectors do not satisfy completeness relation",
                measurement_basis=name
            )
    
    def apply(self, state: QuantumState) -> QuantumState:
        """Apply measurement and return post-measurement state."""
        probabilities = self.measure_probabilities(state)
        
        # Sample outcome based on probabilities
        outcome_idx = np.random.choice(
            len(self.outcome_labels),
            p=list(probabilities.values())
        )
        
        return self.collapse_to_outcome(state, outcome_idx)
    
    def measure_probabilities(self, state: QuantumState) -> Dict[str, float]:
        """Calculate measurement outcome probabilities."""
        probabilities = {}
        for i, (projector, label) in enumerate(zip(self.projectors, self.outcome_labels)):
            # Born rule: P(outcome) = ⟨ψ|P_i|ψ⟩
            prob = np.real(
                state.amplitudes.conj().T @ projector @ state.amplitudes
            )
            probabilities[label] = float(max(0, prob))  # Ensure non-negative
        
        return probabilities
    
    def collapse_to_outcome(self, state: QuantumState, outcome_idx: int) -> QuantumState:
        """Collapse state to specific measurement outcome."""
        projector = self.projectors[outcome_idx]
        
        # Apply projector: |ψ'⟩ = P_i|ψ⟩ / √⟨ψ|P_i|ψ⟩
        projected_state = projector @ state.amplitudes
        norm = np.linalg.norm(projected_state)
        
        if norm < 1e-12:
            raise MeasurementError(
                f"Measurement outcome {self.outcome_labels[outcome_idx]} has zero probability"
            )
        
        collapsed_amplitudes = projected_state / norm
        
        return QuantumState(
            amplitudes=collapsed_amplitudes,
            basis_labels=state.basis_labels,
            is_normalized=True
        )
    
    def matrix_representation(self) -> np.ndarray:
        """Get matrix representation (sum of projectors)."""
        return sum(self.projectors)


class ParametricUnitaryOperator(UnitaryOperator):
    """Parametric unitary operator for variational quantum algorithms."""
    
    def __init__(
        self,
        name: str,
        parameter_symbols: List[sp.Symbol],
        generator_function: callable,
        initial_parameters: Optional[np.ndarray] = None
    ) -> None:
        self.parameter_symbols = parameter_symbols
        self.generator_function = generator_function
        
        if initial_parameters is None:
            initial_parameters = np.zeros(len(parameter_symbols))
        
        self.parameters = initial_parameters
        
        # Generate initial matrix
        generator = self._evaluate_generator(initial_parameters)
        super().__init__(name, generator=generator, angle=1.0)
    
    def _evaluate_generator(self, parameters: np.ndarray) -> np.ndarray:
        """Evaluate the generator with given parameters."""
        param_dict = {
            symbol: param for symbol, param in zip(self.parameter_symbols, parameters)
        }
        return self.generator_function(param_dict)
    
    def update_parameters(self, new_parameters: np.ndarray) -> None:
        """Update the operator parameters."""
        if len(new_parameters) != len(self.parameter_symbols):
            raise ValueError("Parameter count mismatch")
        
        self.parameters = new_parameters
        generator = self._evaluate_generator(new_parameters)
        self.matrix = expm(-1j * generator)
    
    def gradient(self, parameter_idx: int, epsilon: float = 1e-8) -> np.ndarray:
        """Compute parameter gradient using finite differences."""
        params_plus = self.parameters.copy()
        params_minus = self.parameters.copy()
        
        params_plus[parameter_idx] += epsilon
        params_minus[parameter_idx] -= epsilon
        
        matrix_plus = expm(-1j * self._evaluate_generator(params_plus))
        matrix_minus = expm(-1j * self._evaluate_generator(params_minus))
        
        return (matrix_plus - matrix_minus) / (2 * epsilon)


# Pre-defined common quantum gates
class PauliOperators:
    """Collection of Pauli operators."""
    
    @staticmethod
    def X() -> UnitaryOperator:
        """Pauli-X (NOT) gate."""
        return UnitaryOperator("Pauli-X", matrix=np.array([[0, 1], [1, 0]], dtype=complex))
    
    @staticmethod
    def Y() -> UnitaryOperator:
        """Pauli-Y gate."""
        return UnitaryOperator("Pauli-Y", matrix=np.array([[0, -1j], [1j, 0]], dtype=complex))
    
    @staticmethod
    def Z() -> UnitaryOperator:
        """Pauli-Z gate."""
        return UnitaryOperator("Pauli-Z", matrix=np.array([[1, 0], [0, -1]], dtype=complex))


class HadamardOperator(UnitaryOperator):
    """Hadamard gate for creating superposition."""
    
    def __init__(self) -> None:
        matrix = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
        super().__init__("Hadamard", matrix=matrix)


class CNOTOperator(UnitaryOperator):
    """Controlled-NOT gate for creating entanglement."""
    
    def __init__(self) -> None:
        matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0], 
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ], dtype=complex)
        super().__init__("CNOT", matrix=matrix)


class ComputationalBasisMeasurement(MeasurementOperator):
    """Standard computational basis measurement."""
    
    def __init__(self, dimension: int) -> None:
        projectors = []
        labels = []
        
        for i in range(dimension):
            projector = np.zeros((dimension, dimension), dtype=complex)
            projector[i, i] = 1.0
            projectors.append(projector)
            labels.append(f"|{i}⟩")
        
        super().__init__("Computational Basis", projectors, labels)
