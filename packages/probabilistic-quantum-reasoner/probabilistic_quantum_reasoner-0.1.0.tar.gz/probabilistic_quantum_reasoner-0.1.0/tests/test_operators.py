"""
Unit tests for core quantum operators.
"""

import pytest
import numpy as np
from probabilistic_quantum_reasoner.core.operators import (
    UnitaryOperator, MeasurementOperator, QuantumGate
)
from .conftest import assert_quantum_amplitudes_normalized, QuantumTestUtils


class TestUnitaryOperator:
    """Test unitary operator functionality."""
    
    def test_pauli_x_gate(self):
        """Test Pauli-X gate application."""
        # Create Pauli-X gate
        pauli_x = QuantumGate.pauli_x()
        
        # Test on |0⟩ state
        state_0 = np.array([1, 0], dtype=complex)
        result = pauli_x.apply(state_0)
        expected = np.array([0, 1], dtype=complex)
        
        np.testing.assert_allclose(result, expected)
        assert_quantum_amplitudes_normalized(result)
    
    def test_pauli_y_gate(self):
        """Test Pauli-Y gate application."""
        pauli_y = QuantumGate.pauli_y()
        
        # Test on |0⟩ state
        state_0 = np.array([1, 0], dtype=complex)
        result = pauli_y.apply(state_0)
        expected = np.array([0, 1j], dtype=complex)
        
        np.testing.assert_allclose(result, expected)
        assert_quantum_amplitudes_normalized(result)
    
    def test_pauli_z_gate(self):
        """Test Pauli-Z gate application."""
        pauli_z = QuantumGate.pauli_z()
        
        # Test on |1⟩ state
        state_1 = np.array([0, 1], dtype=complex)
        result = pauli_z.apply(state_1)
        expected = np.array([0, -1], dtype=complex)
        
        np.testing.assert_allclose(result, expected)
        assert_quantum_amplitudes_normalized(result)
    
    def test_hadamard_gate(self):
        """Test Hadamard gate creates superposition."""
        hadamard = QuantumGate.hadamard()
        
        # Test on |0⟩ state
        state_0 = np.array([1, 0], dtype=complex)
        result = hadamard.apply(state_0)
        expected = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
        
        np.testing.assert_allclose(result, expected)
        assert_quantum_amplitudes_normalized(result)
    
    def test_rotation_gates(self):
        """Test parametric rotation gates."""
        # Test X rotation
        angle = np.pi / 4
        rx = QuantumGate.rotation_x(angle)
        
        state_0 = np.array([1, 0], dtype=complex)
        result = rx.apply(state_0)
        
        # Should be cos(θ/2)|0⟩ - i*sin(θ/2)|1⟩
        expected = np.array([
            np.cos(angle/2),
            -1j * np.sin(angle/2)
        ], dtype=complex)
        
        np.testing.assert_allclose(result, expected, atol=1e-10)
        assert_quantum_amplitudes_normalized(result)
    
    def test_controlled_not_gate(self):
        """Test CNOT gate on two-qubit system."""
        cnot = QuantumGate.controlled_not()
        
        # Test |10⟩ -> |11⟩
        state_10 = np.array([0, 0, 1, 0], dtype=complex)
        result = cnot.apply(state_10)
        expected = np.array([0, 0, 0, 1], dtype=complex)  # |11⟩
        
        np.testing.assert_allclose(result, expected)
        assert_quantum_amplitudes_normalized(result)
    
    def test_unitary_composition(self):
        """Test composition of unitary operators."""
        # H followed by X should give |+⟩ -> |-⟩
        hadamard = QuantumGate.hadamard()
        pauli_x = QuantumGate.pauli_x()
        
        state_0 = np.array([1, 0], dtype=complex)
        
        # Apply H then X
        plus_state = hadamard.apply(state_0)
        minus_state = pauli_x.apply(plus_state)
        
        expected = np.array([1/np.sqrt(2), -1/np.sqrt(2)], dtype=complex)
        np.testing.assert_allclose(minus_state, expected)
    
    def test_unitary_property(self):
        """Test that operators are actually unitary."""
        gates = [
            QuantumGate.pauli_x(),
            QuantumGate.pauli_y(),
            QuantumGate.pauli_z(),
            QuantumGate.hadamard()
        ]
        
        for gate in gates:
            U = gate.matrix
            U_dagger = U.conj().T
            identity = U @ U_dagger
            
            expected_identity = np.eye(U.shape[0])
            np.testing.assert_allclose(identity, expected_identity, atol=1e-10)


class TestMeasurementOperator:
    """Test measurement operator functionality."""
    
    def test_computational_basis_measurement(self):
        """Test measurement in computational basis."""
        measurement = MeasurementOperator.computational_basis(2)
        
        # Test on |+⟩ state
        plus_state = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
        
        # Should get |0⟩ or |1⟩ with equal probability
        result = measurement.measure(plus_state)
        
        assert "outcome" in result
        assert result["outcome"] in [0, 1]
        assert "probability" in result
        assert 0 <= result["probability"] <= 1
        assert "post_measurement_state" in result
        
        # Post-measurement state should be normalized
        post_state = result["post_measurement_state"]
        assert_quantum_amplitudes_normalized(post_state)
    
    def test_pauli_z_measurement(self):
        """Test Pauli-Z measurement."""
        measurement = MeasurementOperator.pauli_z()
        
        # Test on |0⟩ state (eigenstate with eigenvalue +1)
        state_0 = np.array([1, 0], dtype=complex)
        result = measurement.measure(state_0)
        
        assert result["outcome"] == 1  # +1 eigenvalue
        assert abs(result["probability"] - 1.0) < 1e-10
        np.testing.assert_allclose(result["post_measurement_state"], state_0)
    
    def test_pauli_x_measurement(self):
        """Test Pauli-X measurement."""
        measurement = MeasurementOperator.pauli_x()
        
        # Test on |+⟩ state (eigenstate with eigenvalue +1)
        plus_state = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
        result = measurement.measure(plus_state)
        
        assert result["outcome"] == 1  # +1 eigenvalue
        assert abs(result["probability"] - 1.0) < 1e-10
    
    def test_measurement_statistics(self):
        """Test measurement statistics over many runs."""
        measurement = MeasurementOperator.computational_basis(2)
        plus_state = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
        
        outcomes = []
        n_measurements = 1000
        
        for _ in range(n_measurements):
            result = measurement.measure(plus_state)
            outcomes.append(result["outcome"])
        
        # Should get roughly 50/50 split
        count_0 = outcomes.count(0)
        count_1 = outcomes.count(1)
        
        # Allow some statistical fluctuation
        assert abs(count_0 - n_measurements/2) < n_measurements * 0.1
        assert abs(count_1 - n_measurements/2) < n_measurements * 0.1
    
    def test_born_rule(self):
        """Test Born rule for measurement probabilities."""
        measurement = MeasurementOperator.computational_basis(2)
        
        # Create state |ψ⟩ = α|0⟩ + β|1⟩
        alpha = 0.6
        beta = 0.8
        state = np.array([alpha, beta], dtype=complex)
        
        # Measure multiple times to get statistics
        outcomes = []
        for _ in range(1000):
            result = measurement.measure(state)
            outcomes.append(result["outcome"])
        
        prob_0 = outcomes.count(0) / 1000
        prob_1 = outcomes.count(1) / 1000
        
        # Born rule: P(0) = |α|², P(1) = |β|²
        expected_prob_0 = abs(alpha) ** 2
        expected_prob_1 = abs(beta) ** 2
        
        assert abs(prob_0 - expected_prob_0) < 0.05
        assert abs(prob_1 - expected_prob_1) < 0.05


class TestQuantumGateLibrary:
    """Test the quantum gate library."""
    
    def test_all_gates_unitary(self):
        """Test that all predefined gates are unitary."""
        gates = [
            QuantumGate.identity(2),
            QuantumGate.pauli_x(),
            QuantumGate.pauli_y(),
            QuantumGate.pauli_z(),
            QuantumGate.hadamard(),
            QuantumGate.phase(np.pi/4),
            QuantumGate.rotation_x(np.pi/3),
            QuantumGate.rotation_y(np.pi/3),
            QuantumGate.rotation_z(np.pi/3),
            QuantumGate.controlled_not()
        ]
        
        for gate in gates:
            U = gate.matrix
            U_dagger = U.conj().T
            product = U @ U_dagger
            
            expected = np.eye(U.shape[0])
            np.testing.assert_allclose(product, expected, atol=1e-10)
    
    def test_gate_dimensions(self):
        """Test gate matrix dimensions."""
        assert QuantumGate.pauli_x().matrix.shape == (2, 2)
        assert QuantumGate.hadamard().matrix.shape == (2, 2)
        assert QuantumGate.controlled_not().matrix.shape == (4, 4)
    
    def test_custom_unitary(self):
        """Test custom unitary operator creation."""
        # Create random unitary matrix
        random_unitary = QuantumTestUtils.create_random_unitary(2)
        
        gate = UnitaryOperator(random_unitary)
        
        # Test that it preserves normalization
        state = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
        result = gate.apply(state)
        
        assert_quantum_amplitudes_normalized(result)
    
    @pytest.mark.parametrize("angle", [0, np.pi/4, np.pi/2, np.pi, 2*np.pi])
    def test_rotation_angles(self, angle):
        """Test rotation gates with various angles."""
        rx = QuantumGate.rotation_x(angle)
        ry = QuantumGate.rotation_y(angle) 
        rz = QuantumGate.rotation_z(angle)
        
        state = np.array([1, 0], dtype=complex)
        
        for gate in [rx, ry, rz]:
            result = gate.apply(state)
            assert_quantum_amplitudes_normalized(result)
    
    def test_entangling_gates(self):
        """Test that CNOT creates entanglement."""
        cnot = QuantumGate.controlled_not()
        hadamard = QuantumGate.hadamard()
        
        # Create |+0⟩ = (|00⟩ + |10⟩)/√2
        state_00 = np.array([1, 0, 0, 0], dtype=complex)  # |00⟩
        state_10 = np.array([0, 0, 1, 0], dtype=complex)  # |10⟩
        plus_0_state = (state_00 + state_10) / np.sqrt(2)
        
        # Apply CNOT to get Bell state
        bell_state = cnot.apply(plus_0_state)
        expected_bell = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)], dtype=complex)
        
        np.testing.assert_allclose(bell_state, expected_bell, atol=1e-10)
        assert_quantum_amplitudes_normalized(bell_state)
