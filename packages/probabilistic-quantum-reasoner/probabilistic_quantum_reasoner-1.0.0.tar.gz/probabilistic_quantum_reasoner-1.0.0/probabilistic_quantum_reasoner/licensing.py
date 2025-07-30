"""
QuantumMeta License Manager for Probabilistic Quantum Reasoner.

This module provides comprehensive license validation for all quantum reasoning
operations with strict enforcement and no bypass mechanisms.
"""

import uuid
import platform
import hashlib
import socket
import os
from typing import Dict, List, Optional, Any
from functools import wraps
import sys

try:
    from quantummeta_license import (
        validate_or_grace, 
        LicenseError, 
        LicenseExpiredError,
        FeatureNotLicensedError,
        LicenseNotFoundError
    )
    QUANTUMMETA_AVAILABLE = True
except ImportError:
    QUANTUMMETA_AVAILABLE = False
    # Create dummy classes for type hinting
    class LicenseError(Exception):
        pass
    class LicenseExpiredError(LicenseError):
        pass
    class FeatureNotLicensedError(LicenseError):
        pass
    class LicenseNotFoundError(LicenseError):
        pass


class LicenseManager:
    """
    Manages licensing for Probabilistic Quantum Reasoner.
    
    This class provides license validation with a 24-hour grace period
    for new installations and license transitions.
    """
    
    # Package name for license validation
    PACKAGE_NAME = "probabilistic-quantum-reasoner"
    
    # Contact information for license issues
    CONTACT_EMAIL = "bajpaikrishna715@gmail.com"
    
    # Grace period in hours
    GRACE_PERIOD_HOURS = 24
    
    # Feature tiers
    FEATURE_TIERS = {
        "core": ["basic_networks", "classical_inference"],
        "pro": ["quantum_nodes", "quantum_inference", "entanglement", "causal_reasoning"],
        "enterprise": ["advanced_backends", "distributed_inference", "custom_operators", "optimization"]
    }
    
    def __init__(self):
        """Initialize the license manager."""
        self._machine_id = self._generate_machine_id()
        self._license_checked = {}
        
        # Perform immediate license check
        if not QUANTUMMETA_AVAILABLE:
            self._raise_license_error("QuantumMeta license system not available")
        
        self._validate_core_license()
    
    def _generate_machine_id(self) -> str:
        """
        Generate a unique machine identifier for license binding.
        
        Returns:
            str: Unique machine identifier
        """
        # Collect machine-specific information
        info_components = [
            platform.node(),  # Computer name
            platform.machine(),  # Machine type
            platform.processor(),  # Processor info
        ]
        
        # Add MAC address if available
        try:
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                           for elements in range(0, 2*6, 2)][::-1])
            info_components.append(mac)
        except:
            pass
        
        # Add hostname
        try:
            hostname = socket.gethostname()
            info_components.append(hostname)
        except:
            pass
        
        # Create hash from collected information
        machine_info = '|'.join(filter(None, info_components))
        machine_hash = hashlib.sha256(machine_info.encode()).hexdigest()[:16]
        
        return machine_hash.upper()
    
    def _validate_core_license(self) -> None:
        """
        Validate core license on initialization with 24-hour grace period.
        
        Raises:
            LicenseError: If core license validation fails after grace period
        """
        try:
            # Use 24-hour grace period (convert hours to days)
            grace_days = self.GRACE_PERIOD_HOURS / 24.0
            validate_or_grace(self.PACKAGE_NAME, required_features=["core"], grace_days=grace_days)
            self._license_checked["core"] = True
        except Exception as e:
            self._raise_license_error(f"Core license validation failed: {e}")
    
    def validate_feature_access(self, features: List[str]) -> None:
        """
        Validate access to specific features with 24-hour grace period.
        
        Args:
            features (List[str]): List of features to validate
            
        Raises:
            LicenseError: If any feature is not licensed after grace period
        """
        try:
            # Use 24-hour grace period (convert hours to days)
            grace_days = self.GRACE_PERIOD_HOURS / 24.0
            validate_or_grace(self.PACKAGE_NAME, required_features=features, grace_days=grace_days)
            
            # Cache successful validations
            for feature in features:
                self._license_checked[feature] = True
                
        except LicenseExpiredError as e:
            self._raise_license_expired_error()
        except FeatureNotLicensedError as e:
            self._raise_feature_not_licensed_error(features)
        except LicenseNotFoundError as e:
            self._raise_license_not_found_error()
        except Exception as e:
            self._raise_license_error(f"License validation failed: {e}")
    
    def get_licensed_features(self) -> List[str]:
        """
        Get list of currently licensed features with 24-hour grace period.
        
        Returns:
            List[str]: List of licensed features
        """
        licensed_features = []
        
        for tier, features in self.FEATURE_TIERS.items():
            try:
                # Use 24-hour grace period (convert hours to days)
                grace_days = self.GRACE_PERIOD_HOURS / 24.0
                validate_or_grace(self.PACKAGE_NAME, required_features=[tier], grace_days=grace_days)
                licensed_features.extend(features)
            except:
                continue
        
        return licensed_features
    
    def _raise_license_error(self, message: str) -> None:
        """
        Raise a license error with detailed information.
        
        Args:
            message (str): Error message
            
        Raises:
            LicenseError: Always raises this exception
        """
        error_msg = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        PROBABILISTIC QUANTUM REASONER                        ║
║                              LICENSE VALIDATION FAILED                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║ ERROR: {message:<64} ║
║                                                                              ║
║ This software requires a valid QuantumMeta license to operate.              ║
║ 🕒 Grace Period: {self.GRACE_PERIOD_HOURS} hours for new installations      ║
║                                                                              ║
║ 🔧 MACHINE ID: {self._machine_id:<52} ║
║                                                                              ║
║ 📧 TO OBTAIN A LICENSE:                                                     ║
║    Contact: {self.CONTACT_EMAIL:<57} ║
║    Include your Machine ID in the license request                           ║
║                                                                              ║
║ 🔑 AVAILABLE LICENSE TIERS:                                                 ║
║    • CORE: Basic networks and classical inference                           ║
║    • PRO: Quantum operations, entanglement, causal reasoning                ║
║    • ENTERPRISE: Advanced backends, distributed inference, optimization     ║
║                                                                              ║
║ ⏰ 24-HOUR GRACE PERIOD: Software continues to work during grace period     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        raise LicenseError(error_msg)
    
    def _raise_license_expired_error(self) -> None:
        """Raise error for expired license."""
        error_msg = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        PROBABILISTIC QUANTUM REASONER                        ║
║                                LICENSE EXPIRED                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║ 🕒 Your license has expired and is no longer valid.                         ║
║                                                                              ║
║ 🔧 MACHINE ID: {self._machine_id:<52} ║
║                                                                              ║
║ 📧 TO RENEW YOUR LICENSE:                                                   ║
║    Contact: {self.CONTACT_EMAIL:<57} ║
║    Include your Machine ID for license renewal                              ║
║                                                                              ║
║ ⚠️  NO GRACE PERIOD OR BYPASS AVAILABLE                                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        raise LicenseExpiredError(error_msg)
    
    def _raise_feature_not_licensed_error(self, features: List[str]) -> None:
        """Raise error for unlicensed features."""
        features_str = ", ".join(features)
        error_msg = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        PROBABILISTIC QUANTUM REASONER                        ║
║                           FEATURE NOT LICENSED                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║ 🔒 The following features require a higher license tier:                    ║
║    {features_str:<70} ║
║                                                                              ║
║ 🔧 MACHINE ID: {self._machine_id:<52} ║
║                                                                              ║
║ 📧 TO UPGRADE YOUR LICENSE:                                                 ║
║    Contact: {self.CONTACT_EMAIL:<57} ║
║    Include your Machine ID and desired feature tier                         ║
║                                                                              ║
║ 🔑 AVAILABLE LICENSE TIERS:                                                 ║
║    • CORE: Basic networks and classical inference                           ║
║    • PRO: Quantum operations, entanglement, causal reasoning                ║
║    • ENTERPRISE: Advanced backends, distributed inference, optimization     ║
║                                                                              ║
║ ⏰ 24-HOUR GRACE PERIOD: Software continues to work during grace period     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        raise FeatureNotLicensedError(error_msg)
    
    def _raise_license_not_found_error(self) -> None:
        """Raise error for missing license."""
        error_msg = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        PROBABILISTIC QUANTUM REASONER                        ║
║                             NO LICENSE FOUND                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║ 📋 No valid license was found for this software.                           ║
║ 🕒 Grace Period: {self.GRACE_PERIOD_HOURS} hours for new installations      ║
║                                                                              ║
║ 🔧 MACHINE ID: {self._machine_id:<52} ║
║                                                                              ║
║ 📧 TO OBTAIN A LICENSE:                                                     ║
║    Contact: {self.CONTACT_EMAIL:<57} ║
║    Include your Machine ID in the license request                           ║
║                                                                              ║
║ 🔑 AVAILABLE LICENSE TIERS:                                                 ║
║    • CORE: Basic networks and classical inference                           ║
║    • PRO: Quantum operations, entanglement, causal reasoning                ║
║    • ENTERPRISE: Advanced backends, distributed inference, optimization     ║
║                                                                              ║
║ ⏰ 24-HOUR GRACE PERIOD: Software continues to work during grace period     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        raise LicenseNotFoundError(error_msg)


def requires_license(features: List[str]):
    """
    Decorator to enforce license validation for functions/methods.
    
    Args:
        features (List[str]): Required features for the decorated function
        
    Returns:
        Callable: Decorated function with license validation
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get license manager instance
            if hasattr(args[0], '_license_manager'):
                license_manager = args[0]._license_manager
            else:
                license_manager = LicenseManager()
            
            # Validate feature access
            license_manager.validate_feature_access(features)
            
            # Execute original function
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def requires_license_class(required_features: Dict[str, List[str]]):
    """
    Class decorator to enforce license validation for class instantiation and methods.
    
    Args:
        required_features (Dict[str, List[str]]): Mapping of method names to required features
        
    Returns:
        Callable: Decorated class with license validation
    """
    def decorator(cls):
        # Store original __init__
        original_init = cls.__init__
        
        @wraps(original_init)
        def licensed_init(self, *args, **kwargs):
            # Initialize license manager
            self._license_manager = LicenseManager()
            
            # Validate core features for class instantiation
            if "core" in required_features:
                self._license_manager.validate_feature_access(required_features["core"])
            
            # Call original __init__
            original_init(self, *args, **kwargs)
        
        # Replace __init__
        cls.__init__ = licensed_init
        
        # Add license validation to specified methods
        for method_name, features in required_features.items():
            if method_name == "core":
                continue  # Already handled in __init__
            
            if hasattr(cls, method_name):
                original_method = getattr(cls, method_name)
                
                @wraps(original_method)
                def licensed_method(self, *args, _method=original_method, _features=features, **kwargs):
                    # Validate feature access
                    self._license_manager.validate_feature_access(_features)
                    
                    # Execute original method
                    return _method(self, *args, **kwargs)
                
                setattr(cls, method_name, licensed_method)
        
        return cls
    
    return decorator


# Global license manager instance
_global_license_manager = None

def get_license_manager() -> LicenseManager:
    """
    Get or create the global license manager instance.
    
    Returns:
        LicenseManager: Global license manager instance
    """
    global _global_license_manager
    if _global_license_manager is None:
        _global_license_manager = LicenseManager()
    return _global_license_manager


def validate_license(features: Optional[List[str]] = None) -> None:
    """
    Validate license for specified features.
    
    Args:
        features (Optional[List[str]]): Features to validate. If None, validates core license.
    """
    manager = get_license_manager()
    if features is None:
        features = ["core"]
    manager.validate_feature_access(features)


def get_machine_id() -> str:
    """
    Get the machine ID for license binding.
    
    Returns:
        str: Machine ID
    """
    manager = get_license_manager()
    return manager._machine_id


def display_license_info() -> None:
    """Display current license information."""
    try:
        manager = get_license_manager()
        licensed_features = manager.get_licensed_features()
        
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        PROBABILISTIC QUANTUM REASONER                        ║
║                              LICENSE INFORMATION                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║ 🔧 MACHINE ID: {manager._machine_id:<52} ║
║ ⏰ GRACE PERIOD: {manager.GRACE_PERIOD_HOURS} hours for new installations    ║
║                                                                              ║
║ ✅ LICENSED FEATURES:                                                       ║
""")
        
        for feature in licensed_features:
            print(f"║    • {feature:<66} ║")
        
        print(f"""║                                                                              ║
║ 📧 LICENSE SUPPORT: {manager.CONTACT_EMAIL:<49} ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
        
    except Exception as e:
        print(f"❌ License information unavailable: {e}")
