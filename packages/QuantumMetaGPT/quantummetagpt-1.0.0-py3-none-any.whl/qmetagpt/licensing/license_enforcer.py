"""
QuantumMetaGPT License Enforcer
Robust license validation with no bypass mechanisms.
"""

import platform
import uuid
import hashlib
import sys
import os
from functools import wraps
from typing import List, Optional, Any, Type
import inspect

# Import QuantumMeta License components
try:
    from quantummeta_license import validate_license, LicenseError
    from quantummeta_license import LicenseExpiredError, FeatureNotLicensedError, LicenseNotFoundError
    LICENSING_AVAILABLE = True
except ImportError:
    print("⚠️ QuantumMeta License package not found. Please install: pip install quantummeta-license")
    LICENSING_AVAILABLE = False


class LicenseEnforcementError(Exception):
    """Custom exception for license enforcement failures."""
    pass


def get_machine_id() -> str:
    """Generate a unique machine identifier."""
    try:
        # Get system information
        system_info = {
            'platform': platform.platform(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'node': platform.node(),
            'mac_address': ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
                                   for ele in range(0, 8*6, 8)][::-1])
        }
        
        # Create hash from system info
        info_string = '|'.join(str(v) for v in system_info.values())
        machine_hash = hashlib.sha256(info_string.encode()).hexdigest()[:16]
        return machine_hash.upper()
        
    except Exception:
        # Fallback to UUID-based identifier
        return str(uuid.uuid4()).replace('-', '')[:16].upper()


class LicenseEnforcer:
    """Main license enforcement class with strict validation."""
    
    PACKAGE_NAME = "quantummetagpt"
    CONTACT_EMAIL = "bajpaikrishna715@gmail.com"
    
    def __init__(self):
        self.machine_id = get_machine_id()
        self._license_cache = {}
        
    def validate_license(self, features: Optional[List[str]] = None) -> bool:
        """
        Validate license with comprehensive error handling.
        No bypass mechanisms allowed.
        """
        if not LICENSING_AVAILABLE:
            self._show_license_error("License validation system not available")
            sys.exit(1)
            
        try:
            # Strict validation - no grace period allowed
            from quantummeta_license import validate_license
            validate_license(self.PACKAGE_NAME, required_features=features)
            return True
            
        except LicenseExpiredError as e:
            self._show_license_error(
                "🕒 Your QuantumMetaGPT license has expired",
                details=[
                    "Your license has expired. No grace period available.",
                    f"Machine ID: {self.machine_id}",
                    f"Contact: {self.CONTACT_EMAIL} for license renewal"
                ]
            )
            sys.exit(1)
            
        except FeatureNotLicensedError as e:
            required_features_str = ', '.join(features) if features else 'core'
            self._show_license_error(
                f"🔒 Feature '{required_features_str}' requires a higher license tier",
                details=[
                    "Available QuantumMetaGPT license tiers:",
                    "   • Basic: Core quantum algorithm generation",
                    "   • Pro: Advanced optimization + LLM integration", 
                    "   • Enterprise: Full suite + commercial use",
                    f"Machine ID: {self.machine_id}",
                    f"Contact: {self.CONTACT_EMAIL} for license upgrade"
                ]
            )
            sys.exit(1)
            
        except LicenseNotFoundError as e:
            self._show_license_error(
                "📋 No valid QuantumMetaGPT license found",
                details=[
                    "No license found. QuantumMetaGPT requires a valid license.",
                    "To continue using QuantumMetaGPT:",
                    "1. Purchase a license",
                    "2. Activate existing license: quantum-license activate license.qkey",
                    f"Machine ID: {self.machine_id}",
                    f"Contact: {self.CONTACT_EMAIL}"
                ]
            )
            sys.exit(1)
            
        except LicenseError as e:
            self._show_license_error(
                f"❌ QuantumMetaGPT license validation failed: {e}",
                details=[
                    f"Machine ID: {self.machine_id}",
                    f"Contact: {self.CONTACT_EMAIL}"
                ]
            )
            sys.exit(1)
    
    def _show_license_error(self, message: str, details: Optional[List[str]] = None):
        """Display comprehensive license error information."""
        print("=" * 70)
        print("🚫 QUANTUMMETAGPT LICENSE ERROR")
        print("=" * 70)
        print(message)
        print()
        
        if details:
            for detail in details:
                print(detail)
        
        print()
        print("For immediate assistance:")
        print(f"📧 Email: {self.CONTACT_EMAIL}")
        print(f"🔧 Machine ID: {self.machine_id}")
        print("=" * 70)


# Global license enforcer instance
_license_enforcer = LicenseEnforcer()


def require_license(features: Optional[List[str]] = None):
    """
    Decorator for functions requiring license validation.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _license_enforcer.validate_license(features)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def licensed_method(features: Optional[List[str]] = None):
    """
    Method decorator for license-protected methods.
    """
    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            _license_enforcer.validate_license(features)
            return method(self, *args, **kwargs)
        return wrapper
    return decorator


def licensed_class(features: Optional[List[str]] = None, 
                  protect_all_methods: bool = True,
                  exclude_methods: Optional[List[str]] = None):
    """
    Class decorator that enforces licensing on class instantiation and methods.
    
    Args:
        features: Required license features
        protect_all_methods: If True, protect all public methods
        exclude_methods: Methods to exclude from protection
    """
    def decorator(cls: Type) -> Type:
        exclude_set = set(exclude_methods or [])
        exclude_set.update({'__init__', '__new__', '__str__', '__repr__', 
                           '__getattr__', '__setattr__', '__delattr__'})
        
        # Protect __init__ method
        original_init = cls.__init__
        
        @wraps(original_init)
        def protected_init(self, *args, **kwargs):
            _license_enforcer.validate_license(features)
            return original_init(self, *args, **kwargs)
        
        cls.__init__ = protected_init
        
        # Protect all public methods if requested
        if protect_all_methods:
            for attr_name in dir(cls):
                if (not attr_name.startswith('_') and 
                    attr_name not in exclude_set and
                    callable(getattr(cls, attr_name))):
                    
                    original_method = getattr(cls, attr_name)
                    if inspect.isfunction(original_method) or inspect.ismethod(original_method):
                        protected_method = licensed_method(features)(original_method)
                        setattr(cls, attr_name, protected_method)
        
        # Add license info method
        def get_license_info(self):
            """Get license information for this instance."""
            return {
                'machine_id': _license_enforcer.machine_id,
                'package': _license_enforcer.PACKAGE_NAME,
                'contact': _license_enforcer.CONTACT_EMAIL,
                'required_features': features or ['core']
            }
        
        cls.get_license_info = get_license_info
        
        return cls
    
    return decorator


def show_license_info():
    """Display current license information."""
    if not LICENSING_AVAILABLE:
        print("⚠️ License system not available")
        return
    
    try:
        from quantummeta_license.core.validation import check_license_status
        status = check_license_status(_license_enforcer.PACKAGE_NAME)
        
        print("=" * 50)
        print("📋 QUANTUMMETAGPT LICENSE STATUS")
        print("=" * 50)
        print(f"Machine ID: {_license_enforcer.machine_id}")
        print(f"Package: {_license_enforcer.PACKAGE_NAME}")
        
        if status["status"] == "licensed":
            info = status["license_info"]
            print(f"✅ Status: Licensed")
            print(f"👤 Licensed to: {info['user']}")
            print(f"📅 Expires: {info['expires']}")
            print(f"🔧 Features: {', '.join(info['features'])}")
        else:
            print("❌ Status: No valid license")
            print(f"📧 Contact: {_license_enforcer.CONTACT_EMAIL}")
        
        print("=" * 50)
        
    except Exception as e:
        print(f"Error checking license status: {e}")
        print(f"📧 Contact: {_license_enforcer.CONTACT_EMAIL}")
        print(f"🔧 Machine ID: {_license_enforcer.machine_id}")
