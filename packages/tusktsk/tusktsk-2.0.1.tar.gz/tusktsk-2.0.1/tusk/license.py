"""
TuskLang SDK License Validation Module
Enterprise-grade license validation for Python SDK
"""

import hashlib
import hmac
import json
import time
import uuid
import requests
import os
import pickle
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

class TuskLicense:
    """License validation system for TuskLang Python SDK"""
    
    def __init__(self, license_key: str, api_key: str, cache_dir: Optional[str] = None):
        self.license_key = license_key
        self.api_key = api_key
        self.session_id = str(uuid.uuid4())
        self.license_cache = {}
        self.validation_history = []
        self.expiration_warnings = []
        
        # Set up offline cache directory
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path.home() / '.tusk' / 'license_cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / f"{hashlib.md5(license_key.encode()).hexdigest()}.cache"
        
        # Load offline cache if exists
        self._load_offline_cache()
        
        # Set up logging
        self.logger = logging.getLogger('TuskLicense')
    
    def validate_license_key(self) -> Dict[str, Any]:
        """Validate license key format and checksum"""
        try:
            if not self.license_key or len(self.license_key) < 32:
                return {"valid": False, "error": "Invalid license key format"}
            
            # Check license format
            if not self.license_key.startswith("TUSK-"):
                return {"valid": False, "error": "Invalid license key prefix"}
            
            # Verify checksum
            checksum = hashlib.sha256(self.license_key.encode()).hexdigest()
            if not checksum.startswith('tusk'):
                return {"valid": False, "error": "Invalid license key checksum"}
            
            return {"valid": True, "checksum": checksum}
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def verify_license_server(self, server_url: str = "https://api.tusklang.org/v1/license") -> Dict[str, Any]:
        """Verify license with remote server"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "license_key": self.license_key,
                "session_id": self.session_id,
                "timestamp": int(time.time())
            }
            
            # Add signature for security
            signature = hmac.new(
                self.api_key.encode(),
                json.dumps(data, sort_keys=True).encode(),
                hashlib.sha256
            ).hexdigest()
            data["signature"] = signature
            
            response = requests.post(server_url, json=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                # Update in-memory cache
                self.license_cache[self.license_key] = {
                    "data": result,
                    "timestamp": time.time(),
                    "expires": time.time() + 3600  # Cache for 1 hour
                }
                # Update offline cache
                self._save_offline_cache(result)
                return result
            else:
                self.logger.warning(f"Server returned error: {response.status_code}")
                return self._fallback_to_offline_cache(f"Server error: {response.status_code}")
                
        except requests.RequestException as e:
            self.logger.warning(f"Network error during license validation: {str(e)}")
            return self._fallback_to_offline_cache(f"Network error: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error during license validation: {str(e)}")
            return self._fallback_to_offline_cache(str(e))
    
    def check_license_expiration(self) -> Dict[str, Any]:
        """Check if license is expired or expiring soon"""
        try:
            # Parse license key for expiration info
            parts = self.license_key.split("-")
            if len(parts) < 4:
                return {"expired": True, "error": "Invalid license key format"}
            
            # Extract expiration timestamp (assuming format: TUSK-XXXX-YYYY-EXPIRES)
            expiration_str = parts[-1]
            try:
                expiration_timestamp = int(expiration_str, 16)
                expiration_date = datetime.fromtimestamp(expiration_timestamp)
                current_date = datetime.now()
                
                if expiration_date < current_date:
                    return {
                        "expired": True,
                        "expiration_date": expiration_date.isoformat(),
                        "days_overdue": (current_date - expiration_date).days
                    }
                
                days_until_expiration = (expiration_date - current_date).days
                
                # Warn if expiring within 30 days
                if days_until_expiration <= 30:
                    self.expiration_warnings.append({
                        "timestamp": time.time(),
                        "days_remaining": days_until_expiration
                    })
                
                return {
                    "expired": False,
                    "expiration_date": expiration_date.isoformat(),
                    "days_remaining": days_until_expiration,
                    "warning": days_until_expiration <= 30
                }
                
            except ValueError:
                return {"expired": True, "error": "Invalid expiration timestamp"}
                
        except Exception as e:
            return {"expired": True, "error": str(e)}
    
    def validate_license_permissions(self, feature: str) -> Dict[str, Any]:
        """Validate if license allows specific feature"""
        try:
            # Check cached license data
            if self.license_key in self.license_cache:
                cache_data = self.license_cache[self.license_key]
                if time.time() < cache_data["expires"]:
                    license_data = cache_data["data"]
                    if "features" in license_data:
                        allowed_features = license_data["features"]
                        if feature in allowed_features:
                            return {"allowed": True, "feature": feature}
                        else:
                            return {"allowed": False, "feature": feature, "error": "Feature not licensed"}
            
            # Fallback to basic validation
            if feature in ["basic", "core", "standard"]:
                return {"allowed": True, "feature": feature}
            elif feature in ["premium", "enterprise"]:
                # Check if license key indicates premium
                if "PREMIUM" in self.license_key.upper() or "ENTERPRISE" in self.license_key.upper():
                    return {"allowed": True, "feature": feature}
                else:
                    return {"allowed": False, "feature": feature, "error": "Premium license required"}
            else:
                return {"allowed": False, "feature": feature, "error": "Unknown feature"}
                
        except Exception as e:
            return {"allowed": False, "feature": feature, "error": str(e)}
    
    def get_license_info(self) -> Dict[str, Any]:
        """Get comprehensive license information"""
        try:
            validation_result = self.validate_license_key()
            expiration_result = self.check_license_expiration()
            
            info = {
                "license_key": self.license_key[:8] + "..." + self.license_key[-4:],
                "session_id": self.session_id,
                "validation": validation_result,
                "expiration": expiration_result,
                "cache_status": "cached" if self.license_key in self.license_cache else "not_cached",
                "validation_count": len(self.validation_history),
                "warnings": len(self.expiration_warnings)
            }
            
            # Add cached data if available
            if self.license_key in self.license_cache:
                cache_data = self.license_cache[self.license_key]
                info["cached_data"] = cache_data["data"]
                info["cache_age"] = time.time() - cache_data["timestamp"]
            
            return info
            
        except Exception as e:
            return {"error": str(e)}
    
    def refresh_license_cache(self) -> Dict[str, Any]:
        """Refresh license cache from server"""
        try:
            if self.license_key in self.license_cache:
                del self.license_cache[self.license_key]
            
            return self.verify_license_server()
            
        except Exception as e:
            return {"error": str(e)}
    
    def log_validation_attempt(self, success: bool, details: str = ""):
        """Log license validation attempts"""
        self.validation_history.append({
            "timestamp": time.time(),
            "success": success,
            "details": details,
            "session_id": self.session_id
        })
    
    def get_validation_history(self) -> list:
        """Get validation history"""
        return self.validation_history
    
    def clear_validation_history(self):
        """Clear validation history"""
        self.validation_history.clear()
    
    def _load_offline_cache(self):
        """Load offline license cache from disk"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                    # Verify the cache is for the correct license key
                    if cached_data.get('license_key_hash') == hashlib.sha256(self.license_key.encode()).hexdigest():
                        self.offline_cache = cached_data
                        self.logger.info("Loaded offline license cache")
                    else:
                        self.offline_cache = None
                        self.logger.warning("Offline cache key mismatch")
            else:
                self.offline_cache = None
        except Exception as e:
            self.logger.error(f"Failed to load offline cache: {str(e)}")
            self.offline_cache = None
    
    def _save_offline_cache(self, license_data: Dict[str, Any]):
        """Save license data to offline cache"""
        try:
            cache_data = {
                'license_key_hash': hashlib.sha256(self.license_key.encode()).hexdigest(),
                'license_data': license_data,
                'timestamp': time.time(),
                'expiration': self.check_license_expiration()
            }
            with open(self.cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
            self.offline_cache = cache_data
            self.logger.info("Saved license data to offline cache")
        except Exception as e:
            self.logger.error(f"Failed to save offline cache: {str(e)}")
    
    def _fallback_to_offline_cache(self, error_msg: str) -> Dict[str, Any]:
        """Fallback to offline cache when server is unreachable"""
        if self.offline_cache and self.offline_cache.get('license_data'):
            cache_age = time.time() - self.offline_cache.get('timestamp', 0)
            cache_age_days = cache_age / 86400
            
            # Check if cached license is not expired
            expiration = self.offline_cache.get('expiration', {})
            if not expiration.get('expired', True):
                self.logger.warning(f"Using offline license cache (age: {cache_age_days:.1f} days)")
                return {
                    **self.offline_cache['license_data'],
                    'offline_mode': True,
                    'cache_age_days': cache_age_days,
                    'warning': f'Operating in offline mode due to: {error_msg}'
                }
            else:
                return {
                    "valid": False,
                    "error": f"License expired and server unreachable: {error_msg}",
                    "offline_cache_expired": True
                }
        else:
            return {
                "valid": False,
                "error": f"No offline cache available: {error_msg}",
                "offline_cache_missing": True
            }

# Global license instance
_license_instance: Optional[TuskLicense] = None

def initialize_license(license_key: str, api_key: str, cache_dir: Optional[str] = None) -> TuskLicense:
    """Initialize global license instance"""
    global _license_instance
    _license_instance = TuskLicense(license_key, api_key, cache_dir)
    return _license_instance

def get_license() -> TuskLicense:
    """Get global license instance"""
    if _license_instance is None:
        raise RuntimeError("License not initialized. Call initialize_license() first.")
    return _license_instance 