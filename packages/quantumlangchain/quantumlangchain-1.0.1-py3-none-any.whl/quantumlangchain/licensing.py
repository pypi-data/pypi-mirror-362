"""
QuantumLangChain Licensing Integration System

This module provides comprehensive license validation and enforcement
for all QuantumLangChain components with 24-hour grace period.

Contact: bajpaikrishna715@gmail.com for licensing inquiries.
"""

import os
import hashlib
import platform
import uuid
import time
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from functools import wraps
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# License configuration
LICENSE_CONFIG = {
    "grace_period_hours": 24,
    "contact_email": "bajpaikrishna715@gmail.com",
    "company": "QuantumLangChain Technologies",
    "support_url": "https://quantumlangchain.dev/support"
}

# Feature tiers
FEATURE_TIERS = {
    "evaluation": {
        "features": ["core", "basic_chains", "quantum_memory_basic"],
        "duration_hours": 24,
        "max_operations": 1000
    },
    "basic": {
        "features": ["core", "basic_chains", "quantum_memory", "simple_backends"],
        "price": "$29/month",
        "max_operations": 10000
    },
    "professional": {
        "features": [
            "core", "basic_chains", "quantum_memory", "simple_backends",
            "multi_agent", "advanced_backends", "quantum_retrieval",
            "entangled_agents", "quantum_tools"
        ],
        "price": "$99/month",
        "max_operations": 100000
    },
    "enterprise": {
        "features": [
            "core", "basic_chains", "quantum_memory", "simple_backends",
            "multi_agent", "advanced_backends", "quantum_retrieval",
            "entangled_agents", "quantum_tools", "distributed_systems",
            "custom_backends", "advanced_analytics", "priority_support"
        ],
        "price": "$299/month",
        "max_operations": -1  # Unlimited
    },
    "research": {
        "features": [
            "core", "experimental_apis", "research_backends",
            "academic_license", "quantum_research_tools"
        ],
        "price": "$49/month (Academic)",
        "max_operations": 50000
    }
}


class QuantumLicenseError(Exception):
    """Base class for quantum license errors."""
    
    def __init__(self, message: str, machine_id: Optional[str] = None, 
                 contact_email: str = LICENSE_CONFIG["contact_email"]):
        self.machine_id = machine_id or LicenseManager().get_machine_id()
        self.contact_email = contact_email
        
        full_message = (
            f"🔐 QuantumLangChain License Error\n"
            f"{'='*50}\n"
            f"{message}\n\n"
            f"📧 Contact: {self.contact_email}\n"
            f"🔧 Machine ID: {self.machine_id}\n"
            f"⏰ Grace Period: {LICENSE_CONFIG['grace_period_hours']} hours from first use\n"
            f"🌐 Support: {LICENSE_CONFIG['support_url']}\n"
            f"{'='*50}"
        )
        super().__init__(full_message)


class LicenseExpiredError(QuantumLicenseError):
    """License has expired."""
    
    def __init__(self, expiry_date: str, machine_id: Optional[str] = None):
        message = (
            f"Your QuantumLangChain license expired on {expiry_date}.\n"
            f"Please renew your license to continue using quantum features."
        )
        super().__init__(message, machine_id)


class FeatureNotLicensedError(QuantumLicenseError):
    """Feature not available in current license tier."""
    
    def __init__(self, feature: str, required_tier: str, current_tier: str, 
                 machine_id: Optional[str] = None):
        message = (
            f"Feature '{feature}' requires '{required_tier}' license tier.\n"
            f"Current tier: '{current_tier}'\n"
            f"Upgrade your license to access this feature."
        )
        super().__init__(message, machine_id)


class GracePeriodExpiredError(QuantumLicenseError):
    """Grace period has expired."""
    
    def __init__(self, machine_id: Optional[str] = None):
        message = (
            f"24-hour evaluation period has expired.\n"
            f"Please purchase a license to continue using QuantumLangChain."
        )
        super().__init__(message, machine_id)


class LicenseNotFoundError(QuantumLicenseError):
    """No license found."""
    
    def __init__(self, machine_id: Optional[str] = None):
        message = (
            f"No valid license found for QuantumLangChain.\n"
            f"Starting 24-hour evaluation period.\n"
            f"Please contact us for licensing options."
        )
        super().__init__(message, machine_id)


class UsageLimitExceededError(QuantumLicenseError):
    """Usage limit exceeded for current license tier."""
    
    def __init__(self, limit: int, current_usage: int, machine_id: Optional[str] = None):
        message = (
            f"Usage limit exceeded: {current_usage}/{limit} operations.\n"
            f"Please upgrade your license for higher limits."
        )
        super().__init__(message, machine_id)


class LicenseManager:
    """Comprehensive license management system for QuantumLangChain."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.license_file = Path.home() / ".quantumlangchain" / "license.json"
            self.grace_file = Path.home() / ".quantumlangchain" / "grace.json"
            self.usage_file = Path.home() / ".quantumlangchain" / "usage.json"
            self.machine_id = self._generate_machine_id()
            
            # Ensure directory exists
            self.license_file.parent.mkdir(exist_ok=True)
            
            # Initialize usage tracking
            self.usage_data = self._load_usage_data()
            
            self.__class__._initialized = True
    
    def _generate_machine_id(self) -> str:
        """Generate unique machine identifier."""
        try:
            # Collect hardware information
            mac = uuid.getnode()
            hostname = platform.node()
            system = platform.system()
            processor = platform.processor()
            
            # Create stable machine ID
            machine_string = f"{mac}-{hostname}-{system}-{processor}"
            machine_hash = hashlib.sha256(machine_string.encode()).hexdigest()
            
            return f"QLC-{machine_hash[:16].upper()}"
        except Exception:
            # Fallback to random ID
            return f"QLC-{uuid.uuid4().hex[:16].upper()}"
    
    def get_machine_id(self) -> str:
        """Get machine ID for licensing."""
        return self.machine_id
    
    def _load_license(self) -> Optional[Dict[str, Any]]:
        """Load license from file."""
        try:
            if self.license_file.exists():
                with open(self.license_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading license: {e}")
        return None
    
    def _load_grace_data(self) -> Optional[Dict[str, Any]]:
        """Load grace period data."""
        try:
            if self.grace_file.exists():
                with open(self.grace_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading grace data: {e}")
        return None
    
    def _load_usage_data(self) -> Dict[str, Any]:
        """Load usage tracking data."""
        default_usage = {
            "daily_operations": 0,
            "monthly_operations": 0,
            "last_reset_date": datetime.now().isoformat(),
            "feature_usage": {}
        }
        
        try:
            if self.usage_file.exists():
                with open(self.usage_file, 'r') as f:
                    data = json.load(f)
                    # Reset daily counter if new day
                    last_reset = datetime.fromisoformat(data.get("last_reset_date", ""))
                    if last_reset.date() < datetime.now().date():
                        data["daily_operations"] = 0
                        data["last_reset_date"] = datetime.now().isoformat()
                    return data
        except Exception as e:
            logger.warning(f"Error loading usage data: {e}")
        
        return default_usage
    
    def _save_grace_data(self, grace_data: Dict[str, Any]):
        """Save grace period data."""
        try:
            with open(self.grace_file, 'w') as f:
                json.dump(grace_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving grace data: {e}")
    
    def _save_usage_data(self):
        """Save usage tracking data."""
        try:
            with open(self.usage_file, 'w') as f:
                json.dump(self.usage_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving usage data: {e}")
    
    def start_grace_period(self) -> bool:
        """Start 24-hour grace period."""
        grace_data = self._load_grace_data()
        
        if grace_data and not self._is_grace_expired(grace_data):
            logger.info("Grace period already active")
            return True
        
        # Start new grace period
        new_grace_data = {
            "machine_id": self.machine_id,
            "start_time": datetime.now().isoformat(),
            "expiry_time": (datetime.now() + timedelta(hours=LICENSE_CONFIG["grace_period_hours"])).isoformat(),
            "operations_count": 0
        }
        
        self._save_grace_data(new_grace_data)
        
        logger.info(f"Started {LICENSE_CONFIG['grace_period_hours']}-hour grace period")
        return True
    
    def _is_grace_expired(self, grace_data: Dict[str, Any]) -> bool:
        """Check if grace period has expired."""
        try:
            expiry_time = datetime.fromisoformat(grace_data["expiry_time"])
            return datetime.now() > expiry_time
        except Exception:
            return True
    
    def _is_grace_active(self) -> bool:
        """Check if grace period is currently active."""
        grace_data = self._load_grace_data()
        if not grace_data:
            return False
        
        return not self._is_grace_expired(grace_data)
    
    def _get_license_tier(self) -> str:
        """Get current license tier."""
        license_data = self._load_license()
        
        if license_data and not self._is_license_expired(license_data):
            return license_data.get("tier", "basic")
        
        if self._is_grace_active():
            return "evaluation"
        
        return None
    
    def _is_license_expired(self, license_data: Dict[str, Any]) -> bool:
        """Check if license has expired."""
        try:
            expiry_date = datetime.fromisoformat(license_data["expiry_date"])
            return datetime.now() > expiry_date
        except Exception:
            return True
    
    def _check_usage_limits(self, tier: str) -> bool:
        """Check if usage limits are exceeded."""
        tier_config = FEATURE_TIERS.get(tier, {})
        max_operations = tier_config.get("max_operations", 0)
        
        if max_operations == -1:  # Unlimited
            return True
        
        if max_operations == 0:  # No operations allowed
            return False
        
        current_operations = self.usage_data.get("daily_operations", 0)
        return current_operations < max_operations
    
    def _increment_usage(self, feature: str = "general"):
        """Increment usage counter."""
        self.usage_data["daily_operations"] += 1
        self.usage_data["monthly_operations"] += 1
        
        if feature not in self.usage_data["feature_usage"]:
            self.usage_data["feature_usage"][feature] = 0
        
        self.usage_data["feature_usage"][feature] += 1
        self._save_usage_data()
    
    def validate_license(self, package_name: str, required_features: Optional[List[str]] = None,
                        required_tier: str = "basic") -> bool:
        """
        Comprehensive license validation.
        
        Args:
            package_name: Name of the package requiring validation
            required_features: List of required features
            required_tier: Minimum required license tier
            
        Returns:
            True if license is valid
            
        Raises:
            Various license exceptions based on validation failure
        """
        required_features = required_features or ["core"]
        
        # Check if license exists
        license_data = self._load_license()
        
        if license_data and not self._is_license_expired(license_data):
            # Valid license exists
            tier = license_data.get("tier", "basic")
            
            # Check tier requirements
            if not self._is_tier_sufficient(tier, required_tier):
                raise FeatureNotLicensedError(
                    ", ".join(required_features), required_tier, tier, self.machine_id
                )
            
            # Check feature availability
            available_features = FEATURE_TIERS.get(tier, {}).get("features", [])
            for feature in required_features:
                if feature not in available_features:
                    raise FeatureNotLicensedError(
                        feature, required_tier, tier, self.machine_id
                    )
            
            # Check usage limits
            if not self._check_usage_limits(tier):
                limit = FEATURE_TIERS.get(tier, {}).get("max_operations", 0)
                current = self.usage_data.get("daily_operations", 0)
                raise UsageLimitExceededError(limit, current, self.machine_id)
            
            # All checks passed
            self._increment_usage()
            return True
        
        # No valid license, check grace period
        if self._is_grace_active():
            grace_data = self._load_grace_data()
            
            # Check grace period usage limits
            tier = "evaluation"
            if not self._check_usage_limits(tier):
                limit = FEATURE_TIERS.get(tier, {}).get("max_operations", 0)
                current = self.usage_data.get("daily_operations", 0)
                raise UsageLimitExceededError(limit, current, self.machine_id)
            
            # Check if features are available in evaluation tier
            available_features = FEATURE_TIERS.get(tier, {}).get("features", [])
            for feature in required_features:
                if feature not in available_features:
                    raise FeatureNotLicensedError(
                        feature, required_tier, tier, self.machine_id
                    )
            
            self._increment_usage()
            logger.warning(f"Using grace period - contact {LICENSE_CONFIG['contact_email']} for licensing")
            return True
        
        # Check if grace period has expired
        grace_data = self._load_grace_data()
        if grace_data and self._is_grace_expired(grace_data):
            raise GracePeriodExpiredError(self.machine_id)
        
        # No license and no grace period - start grace period
        self.start_grace_period()
        raise LicenseNotFoundError(self.machine_id)
    
    def _is_tier_sufficient(self, current_tier: str, required_tier: str) -> bool:
        """Check if current tier meets requirements."""
        tier_hierarchy = ["evaluation", "basic", "professional", "enterprise", "research"]
        
        try:
            current_level = tier_hierarchy.index(current_tier)
            required_level = tier_hierarchy.index(required_tier)
            return current_level >= required_level
        except ValueError:
            return False
    
    def get_license_status(self) -> Dict[str, Any]:
        """Get comprehensive license status."""
        license_data = self._load_license()
        grace_data = self._load_grace_data()
        
        status = {
            "machine_id": self.machine_id,
            "has_license": False,
            "license_valid": False,
            "tier": None,
            "grace_active": False,
            "grace_remaining_hours": 0,
            "usage_today": self.usage_data.get("daily_operations", 0),
            "features_available": [],
            "contact_email": LICENSE_CONFIG["contact_email"]
        }
        
        if license_data:
            status["has_license"] = True
            status["license_valid"] = not self._is_license_expired(license_data)
            status["tier"] = license_data.get("tier")
            status["expiry_date"] = license_data.get("expiry_date")
            
            if status["license_valid"]:
                tier_features = FEATURE_TIERS.get(status["tier"], {}).get("features", [])
                status["features_available"] = tier_features
        
        if self._is_grace_active():
            status["grace_active"] = True
            if grace_data:
                expiry_time = datetime.fromisoformat(grace_data["expiry_time"])
                remaining = expiry_time - datetime.now()
                status["grace_remaining_hours"] = max(0, remaining.total_seconds() / 3600)
            
            if not status["license_valid"]:
                status["tier"] = "evaluation"
                status["features_available"] = FEATURE_TIERS["evaluation"]["features"]
        
        return status


# Global license manager instance
_license_manager = LicenseManager()


def validate_license(package_name: str, required_features: Optional[List[str]] = None,
                    required_tier: str = "basic") -> bool:
    """
    Global license validation function.
    
    Args:
        package_name: Name of the package requiring validation
        required_features: List of required features
        required_tier: Minimum required license tier
        
    Returns:
        True if license is valid
    """
    return _license_manager.validate_license(package_name, required_features, required_tier)


def requires_license(features: Optional[List[str]] = None, tier: str = "basic", 
                    package: str = "quantumlangchain"):
    """
    Decorator for license-protected functions and methods.
    
    Args:
        features: Required features
        tier: Required license tier
        package: Package name for validation
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                validate_license(package, features, tier)
                return await func(*args, **kwargs)
            except QuantumLicenseError:
                raise
            except Exception as e:
                logger.error(f"Unexpected error in licensed function {func.__name__}: {e}")
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                validate_license(package, features, tier)
                return func(*args, **kwargs)
            except QuantumLicenseError:
                raise
            except Exception as e:
                logger.error(f"Unexpected error in licensed function {func.__name__}: {e}")
                raise
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


class LicensedComponent:
    """Base class for all licensed QuantumLangChain components."""
    
    def __init__(self, required_features: Optional[List[str]] = None, 
                 required_tier: str = "basic", package: str = "quantumlangchain"):
        self.required_features = required_features or ["core"]
        self.required_tier = required_tier
        self.package = package
        self._validate_component_access()
    
    def _validate_component_access(self):
        """Validate license access for this component."""
        validate_license(self.package, self.required_features, self.required_tier)
    
    def _check_feature_access(self, feature: str) -> bool:
        """Check access to specific feature."""
        try:
            validate_license(self.package, [feature], self.required_tier)
            return True
        except QuantumLicenseError:
            return False
    
    def _require_feature(self, feature: str, operation_name: str = "operation"):
        """Require specific feature for operation."""
        if not self._check_feature_access(feature):
            machine_id = _license_manager.get_machine_id()
            raise FeatureNotLicensedError(
                f"{operation_name} ({feature})", 
                self.required_tier, 
                _license_manager._get_license_tier() or "none",
                machine_id
            )


def get_license_status() -> Dict[str, Any]:
    """Get current license status."""
    return _license_manager.get_license_status()


def get_machine_id() -> str:
    """Get machine ID for licensing."""
    return _license_manager.get_machine_id()


def display_license_info():
    """Display user-friendly license information."""
    status = get_license_status()
    
    print("\n" + "="*60)
    print("🧬 QuantumLangChain License Status")
    print("="*60)
    
    print(f"🔧 Machine ID: {status['machine_id']}")
    
    if status["license_valid"]:
        print(f"✅ License Status: Valid ({status['tier'].title()} Tier)")
        print(f"📅 Expires: {status['expiry_date']}")
        print(f"🔧 Features: {', '.join(status['features_available'])}")
    elif status["grace_active"]:
        hours_remaining = status["grace_remaining_hours"]
        print(f"⏰ Grace Period: {hours_remaining:.1f} hours remaining")
        print(f"🔧 Features: {', '.join(status['features_available'])}")
        print(f"📧 Contact: {status['contact_email']} for licensing")
    else:
        print("❌ No valid license found")
        print(f"📧 Contact: {status['contact_email']} for licensing")
    
    print(f"📊 Usage Today: {status['usage_today']} operations")
    print("="*60 + "\n")


# Package-level license check
def _initialize_package_licensing():
    """Initialize package-level licensing on import."""
    try:
        validate_license("quantumlangchain", ["core"], "basic")
        logger.info("✅ QuantumLangChain: License validated successfully")
    except LicenseNotFoundError:
        logger.warning("⚠️ QuantumLangChain: Starting 24-hour evaluation period")
        print(f"\n🧬 QuantumLangChain Evaluation Period Started")
        print(f"📧 Contact: {LICENSE_CONFIG['contact_email']} for licensing")
        print(f"🔧 Machine ID: {get_machine_id()}")
        print(f"⏰ Grace Period: {LICENSE_CONFIG['grace_period_hours']} hours\n")
    except QuantumLicenseError as e:
        logger.error(f"❌ QuantumLangChain: License validation failed")
        print(str(e))
    except Exception as e:
        logger.error(f"Unexpected licensing error: {e}")


# Initialize licensing on module import
_initialize_package_licensing()
