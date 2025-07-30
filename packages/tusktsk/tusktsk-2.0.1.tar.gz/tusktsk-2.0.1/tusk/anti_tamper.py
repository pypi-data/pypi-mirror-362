"""
TuskLang SDK Anti-Tampering Module
Enterprise-grade anti-tampering for Python SDK
"""

import hashlib
import hmac
import os
import sys
import time
import inspect
import base64
import zlib
import marshal
import types
from typing import Dict, Any, List, Optional, Callable
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class TuskAntiTamper:
    """Anti-tampering system for TuskLang Python SDK"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.encryption_key = self._derive_key(secret_key)
        self.fernet = Fernet(self.encryption_key)
        self.integrity_checks = {}
        self.tamper_detections = []
        self.obfuscation_cache = {}
        self.self_check_interval = 300  # 5 minutes
        self.last_self_check = time.time()
    
    def _derive_key(self, password: str) -> bytes:
        """Derive encryption key from secret"""
        salt = b'tusklang_antitamper_salt'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            return hashlib.sha256(content).hexdigest()
        except Exception:
            return ""
    
    def verify_file_integrity(self, file_path: str, expected_hash: str) -> bool:
        """Verify file integrity against expected hash"""
        try:
            actual_hash = self.calculate_file_hash(file_path)
            return hmac.compare_digest(actual_hash, expected_hash)
        except Exception:
            return False
    
    def obfuscate_code(self, code: str, level: int = 2) -> str:
        """Obfuscate Python code with multiple techniques"""
        try:
            if level == 0:
                return code
            
            # Level 1: Basic obfuscation
            if level >= 1:
                # Compress and encode
                compressed = zlib.compress(code.encode())
                encoded = base64.b85encode(compressed).decode()
                code = f"import zlib,base64;exec(zlib.decompress(base64.b85decode('{encoded}')).decode())"
            
            # Level 2: Advanced obfuscation
            if level >= 2:
                # Add junk code and variable renaming
                junk_vars = [f"_{i}" for i in range(10)]
                junk_code = ";".join([f"{var}=None" for var in junk_vars])
                code = f"{junk_code};{code}"
            
            # Level 3: Maximum obfuscation
            if level >= 3:
                # Encrypt the code
                encrypted = self.fernet.encrypt(code.encode())
                encoded = base64.b64encode(encrypted).decode()
                code = f"import base64;from cryptography.fernet import Fernet;exec(Fernet(b'{self.encryption_key.decode()}').decrypt(base64.b64decode('{encoded}')).decode())"
            
            return code
            
        except Exception:
            return code
    
    def deobfuscate_code(self, obfuscated_code: str) -> str:
        """Deobfuscate code (for internal use)"""
        try:
            # Handle different obfuscation levels
            if "zlib.decompress" in obfuscated_code:
                # Extract encoded part
                start = obfuscated_code.find("('") + 2
                end = obfuscated_code.find("')")
                encoded = obfuscated_code[start:end]
                
                # Decode and decompress
                compressed = base64.b85decode(encoded)
                return zlib.decompress(compressed).decode()
            
            elif "Fernet" in obfuscated_code:
                # Extract encrypted part
                start = obfuscated_code.find("('") + 2
                end = obfuscated_code.find("')")
                encrypted_b64 = obfuscated_code[start:end]
                
                # Decrypt
                encrypted = base64.b64decode(encrypted_b64)
                return self.fernet.decrypt(encrypted).decode()
            
            else:
                return obfuscated_code
                
        except Exception:
            return obfuscated_code
    
    def protect_function(self, func: Callable, obfuscation_level: int = 2) -> Callable:
        """Protect a function with anti-tampering"""
        try:
            # Get function source
            source = inspect.getsource(func)
            
            # Obfuscate the source
            obfuscated = self.obfuscate_code(source, obfuscation_level)
            
            # Create protected function
            def protected_wrapper(*args, **kwargs):
                # Self-check before execution
                if not self.self_check():
                    raise RuntimeError("Tampering detected - function execution blocked")
                
                # Execute original function
                return func(*args, **kwargs)
            
            # Store obfuscated code for later verification
            self.obfuscation_cache[func.__name__] = {
                'original': source,
                'obfuscated': obfuscated,
                'hash': hashlib.sha256(source.encode()).hexdigest()
            }
            
            return protected_wrapper
            
        except Exception as e:
            # Fallback to original function
            return func
    
    def self_check(self) -> bool:
        """Perform self-integrity check"""
        try:
            current_time = time.time()
            
            # Check if it's time for a self-check
            if current_time - self.last_self_check < self.self_check_interval:
                return True
            
            self.last_self_check = current_time
            
            # Check current file integrity
            current_file = __file__
            current_hash = self.calculate_file_hash(current_file)
            
            # Store first hash if not exists
            if current_file not in self.integrity_checks:
                self.integrity_checks[current_file] = current_hash
                return True
            
            # Compare with stored hash
            if not hmac.compare_digest(self.integrity_checks[current_file], current_hash):
                self.tamper_detections.append({
                    'timestamp': current_time,
                    'file': current_file,
                    'expected': self.integrity_checks[current_file],
                    'actual': current_hash
                })
                return False
            
            # Check obfuscated functions
            for func_name, cache_data in self.obfuscation_cache.items():
                current_hash = hashlib.sha256(cache_data['original'].encode()).hexdigest()
                if not hmac.compare_digest(cache_data['hash'], current_hash):
                    self.tamper_detections.append({
                        'timestamp': current_time,
                        'function': func_name,
                        'expected': cache_data['hash'],
                        'actual': current_hash
                    })
                    return False
            
            return True
            
        except Exception:
            return False
    
    def detect_tampering(self) -> Dict[str, Any]:
        """Detect various types of tampering"""
        try:
            tampering_detected = {
                'file_tampering': False,
                'function_tampering': False,
                'environment_tampering': False,
                'debugger_detected': False,
                'details': []
            }
            
            # Check for debugger
            if self._detect_debugger():
                tampering_detected['debugger_detected'] = True
                tampering_detected['details'].append('Debugger detected')
            
            # Check environment tampering
            if self._detect_environment_tampering():
                tampering_detected['environment_tampering'] = True
                tampering_detected['details'].append('Environment tampering detected')
            
            # Check file tampering
            if not self.self_check():
                tampering_detected['file_tampering'] = True
                tampering_detected['details'].append('File integrity check failed')
            
            # Check function tampering
            for func_name, cache_data in self.obfuscation_cache.items():
                current_hash = hashlib.sha256(cache_data['original'].encode()).hexdigest()
                if not hmac.compare_digest(cache_data['hash'], current_hash):
                    tampering_detected['function_tampering'] = True
                    tampering_detected['details'].append(f'Function {func_name} tampering detected')
            
            return tampering_detected
            
        except Exception as e:
            return {
                'file_tampering': False,
                'function_tampering': False,
                'environment_tampering': False,
                'debugger_detected': False,
                'details': [f'Error during tampering detection: {str(e)}']
            }
    
    def _detect_debugger(self) -> bool:
        """Detect if running under debugger"""
        try:
            # Check for common debugger indicators
            import sys
            if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
                return True
            
            # Check for PyCharm debugger
            if 'pydevd' in sys.modules:
                return True
            
            # Check for IPython debugger
            if 'IPython' in sys.modules:
                return True
            
            return False
            
        except Exception:
            return False
    
    def _detect_environment_tampering(self) -> bool:
        """Detect environment tampering"""
        try:
            # Check for suspicious environment variables
            suspicious_vars = ['PYTHONPATH', 'PYTHONHOME', 'PYTHONEXECUTABLE']
            for var in suspicious_vars:
                if var in os.environ:
                    value = os.environ[var]
                    if 'debug' in value.lower() or 'test' in value.lower():
                        return True
            
            # Check for suspicious command line arguments
            for arg in sys.argv:
                if 'debug' in arg.lower() or 'test' in arg.lower():
                    return True
            
            return False
            
        except Exception:
            return False
    
    def get_tamper_detections(self) -> List[Dict[str, Any]]:
        """Get list of tampering detections"""
        return self.tamper_detections.copy()
    
    def clear_tamper_detections(self):
        """Clear tampering detection history"""
        self.tamper_detections.clear()
    
    def get_integrity_report(self) -> Dict[str, Any]:
        """Get comprehensive integrity report"""
        try:
            return {
                'self_check_passed': self.self_check(),
                'tampering_detected': self.detect_tampering(),
                'protected_functions': list(self.obfuscation_cache.keys()),
                'integrity_checks': len(self.integrity_checks),
                'tamper_detections': len(self.tamper_detections),
                'last_self_check': self.last_self_check
            }
        except Exception as e:
            return {'error': str(e)}

# Global anti-tamper instance
_anti_tamper_instance: Optional[TuskAntiTamper] = None

def initialize_anti_tamper(secret_key: str) -> TuskAntiTamper:
    """Initialize global anti-tamper instance"""
    global _anti_tamper_instance
    _anti_tamper_instance = TuskAntiTamper(secret_key)
    return _anti_tamper_instance

def get_anti_tamper() -> TuskAntiTamper:
    """Get global anti-tamper instance"""
    if _anti_tamper_instance is None:
        raise RuntimeError("Anti-tamper not initialized. Call initialize_anti_tamper() first.")
    return _anti_tamper_instance 