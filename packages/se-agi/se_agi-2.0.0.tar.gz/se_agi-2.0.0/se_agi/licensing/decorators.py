"""
SE-AGI License Decorators

Decorators for license validation and feature gating.
"""

import logging
from functools import wraps
from typing import List, Optional, Callable, Any

from .license_manager import SEAGILicenseManager
from .exceptions import SEAGILicenseError, FeatureNotLicensedError


def requires_license(
    required_features: Optional[List[str]] = None,
    package_name: str = "se-agi",
    graceful_degradation: bool = False,
    fallback_result: Any = None
):
    """
    Decorator to require license validation for functions/methods.
    
    Args:
        required_features: List of required features
        package_name: Package name for license validation
        graceful_degradation: If True, return fallback_result instead of raising
        fallback_result: Result to return if license check fails and graceful_degradation=True
    
    Usage:
        @requires_license(["advanced_agents", "meta_learning"])
        def advanced_function():
            return "Advanced feature!"
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            license_manager = SEAGILicenseManager(package_name)
            logger = logging.getLogger(f"SEAGILicense.{func.__name__}")
            
            try:
                license_manager.validate_license(required_features)
                return func(*args, **kwargs)
                
            except SEAGILicenseError as e:
                if graceful_degradation:
                    logger.warning(f"License check failed for {func.__name__}: {e}")
                    return fallback_result
                else:
                    raise RuntimeError(f"License required for {func.__name__}: {e}")
                    
        return wrapper
    return decorator


def licensed_capability(
    feature: str,
    tier: str = "pro",
    package_name: str = "se-agi",
    error_message: Optional[str] = None
):
    """
    Decorator for capability-based licensing.
    
    Args:
        feature: The feature being protected
        tier: Minimum license tier required
        package_name: Package name for license validation
        error_message: Custom error message
        
    Usage:
        @licensed_capability("multimodal_reasoning", "pro")
        def multimodal_analysis():
            return "Multimodal analysis result"
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            license_manager = SEAGILicenseManager(package_name)
            
            if not license_manager.check_feature_access(feature):
                current_tier = license_manager.get_license_tier()
                
                if error_message:
                    raise FeatureNotLicensedError(feature, tier, current_tier)
                else:
                    raise FeatureNotLicensedError(feature, tier, current_tier)
            
            return func(*args, **kwargs)
            
        return wrapper
    return decorator


def license_tier_required(
    minimum_tier: str,
    package_name: str = "se-agi"
):
    """
    Decorator to require a minimum license tier.
    
    Args:
        minimum_tier: Minimum required tier (basic, pro, enterprise)
        package_name: Package name for license validation
        
    Usage:
        @license_tier_required("enterprise")
        def enterprise_only_function():
            return "Enterprise feature"
    """
    tier_hierarchy = {"basic": 0, "pro": 1, "enterprise": 2}
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            license_manager = SEAGILicenseManager(package_name)
            current_tier = license_manager.get_license_tier()
            
            current_level = tier_hierarchy.get(current_tier, -1)
            required_level = tier_hierarchy.get(minimum_tier, 99)
            
            if current_level < required_level:
                raise FeatureNotLicensedError(
                    feature=func.__name__,
                    required_tier=minimum_tier,
                    current_tier=current_tier
                )
            
            return func(*args, **kwargs)
            
        return wrapper
    return decorator


def with_license_check(package_name: str = "se-agi"):
    """
    Class decorator to add license checking to all public methods.
    
    Args:
        package_name: Package name for license validation
        
    Usage:
        @with_license_check("se-agi")
        class LicensedClass:
            def public_method(self):
                return "Licensed method"
    """
    def decorator(cls):
        license_manager = SEAGILicenseManager(package_name)
        
        # Get all public methods
        for attr_name in dir(cls):
            if not attr_name.startswith('_'):
                attr = getattr(cls, attr_name)
                if callable(attr):
                    # Wrap the method with license check
                    wrapped_method = _wrap_method_with_license(attr, license_manager)
                    setattr(cls, attr_name, wrapped_method)
        
        return cls
    return decorator


def _wrap_method_with_license(method: Callable, license_manager: SEAGILicenseManager) -> Callable:
    """Helper function to wrap a method with license checking."""
    @wraps(method)
    def wrapper(*args, **kwargs):
        try:
            license_manager.validate_license()
            return method(*args, **kwargs)
        except SEAGILicenseError as e:
            raise RuntimeError(f"License required for {method.__name__}: {e}")
    
    return wrapper


def graceful_license_check(
    required_features: Optional[List[str]] = None,
    package_name: str = "se-agi",
    fallback_message: str = "Feature requires valid license"
):
    """
    Decorator that gracefully handles license failures.
    
    Args:
        required_features: List of required features
        package_name: Package name for license validation
        fallback_message: Message to return on license failure
        
    Usage:
        @graceful_license_check(["advanced_ai"])
        def ai_function():
            return "AI processing complete"
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            license_manager = SEAGILicenseManager(package_name)
            logger = logging.getLogger(f"SEAGILicense.{func.__name__}")
            
            try:
                license_manager.validate_license(required_features)
                return func(*args, **kwargs)
                
            except SEAGILicenseError as e:
                logger.warning(f"License check failed for {func.__name__}: {e}")
                return {
                    "success": False,
                    "message": fallback_message,
                    "license_error": str(e),
                    "upgrade_info": "Contact sales@seagi.ai for license upgrade"
                }
                
        return wrapper
    return decorator
