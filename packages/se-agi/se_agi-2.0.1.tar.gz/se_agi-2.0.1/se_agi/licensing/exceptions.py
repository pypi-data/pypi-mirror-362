"""
SE-AGI License Exceptions

Custom exceptions for license-related errors in the SE-AGI system.
"""

from typing import List, Optional


class SEAGILicenseError(Exception):
    """Base exception for SE-AGI license errors."""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message)
        self.error_code = error_code
        self.message = message


class FeatureNotLicensedError(SEAGILicenseError):
    """Raised when attempting to use a feature not included in current license."""
    
    def __init__(self, feature: str, required_tier: str, current_tier: str = "basic"):
        message = (
            f"🔒 Feature '{feature}' requires {required_tier} license tier. "
            f"Current tier: {current_tier}. "
            f"Contact bajpaikrishna715@gmail.com for upgrade options."
        )
        super().__init__(message, "FEATURE_NOT_LICENSED")
        self.feature = feature
        self.required_tier = required_tier
        self.current_tier = current_tier


class LicenseExpiredError(SEAGILicenseError):
    """Raised when license has expired."""
    
    def __init__(self, package_name: str, expiry_date: str):
        import uuid
        machine_id = uuid.getnode()
        message = (
            f"🕒 Your SE-AGI license has expired on {expiry_date}. "
            f"Please contact bajpaikrishna715@gmail.com for license renewal. "
            f"Include Machine ID: {machine_id}"
        )
        super().__init__(message, "LICENSE_EXPIRED")
        self.package_name = package_name
        self.expiry_date = expiry_date


class LicenseNotFoundError(SEAGILicenseError):
    """Raised when no license is found and grace period has expired."""
    
    def __init__(self, package_name: str):
        import uuid
        machine_id = uuid.getnode()
        message = (
            f"📋 No license found for {package_name} and grace period has expired. "
            f"To continue using SE-AGI:\n"
            f"1. Contact: bajpaikrishna715@gmail.com (Include Machine ID: {machine_id})\n"
            f"2. Or activate an existing license: quantum-license activate license.qkey"
        )
        super().__init__(message, "LICENSE_NOT_FOUND")
        self.package_name = package_name


class GracePeriodExpiredError(SEAGILicenseError):
    """Raised when grace period has expired."""
    
    def __init__(self, package_name: str, grace_days: int):
        import uuid
        machine_id = uuid.getnode()
        message = (
            f"⏰ Grace period of {grace_days} days has expired for {package_name}. "
            f"Please obtain a valid license to continue using SE-AGI. "
            f"Contact bajpaikrishna715@gmail.com with Machine ID: {machine_id}"
        )
        super().__init__(message, "GRACE_PERIOD_EXPIRED")
        self.package_name = package_name
        self.grace_days = grace_days


class InvalidLicenseError(SEAGILicenseError):
    """Raised when license format is invalid or corrupted."""
    
    def __init__(self, reason: str):
        message = f"❌ Invalid license: {reason}. Please contact bajpaikrishna715@gmail.com"
        super().__init__(message, "INVALID_LICENSE")
        self.reason = reason
