"""
Licensing module for Cognito Simulation Engine.

Provides comprehensive license validation with machine ID tracking,
class-level licensing, and secure validation without bypasses.
"""

import platform
import hashlib
import uuid
import subprocess
import sys
from functools import wraps
from typing import List, Optional, Any
from contextlib import contextmanager

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
    # Fallback classes for when quantummeta_license is not available
    class LicenseError(Exception): pass
    class LicenseExpiredError(LicenseError): pass
    class FeatureNotLicensedError(LicenseError): pass
    class LicenseNotFoundError(LicenseError): pass
    
    def validate_or_grace(package_name, required_features=None, grace_days=None):
        raise LicenseNotFoundError("License validation unavailable")

# Package constants
PACKAGE_NAME = "cognito-sim-engine"
SUPPORT_EMAIL = "bajpaikrishna715@gmail.com"
LICENSE_FEATURES = {
    "core": "Basic cognitive simulation features",
    "pro": "Advanced reasoning and memory systems", 
    "enterprise": "Large-scale simulations and distributed computing",
    "research": "Academic research and publication features"
}


class CognitoLicenseError(Exception):
    """Custom license error for Cognito Simulation Engine."""
    
    def __init__(self, message: str, machine_id: str = None, error_code: str = None):
        self.machine_id = machine_id or get_machine_id()
        self.error_code = error_code
        
        detailed_message = f"""
🔒 Cognito Simulation Engine - License Required

{message}

Machine ID: {self.machine_id}
Support Contact: {SUPPORT_EMAIL}

To resolve this issue:
1. Contact support with your Machine ID: {SUPPORT_EMAIL}
2. Provide this error code: {error_code or 'GENERAL_LICENSE_ERROR'}
3. Or activate an existing license: cognito-license activate <license_file>

Available License Tiers:
• Core: Basic cognitive simulation features
• Pro: Advanced reasoning and memory systems  
• Enterprise: Large-scale simulations and distributed computing
• Research: Academic research and publication features

Thank you for using Cognito Simulation Engine!
"""
        super().__init__(detailed_message)


def get_machine_id() -> str:
    """
    Generate a unique machine identifier.
    
    Returns:
        str: Unique machine identifier
    """
    try:
        # Try to get MAC address
        mac = uuid.getnode()
        mac_str = ':'.join(['{:02x}'.format((mac >> i) & 0xff) for i in range(0, 48, 8)])
        
        # Get system information
        system_info = {
            'platform': platform.platform(),
            'processor': platform.processor(),
            'machine': platform.machine(),
            'node': platform.node(),
            'mac': mac_str
        }
        
        # Create hash of system info
        info_string = '|'.join(f"{k}:{v}" for k, v in sorted(system_info.items()))
        machine_hash = hashlib.sha256(info_string.encode()).hexdigest()[:16].upper()
        
        return f"CSE-{machine_hash}"
        
    except Exception:
        # Fallback to a UUID if system info fails
        fallback_id = str(uuid.uuid4()).replace('-', '').upper()[:16]
        return f"CSE-{fallback_id}"


def validate_license(package_name: str = PACKAGE_NAME, 
                    required_features: Optional[List[str]] = None,
                    grace_days: int = 7) -> bool:
    """
    Validate license with comprehensive error handling.
    
    Args:
        package_name: Name of the package requiring license
        required_features: List of required features
        grace_days: Grace period in days
        
    Returns:
        bool: True if license is valid
        
    Raises:
        CognitoLicenseError: If license validation fails
    """
    if not QUANTUMMETA_AVAILABLE:
        raise CognitoLicenseError(
            "License validation system is not installed. Please install quantummeta-license.",
            error_code="SYSTEM_NOT_INSTALLED"
        )
    
    machine_id = get_machine_id()
    
    try:
        # Attempt license validation - NO DEVELOPMENT MODE BYPASS
        validate_or_grace(package_name, required_features=required_features, grace_days=grace_days)
        return True
        
    except LicenseExpiredError as e:
        raise CognitoLicenseError(
            f"Your license has expired. Please renew your license to continue using Cognito Simulation Engine.",
            machine_id=machine_id,
            error_code="LICENSE_EXPIRED"
        ) from e
        
    except FeatureNotLicensedError as e:
        feature_list = required_features or ["unknown"]
        raise CognitoLicenseError(
            f"Your license does not include the required features: {', '.join(feature_list)}. "
            f"Please upgrade your license to access these features.",
            machine_id=machine_id,
            error_code="FEATURE_NOT_LICENSED"
        ) from e
        
    except LicenseNotFoundError as e:
        raise CognitoLicenseError(
            f"No valid license found for Cognito Simulation Engine. "
            f"Please activate a license to use this software.",
            machine_id=machine_id,
            error_code="LICENSE_NOT_FOUND"
        ) from e
        
    except LicenseError as e:
        raise CognitoLicenseError(
            f"License validation failed: {str(e)}",
            machine_id=machine_id,
            error_code="VALIDATION_FAILED"
        ) from e


def requires_license(features: Optional[List[str]] = None, 
                    tier: Optional[str] = None):
    """
    Decorator for license-protected functions.
    
    Args:
        features: List of required features
        tier: License tier (core, pro, enterprise, research)
        
    Returns:
        Decorated function that validates license before execution
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Determine required features based on tier
            required_features = features or []
            if tier:
                if tier == "pro":
                    required_features = ["core", "pro"]
                elif tier == "enterprise":
                    required_features = ["core", "pro", "enterprise"]  
                elif tier == "research":
                    required_features = ["core", "research"]
                elif tier == "core":
                    required_features = ["core"]
            
            # Validate license
            validate_license(required_features=required_features)
            return func(*args, **kwargs)
        return wrapper
    return decorator


class LicensedClass:
    """
    Base class for license-protected classes.
    
    Provides automatic license validation for class instantiation
    and method-level feature gating.
    """
    
    def __init__(self, license_tier: str = "core", required_features: Optional[List[str]] = None):
        """
        Initialize with license validation.
        
        Args:
            license_tier: Required license tier (core, pro, enterprise, research)
            required_features: Specific features required
        """
        self._license_tier = license_tier
        self._required_features = required_features or []
        self._license_checked = {}
        self._machine_id = get_machine_id()
        
        # Validate base license on instantiation
        self._validate_class_license()
    
    def _validate_class_license(self):
        """Validate license for class instantiation."""
        features = self._required_features.copy()
        
        # Add tier-based features
        if self._license_tier == "pro":
            features.extend(["core", "pro"])
        elif self._license_tier == "enterprise":
            features.extend(["core", "pro", "enterprise"])
        elif self._license_tier == "research":
            features.extend(["core", "research"])
        elif self._license_tier == "core":
            features.append("core")
        
        # Remove duplicates
        features = list(set(features))
        
        try:
            validate_license(required_features=features)
        except CognitoLicenseError:
            raise
    
    def _ensure_feature_license(self, feature: str):
        """
        Ensure specific feature is licensed.
        
        Args:
            feature: Feature name to validate
            
        Raises:
            CognitoLicenseError: If feature is not licensed
        """
        if feature not in self._license_checked:
            try:
                validate_license(required_features=[feature])
                self._license_checked[feature] = True
            except CognitoLicenseError:
                self._license_checked[feature] = False
                raise
        
        if not self._license_checked[feature]:
            raise CognitoLicenseError(
                f"Feature '{feature}' is not available with your current license.",
                machine_id=self._machine_id,
                error_code="FEATURE_ACCESS_DENIED"
            )
    
    def get_machine_id(self) -> str:
        """Get the machine ID for this instance."""
        return self._machine_id
    
    def get_license_tier(self) -> str:
        """Get the license tier for this instance."""
        return self._license_tier


@contextmanager
def licensed_operation(features: Optional[List[str]] = None, 
                      tier: Optional[str] = None):
    """
    Context manager for license-protected operations.
    
    Args:
        features: Required features
        tier: Required license tier
        
    Yields:
        Context for licensed operation
        
    Raises:
        CognitoLicenseError: If license validation fails
    """
    # Determine required features
    required_features = features or []
    if tier:
        if tier == "pro":
            required_features.extend(["core", "pro"])
        elif tier == "enterprise":
            required_features.extend(["core", "pro", "enterprise"])
        elif tier == "research":
            required_features.extend(["core", "research"])
        elif tier == "core":
            required_features.append("core")
    
    # Remove duplicates
    required_features = list(set(required_features))
    
    try:
        # Validate license
        validate_license(required_features=required_features)
        yield
    except CognitoLicenseError:
        raise
    except Exception as e:
        # Re-raise other exceptions
        raise


def get_license_info() -> dict:
    """
    Get comprehensive license information.
    
    Returns:
        dict: License information including machine ID and status
    """
    machine_id = get_machine_id()
    
    if not QUANTUMMETA_AVAILABLE:
        return {
            "status": "error",
            "machine_id": machine_id,
            "error": "License system not available",
            "support_email": SUPPORT_EMAIL
        }
    
    try:
        # Try to validate basic license
        validate_license()
        return {
            "status": "licensed",
            "machine_id": machine_id,
            "package": PACKAGE_NAME,
            "support_email": SUPPORT_EMAIL,
            "available_features": LICENSE_FEATURES
        }
    except CognitoLicenseError as e:
        return {
            "status": "unlicensed",
            "machine_id": machine_id,
            "error": str(e),
            "error_code": e.error_code,
            "support_email": SUPPORT_EMAIL,
            "available_features": LICENSE_FEATURES
        }


def display_license_info():
    """Display license information to the user."""
    info = get_license_info()
    
    print("=" * 60)
    print("🧠 Cognito Simulation Engine - License Information")
    print("=" * 60)
    print(f"Machine ID: {info['machine_id']}")
    print(f"Status: {info['status'].upper()}")
    
    if info['status'] == 'licensed':
        print("✅ License is valid and active")
        print("\nAvailable Features:")
        for feature, description in LICENSE_FEATURES.items():
            print(f"  • {feature}: {description}")
    else:
        print("❌ License validation failed")
        if 'error' in info:
            print(f"Error: {info['error']}")
    
    print(f"\nSupport Contact: {SUPPORT_EMAIL}")
    print("=" * 60)


# Initialize license check on module import
def _init_license_check():
    """Initialize license check when module is imported."""
    try:
        validate_license()
        print("✅ Cognito Simulation Engine - License validated successfully")
    except CognitoLicenseError as e:
        print(f"⚠️ Cognito Simulation Engine - License Notice:")
        print(str(e))
        # Don't raise exception to allow graceful degradation
        # The specific classes/functions will enforce licensing


# Perform initial license check
_init_license_check()
