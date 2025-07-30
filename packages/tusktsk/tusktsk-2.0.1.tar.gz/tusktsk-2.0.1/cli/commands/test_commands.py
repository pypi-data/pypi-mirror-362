#!/usr/bin/env python3
"""
Testing Commands for TuskLang Python CLI
========================================
Implements testing-related commands
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from tsk import TSK, TSKParser
from tsk_enhanced import TuskLangEnhanced
from peanut_config import PeanutConfig
from adapters import SQLiteAdapter, PostgreSQLAdapter, MongoDBAdapter, RedisAdapter
from ..utils.output_formatter import OutputFormatter
from ..utils.error_handler import ErrorHandler
from ..utils.config_loader import ConfigLoader


def handle_test_command(args: Any, cli: Any) -> int:
    """Handle test command"""
    formatter = OutputFormatter(cli.json_output, cli.quiet, cli.verbose)
    error_handler = ErrorHandler(cli.json_output, cli.verbose)
    
    try:
        if args.all:
            return _run_all_tests(formatter, error_handler)
        elif args.parser:
            return _test_parser(formatter, error_handler)
        elif args.fujsen:
            return _test_fujsen(formatter, error_handler)
        elif args.sdk:
            return _test_sdk(formatter, error_handler)
        elif args.performance:
            return _test_performance(formatter, error_handler)
        elif args.suite:
            return _run_test_suite(args.suite, formatter, error_handler)
        else:
            return _run_basic_tests(formatter, error_handler)
            
    except Exception as e:
        return error_handler.handle_error(e)


def _run_all_tests(formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Run all test suites"""
    formatter.section("Running All Test Suites")
    
    test_results = []
    
    # Run each test suite
    test_suites = [
        ("Parser", _test_parser),
        ("FUJSEN", _test_fujsen),
        ("SDK", _test_sdk),
        ("Performance", _test_performance),
        ("Database Adapters", _test_database_adapters),
        ("Configuration", _test_configuration)
    ]
    
    for suite_name, test_func in test_suites:
        formatter.subsection(f"Testing {suite_name}")
        try:
            result = test_func(formatter, error_handler, silent=True)
            status = "✅ PASS" if result == ErrorHandler.SUCCESS else "❌ FAIL"
            test_results.append([suite_name, status])
        except Exception as e:
            test_results.append([suite_name, f"❌ ERROR: {str(e)}"])
    
    # Display results
    formatter.table(
        ['Test Suite', 'Status'],
        test_results,
        'Test Results Summary'
    )
    
    # Check if all tests passed
    failed_tests = [result for result in test_results if '❌' in result[1]]
    if failed_tests:
        formatter.error(f"{len(failed_tests)} test suites failed")
        return ErrorHandler.GENERAL_ERROR
    else:
        formatter.success("All test suites passed!")
        return ErrorHandler.SUCCESS


def _run_basic_tests(formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Run basic tests"""
    formatter.section("Running Basic Tests")
    
    test_results = []
    
    # Test parser
    try:
        result = _test_parser(formatter, error_handler, silent=True)
        test_results.append(["Parser", "✅ PASS" if result == ErrorHandler.SUCCESS else "❌ FAIL"])
    except Exception as e:
        test_results.append(["Parser", f"❌ ERROR: {str(e)}"])
    
    # Test basic functionality
    try:
        result = _test_basic_functionality(formatter, error_handler)
        test_results.append(["Basic Functionality", "✅ PASS" if result == ErrorHandler.SUCCESS else "❌ FAIL"])
    except Exception as e:
        test_results.append(["Basic Functionality", f"❌ ERROR: {str(e)}"])
    
    # Display results
    formatter.table(
        ['Test', 'Status'],
        test_results,
        'Basic Test Results'
    )
    
    failed_tests = [result for result in test_results if '❌' in result[1]]
    if failed_tests:
        formatter.error(f"{len(failed_tests)} tests failed")
        return ErrorHandler.GENERAL_ERROR
    else:
        formatter.success("All basic tests passed!")
        return ErrorHandler.SUCCESS


def _run_test_suite(suite_name: str, formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Run specific test suite"""
    formatter.section(f"Running Test Suite: {suite_name}")
    
    test_suites = {
        'parser': _test_parser,
        'fujsen': _test_fujsen,
        'sdk': _test_sdk,
        'performance': _test_performance,
        'database': _test_database_adapters,
        'config': _test_configuration
    }
    
    if suite_name.lower() not in test_suites:
        formatter.error(f"Unknown test suite: {suite_name}")
        formatter.info(f"Available suites: {', '.join(test_suites.keys())}")
        return ErrorHandler.INVALID_ARGS
    
    return test_suites[suite_name.lower()](formatter, error_handler)


def _test_parser(formatter: OutputFormatter, error_handler: ErrorHandler, silent: bool = False) -> int:
    """Test parser functionality"""
    if not silent:
        formatter.subsection("Testing Parser")
    
    try:
        # Test basic TSK parsing
        test_content = """
[database]
host = "localhost"
port = 5432
debug = true

[server]
host = "0.0.0.0"
port = 8080
workers = 4
"""
        
        # Test basic parser
        data = TSKParser.parse(test_content)
        if not isinstance(data, dict):
            raise Exception("Parser did not return dictionary")
        
        if 'database' not in data or 'server' not in data:
            raise Exception("Parser did not parse sections correctly")
        
        # Test enhanced parser
        enhanced_parser = TuskLangEnhanced()
        enhanced_data = enhanced_parser.parse(test_content)
        
        if not isinstance(enhanced_data, dict):
            raise Exception("Enhanced parser did not return dictionary")
        
        # Test complex parsing
        complex_content = """
$app_name: "Test App"
$version: "1.0.0"

app_name: $app_name
version: $version

server {
    host: "127.0.0.1"
    port: 3000
}

cache >
    driver: "redis"
    ttl: "5m"
<
"""
        
        complex_data = enhanced_parser.parse(complex_content)
        if not isinstance(complex_data, dict):
            raise Exception("Complex parsing failed")
        
        if not silent:
            formatter.success("Parser tests passed")
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        if not silent:
            formatter.error(f"Parser test failed: {e}")
        return ErrorHandler.GENERAL_ERROR


def _test_fujsen(formatter: OutputFormatter, error_handler: ErrorHandler, silent: bool = False) -> int:
    """Test FUJSEN functionality"""
    if not silent:
        formatter.subsection("Testing FUJSEN")
    
    try:
        # Test FUJSEN execution
        tsk = TSK()
        
        # Add test function
        def test_function(x, y):
            return x + y
        
        tsk.set_fujsen('test', 'add_fujsen', test_function)
        
        # Execute function
        result = tsk.execute_fujsen('test', 'add_fujsen', 5, 3)
        if result != 8:
            raise Exception(f"FUJSEN execution failed: expected 8, got {result}")
        
        # Test lambda function
        tsk.set_value('test', 'multiply_fujsen', """
lambda x, y: x * y
""")
        
        result = tsk.execute_fujsen('test', 'multiply_fujsen', 4, 6)
        if result != 24:
            raise Exception(f"Lambda FUJSEN failed: expected 24, got {result}")
        
        # Test JavaScript-style function
        tsk.set_value('test', 'js_style_fujsen', """
(x, y) => {
  if (x > y) return x;
  return y;
}
""")
        
        result = tsk.execute_fujsen('test', 'js_style_fujsen', 10, 15)
        if result != 15:
            raise Exception(f"JS-style FUJSEN failed: expected 15, got {result}")
        
        if not silent:
            formatter.success("FUJSEN tests passed")
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        if not silent:
            formatter.error(f"FUJSEN test failed: {e}")
        return ErrorHandler.GENERAL_ERROR


def _test_sdk(formatter: OutputFormatter, error_handler: ErrorHandler, silent: bool = False) -> int:
    """Test SDK-specific features"""
    if not silent:
        formatter.subsection("Testing SDK Features")
    
    try:
        # Test file operations
        test_file = Path('test_sdk.tsk')
        test_content = """
[test]
value = "hello"
number = 42
"""
        
        # Create test file
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        # Test loading from file
        tsk = TSK.from_file(str(test_file))
        value = tsk.get_value('test', 'value')
        if value != "hello":
            raise Exception(f"File loading failed: expected 'hello', got '{value}'")
        
        # Test saving to file
        tsk.set_value('test', 'new_value', 'world')
        tsk.to_file(str(test_file))
        
        # Verify save
        tsk2 = TSK.from_file(str(test_file))
        new_value = tsk2.get_value('test', 'new_value')
        if new_value != "world":
            raise Exception(f"File saving failed: expected 'world', got '{new_value}'")
        
        # Clean up
        test_file.unlink()
        
        if not silent:
            formatter.success("SDK tests passed")
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        if not silent:
            formatter.error(f"SDK test failed: {e}")
        return ErrorHandler.GENERAL_ERROR


def _test_performance(formatter: OutputFormatter, error_handler: ErrorHandler, silent: bool = False) -> int:
    """Test performance benchmarks"""
    if not silent:
        formatter.subsection("Performance Benchmarks")
    
    try:
        # Create large test data
        large_content = []
        for i in range(1000):
            large_content.append(f'[section_{i}]')
            large_content.append(f'key_{i} = "value_{i}"')
            large_content.append(f'number_{i} = {i}')
        
        large_content = '\n'.join(large_content)
        
        # Benchmark parsing
        start_time = time.time()
        data = TSKParser.parse(large_content)
        parse_time = time.time() - start_time
        
        # Benchmark enhanced parsing
        enhanced_parser = TuskLangEnhanced()
        start_time = time.time()
        enhanced_data = enhanced_parser.parse(large_content)
        enhanced_parse_time = time.time() - start_time
        
        # Benchmark binary compilation
        peanut_config = PeanutConfig()
        start_time = time.time()
        peanut_config.compile_to_binary(data, 'test_performance.pnt')
        compile_time = time.time() - start_time
        
        # Benchmark binary loading
        start_time = time.time()
        loaded_data = peanut_config.load_binary('test_performance.pnt')
        load_time = time.time() - start_time
        
        # Clean up
        Path('test_performance.pnt').unlink()
        
        # Display results
        if not silent:
            formatter.table(
                ['Operation', 'Time (ms)', 'Performance'],
                [
                    ['Basic Parse', f"{parse_time*1000:.2f}", 'Baseline'],
                    ['Enhanced Parse', f"{enhanced_parse_time*1000:.2f}", f"{parse_time/enhanced_parse_time:.1f}x"],
                    ['Binary Compile', f"{compile_time*1000:.2f}", 'N/A'],
                    ['Binary Load', f"{load_time*1000:.2f}", f"{parse_time/load_time:.1f}x faster"]
                ],
                'Performance Results'
            )
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        if not silent:
            formatter.error(f"Performance test failed: {e}")
        return ErrorHandler.GENERAL_ERROR


def _test_database_adapters(formatter: OutputFormatter, error_handler: ErrorHandler, silent: bool = False) -> int:
    """Test database adapters"""
    if not silent:
        formatter.subsection("Testing Database Adapters")
    
    try:
        # Test SQLite adapter
        adapter = SQLiteAdapter({'database': ':memory:'})
        adapter.connect()
        
        # Create test table
        adapter.query("""
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT,
                value INTEGER
            )
        """)
        
        # Insert test data
        adapter.query("INSERT INTO test_table (name, value) VALUES (?, ?)", ["test", 42])
        
        # Query test data
        result = adapter.query("SELECT * FROM test_table")
        if len(result) != 1 or result[0]['name'] != 'test':
            raise Exception("SQLite adapter test failed")
        
        adapter.close()
        
        if not silent:
            formatter.success("Database adapter tests passed")
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        if not silent:
            formatter.error(f"Database adapter test failed: {e}")
        return ErrorHandler.GENERAL_ERROR


def _test_configuration(formatter: OutputFormatter, error_handler: ErrorHandler, silent: bool = False) -> int:
    """Test configuration system"""
    if not silent:
        formatter.subsection("Testing Configuration System")
    
    try:
        # Test PeanutConfig
        peanut_config = PeanutConfig()
        
        # Create test config
        test_config = {
            'app': {
                'name': 'Test App',
                'version': '1.0.0'
            },
            'database': {
                'host': 'localhost',
                'port': 5432
            }
        }
        
        # Test binary compilation
        peanut_config.compile_to_binary(test_config, 'test_config.pnt')
        
        # Test binary loading
        loaded_config = peanut_config.load_binary('test_config.pnt')
        
        if loaded_config != test_config:
            raise Exception("Configuration binary round-trip failed")
        
        # Clean up
        Path('test_config.pnt').unlink()
        
        if not silent:
            formatter.success("Configuration tests passed")
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        if not silent:
            formatter.error(f"Configuration test failed: {e}")
        return ErrorHandler.GENERAL_ERROR


def _test_basic_functionality(formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Test basic functionality"""
    try:
        # Test TSK class
        tsk = TSK()
        tsk.set_section('test', {'key': 'value'})
        
        value = tsk.get_value('test', 'key')
        if value != 'value':
            raise Exception("Basic TSK functionality failed")
        
        # Test string conversion
        tsk_string = tsk.to_string()
        if 'key = "value"' not in tsk_string:
            raise Exception("TSK string conversion failed")
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        formatter.error(f"Basic functionality test failed: {e}")
        return ErrorHandler.GENERAL_ERROR 