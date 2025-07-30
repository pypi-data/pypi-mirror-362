"""
TuskLang SDK Protection Test Suite
Comprehensive testing for Python SDK protection features
"""

import unittest
import sys
import os
import time
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tusk.protection import TuskProtection, initialize_protection, get_protection
from tusk.license import TuskLicense, initialize_license, get_license
from tusk.anti_tamper import TuskAntiTamper, initialize_anti_tamper, get_anti_tamper
from tusk.usage_tracker import TuskUsageTracker, initialize_usage_tracker, get_usage_tracker
from tusk.auth import TuskAuth, initialize_auth, get_auth

class TestTuskProtection(unittest.TestCase):
    """Test cases for TuskProtection class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.license_key = "TUSK-TEST-KEY-12345678901234567890123456789012"
        self.api_key = "test_api_key_123456789012345678901234567890"
        self.secret_key = "test_secret_key_123456789012345678901234567890"
        
        # Initialize protection systems
        self.protection = TuskProtection(self.license_key, self.api_key)
        self.license = TuskLicense(self.license_key, self.api_key)
        self.anti_tamper = TuskAntiTamper(self.secret_key)
        self.usage_tracker = TuskUsageTracker(self.api_key)
        self.auth = TuskAuth(self.secret_key)
    
    def tearDown(self):
        """Clean up after tests"""
        # Clean up any temporary files
        pass
    
    def test_protection_initialization(self):
        """Test protection system initialization"""
        self.assertIsNotNone(self.protection)
        self.assertEqual(self.protection.license_key, self.license_key)
        self.assertEqual(self.protection.api_key, self.api_key)
        self.assertIsNotNone(self.protection.session_id)
    
    def test_license_validation(self):
        """Test license validation"""
        # Test valid license
        result = self.protection.validate_license()
        self.assertTrue(result)
        
        # Test invalid license
        invalid_protection = TuskProtection("invalid_key", self.api_key)
        result = invalid_protection.validate_license()
        self.assertFalse(result)
    
    def test_data_encryption_decryption(self):
        """Test data encryption and decryption"""
        test_data = "sensitive test data"
        
        # Encrypt data
        encrypted = self.protection.encrypt_data(test_data)
        self.assertNotEqual(encrypted, test_data)
        self.assertIsInstance(encrypted, str)
        
        # Decrypt data
        decrypted = self.protection.decrypt_data(encrypted)
        self.assertEqual(decrypted, test_data)
    
    def test_integrity_verification(self):
        """Test data integrity verification"""
        test_data = "test data for integrity check"
        
        # Generate signature
        signature = self.protection.generate_signature(test_data)
        self.assertIsInstance(signature, str)
        self.assertGreater(len(signature), 0)
        
        # Verify integrity
        result = self.protection.verify_integrity(test_data, signature)
        self.assertTrue(result)
        
        # Test with invalid signature
        invalid_signature = "invalid_signature"
        result = self.protection.verify_integrity(test_data, invalid_signature)
        self.assertFalse(result)
    
    def test_usage_tracking(self):
        """Test usage tracking functionality"""
        # Track usage
        self.protection.track_usage("test_operation", True)
        
        # Get metrics
        metrics = self.protection.get_metrics()
        self.assertIsInstance(metrics, dict)
        self.assertIn("api_calls", metrics)
        self.assertIn("errors", metrics)
        self.assertIn("session_id", metrics)
        self.assertEqual(metrics["api_calls"], 1)
        self.assertEqual(metrics["errors"], 0)
    
    def test_code_obfuscation(self):
        """Test code obfuscation"""
        test_code = "print('Hello, World!')"
        
        # Obfuscate code
        obfuscated = self.protection.obfuscate_code(test_code)
        self.assertNotEqual(obfuscated, test_code)
        self.assertIsInstance(obfuscated, str)
    
    def test_tamper_detection(self):
        """Test tamper detection"""
        # Test tamper detection
        result = self.protection.detect_tampering()
        self.assertIsInstance(result, bool)
    
    def test_violation_reporting(self):
        """Test violation reporting"""
        violation = self.protection.report_violation("test_violation", "Test violation details")
        self.assertIsInstance(violation, dict)
        self.assertIn("timestamp", violation)
        self.assertIn("session_id", violation)
        self.assertIn("type", violation)
        self.assertIn("details", violation)

class TestTuskLicense(unittest.TestCase):
    """Test cases for TuskLicense class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.license_key = "TUSK-TEST-KEY-12345678901234567890123456789012"
        self.api_key = "test_api_key_123456789012345678901234567890"
        self.license = TuskLicense(self.license_key, self.api_key)
    
    def test_license_key_validation(self):
        """Test license key validation"""
        result = self.license.validate_license_key()
        self.assertIsInstance(result, dict)
        self.assertIn("valid", result)
    
    def test_license_expiration_check(self):
        """Test license expiration checking"""
        result = self.license.check_license_expiration()
        self.assertIsInstance(result, dict)
        self.assertIn("expired", result)
    
    def test_license_permissions(self):
        """Test license permission validation"""
        result = self.license.validate_license_permissions("basic")
        self.assertIsInstance(result, dict)
        self.assertIn("allowed", result)
    
    def test_license_info(self):
        """Test license information retrieval"""
        info = self.license.get_license_info()
        self.assertIsInstance(info, dict)
        self.assertIn("license_key", info)
        self.assertIn("session_id", info)
        self.assertIn("validation", info)
        self.assertIn("expiration", info)

class TestTuskAntiTamper(unittest.TestCase):
    """Test cases for TuskAntiTamper class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.secret_key = "test_secret_key_123456789012345678901234567890"
        self.anti_tamper = TuskAntiTamper(self.secret_key)
    
    def test_file_integrity(self):
        """Test file integrity checking"""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            temp_file = f.name
        
        try:
            # Calculate file hash
            file_hash = self.anti_tamper.calculate_file_hash(temp_file)
            self.assertIsInstance(file_hash, str)
            self.assertGreater(len(file_hash), 0)
            
            # Verify file integrity
            result = self.anti_tamper.verify_file_integrity(temp_file, file_hash)
            self.assertTrue(result)
            
            # Test with invalid hash
            invalid_hash = "invalid_hash"
            result = self.anti_tamper.verify_file_integrity(temp_file, invalid_hash)
            self.assertFalse(result)
        finally:
            # Clean up
            os.unlink(temp_file)
    
    def test_code_obfuscation(self):
        """Test code obfuscation"""
        test_code = "def test_function(): return 'test'"
        
        # Test different obfuscation levels
        for level in range(4):
            obfuscated = self.anti_tamper.obfuscate_code(test_code, level)
            self.assertIsInstance(obfuscated, str)
            if level > 0:
                self.assertNotEqual(obfuscated, test_code)
    
    def test_self_check(self):
        """Test self-integrity check"""
        result = self.anti_tamper.self_check()
        self.assertIsInstance(result, bool)
    
    def test_tampering_detection(self):
        """Test tampering detection"""
        result = self.anti_tamper.detect_tampering()
        self.assertIsInstance(result, dict)
        self.assertIn("file_tampering", result)
        self.assertIn("function_tampering", result)
        self.assertIn("environment_tampering", result)
        self.assertIn("debugger_detected", result)

class TestTuskUsageTracker(unittest.TestCase):
    """Test cases for TuskUsageTracker class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key_123456789012345678901234567890"
        self.usage_tracker = TuskUsageTracker(self.api_key)
    
    def test_event_tracking(self):
        """Test event tracking"""
        # Track event
        self.usage_tracker.track_event("test_event", {"test": "data"})
        
        # Get usage summary
        summary = self.usage_tracker.get_usage_summary()
        self.assertIsInstance(summary, dict)
        self.assertIn("total_events", summary)
        self.assertIn("session_id", summary)
        self.assertEqual(summary["total_events"], 1)
    
    def test_api_call_tracking(self):
        """Test API call tracking"""
        self.usage_tracker.track_api_call("/test/endpoint", "GET", 200, 0.1)
        
        summary = self.usage_tracker.get_usage_summary()
        self.assertEqual(summary["api_calls"], 1)
        self.assertEqual(summary["errors"], 0)
    
    def test_error_tracking(self):
        """Test error tracking"""
        self.usage_tracker.track_error("test_error", "Test error message")
        
        summary = self.usage_tracker.get_usage_summary()
        self.assertEqual(summary["errors"], 1)
    
    def test_feature_usage_tracking(self):
        """Test feature usage tracking"""
        self.usage_tracker.track_feature_usage("test_feature", True, {"metadata": "test"})
        
        events = self.usage_tracker.get_events_by_type("feature_usage")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].event_data["feature"], "test_feature")
    
    def test_performance_tracking(self):
        """Test performance tracking"""
        self.usage_tracker.track_performance("test_operation", 0.5, 1024)
        
        events = self.usage_tracker.get_events_by_type("performance")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].event_data["operation"], "test_operation")

class TestTuskAuth(unittest.TestCase):
    """Test cases for TuskAuth class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.master_key = "test_master_key_123456789012345678901234567890"
        self.auth = TuskAuth(self.master_key)
    
    def test_api_key_generation(self):
        """Test API key generation"""
        api_key = self.auth.generate_api_key("test_user", ["read", "write"])
        self.assertIsInstance(api_key, str)
        self.assertIn(".", api_key)  # Should contain key_id.secret format
    
    def test_api_key_validation(self):
        """Test API key validation"""
        # Generate API key
        api_key = self.auth.generate_api_key("test_user", ["read", "write"])
        
        # Validate API key
        result = self.auth.validate_api_key(api_key)
        self.assertIsInstance(result, dict)
        self.assertIn("user_id", result)
        self.assertIn("permissions", result)
        self.assertEqual(result["user_id"], "test_user")
    
    def test_auth_token_generation(self):
        """Test authentication token generation"""
        token = self.auth.generate_auth_token("test_user", ["read", "write"])
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 0)
    
    def test_auth_token_validation(self):
        """Test authentication token validation"""
        # Generate token
        token = self.auth.generate_auth_token("test_user", ["read", "write"])
        
        # Validate token
        result = self.auth.validate_auth_token(token)
        self.assertIsInstance(result, dict)
        self.assertIn("user_id", result)
        self.assertIn("permissions", result)
        self.assertEqual(result["user_id"], "test_user")
    
    def test_permission_checking(self):
        """Test permission checking"""
        auth_data = {"permissions": ["read", "write"]}
        
        # Test allowed permission
        result = self.auth.check_permission("test_user", "read", auth_data)
        self.assertTrue(result)
        
        # Test denied permission
        result = self.auth.check_permission("test_user", "admin", auth_data)
        self.assertFalse(result)
    
    def test_sensitive_data_encryption(self):
        """Test sensitive data encryption"""
        sensitive_data = "sensitive information"
        
        # Encrypt data
        encrypted = self.auth.encrypt_sensitive_data(sensitive_data)
        self.assertNotEqual(encrypted, sensitive_data)
        
        # Decrypt data
        decrypted = self.auth.decrypt_sensitive_data(encrypted)
        self.assertEqual(decrypted, sensitive_data)

class TestGlobalInstances(unittest.TestCase):
    """Test cases for global instance management"""
    
    def test_global_protection_instance(self):
        """Test global protection instance management"""
        # Initialize global instance
        protection = initialize_protection("test_key", "test_api")
        self.assertIsNotNone(protection)
        
        # Get global instance
        retrieved = get_protection()
        self.assertEqual(protection, retrieved)
    
    def test_global_license_instance(self):
        """Test global license instance management"""
        # Initialize global instance
        license = initialize_license("test_key", "test_api")
        self.assertIsNotNone(license)
        
        # Get global instance
        retrieved = get_license()
        self.assertEqual(license, retrieved)
    
    def test_global_anti_tamper_instance(self):
        """Test global anti-tamper instance management"""
        # Initialize global instance
        anti_tamper = initialize_anti_tamper("test_secret")
        self.assertIsNotNone(anti_tamper)
        
        # Get global instance
        retrieved = get_anti_tamper()
        self.assertEqual(anti_tamper, retrieved)
    
    def test_global_usage_tracker_instance(self):
        """Test global usage tracker instance management"""
        # Initialize global instance
        usage_tracker = initialize_usage_tracker("test_api")
        self.assertIsNotNone(usage_tracker)
        
        # Get global instance
        retrieved = get_usage_tracker()
        self.assertEqual(usage_tracker, retrieved)
    
    def test_global_auth_instance(self):
        """Test global auth instance management"""
        # Initialize global instance
        auth = initialize_auth("test_master")
        self.assertIsNotNone(auth)
        
        # Get global instance
        retrieved = get_auth()
        self.assertEqual(auth, retrieved)

def run_performance_tests():
    """Run performance tests"""
    print("Running performance tests...")
    
    # Test encryption/decryption performance
    protection = TuskProtection("test_key", "test_api")
    test_data = "x" * 1000  # 1KB of data
    
    start_time = time.time()
    for _ in range(100):
        encrypted = protection.encrypt_data(test_data)
        decrypted = protection.decrypt_data(encrypted)
    end_time = time.time()
    
    print(f"Encryption/Decryption: 100 operations in {end_time - start_time:.3f} seconds")
    
    # Test signature generation performance
    start_time = time.time()
    for _ in range(1000):
        protection.generate_signature(test_data)
    end_time = time.time()
    
    print(f"Signature Generation: 1000 operations in {end_time - start_time:.3f} seconds")

def run_security_tests():
    """Run security tests"""
    print("Running security tests...")
    
    # Test key derivation
    protection = TuskProtection("test_key", "test_api")
    key1 = protection._derive_key("password1")
    key2 = protection._derive_key("password2")
    
    assert key1 != key2, "Different passwords should produce different keys"
    print("✓ Key derivation security test passed")
    
    # Test signature uniqueness
    data1 = "data1"
    data2 = "data2"
    sig1 = protection.generate_signature(data1)
    sig2 = protection.generate_signature(data2)
    
    assert sig1 != sig2, "Different data should produce different signatures"
    print("✓ Signature uniqueness test passed")

if __name__ == '__main__':
    # Run unit tests
    unittest.main(verbosity=2, exit=False)
    
    # Run performance tests
    run_performance_tests()
    
    # Run security tests
    run_security_tests()
    
    print("\nAll tests completed!") 