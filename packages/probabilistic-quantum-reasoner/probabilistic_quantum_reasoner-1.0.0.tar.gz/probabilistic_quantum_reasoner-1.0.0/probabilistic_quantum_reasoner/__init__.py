"""
Probabilistic Quantum Reasoner

A quantum-classical hybrid reasoning engine for uncertainty-aware AI inference.
This library fuses quantum probabilistic graphical models (QPGMs) with classical
probabilistic logic to enable advanced reasoning under uncertainty.

Author: Krishna Bajpai
Email: bajpaikrishna715@gmail.com
GitHub: https://github.com/krish567366/probabilistic-quantum-reasoner

IMPORTANT: This software requires a valid QuantumMeta license.
Contact bajpaikrishna715@gmail.com for licensing information.
"""

__version__ = "0.1.0"
__author__ = "Krishna Bajpai"
__email__ = "bajpaikrishna715@gmail.com"

# Initialize license validation on import
from .licensing import get_license_manager, display_license_info, get_machine_id

# Validate core license immediately on package import with 24-hour grace period
try:
    _license_manager = get_license_manager()
    print("✅ Probabilistic Quantum Reasoner: License validated successfully")
    print(f"🔧 Machine ID: {get_machine_id()}")
    print(f"⏰ Grace Period: 24 hours for new installations")
except Exception as e:
    # Show license error but don't exit during grace period
    print(f"⚠️  License validation notice: {e}")
    print("📧 Contact bajpaikrishna715@gmail.com for licensing information")
    
    # Only exit if this is a hard license failure (not grace period)
    if "grace period" not in str(e).lower():
        import sys
        sys.exit(1)

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

# Licensing utilities
from .licensing import (
    get_machine_id,
    display_license_info,
    validate_license,
    LicenseError,
    LicenseExpiredError,
    FeatureNotLicensedError,
    LicenseNotFoundError
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
    
    # Licensing
    "get_machine_id",
    "display_license_info",
    "validate_license",
    "LicenseError",
    "LicenseExpiredError", 
    "FeatureNotLicensedError",
    "LicenseNotFoundError",
]

# Package metadata
__title__ = "probabilistic-quantum-reasoner"
__description__ = "A quantum-classical hybrid reasoning engine for uncertainty-aware AI inference"
__url__ = "https://github.com/krish567366/probabilistic-quantum-reasoner"
__version_info__ = tuple(int(i) for i in __version__.split("."))
