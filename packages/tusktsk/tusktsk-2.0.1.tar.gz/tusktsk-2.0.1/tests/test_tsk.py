#!/usr/bin/env python3
"""
Comprehensive test suite for TSK Python SDK
Tests all features including parsing, fujsen, shell storage, and more
"""

import sys
import os
import unittest
import tempfile
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tsk import TSK, TSKParser, ShellStorage, parse_with_comments

# Test data
SAMPLE_TSK = """# Flexchain Configuration
# Created: 2024-01-01

[storage]
id = "flex_123"
type = "image/jpeg"
size = 245760
created = 1719978000
chunks = 4

[metadata]
filename = "sunset.jpg"
album = "vacation_2024"
tags = [ "sunset", "beach", "california" ]
owner = "user_123"
location = "Santa Monica"
settings = { "quality" = 95, "format" = "progressive" }

[verification]
hash = "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
checksum = "md5:5d41402abc4b2a76b9719d911017c592"

[multiline]
description = \"\"\"
This is a beautiful sunset photo
taken at Santa Monica beach
during summer vacation 2024
\"\"\"

[types]
string = "hello"
number = 42
float = 3.14159
boolean = true
false_bool = false
null_value = null
empty_array = [ ]
empty_object = { }
"""

FUJSEN_TSK = """
[contract]
name = "PaymentProcessor"
version = "1.0.0"

# Main payment processing function
process_fujsen = \"\"\"
def process(amount, recipient):
    if amount <= 0:
        raise ValueError("Invalid amount")
    if not recipient:
        raise ValueError("No recipient specified")
    
    import time
    return {
        'success': True,
        'transactionId': f'tx_{int(time.time() * 1000)}',
        'amount': amount,
        'recipient': recipient,
        'fee': amount * 0.01
    }
\"\"\"

# Validation functions
validate_amount_fujsen = \"\"\"
lambda amount: (
    isinstance(amount, (int, float)) and 
    amount > 0 and 
    amount <= 1000000
)
\"\"\"

# Simple calculation
calculate_fee_fujsen = \"\"\"
lambda amount: amount * 0.025
\"\"\"

# Complex nested function
swap_fujsen = \"\"\"
def swap(amount_in, token_in):
    reserves = {'FLEX': 100000, 'USDT': 50000}
    k = reserves['FLEX'] * reserves['USDT']
    
    if token_in == 'FLEX':
        new_reserve_a = reserves['FLEX'] + amount_in
        new_reserve_b = k / new_reserve_a
        amount_out = reserves['USDT'] - new_reserve_b
    else:
        new_reserve_b = reserves['USDT'] + amount_in
        new_reserve_a = k / new_reserve_b
        amount_out = reserves['FLEX'] - new_reserve_a
    
    fee = amount_out * 0.003
    return {
        'amount_out': amount_out - fee,
        'fee': fee,
        'price_impact': ((amount_out / amount_in) - 1) * 100
    }
\"\"\"
"""


class TestTSKParser(unittest.TestCase):
    """Test TSK parsing functionality"""
    
    def test_basic_parsing(self):
        """Test basic TSK parsing"""
        tsk = TSK.from_string(SAMPLE_TSK)
        
        # Test section access
        self.assertEqual(tsk.get_value('storage', 'id'), 'flex_123')
        self.assertEqual(tsk.get_value('storage', 'size'), 245760)
        self.assertEqual(tsk.get_value('types', 'boolean'), True)
        self.assertEqual(tsk.get_value('types', 'false_bool'), False)
        self.assertIsNone(tsk.get_value('types', 'null_value'))
        
    def test_array_parsing(self):
        """Test array parsing"""
        tsk = TSK.from_string(SAMPLE_TSK)
        
        tags = tsk.get_value('metadata', 'tags')
        self.assertEqual(tags, ['sunset', 'beach', 'california'])
        
        # Empty array
        self.assertEqual(tsk.get_value('types', 'empty_array'), [])
        
    def test_object_parsing(self):
        """Test object/dict parsing"""
        tsk = TSK.from_string(SAMPLE_TSK)
        
        settings = tsk.get_value('metadata', 'settings')
        self.assertEqual(settings, {'quality': 95, 'format': 'progressive'})
        
        # Empty object
        self.assertEqual(tsk.get_value('types', 'empty_object'), {})
        
    def test_multiline_strings(self):
        """Test multiline string parsing"""
        tsk = TSK.from_string(SAMPLE_TSK)
        
        description = tsk.get_value('multiline', 'description')
        self.assertIn('beautiful sunset', description)
        self.assertIn('\n', description)
        self.assertIn('Santa Monica beach', description)
        
    def test_comment_preservation(self):
        """Test that comments are preserved"""
        data, comments = parse_with_comments(SAMPLE_TSK)
        
        # Check comments were captured
        self.assertGreater(len(comments), 0)
        self.assertEqual(comments[0], '# Flexchain Configuration')
        self.assertEqual(comments[1], '# Created: 2024-01-01')
        
        # Data should still parse correctly
        self.assertEqual(data['storage']['id'], 'flex_123')


class TestFujsen(unittest.TestCase):
    """Test fujsen execution functionality"""
    
    def test_function_execution(self):
        """Test basic fujsen execution"""
        tsk = TSK.from_string(FUJSEN_TSK)
        
        # Test process function
        result = tsk.execute_fujsen('contract', 'process_fujsen', 100, 'alice@example.com')
        self.assertTrue(result['success'])
        self.assertEqual(result['amount'], 100)
        self.assertEqual(result['recipient'], 'alice@example.com')
        self.assertEqual(result['fee'], 1.0)
        self.assertTrue(result['transactionId'].startswith('tx_'))
        
    def test_lambda_execution(self):
        """Test lambda fujsen execution"""
        tsk = TSK.from_string(FUJSEN_TSK)
        
        # Test validation
        self.assertTrue(tsk.execute_fujsen('contract', 'validate_amount_fujsen', 100))
        self.assertFalse(tsk.execute_fujsen('contract', 'validate_amount_fujsen', -50))
        self.assertFalse(tsk.execute_fujsen('contract', 'validate_amount_fujsen', 'abc'))
        self.assertFalse(tsk.execute_fujsen('contract', 'validate_amount_fujsen', 2000000))
        
        # Test calculation
        self.assertEqual(tsk.execute_fujsen('contract', 'calculate_fee_fujsen', 1000), 25.0)
        
    def test_complex_function(self):
        """Test complex fujsen with internal state"""
        tsk = TSK.from_string(FUJSEN_TSK)
        
        # Test swap function
        result = tsk.execute_fujsen('contract', 'swap_fujsen', 1000, 'FLEX')
        self.assertGreater(result['amount_out'], 0)
        self.assertGreater(result['fee'], 0)
        self.assertLess(result['price_impact'], 0)
        
    def test_error_handling(self):
        """Test fujsen error handling"""
        tsk = TSK.from_string(FUJSEN_TSK)
        
        # Test invalid amount
        with self.assertRaises(ValueError) as ctx:
            tsk.execute_fujsen('contract', 'process_fujsen', -100, 'alice')
        self.assertIn('Invalid amount', str(ctx.exception))
        
        # Test missing fujsen
        with self.assertRaises(ValueError) as ctx:
            tsk.execute_fujsen('missing', 'fujsen')
        self.assertIn('No fujsen found', str(ctx.exception))
        
    def test_fujsen_caching(self):
        """Test that fujsen functions are cached"""
        tsk = TSK.from_string(FUJSEN_TSK)
        
        # First execution
        start = time.time()
        for _ in range(100):
            tsk.execute_fujsen('contract', 'calculate_fee_fujsen', 100)
        first_time = time.time() - start
        
        # Should be much faster due to caching
        start = time.time()
        for _ in range(1000):
            tsk.execute_fujsen('contract', 'calculate_fee_fujsen', 100)
        cached_time = time.time() - start
        
        # Cached should be at least 5x faster per iteration
        self.assertLess(cached_time / 1000, first_time / 100 * 5)
        
    def test_context_binding(self):
        """Test fujsen execution with custom context"""
        tsk = TSK()
        
        # Add fujsen that uses context
        tsk.set_value('context_test', 'greet_fujsen', """
def greet(name):
    return greeting + ' ' + name + '!'
""")
        
        # Execute with context
        context = {'greeting': 'Hello'}
        result = tsk.execute_fujsen_with_context('context_test', 'greet_fujsen', context, 'World')
        self.assertEqual(result, 'Hello World!')
        
        # Different context
        context2 = {'greeting': 'Bonjour'}
        result2 = tsk.execute_fujsen_with_context('context_test', 'greet_fujsen', context2, 'Monde')
        self.assertEqual(result2, 'Bonjour Monde!')


class TestShellStorage(unittest.TestCase):
    """Test shell binary storage functionality"""
    
    def test_pack_unpack(self):
        """Test shell pack/unpack operations"""
        # Test data
        test_data = {
            'version': 1,
            'type': 'test',
            'id': 'test_123',
            'compression': 'gzip',
            'data': 'Hello, World! This is test data.'
        }
        
        # Pack
        packed = ShellStorage.pack(test_data)
        self.assertIsInstance(packed, bytes)
        self.assertTrue(packed.startswith(b'FLEX'))
        
        # Unpack
        unpacked = ShellStorage.unpack(packed)
        self.assertEqual(unpacked['id'], 'test_123')
        self.assertEqual(unpacked['data'], 'Hello, World! This is test data.')
        
    def test_binary_data(self):
        """Test shell storage with binary data"""
        binary_data = b'\x00\x01\x02\x03\xFF\xFE\xFD'
        
        test_data = {
            'version': 1,
            'type': 'binary',
            'id': 'binary_test',
            'compression': 'gzip',
            'data': binary_data
        }
        
        packed = ShellStorage.pack(test_data)
        unpacked = ShellStorage.unpack(packed)
        
        # Binary data is converted to string in unpack
        self.assertEqual(unpacked['id'], 'binary_test')
        
    def test_invalid_format(self):
        """Test shell format validation"""
        invalid_data = b'INVALID_HEADER_DATA'
        
        with self.assertRaises(ValueError) as ctx:
            ShellStorage.unpack(invalid_data)
        self.assertIn('Invalid shell format', str(ctx.exception))


class TestTSKStorage(unittest.TestCase):
    """Test TSK storage integration"""
    
    def test_store_with_shell(self):
        """Test storing data with shell format"""
        tsk = TSK()
        test_data = 'This is test data for shell storage!'
        
        # Store data
        storage = tsk.store_with_shell(test_data, {
            'filename': 'test.txt',
            'author': 'Test Suite'
        })
        
        self.assertEqual(storage['type'], 'text/plain')
        self.assertTrue(storage['storage_id'].startswith('flex_'))
        self.assertIsInstance(storage['shell_data'], bytes)
        self.assertIn('[storage]', storage['tsk_data'])
        
    def test_retrieve_from_shell(self):
        """Test retrieving data from shell"""
        tsk = TSK()
        original_data = 'Test data to store and retrieve'
        
        # Store
        storage = tsk.store_with_shell(original_data, {'test': True})
        
        # Create new TSK from stored data
        tsk2 = TSK.from_string(storage['tsk_data'])
        
        # Retrieve
        retrieved = tsk2.retrieve_from_shell(storage['shell_data'])
        self.assertEqual(retrieved['data'], original_data)
        self.assertEqual(retrieved['metadata'], {'test': True})
        
    def test_type_detection(self):
        """Test content type detection"""
        tsk = TSK()
        
        # Text
        self.assertEqual(tsk.detect_type('Hello, World!'), 'text/plain')
        
        # JPEG
        jpeg_header = b'\xFF\xD8\xFF\xE0'
        self.assertEqual(tsk.detect_type(jpeg_header), 'image/jpeg')
        
        # PNG
        png_header = b'\x89PNG\r\n\x1a\n'
        self.assertEqual(tsk.detect_type(png_header), 'image/png')
        
        # PDF
        pdf_header = b'%PDF-1.4'
        self.assertEqual(tsk.detect_type(pdf_header), 'application/pdf')
        
        # Binary
        binary_data = b'\x00\x01\x02\x03'
        self.assertEqual(tsk.detect_type(binary_data), 'application/octet-stream')


class TestFileOperations(unittest.TestCase):
    """Test file I/O operations"""
    
    def test_save_load_file(self):
        """Test saving and loading TSK files"""
        # Create TSK
        tsk = TSK()
        tsk.set_section('test', {
            'message': 'Hello from file test',
            'timestamp': int(time.time())
        })
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tsk', delete=False) as f:
            temp_path = f.name
            tsk.to_file(temp_path)
        
        try:
            # Load from file
            loaded = TSK.from_file(temp_path)
            self.assertEqual(loaded.get_value('test', 'message'), 'Hello from file test')
            
            # Verify file exists
            self.assertTrue(Path(temp_path).exists())
        finally:
            # Clean up
            os.unlink(temp_path)


class TestDynamicFujsen(unittest.TestCase):
    """Test dynamic fujsen creation"""
    
    def test_set_fujsen(self):
        """Test setting fujsen dynamically"""
        tsk = TSK()
        
        # Define function
        def multiply(a, b):
            return a * b
        
        # Set as fujsen
        tsk.set_fujsen('math', 'multiply_fujsen', multiply)
        
        # Execute
        result = tsk.execute_fujsen('math', 'multiply_fujsen', 7, 8)
        self.assertEqual(result, 56)
        
    def test_lambda_fujsen(self):
        """Test setting lambda as fujsen"""
        tsk = TSK()
        
        # Lambda function
        square = lambda x: x ** 2
        
        # Set as fujsen
        tsk.set_fujsen('math', 'square_fujsen', square)
        
        # Execute
        result = tsk.execute_fujsen('math', 'square_fujsen', 9)
        self.assertEqual(result, 81)
        
    def test_invalid_fujsen(self):
        """Test error on non-callable fujsen"""
        tsk = TSK()
        
        with self.assertRaises(ValueError) as ctx:
            tsk.set_fujsen('bad', 'not_callable', 'not a function')
        self.assertIn('must be a callable', str(ctx.exception))


class TestRoundTrip(unittest.TestCase):
    """Test round-trip parsing and generation"""
    
    def test_round_trip(self):
        """Test that data survives parsing and regeneration"""
        # Parse original
        tsk = TSK.from_string(SAMPLE_TSK)
        
        # Modify
        tsk.set_value('storage', 'updated', True)
        tsk.set_section('new_section', {
            'key1': 'value1',
            'key2': 42,
            'key3': [1, 2, 3]
        })
        
        # Convert to string
        output = tsk.to_string()
        
        # Parse again
        reparsed = TSK.from_string(output)
        
        # Verify modifications
        self.assertTrue(reparsed.get_value('storage', 'updated'))
        self.assertEqual(reparsed.get_value('new_section', 'key1'), 'value1')
        self.assertEqual(reparsed.get_value('new_section', 'key2'), 42)
        self.assertEqual(reparsed.get_value('new_section', 'key3'), [1, 2, 3])
        
        # Original data should persist
        self.assertEqual(reparsed.get_value('storage', 'id'), 'flex_123')
        
    def test_special_characters(self):
        """Test handling of special characters"""
        tsk = TSK()
        
        # Special characters
        special = 'Line with "quotes" and \\backslashes\\'
        tsk.set_value('test', 'special', special)
        
        # Round trip
        output = tsk.to_string()
        reparsed = TSK.from_string(output)
        
        self.assertEqual(reparsed.get_value('test', 'special'), special)


class TestComplexData(unittest.TestCase):
    """Test complex nested data structures"""
    
    def test_deeply_nested(self):
        """Test deeply nested structures"""
        complex_tsk = """
[deeply]
nested = { "level1" = { "level2" = { "level3" = { "value" = 42 } } } }
matrix = [ [ 1, 2, 3 ], [ 4, 5, 6 ], [ 7, 8, 9 ] ]
mixed = [ "string", 123, true, { "key" = "value" }, [ "nested", "array" ] ]
"""
        
        tsk = TSK.from_string(complex_tsk)
        
        # Test deep nesting
        nested = tsk.get_value('deeply', 'nested')
        self.assertEqual(nested['level1']['level2']['level3']['value'], 42)
        
        # Test matrix
        matrix = tsk.get_value('deeply', 'matrix')
        self.assertEqual(matrix[1][1], 5)
        self.assertEqual(matrix[2], [7, 8, 9])
        
        # Test mixed array
        mixed = tsk.get_value('deeply', 'mixed')
        self.assertEqual(mixed[0], 'string')
        self.assertEqual(mixed[1], 123)
        self.assertTrue(mixed[2])
        self.assertEqual(mixed[3], {'key': 'value'})
        self.assertEqual(mixed[4], ['nested', 'array'])


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def test_missing_section(self):
        """Test accessing missing sections"""
        tsk = TSK()
        
        self.assertIsNone(tsk.get_value('missing', 'key'))
        self.assertIsNone(tsk.get_section('missing'))
        
    def test_malformed_fujsen(self):
        """Test malformed fujsen code"""
        tsk = TSK()
        
        # Invalid Python code
        tsk.set_value('bad', 'fujsen', 'this is not valid python {')
        
        with self.assertRaises(ValueError):
            tsk.execute_fujsen('bad', 'fujsen')
            
    def test_empty_collections(self):
        """Test empty arrays and objects"""
        tsk_str = """
[empty]
array = [ ]
object = { }
"""
        tsk = TSK.from_string(tsk_str)
        
        self.assertEqual(tsk.get_value('empty', 'array'), [])
        self.assertEqual(tsk.get_value('empty', 'object'), {})


if __name__ == '__main__':
    # Run tests with verbosity
    unittest.main(verbosity=2)