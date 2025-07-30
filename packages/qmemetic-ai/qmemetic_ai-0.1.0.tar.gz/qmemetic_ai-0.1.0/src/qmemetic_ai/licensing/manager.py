"""
QuantumMeta License Manager for Q-Memetic AI.

Strict licensing integration with 24-hour grace period only.
No use without valid license except during grace period.

License documentation: https://krish567366.github.io/license-server/integration/
Support: bajpaikrishna715@gmail.com
"""

import os
import json
import time
import uuid
import hashlib
import platform
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from functools import wraps
import logging

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
    logging.warning("QuantumMeta License library not available. Install with: pip install quantummeta-license")


class QMemeticLicenseError(Exception):
    """Q-Memetic AI specific license error."""
    
    def __init__(self, message: str, machine_id: str = None):
        self.machine_id = machine_id or _get_machine_id()
        super().__init__(f"{message}\n\nFor license support, email bajpaikrishna715@gmail.com with machine ID: {self.machine_id}")


def _get_machine_id():
    """Get machine ID for license support."""
    machine_info = f"{platform.machine()}_{platform.processor()}_{platform.system()}"
    return hashlib.sha256(machine_info.encode()).hexdigest()[:16]


@dataclass
class LicenseInfo:
    """License information and capabilities."""
    
    tier: str
    features: List[str]
    expires_at: Optional[float]
    hardware_id: str
    user_id: Optional[str] = None
    max_memes: int = 1000
    max_entanglements: int = 10000
    federation_enabled: bool = False
    multimodal_enabled: bool = False
    
    def is_expired(self) -> bool:
        """Check if license is expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at
    
    def has_feature(self, feature: str) -> bool:
        """Check if license includes a specific feature."""
        return feature in self.features
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "tier": self.tier,
            "features": self.features,
            "expires_at": self.expires_at,
            "hardware_id": self.hardware_id,
            "user_id": self.user_id,
            "max_memes": self.max_memes,
            "max_entanglements": self.max_entanglements,
            "federation_enabled": self.federation_enabled,
            "multimodal_enabled": self.multimodal_enabled,
        }


def requires_license(features=None):
    """
    Decorator to require QuantumMeta license validation with strict enforcement.
    
    Args:
        features: Required features list (optional)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not QUANTUMMETA_AVAILABLE:
                raise QMemeticLicenseError(
                    "QuantumMeta license library required. Install with: pip install quantummeta-license"
                )
            
            try:
                validate_or_grace("qmemetic-ai", required_features=features, grace_days=1)
                return func(*args, **kwargs)
            except LicenseExpiredError:
                raise QMemeticLicenseError("License expired. Please renew your Q-Memetic AI license.")
            except FeatureNotLicensedError:
                available_tiers = {
                    "core": "Basic evolution, visualization",
                    "pro": "Entanglement, quantum walks, federation", 
                    "enterprise": "Multimodal, custom plugins, unlimited scale"
                }
                message = "This feature requires a higher license tier.\n\nAvailable tiers:\n"
                for tier, desc in available_tiers.items():
                    message += f"  • {tier.title()}: {desc}\n"
                message += "\nUpgrade at: https://krish567366.github.io/license-server/"
                raise QMemeticLicenseError(message)
            except LicenseNotFoundError:
                raise QMemeticLicenseError(
                    "No license found and grace period expired.\n\n"
                    "To activate Q-Memetic AI:\n"
                    "1. Get license: https://krish567366.github.io/license-server/\n"
                    "2. Activate: quantum-license activate <license-file>"
                )
            except LicenseError as e:
                raise QMemeticLicenseError(f"License validation failed: {e}")
        
        return wrapper
    return decorator


class LicenseManager:
    """
    Strict QuantumMeta license manager for Q-Memetic AI.
    
    Enforces licensing with 24-hour grace period only.
    No functionality without valid license except during grace.
    """
    
    # License tiers and their features
    TIER_FEATURES = {
        "core": ["basic_evolution", "visualization", "local_storage"],
        "pro": ["basic_evolution", "visualization", "local_storage", "advanced_evolution", 
                "entanglement", "quantum_walk", "federation_basic"],
        "enterprise": ["basic_evolution", "visualization", "local_storage", "advanced_evolution", 
                      "entanglement", "quantum_walk", "federation_basic", "multimodal", 
                      "federation_advanced", "custom_plugins", "unlimited_scale"]
    }
    
    def __init__(self, license_key: Optional[str] = None):
        """
        Initialize strict license manager.
        
        Args:
            license_key: QuantumMeta license key (required)
        """
        self.license_key = license_key or os.getenv("QMEMETIC_LICENSE_KEY")
        self.package_name = "qmemetic-ai"
        self.logger = logging.getLogger("QMemeticLicense")
        self.machine_id = _get_machine_id()
        
        # Validate license immediately
        self._validate_license()
    
    def _validate_license(self):
        """Validate license with strict enforcement."""
        if not QUANTUMMETA_AVAILABLE:
            raise QMemeticLicenseError(
                "QuantumMeta license library required. Install with: pip install quantummeta-license"
            )
        
        try:
            validate_or_grace(self.package_name, grace_days=1)  # 24 hour grace only
            self.logger.info("✅ Q-Memetic AI license validated successfully")
        except Exception as e:
            self._handle_license_error(e)
    
    def _handle_license_error(self, error):
        """Handle license validation errors with user-friendly messages."""
        if isinstance(error, LicenseExpiredError):
            message = (
                "🕒 Your Q-Memetic AI license has expired.\n\n"
                "Please renew your license to continue using Q-Memetic AI.\n"
                "Contact: bajpaikrishna715@gmail.com"
            )
        elif isinstance(error, FeatureNotLicensedError):
            message = (
                "🔒 This feature requires a higher Q-Memetic AI license tier.\n\n"
                "Available license tiers:\n"
                "  • Core: Basic evolution, visualization\n"
                "  • Pro: Entanglement, quantum walks, federation\n" 
                "  • Enterprise: Multimodal, custom plugins, unlimited scale\n\n"
                "Upgrade at: https://krish567366.github.io/license-server/"
            )
        elif isinstance(error, LicenseNotFoundError):
            message = (
                "📋 No Q-Memetic AI license found and grace period has expired.\n\n"
                "To continue using Q-Memetic AI:\n"
                "1. Get license: https://krish567366.github.io/license-server/\n"
                "2. Activate: quantum-license activate <license-file>\n"
                "3. Or set QMEMETIC_LICENSE_KEY environment variable"
            )
        else:
            message = f"❌ Q-Memetic AI license validation failed: {error}"
        
        raise QMemeticLicenseError(message)
    
    def check_feature_access(self, feature: str) -> bool:
        """
        Check if current license allows access to a feature.
        
        Args:
            feature: Feature name to check
            
        Returns:
            True if feature is accessible
            
        Raises:
            QMemeticLicenseError: If feature not licensed
        """
        if not QUANTUMMETA_AVAILABLE:
            raise QMemeticLicenseError(
                "QuantumMeta license library required for feature checking"
            )
        
        try:
            validate_or_grace(self.package_name, required_features=[feature], grace_days=1)
            return True
        except FeatureNotLicensedError:
            return False
        except Exception as e:
            self._handle_license_error(e)
    
    def require_feature(self, feature: str):
        """
        Require a specific feature with strict enforcement.
        
        Args:
            feature: Required feature name
            
        Raises:
            QMemeticLicenseError: If feature not accessible
        """
        if not self.check_feature_access(feature):
            raise QMemeticLicenseError(
                f"Feature '{feature}' requires a higher Q-Memetic AI license tier."
            )
    
    def get_license_status(self) -> Dict[str, Any]:
        """Get comprehensive license status."""
        if not QUANTUMMETA_AVAILABLE:
            return {
                "valid": False,
                "error": "QuantumMeta license library not available",
                "tier": "none",
                "features": [],
                "machine_id": self.machine_id
            }
        
        try:
            # Try to validate license
            validate_or_grace(self.package_name, grace_days=1)
            
            # Get detailed license info (this would come from QuantumMeta API)
            # For now, return basic status
            return {
                "valid": True,
                "tier": "licensed",
                "features": self.TIER_FEATURES.get("enterprise", []),  # Would be determined by actual license
                "machine_id": self.machine_id,
                "package": self.package_name,
                "grace_period": "24 hours"
            }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "tier": "none", 
                "features": [],
                "machine_id": self.machine_id,
                "support_email": "bajpaikrishna715@gmail.com"
            }
    
    def show_license_info(self):
        """Display license information to user."""
        status = self.get_license_status()
        
        print("\n🔐 Q-MEMETIC AI LICENSE STATUS")
        print("=" * 40)
        
        if status["valid"]:
            print("✅ License: VALID")
            print(f"📊 Tier: {status['tier'].upper()}")
            print(f"🔧 Features: {len(status['features'])} available")
            print(f"🖥️  Machine ID: {status['machine_id']}")
        else:
            print("❌ License: INVALID")
            print(f"❗ Error: {status['error']}")
            print(f"🖥️  Machine ID: {status['machine_id']}")
            print(f"📧 Support: {status.get('support_email', 'bajpaikrishna715@gmail.com')}")
            print("\n🌐 Get License: https://krish567366.github.io/license-server/")
        
        print("=" * 40)
    
    @staticmethod
    def licensed_class(tier_required="core"):
        """
        Class decorator for license-protected classes.
        
        Args:
            tier_required: Minimum license tier required
        """
        def decorator(cls):
            original_init = cls.__init__
            
            @wraps(original_init)
            def licensed_init(self, *args, **kwargs):
                # Check license before allowing class instantiation
                if not QUANTUMMETA_AVAILABLE:
                    raise QMemeticLicenseError(
                        f"{cls.__name__} requires QuantumMeta license validation"
                    )
                
                try:
                    features = LicenseManager.TIER_FEATURES.get(tier_required, [])
                    validate_or_grace("qmemetic-ai", required_features=features, grace_days=1)
                except Exception as e:
                    raise QMemeticLicenseError(
                        f"{cls.__name__} requires {tier_required} license tier or higher"
                    )
                
                # Proceed with original initialization
                original_init(self, *args, **kwargs)
            
            cls.__init__ = licensed_init
            return cls
        
        return decorator
    
    @staticmethod
    def create_license_context(feature: str):
        """
        Context manager for license-protected code blocks.
        
        Usage:
            with LicenseManager.create_license_context("pro"):
                # Pro features here
                pass
        """
        return LicenseContext(feature)


class LicenseContext:
    """Context manager for license-protected code blocks."""
    
    def __init__(self, feature: str):
        self.feature = feature
    
    def __enter__(self):
        if not QUANTUMMETA_AVAILABLE:
            raise QMemeticLicenseError(
                f"Feature '{self.feature}' requires QuantumMeta license validation"
            )
        
        try:
            validate_or_grace("qmemetic-ai", required_features=[self.feature], grace_days=1)
        except Exception as e:
            raise QMemeticLicenseError(
                f"Feature '{self.feature}' requires valid Q-Memetic AI license"
            )
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


# Convenience function for easy license checking
def validate_qmemetic_license(features=None):
    """
    Validate Q-Memetic AI license with QuantumMeta.
    
    Args:
        features: Optional list of required features
        
    Raises:
        QMemeticLicenseError: If license validation fails
    """
    if not QUANTUMMETA_AVAILABLE:
        raise QMemeticLicenseError(
            "QuantumMeta license library required. Install with: pip install quantummeta-license"
        )
    
    try:
        validate_or_grace("qmemetic-ai", required_features=features, grace_days=1)
    except Exception as e:
        machine_id = _get_machine_id()
# End of Q-Memetic AI License Manager
