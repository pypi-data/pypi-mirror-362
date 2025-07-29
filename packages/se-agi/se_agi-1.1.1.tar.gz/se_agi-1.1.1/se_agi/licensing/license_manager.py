"""
SE-AGI License Manager

Manages license validation and feature access for the SE-AGI system.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path

try:
    from quantummeta_license import validate_or_grace, LicenseError
    from quantummeta_license.core.license_manager import LicenseManager
    from quantummeta_license.core.validation import check_license_status
    QUANTUMMETA_AVAILABLE = True
except ImportError:
    QUANTUMMETA_AVAILABLE = False

from .exceptions import (
    SEAGILicenseError,
    FeatureNotLicensedError,
    LicenseExpiredError,
    LicenseNotFoundError,
    GracePeriodExpiredError
)


class SEAGILicenseManager:
    """
    SE-AGI License Manager for handling licensing across the system.
    
    Features:
    - Multi-tier licensing (Basic, Pro, Enterprise)
    - Feature-based access control
    - Grace period management
    """
    
    # License tiers and their features
    LICENSE_TIERS = {
        "basic": {
            "features": ["core", "basic_agents", "simple_reasoning"],
            "max_agents": 5,
            "memory_limit": "1GB",
            "evolution_enabled": False
        },
        "pro": {
            "features": ["core", "basic_agents", "simple_reasoning", "advanced_agents", 
                        "multimodal", "meta_learning", "evolution"],
            "max_agents": 50,
            "memory_limit": "10GB", 
            "evolution_enabled": True
        },
        "enterprise": {
            "features": ["core", "basic_agents", "simple_reasoning", "advanced_agents",
                        "multimodal", "meta_learning", "evolution", "distributed",
                        "custom_models", "api_access", "priority_support"],
            "max_agents": -1,  # Unlimited
            "memory_limit": "unlimited",
            "evolution_enabled": True
        }
    }
    
    def __init__(self, package_name: str = "se-agi", grace_days: int = 14):
        self.package_name = package_name
        self.grace_days = grace_days
        self.logger = logging.getLogger(f"SEAGILicense.{package_name}")
        self._license_cache = {}
        self._feature_cache = {}
        
        if not QUANTUMMETA_AVAILABLE:
            self.logger.error("QuantumMeta License package not available")
            raise SEAGILicenseError(
                "License system not available. Please install: pip install quantummeta-license\n"
                "Contact: bajpaikrishna715@gmail.com for support"
            )
    
    def validate_license(self, required_features: Optional[List[str]] = None) -> bool:
        """
        Validate SE-AGI license with optional feature requirements.
        
        Args:
            required_features: List of required features
            
        Returns:
            True if license is valid
            
        Raises:
            SEAGILicenseError: If license validation fails
        """
        if not QUANTUMMETA_AVAILABLE:
            raise SEAGILicenseError(
                "QuantumMeta License system not available. "
                "Please install: pip install quantummeta-license\n"
                "Contact: bajpaikrishna715@gmail.com for support"
            )
        
        try:
            # Validate basic license
            validate_or_grace(self.package_name, grace_days=self.grace_days)
            
            # Check feature requirements
            if required_features:
                return self._validate_features(required_features)
            
            return True
            
        except LicenseError as e:
            self._handle_license_error(e)
            return False
    
    def _validate_features(self, required_features: List[str]) -> bool:
        """Validate that required features are available."""
        available_features = self.get_available_features()
        
        for feature in required_features:
            if feature not in available_features:
                current_tier = self.get_license_tier()
                required_tier = self._get_required_tier_for_feature(feature)
                
                raise FeatureNotLicensedError(
                    feature=feature,
                    required_tier=required_tier,
                    current_tier=current_tier
                )
        
        return True
    
    def get_available_features(self) -> List[str]:
        """Get list of features available with current license."""
        if not QUANTUMMETA_AVAILABLE:
            raise SEAGILicenseError(
                "QuantumMeta License system not available. "
                "Please install: pip install quantummeta-license\n"
                "Contact: bajpaikrishna715@gmail.com for support"
            )
        
        # Check cache first
        cache_key = f"{self.package_name}_features"
        if cache_key in self._feature_cache:
            cache_time, features = self._feature_cache[cache_key]
            if datetime.now() - cache_time < timedelta(minutes=5):
                return features
        
        try:
            manager = LicenseManager()
            license_obj = manager.get_license(self.package_name)
            
            if license_obj and not license_obj.is_expired():
                features = license_obj.features or self.LICENSE_TIERS["basic"]["features"]
            else:
                # Grace period - basic features only
                features = self.LICENSE_TIERS["basic"]["features"]
            
            # Cache the result
            self._feature_cache[cache_key] = (datetime.now(), features)
            return features
            
        except Exception as e:
            self.logger.error(f"Error getting features: {e}")
            return self.LICENSE_TIERS["basic"]["features"]
    
    def get_license_tier(self) -> str:
        """Get the current license tier."""
        features = self.get_available_features()
        
        # Determine tier based on available features
        for tier, tier_info in reversed(list(self.LICENSE_TIERS.items())):
            tier_features = set(tier_info["features"])
            if tier_features.issubset(set(features)):
                return tier
        
        return "basic"
    
    def _get_required_tier_for_feature(self, feature: str) -> str:
        """Get the minimum tier required for a feature."""
        for tier, tier_info in self.LICENSE_TIERS.items():
            if feature in tier_info["features"]:
                return tier
        return "enterprise"  # Unknown features require enterprise
    
    def check_feature_access(self, feature: str) -> bool:
        """Check if a specific feature is accessible."""
        try:
            return self._validate_features([feature])
        except FeatureNotLicensedError:
            return False
    
    def get_license_info(self) -> Dict[str, Any]:
        """Get detailed license information."""
        if not QUANTUMMETA_AVAILABLE:
            raise SEAGILicenseError(
                "QuantumMeta License system not available. "
                "Please install: pip install quantummeta-license\n"
                "Contact: bajpaikrishna715@gmail.com for support"
            )
        
        try:
            status = check_license_status(self.package_name)
            
            if status["status"] == "licensed":
                info = status["license_info"]
                return {
                    "status": "licensed",
                    "tier": self.get_license_tier(),
                    "features": self.get_available_features(),
                    "expires": info.get("expires", "Unknown"),
                    "user": info.get("user", "Unknown")
                }
            elif status["status"] == "grace_period":
                grace = status["grace_info"]
                return {
                    "status": "grace_period",
                    "tier": "basic",
                    "features": self.LICENSE_TIERS["basic"]["features"],
                    "expires": grace.get("expiry_date", "Unknown"),
                    "days_remaining": grace.get("days_remaining", 0)
                }
            else:
                return {
                    "status": "expired",
                    "tier": "none",
                    "features": [],
                    "expires": "Expired",
                    "user": "None"
                }
                
        except Exception as e:
            self.logger.error(f"Error getting license info: {e}")
            return {
                "status": "error",
                "tier": "unknown",
                "features": [],
                "error": str(e)
            }
    
    def display_license_info(self) -> None:
        """Display license information to the user."""
        info = self.get_license_info()
        status = info["status"]
        
        print("\n" + "="*50)
        print("🧠 SE-AGI License Information")
        print("="*50)
        
        if status == "licensed":
            print(f"✅ Licensed to: {info['user']}")
            print(f"📅 Expires: {info['expires']}")
            print(f"🏆 Tier: {info['tier'].title()}")
            print(f"🔧 Features: {', '.join(info['features'])}")
            
        elif status == "grace_period":
            print(f"⏳ Grace period: {info['days_remaining']} days remaining")
            print(f"📅 Expires: {info['expires']}")
            print(f"🔧 Features: {', '.join(info['features'])}")
            print("\n⚠️  Please obtain a license before grace period expires")
            print("📧 Contact: bajpaikrishna715@gmail.com")
            print("🔧 Include your Machine ID in the request")
            self._display_machine_id()
            
        else:
            print("❌ No valid license found")
            print("� Contact: bajpaikrishna715@gmail.com for licensing")
            print("🔧 Include your Machine ID in the request")
            self._display_machine_id()
            
        print("="*50 + "\n")
    
    def _display_machine_id(self) -> None:
        """Display machine ID for licensing purposes."""
        import uuid
        machine_id = uuid.getnode()
        print(f"🖥️  Machine ID: {machine_id}")
        print("   (Copy this ID when contacting for license)")
    
    def _handle_license_error(self, error: Exception) -> None:
        """Handle and convert license errors to SE-AGI specific errors."""
        error_msg = str(error).lower()
        
        if "expired" in error_msg:
            raise LicenseExpiredError(self.package_name, "unknown")
        elif "not found" in error_msg:
            raise LicenseNotFoundError(self.package_name)
        elif "grace" in error_msg:
            raise GracePeriodExpiredError(self.package_name, self.grace_days)
        else:
            raise SEAGILicenseError(f"License validation failed: {error}")
    
    def get_tier_limits(self) -> Dict[str, Any]:
        """Get limits for current license tier."""
        tier = self.get_license_tier()
        return self.LICENSE_TIERS.get(tier, self.LICENSE_TIERS["basic"])
