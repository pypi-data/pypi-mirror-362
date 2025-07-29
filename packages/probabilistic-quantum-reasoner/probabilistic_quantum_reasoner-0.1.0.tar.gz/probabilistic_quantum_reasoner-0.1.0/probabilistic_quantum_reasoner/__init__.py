"""
Probabilistic Quantum Reasoner

A quantum-classical hybrid reasoning engine for uncertainty-aware AI inference.
This library fuses quantum probabilistic graphical models (QPGMs) with classical
probabilistic logic to enable advanced reasoning under uncertainty.

Author: Krishna Bajpai
Email: bajpaikrishna715@gmail.com
GitHub: https://github.com/krish567366/probabilistic-quantum-reasoner
"""

__version__ = "0.1.0"
__author__ = "Krishna Bajpai"
__email__ = "bajpaikrishna715@gmail.com"

# Core imports
from .core.network import QuantumBayesianNetwork
from .core.nodes import QuantumNode, StochasticNode, HybridNode
from .core.operators import QuantumOperator, UnitaryOperator, MeasurementOperator

# Inference engines
from .inference.engine import QuantumInferenceEngine
from .inference.causal import QuantumCausalInference
from .inference.belief_propagation import QuantumBeliefPropagation

# Backends
from .backends.qiskit_backend import QiskitBackend
from .backends.pennylane_backend import PennyLaneBackend
from .backends.simulator import ClassicalSimulator

# Exceptions
from .core.exceptions import (
    QuantumReasonerError,
    NetworkTopologyError,
    InferenceError,
    BackendError,
)

__all__ = [
    # Core classes
    "QuantumBayesianNetwork",
    "QuantumNode",
    "StochasticNode", 
    "HybridNode",
    "QuantumOperator",
    "UnitaryOperator",
    "MeasurementOperator",
    
    # Inference engines
    "QuantumInferenceEngine",
    "QuantumCausalInference",
    "QuantumBeliefPropagation",
    
    # Backends
    "QiskitBackend",
    "PennyLaneBackend",
    "ClassicalSimulator",
    
    # Exceptions
    "QuantumReasonerError",
    "NetworkTopologyError", 
    "InferenceError",
    "BackendError",
]

# Package metadata
__title__ = "probabilistic-quantum-reasoner"
__description__ = "A quantum-classical hybrid reasoning engine for uncertainty-aware AI inference"
__url__ = "https://github.com/krish567366/probabilistic-quantum-reasoner"
__version_info__ = tuple(int(i) for i in __version__.split("."))
