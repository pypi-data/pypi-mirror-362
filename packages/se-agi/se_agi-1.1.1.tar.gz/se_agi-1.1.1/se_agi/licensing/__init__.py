"""
SE-AGI Licensing Module

Integrates QuantumMeta License Server for proper license management
and feature gating across the SE-AGI ecosystem.
"""

from .license_manager import SEAGILicenseManager
from .decorators import requires_license, licensed_capability
from .exceptions import SEAGILicenseError, FeatureNotLicensedError
from .validation import validate_seagi_license, check_feature_access

__all__ = [
    'SEAGILicenseManager',
    'requires_license', 
    'licensed_capability',
    'SEAGILicenseError',
    'FeatureNotLicensedError', 
    'validate_seagi_license',
    'check_feature_access'
]
