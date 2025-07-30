"""
Quantum GANs Pro License Manager

This module handles license validation for the quantum-generative-adversarial-networks-pro package.
All functionality requires a valid license from Krishna Bajpai (bajpaikrishna715@gmail.com).
"""

import os
import sys
import uuid
import hashlib
import platform
from functools import wraps
from typing import Optional, List, Dict, Any
import warnings


class LicenseError(Exception):
    """Base license validation error."""
    pass


class LicenseExpiredError(LicenseError):
    """License has expired."""
    pass


class LicenseNotFoundError(LicenseError):
    """No valid license found."""
    pass


class FeatureNotLicensedError(LicenseError):
    """Feature not licensed."""
    pass


class MachineIdMismatchError(LicenseError):
    """License machine ID does not match current machine."""
    pass


class LicenseManager:
    """
    Manages license validation for Quantum GANs Pro.
    
    No development mode, no bypass - all functionality requires valid license.
    """
    
    PACKAGE_NAME = "quantum-generative-adversarial-networks-pro"
    LICENSE_FILE = ".qgans_pro_license"
    AUTHOR_EMAIL = "bajpaikrishna715@gmail.com"
    
    def __init__(self):
        self._machine_id = self._get_machine_id()
        self._license_cache = {}
    
    def _get_machine_id(self) -> str:
        """Generate unique machine identifier."""
        try:
            # Get machine-specific information
            hostname = platform.node()
            mac = hex(uuid.getnode())[2:]
            platform_info = platform.platform()
            
            # Create unique machine fingerprint
            machine_string = f"{hostname}-{mac}-{platform_info}"
            machine_id = hashlib.sha256(machine_string.encode()).hexdigest()[:16]
            
            return machine_id
        except Exception:
            # Fallback machine ID
            return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:16]
    
    def get_machine_id(self) -> str:
        """Get the current machine ID for license registration."""
        return self._machine_id
    
    def _find_license_file(self) -> Optional[str]:
        """Find license file in various locations."""
        # Possible locations for license file
        search_paths = [
            os.getcwd(),  # Current directory
            os.path.expanduser("~"),  # Home directory
            os.path.expanduser("~/.qgans_pro"),  # Hidden config directory
            os.path.dirname(os.path.abspath(__file__)),  # Package directory
            "/etc/qgans_pro",  # System-wide (Linux/Mac)
            os.path.join(os.environ.get("APPDATA", ""), "qgans_pro")  # Windows
        ]
        
        for path in search_paths:
            if not path:
                continue
            license_path = os.path.join(path, self.LICENSE_FILE)
            if os.path.exists(license_path):
                return license_path
        
        return None
    
    def _validate_license_format(self, license_data: Dict[str, Any]) -> bool:
        """Validate license file format and signature."""
        required_fields = ["package", "user", "email", "machine_id", "features", "expiry", "signature"]
        
        # Check required fields
        if not all(field in license_data for field in required_fields):
            return False
        
        # Verify package name
        if license_data["package"] != self.PACKAGE_NAME:
            return False
        
        # Verify machine ID
        if license_data["machine_id"] != self._machine_id:
            return False
        
        # TODO: Add cryptographic signature verification
        # For now, simple validation
        expected_signature = hashlib.sha256(
            f"{license_data['package']}-{license_data['user']}-{license_data['machine_id']}".encode()
        ).hexdigest()[:32]
        
        return license_data["signature"].startswith(expected_signature[:8])
    
    def validate_license(self, required_features: Optional[List[str]] = None) -> bool:
        """
        Validate license for the package.
        
        Args:
            required_features: List of required features
            
        Returns:
            True if license is valid
            
        Raises:
            LicenseError: If license validation fails
        """
        # Check cache first
        cache_key = f"{self.PACKAGE_NAME}-{'-'.join(required_features or [])}"
        if cache_key in self._license_cache:
            cached_result = self._license_cache[cache_key]
            if cached_result["valid"]:
                return True
            else:
                raise cached_result["error"]
        
        # Find license file
        license_file = self._find_license_file()
        if not license_file:
            error = LicenseNotFoundError(
                f"❌ No valid license found for {self.PACKAGE_NAME}\n"
                f"📧 Contact: {self.AUTHOR_EMAIL}\n"
                f"🔧 Machine ID: {self._machine_id}\n"
                f"💡 Please provide your Machine ID when requesting a license."
            )
            self._license_cache[cache_key] = {"valid": False, "error": error}
            raise error
        
        try:
            # Read and parse license
            import json
            with open(license_file, 'r') as f:
                license_data = json.load(f)
        except Exception as e:
            error = LicenseError(
                f"❌ Invalid license file format: {e}\n"
                f"📧 Contact: {self.AUTHOR_EMAIL}\n"
                f"🔧 Machine ID: {self._machine_id}"
            )
            self._license_cache[cache_key] = {"valid": False, "error": error}
            raise error
        
        # Validate license format
        if not self._validate_license_format(license_data):
            error = LicenseError(
                f"❌ Invalid license file or machine mismatch\n"
                f"📧 Contact: {self.AUTHOR_EMAIL}\n"
                f"🔧 Your Machine ID: {self._machine_id}\n"
                f"🔧 License Machine ID: {license_data.get('machine_id', 'unknown')}\n"
                f"💡 License must be generated for this specific machine."
            )
            self._license_cache[cache_key] = {"valid": False, "error": error}
            raise error
        
        # Check expiry
        from datetime import datetime
        try:
            expiry_date = datetime.fromisoformat(license_data["expiry"])
            if datetime.now() > expiry_date:
                error = LicenseExpiredError(
                    f"🕒 License expired on {expiry_date.strftime('%Y-%m-%d')}\n"
                    f"📧 Contact for renewal: {self.AUTHOR_EMAIL}\n"
                    f"🔧 Machine ID: {self._machine_id}"
                )
                self._license_cache[cache_key] = {"valid": False, "error": error}
                raise error
        except ValueError:
            error = LicenseError(
                f"❌ Invalid license expiry date format\n"
                f"📧 Contact: {self.AUTHOR_EMAIL}\n"
                f"🔧 Machine ID: {self._machine_id}"
            )
            self._license_cache[cache_key] = {"valid": False, "error": error}
            raise error
        
        # Check required features
        if required_features:
            licensed_features = license_data.get("features", [])
            missing_features = [f for f in required_features if f not in licensed_features]
            if missing_features:
                error = FeatureNotLicensedError(
                    f"🔒 Features not licensed: {', '.join(missing_features)}\n"
                    f"✅ Your licensed features: {', '.join(licensed_features)}\n"
                    f"📧 Contact for feature upgrade: {self.AUTHOR_EMAIL}\n"
                    f"🔧 Machine ID: {self._machine_id}"
                )
                self._license_cache[cache_key] = {"valid": False, "error": error}
                raise error
        
        # Cache successful validation
        self._license_cache[cache_key] = {"valid": True, "error": None}
        return True
    
    def get_license_info(self) -> Optional[Dict[str, Any]]:
        """Get license information if available."""
        license_file = self._find_license_file()
        if not license_file:
            return None
        
        try:
            import json
            with open(license_file, 'r') as f:
                return json.load(f)
        except Exception:
            return None
    
    def show_license_status(self):
        """Display current license status."""
        print(f"\n🔐 Quantum GANs Pro License Status")
        print("=" * 50)
        print(f"📦 Package: {self.PACKAGE_NAME}")
        print(f"🔧 Machine ID: {self._machine_id}")
        
        license_info = self.get_license_info()
        if license_info:
            from datetime import datetime
            try:
                expiry = datetime.fromisoformat(license_info["expiry"])
                days_left = (expiry - datetime.now()).days
                
                print(f"✅ Licensed to: {license_info['user']} ({license_info['email']})")
                print(f"📅 Expires: {expiry.strftime('%Y-%m-%d')} ({days_left} days)")
                print(f"🔧 Features: {', '.join(license_info['features'])}")
                
                if days_left < 30:
                    print(f"⚠️  License expires in {days_left} days!")
                    print(f"📧 Contact for renewal: {self.AUTHOR_EMAIL}")
            except Exception:
                print("❌ Invalid license file")
        else:
            print("❌ No license found")
        
        print(f"📧 Support: {self.AUTHOR_EMAIL}")
        print("=" * 50)


# Global license manager instance
_license_manager = LicenseManager()


def requires_license(features: Optional[List[str]] = None, critical: bool = True):
    """
    Decorator to require license validation for functions/methods.
    
    Args:
        features: Required features list
        critical: If True, raises exception on validation failure
        
    Usage:
        @requires_license(features=["quantum", "training"])
        def advanced_training():
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                _license_manager.validate_license(required_features=features)
                return func(*args, **kwargs)
            except LicenseError as e:
                if critical:
                    raise RuntimeError(f"🔒 License required for {func.__name__}:\n{e}")
                else:
                    warnings.warn(f"License validation failed for {func.__name__}: {e}")
                    return None
        return wrapper
    return decorator


def requires_license_class(features: Optional[List[str]] = None):
    """
    Class decorator to require license validation for all class methods.
    
    Args:
        features: Required features list
        
    Usage:
        @requires_license_class(features=["quantum"])
        class QuantumGenerator:
            pass
    """
    def decorator(cls):
        # Get original __init__ and __new__ methods
        original_init = cls.__init__
        original_new = cls.__new__
        
        @wraps(original_init)
        def licensed_init(self, *args, **kwargs):
            # Validate license before instance creation
            _license_manager.validate_license(required_features=features)
            return original_init(self, *args, **kwargs)
        
        @wraps(original_new)
        def licensed_new(cls, *args, **kwargs):
            # Validate license before class instantiation
            _license_manager.validate_license(required_features=features)
            if original_new is object.__new__:
                return original_new(cls)
            return original_new(cls, *args, **kwargs)
        
        # Replace methods
        cls.__init__ = licensed_init
        cls.__new__ = licensed_new
        
        # Add license info to class
        cls._license_features = features
        cls._license_manager = _license_manager
        
        return cls
    return decorator


def validate_package_license():
    """Validate license for the entire package."""
    try:
        _license_manager.validate_license()
        return True
    except LicenseError as e:
        print(f"\n{e}\n")
        return False


def get_machine_id() -> str:
    """Get machine ID for license registration."""
    return _license_manager.get_machine_id()


def show_license_status():
    """Show current license status."""
    _license_manager.show_license_status()


def create_license_request():
    """Create a license request with machine information."""
    machine_id = get_machine_id()
    
    print("\n🔐 Quantum GANs Pro License Request")
    print("=" * 50)
    print(f"📦 Package: {LicenseManager.PACKAGE_NAME}")
    print(f"🔧 Machine ID: {machine_id}")
    print(f"💻 Platform: {platform.platform()}")
    print(f"🏠 Hostname: {platform.node()}")
    print("=" * 50)
    print(f"📧 Send this information to: {LicenseManager.AUTHOR_EMAIL}")
    print("📝 Include the following in your request:")
    print(f"   - Your name and organization")
    print(f"   - Machine ID: {machine_id}")
    print(f"   - Intended use case")
    print(f"   - Required features (if known)")
    print("=" * 50)
    
    return {
        "package": LicenseManager.PACKAGE_NAME,
        "machine_id": machine_id,
        "platform": platform.platform(),
        "hostname": platform.node()
    }


# Package-level license validation - NO BYPASS
if not validate_package_license():
    print("\n💡 To request a license, run:")
    print("   python -c \"from qgans_pro.license import create_license_request; create_license_request()\"")
    print(f"\n📧 Contact: {LicenseManager.AUTHOR_EMAIL}")
    
    # Prevent import without license
    sys.exit(1)
