"""
Inference module for the probabilistic quantum reasoner.

This module contains various inference algorithms for quantum-classical hybrid
probabilistic graphical models, including belief propagation, variational
inference, and causal reasoning.
"""

from .engine import QuantumInferenceEngine
from .belief_propagation import QuantumBeliefPropagation, Message
from .causal import QuantumCausalInference
from .variational import VariationalQuantumInference

__all__ = [
    "QuantumInferenceEngine",
    "QuantumBeliefPropagation",
    "Message",
    "QuantumCausalInference", 
    "VariationalQuantumInference",
]
