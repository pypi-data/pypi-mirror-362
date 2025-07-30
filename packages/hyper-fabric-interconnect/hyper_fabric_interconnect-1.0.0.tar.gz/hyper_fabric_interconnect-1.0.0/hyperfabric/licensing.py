"""
HyperFabric Interconnect Licensing System
Secure license validation with no bypass mechanisms.
"""

import platform
import hashlib
import uuid
from typing import List, Optional
from quantummeta_license import (
    validate_or_grace, 
    LicenseError, 
    LicenseExpiredError,
    FeatureNotLicensedError,
    LicenseNotFoundError
)

# Package licensing configuration
PACKAGE_NAME = "hyper-fabric-interconnect"
LICENSE_CONTACT_EMAIL = "bajpaikrishna715@gmail.com"

# License tiers and features
LICENSE_FEATURES = {
    "basic": ["core", "networking", "basic_routing"],
    "professional": ["core", "networking", "basic_routing", "ml_routing", "quantum_basic"],
    "enterprise": ["core", "networking", "basic_routing", "ml_routing", "quantum_basic", 
                   "quantum_advanced", "neuromorphic", "enterprise_analytics", "priority_support"]
}


def get_machine_id() -> str:
    """Generate unique machine identifier for licensing."""
    try:
        # Get MAC address
        mac = uuid.getnode()
        
        # Get system information
        system_info = f"{platform.system()}-{platform.machine()}-{platform.processor()}"
        
        # Create unique machine fingerprint
        machine_data = f"{mac}-{system_info}"
        machine_id = hashlib.sha256(machine_data.encode()).hexdigest()[:16]
        
        return machine_id.upper()
    except Exception:
        # Fallback to basic UUID if system info fails
        return str(uuid.uuid4()).replace("-", "")[:16].upper()


def format_license_error(error_type: str, features: Optional[List[str]] = None) -> str:
    """Format user-friendly license error messages."""
    machine_id = get_machine_id()
    
    base_message = f"""
╔══════════════════════════════════════════════════════════════╗
║                  HYPERFABRIC LICENSE REQUIRED                 ║
╠══════════════════════════════════════════════════════════════╣
║ Machine ID: {machine_id}                              ║
╠══════════════════════════════════════════════════════════════╣
"""
    
    if error_type == "expired":
        message = base_message + f"""║ 🕒 Your HyperFabric license has EXPIRED                       ║
║                                                              ║
║ To continue using HyperFabric Interconnect:                  ║
║   • Contact: {LICENSE_CONTACT_EMAIL}                    ║
║   • Include your Machine ID in the email                    ║
║   • Request license renewal                                  ║
║                                                              ║
║ No grace period or bypass available.                        ║
╚══════════════════════════════════════════════════════════════╝"""
    
    elif error_type == "feature_not_licensed":
        required_features_str = ", ".join(features) if features else "unknown"
        message = base_message + f"""║ 🔒 FEATURE NOT LICENSED                                       ║
║                                                              ║
║ Required features: {required_features_str:<38} ║
║                                                              ║
║ Available License Tiers:                                     ║
║   • BASIC: Core networking, basic routing                    ║
║   • PROFESSIONAL: + ML routing, basic quantum               ║
║   • ENTERPRISE: + Advanced quantum, neuromorphic, support   ║
║                                                              ║
║ To upgrade your license:                                     ║
║   • Contact: {LICENSE_CONTACT_EMAIL}                    ║
║   • Include your Machine ID: {machine_id}              ║
║   • Specify required tier                                    ║
╚══════════════════════════════════════════════════════════════╝"""
    
    elif error_type == "not_found":
        message = base_message + f"""║ 📋 NO VALID LICENSE FOUND                                     ║
║                                                              ║
║ HyperFabric Interconnect requires a valid license.          ║
║ No trial period or development mode available.              ║
║                                                              ║
║ To obtain a license:                                         ║
║   • Contact: {LICENSE_CONTACT_EMAIL}                    ║
║   • Include your Machine ID: {machine_id}              ║
║   • Specify your intended use case                          ║
║                                                              ║
║ License activation:                                          ║
║   hfabric license activate <license-file>                   ║
╚══════════════════════════════════════════════════════════════╝"""
    
    else:
        message = base_message + f"""║ ❌ LICENSE VALIDATION FAILED                                   ║
║                                                              ║
║ Contact technical support:                                   ║
║   • Email: {LICENSE_CONTACT_EMAIL}                      ║
║   • Include your Machine ID: {machine_id}              ║
║   • Describe the issue                                       ║
╚══════════════════════════════════════════════════════════════╝"""
    
    return message


class LicenseValidator:
    """Secure license validator with no bypass mechanisms."""
    
    def __init__(self):
        self._package_name = PACKAGE_NAME
        self._license_cache = {}
        self._machine_id = get_machine_id()
    
    def validate_license(self, required_features: Optional[List[str]] = None) -> bool:
        """
        Validate license with strict enforcement.
        
        Args:
            required_features: List of required features
            
        Returns:
            bool: True if licensed, raises exception otherwise
            
        Raises:
            LicenseError: If license validation fails
        """
        # NO DEVELOPMENT MODE - NO BYPASS - STRICT ENFORCEMENT
        try:
            # Always validate against the licensing server
            validate_or_grace(self._package_name, required_features=required_features)
            return True
            
        except LicenseExpiredError as e:
            error_msg = format_license_error("expired")
            print(error_msg)
            raise LicenseError(f"License expired. Machine ID: {self._machine_id}. Contact: {LICENSE_CONTACT_EMAIL}")
            
        except FeatureNotLicensedError as e:
            error_msg = format_license_error("feature_not_licensed", required_features)
            print(error_msg)
            raise LicenseError(f"Feature not licensed. Machine ID: {self._machine_id}. Contact: {LICENSE_CONTACT_EMAIL}")
            
        except LicenseNotFoundError as e:
            error_msg = format_license_error("not_found")
            print(error_msg)
            raise LicenseError(f"No license found. Machine ID: {self._machine_id}. Contact: {LICENSE_CONTACT_EMAIL}")
            
        except LicenseError as e:
            error_msg = format_license_error("general")
            print(error_msg)
            raise LicenseError(f"License validation failed. Machine ID: {self._machine_id}. Contact: {LICENSE_CONTACT_EMAIL}")
    
    def get_licensed_features(self) -> List[str]:
        """Get list of currently licensed features."""
        try:
            from quantummeta_license.core.license_manager import LicenseManager
            manager = LicenseManager()
            license_obj = manager.get_license(self._package_name)
            
            if license_obj and not license_obj.is_expired():
                return license_obj.features
            else:
                return []
        except Exception:
            return []
    
    def check_feature_availability(self, feature: str) -> bool:
        """Check if a specific feature is available."""
        try:
            self.validate_license([feature])
            return True
        except LicenseError:
            return False


# Global license validator instance
_license_validator = LicenseValidator()


def require_license(features: Optional[List[str]] = None):
    """
    Decorator for license-protected functions.
    
    Args:
        features: List of required features
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # STRICT LICENSE VALIDATION - NO BYPASS
            _license_validator.validate_license(features)
            return func(*args, **kwargs)
        return wrapper
    return decorator


class LicensedClass:
    """Base class for license-protected classes."""
    
    def __init__(self, license_tier: str = "basic"):
        """
        Initialize licensed class.
        
        Args:
            license_tier: Required license tier (basic, professional, enterprise)
        """
        self._license_tier = license_tier
        self._required_features = LICENSE_FEATURES.get(license_tier, ["core"])
        self._validator = _license_validator
        
        # IMMEDIATE LICENSE VALIDATION - NO GRACE PERIOD
        self._validate_class_license()
    
    def _validate_class_license(self):
        """Validate license for class instantiation."""
        try:
            self._validator.validate_license(self._required_features)
        except LicenseError as e:
            # Print detailed error and re-raise
            print(f"\n⚠️  Class instantiation failed - License validation required")
            raise e
    
    def _validate_method_license(self, additional_features: Optional[List[str]] = None):
        """Validate license for method execution."""
        features = self._required_features.copy()
        if additional_features:
            features.extend(additional_features)
        
        self._validator.validate_license(features)
    
    def get_license_info(self) -> dict:
        """Get current license information."""
        try:
            licensed_features = self._validator.get_licensed_features()
            return {
                "licensed": True,
                "tier": self._license_tier,
                "features": licensed_features,
                "machine_id": self._validator._machine_id
            }
        except Exception:
            return {
                "licensed": False,
                "tier": None,
                "features": [],
                "machine_id": self._validator._machine_id
            }


def validate_package_license():
    """Validate package-level license on import."""
    try:
        _license_validator.validate_license(["core"])
        return True
    except LicenseError:
        # License validation failed - allow import but restrict functionality
        return False


def get_machine_info() -> dict:
    """Get machine information for licensing support."""
    return {
        "machine_id": get_machine_id(),
        "platform": platform.platform(),
        "system": platform.system(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "contact_email": LICENSE_CONTACT_EMAIL
    }
