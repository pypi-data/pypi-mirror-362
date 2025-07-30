"""
Example implementations demonstrating quantum Bayesian reasoning.

This module provides practical examples of quantum-classical hybrid reasoning
including weather-mood modeling, quantum XOR gates, and causal inference.
"""

from .weather_mood import WeatherMoodExample
from .quantum_xor import QuantumXORExample
from .prisoners_dilemma import QuantumPrisonersDilemmaExample

__all__ = [
    "WeatherMoodExample", 
    "QuantumXORExample",
    "QuantumPrisonersDilemmaExample",
]
