"""
TuskLang SDK Authentication Module
Enterprise-grade authentication and key management for Python SDK
"""

import hashlib
import hmac
import json
import time
import uuid
import base64
import secrets
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

@dataclass
class AuthToken:
    """Represents an authentication token"""
    token: str
    expires_at: float
    user_id: str
    permissions: List[str]
    created_at: float

@dataclass
class ApiKey:
    """Represents an API key"""
    key_id: str
    key_hash: str
    user_id: str
    permissions: List[str]
    created_at: float
    last_used: Optional[float] = None
    expires_at: Optional[float] = None

class TuskAuth:
    """Authentication system for TuskLang Python SDK"""
    
    def __init__(self, master_key: str):
        self.master_key = master_key
        self.encryption_key = self._derive_key(master_key)
        self.fernet = Fernet(self.encryption_key)
        
        # Key storage
        self.api_keys: Dict[str, ApiKey] = {}
        self.auth_tokens: Dict[str, AuthToken] = {}
        self.key_rotation_schedule = {}
        
        # Security settings
        self.token_expiry = 3600  # 1 hour
        self.key_expiry = 86400 * 30  # 30 days
        self.max_failed_attempts = 5
        self.lockout_duration = 300  # 5 minutes
        self.failed_attempts = {}
        
        # Generate master key pair
        self._generate_master_keys()
    
    def _derive_key(self, password: str) -> bytes:
        """Derive encryption key from master key"""
        salt = b'tusklang_auth_salt'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def _generate_master_keys(self):
        """Generate master RSA key pair"""
        try:
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            self.public_key = self.private_key.public_key()
        except Exception as e:
            # Fallback to symmetric encryption
            self.private_key = None
            self.public_key = None
    
    def generate_api_key(self, user_id: str, permissions: List[str], expires_in: Optional[int] = None) -> str:
        """Generate a new API key"""
        try:
            # Generate key ID and secret
            key_id = str(uuid.uuid4())
            secret = secrets.token_urlsafe(32)
            full_key = f"{key_id}.{secret}"
            
            # Hash the secret for storage
            key_hash = hashlib.sha256(secret.encode()).hexdigest()
            
            # Calculate expiry
            created_at = time.time()
            expires_at = None
            if expires_in:
                expires_at = created_at + expires_in
            
            # Store API key
            api_key = ApiKey(
                key_id=key_id,
                key_hash=key_hash,
                user_id=user_id,
                permissions=permissions,
                created_at=created_at,
                expires_at=expires_at
            )
            
            self.api_keys[key_id] = api_key
            
            # Schedule key rotation if needed
            if expires_at:
                self.key_rotation_schedule[key_id] = expires_at
            
            return full_key
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate API key: {str(e)}")
    
    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate an API key"""
        try:
            # Parse key
            if '.' not in api_key:
                return None
            
            key_id, secret = api_key.split('.', 1)
            
            # Check if key exists
            if key_id not in self.api_keys:
                return None
            
            stored_key = self.api_keys[key_id]
            
            # Check if key is expired
            if stored_key.expires_at and time.time() > stored_key.expires_at:
                return None
            
            # Validate secret
            secret_hash = hashlib.sha256(secret.encode()).hexdigest()
            if not hmac.compare_digest(stored_key.key_hash, secret_hash):
                return None
            
            # Update last used
            stored_key.last_used = time.time()
            
            return {
                'user_id': stored_key.user_id,
                'permissions': stored_key.permissions,
                'key_id': key_id
            }
            
        except Exception:
            return None
    
    def revoke_api_key(self, key_id: str) -> bool:
        """Revoke an API key"""
        try:
            if key_id in self.api_keys:
                del self.api_keys[key_id]
                if key_id in self.key_rotation_schedule:
                    del self.key_rotation_schedule[key_id]
                return True
            return False
        except Exception:
            return False
    
    def generate_auth_token(self, user_id: str, permissions: List[str], expires_in: Optional[int] = None) -> str:
        """Generate an authentication token"""
        try:
            # Generate token
            token_data = {
                'user_id': user_id,
                'permissions': permissions,
                'created_at': time.time(),
                'nonce': secrets.token_urlsafe(16)
            }
            
            # Set expiry
            if expires_in:
                token_data['expires_at'] = time.time() + expires_in
            else:
                token_data['expires_at'] = time.time() + self.token_expiry
            
            # Sign token
            token_json = json.dumps(token_data, sort_keys=True)
            signature = hmac.new(
                self.master_key.encode(),
                token_json.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Create final token
            token_parts = [token_json, signature]
            token = base64.urlsafe_b64encode('.'.join(token_parts).encode()).decode()
            
            # Store token
            auth_token = AuthToken(
                token=token,
                expires_at=token_data['expires_at'],
                user_id=user_id,
                permissions=permissions,
                created_at=token_data['created_at']
            )
            
            self.auth_tokens[token] = auth_token
            
            return token
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate auth token: {str(e)}")
    
    def validate_auth_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate an authentication token"""
        try:
            # Decode token
            decoded = base64.urlsafe_b64decode(token.encode()).decode()
            token_json, signature = decoded.split('.', 1)
            
            # Verify signature
            expected_signature = hmac.new(
                self.master_key.encode(),
                token_json.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                return None
            
            # Parse token data
            token_data = json.loads(token_json)
            
            # Check expiry
            if 'expires_at' in token_data and time.time() > token_data['expires_at']:
                return None
            
            # Check if token is in storage
            if token not in self.auth_tokens:
                return None
            
            return {
                'user_id': token_data['user_id'],
                'permissions': token_data['permissions'],
                'created_at': token_data['created_at']
            }
            
        except Exception:
            return None
    
    def revoke_auth_token(self, token: str) -> bool:
        """Revoke an authentication token"""
        try:
            if token in self.auth_tokens:
                del self.auth_tokens[token]
                return True
            return False
        except Exception:
            return False
    
    def check_permission(self, user_id: str, permission: str, auth_data: Dict[str, Any]) -> bool:
        """Check if user has specific permission"""
        try:
            permissions = auth_data.get('permissions', [])
            return permission in permissions or 'admin' in permissions
        except Exception:
            return False
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            return self.fernet.encrypt(data.encode()).decode()
        except Exception:
            return data
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            return self.fernet.decrypt(encrypted_data.encode()).decode()
        except Exception:
            return encrypted_data
    
    def rotate_keys(self) -> List[str]:
        """Rotate expired keys"""
        try:
            current_time = time.time()
            rotated_keys = []
            
            # Check API keys
            keys_to_remove = []
            for key_id, api_key in self.api_keys.items():
                if api_key.expires_at and current_time > api_key.expires_at:
                    keys_to_remove.append(key_id)
                    rotated_keys.append(key_id)
            
            for key_id in keys_to_remove:
                del self.api_keys[key_id]
                if key_id in self.key_rotation_schedule:
                    del self.key_rotation_schedule[key_id]
            
            # Check auth tokens
            tokens_to_remove = []
            for token, auth_token in self.auth_tokens.items():
                if current_time > auth_token.expires_at:
                    tokens_to_remove.append(token)
                    rotated_keys.append(token)
            
            for token in tokens_to_remove:
                del self.auth_tokens[token]
            
            return rotated_keys
            
        except Exception as e:
            raise RuntimeError(f"Failed to rotate keys: {str(e)}")
    
    def get_auth_stats(self) -> Dict[str, Any]:
        """Get authentication statistics"""
        try:
            current_time = time.time()
            
            # Count active keys and tokens
            active_api_keys = sum(1 for key in self.api_keys.values() 
                                if not key.expires_at or current_time < key.expires_at)
            
            active_tokens = sum(1 for token in self.auth_tokens.values() 
                              if current_time < token.expires_at)
            
            # Count expired items
            expired_api_keys = sum(1 for key in self.api_keys.values() 
                                 if key.expires_at and current_time >= key.expires_at)
            
            expired_tokens = sum(1 for token in self.auth_tokens.values() 
                               if current_time >= token.expires_at)
            
            return {
                'active_api_keys': active_api_keys,
                'active_tokens': active_tokens,
                'expired_api_keys': expired_api_keys,
                'expired_tokens': expired_tokens,
                'total_api_keys': len(self.api_keys),
                'total_tokens': len(self.auth_tokens),
                'failed_attempts': len(self.failed_attempts)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def cleanup_expired(self):
        """Clean up expired keys and tokens"""
        try:
            self.rotate_keys()
            
            # Clean up failed attempts
            current_time = time.time()
            expired_attempts = []
            for user_id, attempt_data in self.failed_attempts.items():
                if current_time - attempt_data['last_attempt'] > self.lockout_duration:
                    expired_attempts.append(user_id)
            
            for user_id in expired_attempts:
                del self.failed_attempts[user_id]
                
        except Exception as e:
            raise RuntimeError(f"Failed to cleanup expired items: {str(e)}")

# Global auth instance
_auth_instance: Optional[TuskAuth] = None

def initialize_auth(master_key: str) -> TuskAuth:
    """Initialize global auth instance"""
    global _auth_instance
    _auth_instance = TuskAuth(master_key)
    return _auth_instance

def get_auth() -> TuskAuth:
    """Get global auth instance"""
    if _auth_instance is None:
        raise RuntimeError("Auth not initialized. Call initialize_auth() first.")
    return _auth_instance 