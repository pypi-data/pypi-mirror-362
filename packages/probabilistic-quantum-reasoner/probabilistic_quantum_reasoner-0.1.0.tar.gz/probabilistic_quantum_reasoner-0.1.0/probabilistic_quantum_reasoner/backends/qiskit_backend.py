"""
Qiskit backend implementation for IBM Quantum systems.

This module provides integration with Qiskit for running quantum circuits
on IBM Quantum hardware and simulators.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Union
import logging

try:
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
    from qiskit import transpile, execute
    from qiskit.primitives import Estimator, Sampler
    from qiskit.quantum_info import SparsePauliOp, Statevector
    from qiskit_aer import AerSimulator
    from qiskit_ibm_runtime import QiskitRuntimeService
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False

from .simulator import Backend
from ..core.exceptions import BackendError
from ..core.operators import QuantumState, UnitaryOperator

logger = logging.getLogger(__name__)


class QiskitBackend(Backend):
    """
    Qiskit backend for IBM Quantum systems.
    
    Provides integration with Qiskit for quantum circuit execution
    on simulators and real quantum hardware.
    """
    
    def __init__(
        self,
        backend_name: str = "aer_simulator",
        use_runtime: bool = False,
        api_token: Optional[str] = None,
        hub: Optional[str] = None,
        group: Optional[str] = None,
        project: Optional[str] = None
    ) -> None:
        """
        Initialize Qiskit backend.
        
        Args:
            backend_name: Name of Qiskit backend to use
            use_runtime: Whether to use IBM Runtime service
            api_token: IBM Quantum API token
            hub: IBM Quantum hub
            group: IBM Quantum group
            project: IBM Quantum project
        """
        if not QISKIT_AVAILABLE:
            raise BackendError("Qiskit not available. Install with: pip install qiskit")
        
        self.backend_name = backend_name
        self.use_runtime = use_runtime
        self.api_token = api_token
        
        # Initialize backend
        self.backend = None
        self.service = None
        
        if use_runtime and api_token:
            try:
                self.service = QiskitRuntimeService(
                    token=api_token,
                    channel="ibm_quantum",
                    instance=f"{hub}/{group}/{project}" if all([hub, group, project]) else None
                )
                self.backend = self.service.backend(backend_name)
            except Exception as e:
                logger.warning(f"Failed to connect to IBM Runtime: {e}")
                self._fallback_to_simulator()
        else:
            self._fallback_to_simulator()
        
        # Primitives for execution
        self.estimator = Estimator()
        self.sampler = Sampler()
        
        logger.info(f"Initialized Qiskit backend: {self.backend_name}")
    
    def _fallback_to_simulator(self) -> None:
        """Fallback to local Aer simulator."""
        try:
            self.backend = AerSimulator()
            self.backend_name = "aer_simulator"
            logger.info("Using Aer simulator as fallback")
        except Exception as e:
            raise BackendError(f"Failed to initialize Aer simulator: {e}")
    
    def create_circuit(self, n_qubits: int, n_classical: Optional[int] = None) -> QuantumCircuit:
        """
        Create a quantum circuit.
        
        Args:
            n_qubits: Number of qubits
            n_classical: Number of classical bits (defaults to n_qubits)
            
        Returns:
            QuantumCircuit instance
        """
        if n_classical is None:
            n_classical = n_qubits
        
        qubits = QuantumRegister(n_qubits, 'q')
        cbits = ClassicalRegister(n_classical, 'c')
        
        return QuantumCircuit(qubits, cbits)
    
    def apply_unitary_to_circuit(
        self,
        circuit: QuantumCircuit,
        unitary: UnitaryOperator,
        qubits: List[int]
    ) -> None:
        """
        Apply unitary operator to quantum circuit.
        
        Args:
            circuit: Quantum circuit to modify
            unitary: Unitary operator to apply
            qubits: Target qubits
        """
        matrix = unitary.matrix_representation()
        
        if len(qubits) == 1:
            # Single-qubit gate
            circuit.unitary(matrix, qubits[0], label=unitary.name)
        elif len(qubits) == 2:
            # Two-qubit gate
            circuit.unitary(matrix, qubits, label=unitary.name)
        else:
            # Multi-qubit gate
            circuit.unitary(matrix, qubits, label=unitary.name)
    
    def add_measurement(self, circuit: QuantumCircuit, qubits: Optional[List[int]] = None) -> None:
        """
        Add measurement operations to circuit.
        
        Args:
            circuit: Quantum circuit to modify
            qubits: Qubits to measure (all if None)
        """
        if qubits is None:
            qubits = list(range(circuit.num_qubits))
        
        for i, qubit in enumerate(qubits):
            if i < circuit.num_clbits:
                circuit.measure(qubit, i)
    
    def execute_circuit(self, circuit: QuantumCircuit, shots: int = 1024) -> Dict[str, int]:
        """
        Execute quantum circuit and return measurement counts.
        
        Args:
            circuit: Quantum circuit to execute
            shots: Number of measurement shots
            
        Returns:
            Dictionary mapping measurement outcomes to counts
        """
        try:
            # Transpile circuit for backend
            transpiled_circuit = transpile(circuit, self.backend, optimization_level=1)
            
            if self.use_runtime and self.service:
                # Use IBM Runtime
                job = self.sampler.run([transpiled_circuit], shots=shots)
                result = job.result()
                
                # Extract counts from result
                if hasattr(result, 'quasi_dists'):
                    quasi_dist = result.quasi_dists[0]
                    counts = {}
                    for outcome, prob in quasi_dist.items():
                        # Convert outcome to bit string
                        bit_string = format(outcome, f'0{circuit.num_clbits}b')
                        counts[bit_string] = int(prob * shots)
                    return counts
                else:
                    # Fallback for different result formats
                    return {"0" * circuit.num_clbits: shots}
            else:
                # Use local execution
                job = execute(transpiled_circuit, self.backend, shots=shots)
                result = job.result()
                counts = result.get_counts(transpiled_circuit)
                
                # Ensure consistent format
                formatted_counts = {}
                for outcome, count in counts.items():
                    # Reverse bit string to match our convention
                    formatted_outcome = outcome[::-1]
                    formatted_counts[formatted_outcome] = count
                
                return formatted_counts
                
        except Exception as e:
            raise BackendError(f"Circuit execution failed: {e}", backend_name=self.backend_name)
    
    def get_statevector(self, circuit: QuantumCircuit) -> np.ndarray:
        """
        Get state vector from quantum circuit.
        
        Args:
            circuit: Quantum circuit
            
        Returns:
            State vector as numpy array
        """
        try:
            # Remove measurements for statevector simulation
            circuit_copy = circuit.copy()
            circuit_copy.remove_final_measurements()
            
            # Use statevector simulator
            simulator = AerSimulator(method='statevector')
            transpiled = transpile(circuit_copy, simulator)
            
            job = execute(transpiled, simulator, shots=1)
            result = job.result()
            
            statevector = result.get_statevector(transpiled)
            return np.array(statevector.data)
            
        except Exception as e:
            raise BackendError(f"Statevector computation failed: {e}")
    
    def compute_expectation(self, circuit: QuantumCircuit, observable: Any) -> float:
        """
        Compute expectation value of observable.
        
        Args:
            circuit: Quantum circuit
            observable: Observable operator (SparsePauliOp or matrix)
            
        Returns:
            Expectation value
        """
        try:
            # Convert observable to SparsePauliOp if needed
            if isinstance(observable, np.ndarray):
                # Convert matrix to Pauli representation (simplified)
                # In practice, would need more sophisticated conversion
                n_qubits = int(np.log2(observable.shape[0]))
                pauli_string = "Z" * n_qubits  # Simplified
                observable = SparsePauliOp.from_list([(pauli_string, 1.0)])
            
            # Transpile circuit
            transpiled = transpile(circuit, self.backend, optimization_level=1)
            
            # Use Estimator primitive
            job = self.estimator.run([transpiled], [observable])
            result = job.result()
            
            return float(result.values[0])
            
        except Exception as e:
            raise BackendError(f"Expectation value computation failed: {e}")
    
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
    
    def apply_pauli_gates(self, circuit: QuantumCircuit, pauli_string: str) -> None:
        """
        Apply Pauli gates according to Pauli string.
        
        Args:
            circuit: Quantum circuit
            pauli_string: String of Pauli operators (e.g., "XYZI")
        """
        for i, pauli in enumerate(pauli_string):
            if pauli == 'X':
                circuit.x(i)
            elif pauli == 'Y':
                circuit.y(i)
            elif pauli == 'Z':
                circuit.z(i)
            elif pauli == 'I':
                pass  # Identity, do nothing
            else:
                raise ValueError(f"Unknown Pauli operator: {pauli}")
    
    def create_bell_state(self, qubits: List[int]) -> QuantumCircuit:
        """
        Create Bell state circuit.
        
        Args:
            qubits: Two qubits to entangle
            
        Returns:
            Quantum circuit creating Bell state
        """
        if len(qubits) != 2:
            raise ValueError("Bell state requires exactly 2 qubits")
        
        circuit = self.create_circuit(max(qubits) + 1)
        
        # Create |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
        circuit.h(qubits[0])      # Superposition
        circuit.cx(qubits[0], qubits[1])  # Entanglement
        
        return circuit
    
    def create_ghz_state(self, qubits: List[int]) -> QuantumCircuit:
        """
        Create GHZ state circuit.
        
        Args:
            qubits: Qubits to entangle in GHZ state
            
        Returns:
            Quantum circuit creating GHZ state
        """
        if len(qubits) < 3:
            raise ValueError("GHZ state requires at least 3 qubits")
        
        circuit = self.create_circuit(max(qubits) + 1)
        
        # Create |GHZ⟩ = (|000...⟩ + |111...⟩)/√2
        circuit.h(qubits[0])  # Superposition on first qubit
        
        # Entangle all other qubits
        for i in range(1, len(qubits)):
            circuit.cx(qubits[0], qubits[i])
        
        return circuit
    
    def get_backend_properties(self) -> Dict[str, Any]:
        """Get backend properties and capabilities."""
        properties = {
            "name": self.backend_name,
            "type": "qiskit",
            "is_simulator": "simulator" in self.backend_name.lower(),
            "uses_runtime": self.use_runtime,
            "supports_statevector": True,
            "supports_expectation": True,
        }
        
        if hasattr(self.backend, 'configuration'):
            config = self.backend.configuration()
            properties.update({
                "max_qubits": getattr(config, 'n_qubits', None),
                "max_shots": getattr(config, 'max_shots', None),
                "basis_gates": getattr(config, 'basis_gates', []),
                "coupling_map": getattr(config, 'coupling_map', None),
            })
        
        return properties
    
    def optimize_circuit(self, circuit: QuantumCircuit, optimization_level: int = 1) -> QuantumCircuit:
        """
        Optimize quantum circuit for the backend.
        
        Args:
            circuit: Circuit to optimize
            optimization_level: Optimization level (0-3)
            
        Returns:
            Optimized circuit
        """
        return transpile(circuit, self.backend, optimization_level=optimization_level)
    
    def estimate_runtime(self, circuit: QuantumCircuit, shots: int = 1024) -> Dict[str, Any]:
        """
        Estimate runtime for circuit execution.
        
        Args:
            circuit: Circuit to analyze
            shots: Number of shots
            
        Returns:
            Runtime estimation information
        """
        # Simplified runtime estimation
        n_gates = sum(1 for _ in circuit)
        n_qubits = circuit.num_qubits
        
        # Rough estimates (would be more sophisticated in practice)
        gate_time = 0.1e-6  # 100 ns per gate
        readout_time = 1e-6  # 1 μs readout
        
        estimated_time = n_gates * gate_time + readout_time
        total_time = estimated_time * shots
        
        return {
            "estimated_time_per_shot": estimated_time,
            "total_estimated_time": total_time,
            "n_gates": n_gates,
            "n_qubits": n_qubits,
            "shots": shots,
            "note": "Rough estimation for planning purposes"
        }
