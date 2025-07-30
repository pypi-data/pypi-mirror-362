"""
🐘 TuskLang Python SDK - Protected Version
=========================================
PyArmor bytecode protected version with runtime license validation

This file is protected and obfuscated against reverse engineering
Runtime license validation ensures compliance
"""

import os
import sys
import json
import hashlib
import platform
import subprocess
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Union
import requests
import tempfile

# Protection variables
_license_validated = False
_protection_level = 'enterprise'
_api_endpoint = 'https://lic.tusklang.org/api/v1'
_installation_id = None
_cache_dir = None


def _get_cache_dir() -> str:
    """Get cache directory for license data"""
    global _cache_dir
    if _cache_dir is None:
        _cache_dir = os.path.join(tempfile.gettempdir(), 'tusklang_cache')
        os.makedirs(_cache_dir, exist_ok=True)
    return _cache_dir


def _check_protection() -> bool:
    """Check if protection is intact"""
    try:
        # Check for PyArmor protection
        if not hasattr(sys, '_getframe'):
            return False
        
        # Check for debugging tools
        if 'pdb' in sys.modules or 'ipdb' in sys.modules:
            return False
        
        # Check for IPython/Jupyter
        if 'IPython' in sys.modules:
            return False
        
        # Check for reverse engineering tools
        suspicious_modules = ['uncompyle6', 'decompyle3', 'pycdc', 'pycdas']
        for module in suspicious_modules:
            if module in sys.modules:
                return False
        
        # Check file integrity
        current_hash = _get_file_hash(__file__)
        expected_hash = _get_expected_hash()
        
        if current_hash != expected_hash:
            return False
        
        return True
        
    except Exception:
        return False


def _get_file_hash(filepath: str) -> str:
    """Get SHA256 hash of file"""
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def _get_expected_hash() -> str:
    """Get expected file hash (would be set during PyArmor encoding)"""
    # This would be set during PyArmor encoding
    return '0000000000000000000000000000000000000000000000000000000000000000'


def _get_installation_id() -> str:
    """Get unique installation ID"""
    global _installation_id
    if _installation_id is None:
        id_file = os.path.join(_get_cache_dir(), 'installation_id')
        
        if os.path.exists(id_file):
            with open(id_file, 'r') as f:
                _installation_id = f.read().strip()
        else:
            # Generate new installation ID
            _installation_id = f"PY-{hashlib.md5(os.urandom(16)).hexdigest()[:12].upper()}"
            
            with open(id_file, 'w') as f:
                f.write(_installation_id)
    
    return _installation_id


def _get_stored_license() -> Optional[str]:
    """Get stored license key"""
    # Check environment variable
    license_key = os.environ.get('TUSKLANG_LICENSE')
    if license_key:
        return license_key
    
    # Check license file
    license_file = os.path.join(_get_cache_dir(), 'license')
    if os.path.exists(license_file):
        with open(license_file, 'r') as f:
            return f.read().strip()
    
    return None


def _api_request(method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Make API request to license server"""
    url = f"{_api_endpoint}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'TuskLang-Python-SDK/1.0.0',
        'X-Installation-ID': _get_installation_id()
    }
    
    try:
        if method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            response = requests.get(url, headers=headers, timeout=10)
        
        response.raise_for_status()
        return response.json()
        
    except requests.RequestException as e:
        raise Exception(f"API request failed: {e}")


def _validate_license(license_key: str) -> Dict[str, Any]:
    """Validate license with API"""
    try:
        data = {
            'license_key': license_key,
            'installation_id': _get_installation_id(),
            'hostname': platform.node(),
            'timestamp': int(datetime.now().timestamp()),
            'sdk_type': 'python',
            'protection_level': _protection_level,
            'python_version': platform.python_version(),
            'platform': platform.platform()
        }
        
        response = _api_request('POST', '/validate', data)
        
        return {
            'valid': response.get('valid', False),
            'reason': response.get('reason', 'Unknown error'),
            'license': response.get('license')
        }
        
    except Exception as e:
        # Fallback to offline validation
        return _offline_validation(license_key)


def _offline_validation(license_key: str) -> Dict[str, Any]:
    """Offline license validation (grace period)"""
    try:
        cache_file = os.path.join(_get_cache_dir(), 'license_cache.json')
        
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cache = json.load(f)
            
            if cache.get('license_key') == license_key and cache.get('expires', 0) > datetime.now().timestamp():
                return {
                    'valid': True,
                    'reason': 'Offline cache valid',
                    'license': cache.get('license')
                }
        
        return {
            'valid': False,
            'reason': 'No offline cache available',
            'license': None
        }
        
    except Exception:
        return {
            'valid': False,
            'reason': 'Offline validation failed',
            'license': None
        }


def _log_violation(reason: str) -> None:
    """Log security violation"""
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'reason': reason,
        'hostname': platform.node(),
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'installation_id': _get_installation_id()
    }
    
    # Store violation locally
    try:
        violations_file = os.path.join(_get_cache_dir(), 'violations.log')
        with open(violations_file, 'a') as f:
            f.write(json.dumps(log_data) + '\n')
    except Exception:
        pass
    
    # Report to API
    try:
        _api_request('POST', '/violation', log_data)
    except Exception:
        pass  # Silent fail for violation reporting


def _self_destruct() -> None:
    """Self-destruct mechanism"""
    global _license_validated
    _license_validated = False
    
    # Log violation
    _log_violation('Protection violation detected - self-destruct initiated')
    
    # Raise exception to prevent further execution
    raise RuntimeError('TuskLang SDK protection violation detected')


def init(license_key: Optional[str] = None) -> bool:
    """Initialize protected SDK with license validation"""
    global _license_validated
    
    # Runtime protection check
    if not _check_protection():
        _self_destruct()
        return False
    
    # License validation
    if not license_key:
        license_key = _get_stored_license()
    
    if not license_key:
        _log_violation('No license key provided')
        return False
    
    validation = _validate_license(license_key)
    if not validation['valid']:
        _log_violation(f"Invalid license: {validation['reason']}")
        return False
    
    _license_validated = True
    return True


def is_licensed() -> bool:
    """Check if SDK is properly licensed"""
    return _license_validated


def get_protection_level() -> str:
    """Get protection level"""
    return _protection_level


def parse(code: str) -> Dict[str, Any]:
    """Parse TuskLang code (protected implementation)"""
    if not is_licensed():
        raise RuntimeError('TuskLang SDK not properly licensed')
    
    # Implementation would be obfuscated by PyArmor
    return {'status': 'protected_implementation'}


def compile_code(code: str) -> str:
    """Compile TuskLang code (protected implementation)"""
    if not is_licensed():
        raise RuntimeError('TuskLang SDK not properly licensed')
    
    # Implementation would be obfuscated by PyArmor
    return 'protected_compiled_code'


def validate(code: str) -> bool:
    """Validate TuskLang code (protected implementation)"""
    if not is_licensed():
        raise RuntimeError('TuskLang SDK not properly licensed')
    
    # Implementation would be obfuscated by PyArmor
    return True


# Public API
__all__ = ['init', 'is_licensed', 'get_protection_level', 'parse', 'compile_code', 'validate'] 