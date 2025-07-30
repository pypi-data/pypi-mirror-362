#!/usr/bin/env python3
"""
TuskLang Python CLI - License Commands
======================================
License management operations
"""

import os
import json
import hashlib
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from pathlib import Path

from ..utils import output_formatter, error_handler, config_loader


class LicenseManager:
    """License management system"""
    
    def __init__(self):
        self.license_file = Path.home() / '.tsk' / 'license.json'
        self.license_file.parent.mkdir(exist_ok=True)
        self.load_license()
    
    def load_license(self):
        """Load license information"""
        if self.license_file.exists():
            try:
                with open(self.license_file, 'r') as f:
                    self.license_data = json.load(f)
            except Exception:
                self.license_data = {}
        else:
            self.license_data = {}
    
    def save_license(self):
        """Save license information"""
        with open(self.license_file, 'w') as f:
            json.dump(self.license_data, f, indent=2)
    
    def validate_license(self, key: str) -> Dict[str, Any]:
        """Validate license key with server"""
        try:
            # In a real implementation, this would validate with a license server
            # For now, we'll simulate validation
            
            # Simulate network request
            response = {
                'valid': True,
                'type': 'pro' if key.startswith('PRO-') else 'community',
                'expires': (datetime.now() + timedelta(days=365)).isoformat(),
                'features': ['ai', 'binary', 'css', 'license'] if key.startswith('PRO-') else ['basic'],
                'user': 'demo@example.com',
                'company': 'Demo Company'
            }
            
            return response
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def activate_license(self, key: str) -> bool:
        """Activate license key"""
        # Validate the license
        validation = self.validate_license(key)
        
        if not validation.get('valid', False):
            return False
        
        # Store license information
        self.license_data = {
            'key': key,
            'type': validation.get('type', 'unknown'),
            'expires': validation.get('expires'),
            'features': validation.get('features', []),
            'user': validation.get('user'),
            'company': validation.get('company'),
            'activated': datetime.now().isoformat(),
            'hash': hashlib.sha256(key.encode()).hexdigest()
        }
        
        self.save_license()
        return True
    
    def check_license(self) -> Dict[str, Any]:
        """Check current license status"""
        if not self.license_data:
            return {
                'status': 'inactive',
                'message': 'No license found'
            }
        
        # Check if license is expired
        if 'expires' in self.license_data:
            expires = datetime.fromisoformat(self.license_data['expires'])
            if datetime.now() > expires:
                return {
                    'status': 'expired',
                    'message': f'License expired on {expires.strftime("%Y-%m-%d")}',
                    'license': self.license_data
                }
        
        return {
            'status': 'active',
            'message': 'License is valid',
            'license': self.license_data
        }
    
    def has_feature(self, feature: str) -> bool:
        """Check if license has specific feature"""
        status = self.check_license()
        if status['status'] != 'active':
            return False
        
        features = self.license_data.get('features', [])
        return feature in features or 'pro' in self.license_data.get('type', '')


def handle_license_command(args, cli):
    """Handle license commands"""
    if args.license_command == 'check':
        return handle_check_command(args, cli)
    elif args.license_command == 'activate':
        return handle_activate_command(args, cli)
    else:
        output_formatter.print_error("Unknown license command")
        return 1


def handle_check_command(args, cli):
    """Handle license check command"""
    try:
        license_mgr = LicenseManager()
        status = license_mgr.check_license()
        
        if cli.json_output:
            output_formatter.print_json(status)
        else:
            if status['status'] == 'active':
                license_data = status['license']
                print(f"✅ License Status: {status['status'].upper()}")
                print(f"   Type: {license_data.get('type', 'unknown').upper()}")
                print(f"   User: {license_data.get('user', 'unknown')}")
                print(f"   Company: {license_data.get('company', 'unknown')}")
                print(f"   Expires: {license_data.get('expires', 'unknown')}")
                print(f"   Features: {', '.join(license_data.get('features', []))}")
                print(f"   Activated: {license_data.get('activated', 'unknown')}")
            elif status['status'] == 'expired':
                print(f"❌ License Status: {status['status'].upper()}")
                print(f"   {status['message']}")
                license_data = status['license']
                print(f"   Type: {license_data.get('type', 'unknown').upper()}")
                print(f"   User: {license_data.get('user', 'unknown')}")
            else:
                print(f"⚠️  License Status: {status['status'].upper()}")
                print(f"   {status['message']}")
                print(f"   Run 'tsk license activate <key>' to activate a license")
        
        return 0 if status['status'] == 'active' else 1
        
    except Exception as e:
        output_formatter.print_error(f"License check error: {str(e)}")
        return 1


def handle_activate_command(args, cli):
    """Handle license activate command"""
    try:
        license_mgr = LicenseManager()
        
        # Validate key format
        key = args.key.strip()
        if not key:
            output_formatter.print_error("License key cannot be empty")
            return 1
        
        # Check if key looks valid
        if not (key.startswith('PRO-') or key.startswith('COMM-') or len(key) >= 16):
            output_formatter.print_error("Invalid license key format")
            return 1
        
        # Activate the license
        if license_mgr.activate_license(key):
            if cli.json_output:
                output_formatter.print_json({
                    'success': True,
                    'message': 'License activated successfully',
                    'license': license_mgr.license_data
                })
            else:
                print(f"✅ License activated successfully!")
                license_data = license_mgr.license_data
                print(f"   Type: {license_data.get('type', 'unknown').upper()}")
                print(f"   User: {license_data.get('user', 'unknown')}")
                print(f"   Company: {license_data.get('company', 'unknown')}")
                print(f"   Expires: {license_data.get('expires', 'unknown')}")
                print(f"   Features: {', '.join(license_data.get('features', []))}")
            
            return 0
        else:
            output_formatter.print_error("Failed to activate license. Please check your key.")
            return 1
        
    except Exception as e:
        output_formatter.print_error(f"License activation error: {str(e)}")
        return 1


def check_feature_access(feature: str) -> bool:
    """Check if current license has access to a feature"""
    license_mgr = LicenseManager()
    return license_mgr.has_feature(feature)


def require_license(feature: str):
    """Decorator to require license for specific features"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not check_feature_access(feature):
                output_formatter.print_error(f"Feature '{feature}' requires a valid license")
                output_formatter.print_error("Run 'tsk license check' to see your license status")
                return 1
            return func(*args, **kwargs)
        return wrapper
    return decorator 