"""
SE-AGI License Validation

Core validation functions for SE-AGI licensing.
"""

import logging
from typing import List, Optional, Dict, Any

from .license_manager import SEAGILicenseManager
from .exceptions import SEAGILicenseError


def validate_seagi_license(
    required_features: Optional[List[str]] = None,
    package_name: str = "se-agi",
    grace_days: int = 14
) -> bool:
    """
    Validate SE-AGI license with optional feature requirements.
    
    Args:
        required_features: List of required features
        package_name: Package name for license validation
        grace_days: Grace period in days
        
    Returns:
        True if license is valid
        
    Raises:
        SEAGILicenseError: If license validation fails
    """
    license_manager = SEAGILicenseManager(package_name, grace_days)
    return license_manager.validate_license(required_features)


def check_feature_access(
    feature: str,
    package_name: str = "se-agi"
) -> bool:
    """
    Check if a specific feature is accessible with current license.
    
    Args:
        feature: Feature to check
        package_name: Package name for license validation
        
    Returns:
        True if feature is accessible
    """
    license_manager = SEAGILicenseManager(package_name)
    return license_manager.check_feature_access(feature)


def get_license_status(package_name: str = "se-agi") -> Dict[str, Any]:
    """
    Get comprehensive license status information.
    
    Args:
        package_name: Package name for license validation
        
    Returns:
        Dictionary with license status information
    """
    license_manager = SEAGILicenseManager(package_name)
    return license_manager.get_license_info()


def get_available_features(package_name: str = "se-agi") -> List[str]:
    """
    Get list of features available with current license.
    
    Args:
        package_name: Package name for license validation
        
    Returns:
        List of available features
    """
    license_manager = SEAGILicenseManager(package_name)
    return license_manager.get_available_features()


def get_license_tier(package_name: str = "se-agi") -> str:
    """
    Get the current license tier.
    
    Args:
        package_name: Package name for license validation
        
    Returns:
        License tier (basic, pro, enterprise)
    """
    license_manager = SEAGILicenseManager(package_name)
    return license_manager.get_license_tier()


def display_license_info(package_name: str = "se-agi") -> None:
    """
    Display license information to the user.
    
    Args:
        package_name: Package name for license validation
    """
    license_manager = SEAGILicenseManager(package_name)
    license_manager.display_license_info()


def validate_tier_requirement(
    required_tier: str,
    package_name: str = "se-agi"
) -> bool:
    """
    Validate that current license meets tier requirements.
    
    Args:
        required_tier: Required license tier
        package_name: Package name for license validation
        
    Returns:
        True if tier requirement is met
    """
    tier_hierarchy = {"basic": 0, "pro": 1, "enterprise": 2}
    
    current_tier = get_license_tier(package_name)
    current_level = tier_hierarchy.get(current_tier, -1)
    required_level = tier_hierarchy.get(required_tier, 99)
    
    return current_level >= required_level


def check_agent_limit(
    current_agents: int,
    package_name: str = "se-agi"
) -> bool:
    """
    Check if current number of agents is within license limits.
    
    Args:
        current_agents: Current number of active agents
        package_name: Package name for license validation
        
    Returns:
        True if within limits
    """
    license_manager = SEAGILicenseManager(package_name)
    limits = license_manager.get_tier_limits()
    max_agents = limits.get("max_agents", 5)
    
    if max_agents == -1:  # Unlimited
        return True
    
    return current_agents <= max_agents


def is_evolution_enabled(package_name: str = "se-agi") -> bool:
    """
    Check if evolution features are enabled in current license.
    
    Args:
        package_name: Package name for license validation
        
    Returns:
        True if evolution is enabled
    """
    license_manager = SEAGILicenseManager(package_name)
    limits = license_manager.get_tier_limits()
    return limits.get("evolution_enabled", False)


def safe_license_check(
    required_features: Optional[List[str]] = None,
    package_name: str = "se-agi"
) -> Dict[str, Any]:
    """
    Safe license check that never raises exceptions.
    
    Args:
        required_features: List of required features
        package_name: Package name for license validation
        
    Returns:
        Dictionary with validation results
    """
    try:
        license_manager = SEAGILicenseManager(package_name)
        is_valid = license_manager.validate_license(required_features)
        
        return {
            "valid": is_valid,
            "tier": license_manager.get_license_tier(),
            "features": license_manager.get_available_features(),
            "error": None
        }
        
    except SEAGILicenseError as e:
        return {
            "valid": False,
            "tier": "none",
            "features": [],
            "error": str(e),
            "error_code": getattr(e, 'error_code', 'UNKNOWN')
        }
    except Exception as e:
        logging.getLogger("SEAGILicense").error(f"Unexpected error in license check: {e}")
        return {
            "valid": False,
            "tier": "unknown",
            "features": [],
            "error": f"Unexpected error: {e}",
            "error_code": "SYSTEM_ERROR"
        }
