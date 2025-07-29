"""
Backend implementations for quantum computing frameworks.

This module provides backend abstractions for different quantum computing
frameworks including Qiskit, PennyLane, and classical simulation.
"""

from .qiskit_backend import QiskitBackend
from .pennylane_backend import PennyLaneBackend  
from .simulator import ClassicalSimulator

__all__ = [
    "QiskitBackend",
    "PennyLaneBackend",
    "ClassicalSimulator",
]
