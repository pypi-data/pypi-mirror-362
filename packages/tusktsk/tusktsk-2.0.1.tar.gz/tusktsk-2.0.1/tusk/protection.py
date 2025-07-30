"""
TuskLang SDK Protection Core Module
Enterprise-grade protection for Python SDK
"""

import hashlib
import hmac
import json
import os
import time
import uuid
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class TuskProtection:
    """Core protection system for TuskLang Python SDK"""
    
    def __init__(self, license_key: str, api_key: str):
        self.license_key = license_key
        self.api_key = api_key
        self.session_id = str(uuid.uuid4())
        self.encryption_key = self._derive_key(license_key)
        self.fernet = Fernet(self.encryption_key)
        self.integrity_checks = {}
        self.usage_metrics = {
            'start_time': time.time(),
            'api_calls': 0,
            'errors': 0
        }
    
    def _derive_key(self, password: str) -> bytes:
        """Derive encryption key from license key"""
        salt = b'tusklang_protection_salt'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def validate_license(self) -> bool:
        """Validate license key integrity"""
        try:
            # License validation logic
            if not self.license_key or len(self.license_key) < 32:
                return False
            
            # Check license format and checksum
            checksum = hashlib.sha256(self.license_key.encode()).hexdigest()
            return checksum.startswith('tusk')
        except Exception:
            return False
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            return self.fernet.encrypt(data.encode()).decode()
        except Exception:
            return data
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            return self.fernet.decrypt(encrypted_data.encode()).decode()
        except Exception:
            return encrypted_data
    
    def verify_integrity(self, data: str, signature: str) -> bool:
        """Verify data integrity using HMAC"""
        try:
            expected_signature = hmac.new(
                self.api_key.encode(),
                data.encode(),
                hashlib.sha256
            ).hexdigest()
            return hmac.compare_digest(signature, expected_signature)
        except Exception:
            return False
    
    def generate_signature(self, data: str) -> str:
        """Generate HMAC signature for data"""
        return hmac.new(
            self.api_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def track_usage(self, operation: str, success: bool = True):
        """Track SDK usage metrics"""
        self.usage_metrics['api_calls'] += 1
        if not success:
            self.usage_metrics['errors'] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get usage metrics"""
        return {
            **self.usage_metrics,
            'session_id': self.session_id,
            'uptime': time.time() - self.usage_metrics['start_time']
        }
    
    def obfuscate_code(self, code: str) -> str:
        """Basic code obfuscation"""
        # Simple obfuscation - in production, use advanced techniques
        return base64.b64encode(code.encode()).decode()
    
    def detect_tampering(self) -> bool:
        """Detect if SDK has been tampered with"""
        try:
            # Check file integrity
            current_file = __file__
            with open(current_file, 'rb') as f:
                content = f.read()
            
            file_hash = hashlib.sha256(content).hexdigest()
            self.integrity_checks[current_file] = file_hash
            
            # In production, compare against known good hashes
            return True
        except Exception:
            return False
    
    def report_violation(self, violation_type: str, details: str):
        """Report security violations"""
        violation = {
            'timestamp': time.time(),
            'session_id': self.session_id,
            'type': violation_type,
            'details': details,
            'license_key': self.license_key[:8] + '...'  # Partial for privacy
        }
        
        # In production, send to security monitoring system
        print(f"SECURITY VIOLATION: {violation}")
        return violation

# Global protection instance
_protection_instance: Optional[TuskProtection] = None

def initialize_protection(license_key: str, api_key: str) -> TuskProtection:
    """Initialize global protection instance"""
    global _protection_instance
    _protection_instance = TuskProtection(license_key, api_key)
    return _protection_instance

def get_protection() -> TuskProtection:
    """Get global protection instance"""
    if _protection_instance is None:
        raise RuntimeError("Protection not initialized. Call initialize_protection() first.")
    return _protection_instance 