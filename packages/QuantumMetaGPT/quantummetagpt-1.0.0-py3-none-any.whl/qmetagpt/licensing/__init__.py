"""
QuantumMetaGPT Licensing System
Comprehensive license protection for all classes and functions.
"""

from .license_enforcer import (
    LicenseEnforcer,
    licensed_class,
    licensed_method,
    require_license,
    get_machine_id,
    show_license_info
)

__all__ = [
    'LicenseEnforcer',
    'licensed_class',
    'licensed_method', 
    'require_license',
    'get_machine_id',
    'show_license_info'
]
