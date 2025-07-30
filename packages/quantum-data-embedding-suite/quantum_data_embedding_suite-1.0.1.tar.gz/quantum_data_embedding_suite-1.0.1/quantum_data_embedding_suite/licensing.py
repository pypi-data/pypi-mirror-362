"""
Quantum Data Embedding Suite Licensing Module

This module provides license validation and enforcement for all components
of the Quantum Data Embedding Suite package.
"""

import uuid
import platform
import hashlib
from typing import Optional, Dict, Any
from functools import wraps
from quantummeta_license import validate_or_grace, LicenseError


class LicenseManager:
    """Centralized license management for Quantum Data Embedding Suite."""
    
    PACKAGE_NAME = "quantum-data-embedding-suite"
    CONTACT_EMAIL = "bajpaikrishna715@gmail.com"
    
    def __init__(self):
        self._machine_id = self._generate_machine_id()
        self._system_info = self._get_system_info()
    
    def _generate_machine_id(self) -> str:
        """Generate a unique machine identifier."""
        # Combine multiple hardware identifiers for uniqueness
        mac_address = str(uuid.getnode())
        hostname = platform.node()
        system = platform.system()
        processor = platform.processor()
        
        # Create a hash of combined identifiers
        combined = f"{mac_address}-{hostname}-{system}-{processor}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def _get_system_info(self) -> Dict[str, str]:
        """Get system information for support purposes."""
        return {
            "system": platform.system(),
            "platform": platform.platform(),
            "architecture": platform.architecture()[0],
            "python_version": platform.python_version(),
            "hostname": platform.node(),
        }
    
    def validate_license(self, required_features: Optional[list] = None) -> bool:
        """
        Validate license for the package.
        
        Parameters
        ----------
        required_features : list, optional
            List of required features for validation
            
        Returns
        -------
        bool
            True if license is valid
            
        Raises
        ------
        LicenseValidationError
            If license validation fails
        """
        try:
            validate_or_grace(self.PACKAGE_NAME, required_features=required_features)
            return True
        except LicenseError as e:
            raise LicenseValidationError(
                original_error=e,
                machine_id=self._machine_id,
                system_info=self._system_info,
                contact_email=self.CONTACT_EMAIL,
                package_name=self.PACKAGE_NAME
            )
    
    def get_machine_id(self) -> str:
        """Get the machine ID for license activation."""
        return self._machine_id
    
    def get_system_info(self) -> Dict[str, str]:
        """Get system information."""
        return self._system_info.copy()


class LicenseValidationError(Exception):
    """Custom exception for license validation failures with detailed error information."""
    
    def __init__(
        self, 
        original_error: LicenseError,
        machine_id: str,
        system_info: Dict[str, str],
        contact_email: str,
        package_name: str
    ):
        self.original_error = original_error
        self.machine_id = machine_id
        self.system_info = system_info
        self.contact_email = contact_email
        self.package_name = package_name
        
        # Create detailed error message
        super().__init__(self._create_error_message())
    
    def _create_error_message(self) -> str:
        """Create a comprehensive error message with licensing information."""
        message = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    🚫 QUANTUM DATA EMBEDDING SUITE LICENSE ERROR             ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ❌ License Validation Failed                                                ║
║  📦 Package: {self.package_name:<56} ║
║  🔍 Error: {str(self.original_error):<58} ║
║                                                                               ║
║  💻 System Information:                                                      ║
║     • Machine ID: {self.machine_id:<51} ║
║     • System: {self.system_info.get('system', 'Unknown'):<59} ║
║     • Platform: {self.system_info.get('platform', 'Unknown')[:55]:<55} ║
║     • Python: {self.system_info.get('python_version', 'Unknown'):<59} ║
║                                                                               ║
║  📧 To obtain a valid license:                                               ║
║     • Contact: {self.contact_email:<55} ║
║     • Include your Machine ID in the email                                   ║
║     • Specify the features you need access to                                ║
║                                                                               ║
║  🔐 License Features Available:                                              ║
║     • Basic: Core embedding and kernel functionality                         ║
║     • Pro: Advanced algorithms and optimization                              ║
║     • Enterprise: Full feature set with priority support                     ║
║                                                                               ║
║  📚 For more information visit:                                              ║
║     https://github.com/krish567366/quantum-data-embedding-suite              ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
        return message


# Global license manager instance
_license_manager = LicenseManager()


def requires_license(features: Optional[list] = None):
    """
    Decorator to enforce license validation on classes and methods.
    
    Parameters
    ----------
    features : list, optional
        List of required license features
        
    Returns
    -------
    decorator
        License validation decorator
    """
    def decorator(cls_or_func):
        if isinstance(cls_or_func, type):
            # Class decorator
            original_init = cls_or_func.__init__
            
            @wraps(original_init)
            def licensed_init(self, *args, **kwargs):
                _license_manager.validate_license(features)
                original_init(self, *args, **kwargs)
            
            cls_or_func.__init__ = licensed_init
            return cls_or_func
        else:
            # Function decorator
            @wraps(cls_or_func)
            def licensed_function(*args, **kwargs):
                _license_manager.validate_license(features)
                return cls_or_func(*args, **kwargs)
            
            return licensed_function
    
    return decorator


def validate_license_for_class(cls, features: Optional[list] = None):
    """
    Class method to validate license during instantiation.
    
    Parameters
    ----------
    cls : class
        The class being instantiated
    features : list, optional
        Required license features
    """
    _license_manager.validate_license(features)


def get_machine_id() -> str:
    """Get the current machine ID for license activation."""
    return _license_manager.get_machine_id()


def get_system_info() -> Dict[str, str]:
    """Get system information for support purposes."""
    return _license_manager.get_system_info()


def validate_license_strict() -> None:
    """
    Strict license validation that blocks package usage.
    Raises an exception if license is not valid and grace period has expired.
    """
    try:
        from quantummeta_license import validate_or_grace, LicenseError
        validate_or_grace(_license_manager.PACKAGE_NAME)
    except LicenseError as e:
        # Check if this is a grace period expiry or no license at all
        error_str = str(e).lower()
        if "grace period" in error_str and "expired" in error_str:
            # Grace period has expired - block package completely
            raise LicenseValidationError(
                original_error=e,
                machine_id=_license_manager.get_machine_id(),
                system_info=_license_manager.get_system_info(),
                contact_email=_license_manager.CONTACT_EMAIL,
                package_name=_license_manager.PACKAGE_NAME
            )
        elif "no license" in error_str or "not found" in error_str:
            # No license found but might be in grace period
            # Allow import but show warning
            pass
        else:
            # Other license errors - block package
            raise LicenseValidationError(
                original_error=e,
                machine_id=_license_manager.get_machine_id(),
                system_info=_license_manager.get_system_info(),
                contact_email=_license_manager.CONTACT_EMAIL,
                package_name=_license_manager.PACKAGE_NAME
            )


def check_license_status() -> Dict[str, Any]:
    """
    Check current license status without raising exceptions.
    
    Returns
    -------
    dict
        License status information
    """
    try:
        _license_manager.validate_license()
        return {
            "status": "valid",
            "machine_id": _license_manager.get_machine_id(),
            "message": "License is valid and active"
        }
    except LicenseValidationError as e:
        return {
            "status": "invalid",
            "machine_id": _license_manager.get_machine_id(),
            "error": str(e.original_error),
            "message": "License validation failed"
        }
