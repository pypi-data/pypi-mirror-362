"""
Licensing integration for Entanglement-Enhanced NLP
Provides secure license validation with no bypass options.
"""

import platform
import uuid
import hashlib
from typing import Dict, List, Optional, Union
import warnings

try:
    from quantummeta_license import (
        validate_or_grace, 
        LicenseError, 
        LicenseExpiredError,
        FeatureNotLicensedError,
        LicenseNotFoundError
    )
    LICENSING_AVAILABLE = True
except ImportError:
    LICENSING_AVAILABLE = False
    warnings.warn(
        "QuantumMeta License package not found. "
        "Please install: pip install quantummeta-license",
        ImportWarning
    )


class LicenseManager:
    """
    Secure license manager for Entanglement-Enhanced NLP.
    No development mode or bypass options available.
    """
    
    PACKAGE_NAME = "entanglement-enhanced-nlp"
    CONTACT_EMAIL = "bajpaikrishna715@gmail.com"
    
    # Feature tiers
    CORE_FEATURES = ["basic_embedding", "basic_attention"]
    PRO_FEATURES = CORE_FEATURES + ["quantum_contextualizer", "advanced_embedding", "visualization"]
    ENTERPRISE_FEATURES = PRO_FEATURES + ["distributed_processing", "custom_quantum_ops", "enterprise_support"]
    
    def __init__(self):
        """Initialize license manager."""
        self._license_cache = {}
        self._machine_id = self._get_machine_id()
    
    def _get_machine_id(self) -> str:
        """Generate unique machine identifier."""
        # Get multiple hardware identifiers
        node = str(uuid.getnode())  # MAC address
        machine = platform.machine()
        system = platform.system()
        processor = platform.processor()
        
        # Create combined identifier
        combined = f"{node}-{machine}-{system}-{processor}"
        
        # Hash for privacy and consistency
        machine_hash = hashlib.sha256(combined.encode()).hexdigest()[:16]
        return machine_hash
    
    def _show_license_error(self, error_type: str, feature_name: str = "", additional_info: str = ""):
        """Display comprehensive license error with contact information and machine ID."""
        print("\n" + "="*70)
        print("🔒 ENTANGLEMENT-ENHANCED NLP - LICENSE REQUIRED")
        print("="*70)
        
        if error_type == "expired":
            print("🕒 Your license has EXPIRED.")
            print("   Your quantum NLP capabilities have been suspended.")
        elif error_type == "feature_not_licensed":
            print(f"🚫 Feature '{feature_name}' requires a higher license tier.")
            print("   Current operation cannot proceed without proper licensing.")
        elif error_type == "not_found":
            print("📋 No valid license found.")
            print("   This software requires a valid license to operate.")
        else:
            print(f"❌ License validation failed: {additional_info}")
        
        print("\n📧 TO OBTAIN A LICENSE:")
        print(f"   Contact: {self.CONTACT_EMAIL}")
        print("   Subject: Entanglement-Enhanced NLP License Request")
        print("\n🖥️  MACHINE INFORMATION (Required for licensing):")
        print(f"   Machine ID: {self._machine_id}")
        print(f"   System: {platform.system()} {platform.release()}")
        print(f"   Architecture: {platform.machine()}")
        
        print("\n🎯 AVAILABLE LICENSE TIERS:")
        print("   • CORE: Basic embedding and attention mechanisms")
        print("   • PRO: Full quantum contextualizer + visualization")
        print("   • ENTERPRISE: All features + enterprise support")
        
        print("\n⚠️  SOFTWARE OPERATION SUSPENDED")
        print("   No functionality available without proper licensing.")
        print("="*70)
    
    def validate_license(self, required_features: Optional[List[str]] = None) -> bool:
        """
        Validate license with strict enforcement.
        No bypass or development mode available.
        """
        if not LICENSING_AVAILABLE:
            self._show_license_error("not_found", additional_info="QuantumMeta License package not installed")
            raise RuntimeError("License validation failed: No licensing system available")
        
        required_features = required_features or ["core"]
        
        try:
            # Strict validation - no grace period, no development mode
            validate_or_grace(self.PACKAGE_NAME, required_features=required_features, grace_days=0)
            return True
            
        except LicenseExpiredError as e:
            self._show_license_error("expired")
            raise RuntimeError("License expired - software operation suspended") from e
            
        except FeatureNotLicensedError as e:
            feature_name = ", ".join(required_features)
            self._show_license_error("feature_not_licensed", feature_name)
            raise RuntimeError(f"Feature not licensed: {feature_name}") from e
            
        except LicenseNotFoundError as e:
            self._show_license_error("not_found")
            raise RuntimeError("No valid license found - software operation suspended") from e
            
        except LicenseError as e:
            self._show_license_error("validation_failed", additional_info=str(e))
            raise RuntimeError(f"License validation failed: {e}") from e
    
    def get_licensed_features(self) -> List[str]:
        """Get list of currently licensed features."""
        if not LICENSING_AVAILABLE:
            return []
        
        try:
            # Check each tier
            if self._check_features_quietly(self.ENTERPRISE_FEATURES):
                return self.ENTERPRISE_FEATURES
            elif self._check_features_quietly(self.PRO_FEATURES):
                return self.PRO_FEATURES
            elif self._check_features_quietly(self.CORE_FEATURES):
                return self.CORE_FEATURES
            else:
                return []
        except:
            return []
    
    def _check_features_quietly(self, features: List[str]) -> bool:
        """Check features without showing errors."""
        try:
            validate_or_grace(self.PACKAGE_NAME, required_features=features, grace_days=0)
            return True
        except:
            return False
    
    def get_license_info(self) -> Dict[str, Union[str, List[str]]]:
        """Get license information for display."""
        return {
            "package": self.PACKAGE_NAME,
            "machine_id": self._machine_id,
            "contact": self.CONTACT_EMAIL,
            "licensed_features": self.get_licensed_features(),
            "system_info": {
                "platform": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "processor": platform.processor()
            }
        }


# Global license manager instance
_license_manager = LicenseManager()


def requires_license(features: Optional[List[str]] = None):
    """
    Decorator for license-protected functions and methods.
    No bypass available.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            _license_manager.validate_license(features)
            return func(*args, **kwargs)
        
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator


def validate_class_license(features: Optional[List[str]] = None):
    """
    Validate license for class instantiation.
    Must be called in __init__ method.
    """
    _license_manager.validate_license(features)


def get_license_manager() -> LicenseManager:
    """Get the global license manager instance."""
    return _license_manager


def show_license_status():
    """Show current license status."""
    manager = get_license_manager()
    info = manager.get_license_info()
    
    print("\n🌌 ENTANGLEMENT-ENHANCED NLP - LICENSE STATUS")
    print("="*50)
    print(f"Package: {info['package']}")
    print(f"Machine ID: {info['machine_id']}")
    print(f"System: {info['system_info']['platform']} {info['system_info']['release']}")
    
    licensed_features = info['licensed_features']
    if licensed_features:
        print(f"✅ Licensed Features: {', '.join(licensed_features)}")
        
        if set(licensed_features) >= set(LicenseManager.ENTERPRISE_FEATURES):
            print("🏆 License Tier: ENTERPRISE")
        elif set(licensed_features) >= set(LicenseManager.PRO_FEATURES):
            print("💎 License Tier: PRO")
        elif set(licensed_features) >= set(LicenseManager.CORE_FEATURES):
            print("⭐ License Tier: CORE")
    else:
        print("❌ No valid license found")
        print(f"📧 Contact: {info['contact']} to obtain a license")
    
    print("="*50)
