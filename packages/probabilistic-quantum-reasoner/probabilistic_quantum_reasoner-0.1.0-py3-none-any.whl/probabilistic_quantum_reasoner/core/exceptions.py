"""
Exception classes for the probabilistic quantum reasoner library.

This module defines custom exceptions used throughout the library to provide
clear error messages and appropriate error handling for quantum reasoning operations.
"""

from typing import Optional, Any


class QuantumReasonerError(Exception):
    """Base exception class for all quantum reasoner errors."""
    
    def __init__(self, message: str, details: Optional[dict] = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self) -> str:
        if self.details:
            detail_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} (Details: {detail_str})"
        return self.message


class NetworkTopologyError(QuantumReasonerError):
    """Raised when there are issues with network topology or structure."""
    
    def __init__(
        self, 
        message: str, 
        node_id: Optional[str] = None,
        edge_info: Optional[tuple] = None,
        **kwargs
    ) -> None:
        details = {}
        if node_id:
            details["node_id"] = node_id
        if edge_info:
            details["edge"] = edge_info
        details.update(kwargs)
        super().__init__(message, details)


class InferenceError(QuantumReasonerError):
    """Raised when inference operations fail or produce invalid results."""
    
    def __init__(
        self,
        message: str,
        algorithm: Optional[str] = None,
        convergence_info: Optional[dict] = None,
        **kwargs
    ) -> None:
        details = {}
        if algorithm:
            details["algorithm"] = algorithm
        if convergence_info:
            details.update(convergence_info)
        details.update(kwargs)
        super().__init__(message, details)


class BackendError(QuantumReasonerError):
    """Raised when quantum backend operations fail."""
    
    def __init__(
        self,
        message: str,
        backend_name: Optional[str] = None,
        backend_error: Optional[Exception] = None,
        **kwargs
    ) -> None:
        details = {}
        if backend_name:
            details["backend"] = backend_name
        if backend_error:
            details["original_error"] = str(backend_error)
        details.update(kwargs)
        super().__init__(message, details)


class QuantumStateError(QuantumReasonerError):
    """Raised when quantum state operations are invalid."""
    
    def __init__(
        self,
        message: str,
        state_info: Optional[dict] = None,
        **kwargs
    ) -> None:
        details = {}
        if state_info:
            details.update(state_info)
        details.update(kwargs)
        super().__init__(message, details)


class EntanglementError(QuantumReasonerError):
    """Raised when entanglement operations fail or are invalid."""
    
    def __init__(
        self,
        message: str,
        entangled_nodes: Optional[list] = None,
        **kwargs
    ) -> None:
        details = {}
        if entangled_nodes:
            details["entangled_nodes"] = entangled_nodes
        details.update(kwargs)
        super().__init__(message, details)


class MeasurementError(QuantumReasonerError):
    """Raised when quantum measurement operations fail."""
    
    def __init__(
        self,
        message: str,
        measurement_basis: Optional[str] = None,
        **kwargs
    ) -> None:
        details = {}
        if measurement_basis:
            details["measurement_basis"] = measurement_basis
        details.update(kwargs)
        super().__init__(message, details)


class CausalInferenceError(InferenceError):
    """Raised when causal inference operations fail."""
    
    def __init__(
        self,
        message: str,
        intervention: Optional[dict] = None,
        confounders: Optional[list] = None,
        **kwargs
    ) -> None:
        details = {}
        if intervention:
            details["intervention"] = intervention
        if confounders:
            details["confounders"] = confounders
        details.update(kwargs)
        super().__init__(message, **details)
