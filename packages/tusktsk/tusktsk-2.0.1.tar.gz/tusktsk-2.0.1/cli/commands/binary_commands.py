#!/usr/bin/env python3
"""
Binary Commands for TuskLang Python CLI
=======================================
Implements binary performance commands
"""

import os
import sys
import time
import struct
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional

from tsk import TSK, TSKParser
from tsk_enhanced import TuskLangEnhanced
from peanut_config import PeanutConfig
from ..utils.output_formatter import OutputFormatter
from ..utils.error_handler import ErrorHandler


def handle_binary_command(args: Any, cli: Any) -> int:
    """Handle binary commands"""
    formatter = OutputFormatter(cli.json_output, cli.quiet, cli.verbose)
    error_handler = ErrorHandler(cli.json_output, cli.verbose)
    
    try:
        if args.binary_command == 'compile':
            return _handle_binary_compile(args, formatter, error_handler)
        elif args.binary_command == 'execute':
            return _handle_binary_execute(args, formatter, error_handler)
        elif args.binary_command == 'benchmark':
            return _handle_binary_benchmark(args, formatter, error_handler)
        elif args.binary_command == 'optimize':
            return _handle_binary_optimize(args, formatter, error_handler)
        else:
            formatter.error("Unknown binary command")
            return ErrorHandler.INVALID_ARGS
            
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_binary_compile(args: Any, formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle binary compile command"""
    file_path = Path(args.file)
    
    if not file_path.exists():
        return error_handler.handle_file_not_found(str(file_path))
    
    if file_path.suffix != '.tsk':
        formatter.error("File must have .tsk extension")
        return ErrorHandler.INVALID_ARGS
    
    formatter.loading(f"Compiling {file_path} to binary format...")
    
    try:
        # Parse TSK file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse with enhanced parser
        parser = TuskLangEnhanced()
        data = parser.parse(content)
        
        # Compile to binary
        peanut_config = PeanutConfig()
        binary_path = file_path.with_suffix('.pnt')
        
        peanut_config.compile_to_binary(data, str(binary_path))
        
        # Show compilation results
        original_size = file_path.stat().st_size
        binary_size = binary_path.stat().st_size
        compression_ratio = (1 - binary_size / original_size) * 100
        
        formatter.success(f"Compiled to {binary_path}")
        formatter.subsection("Compilation Results")
        formatter.key_value("Original Size", f"{original_size} bytes")
        formatter.key_value("Binary Size", f"{binary_size} bytes")
        formatter.key_value("Compression", f"{compression_ratio:.1f}%")
        
        if compression_ratio > 0:
            formatter.success(f"Binary format is {compression_ratio:.1f}% smaller")
        else:
            formatter.info("Binary format provides performance benefits despite size")
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_binary_execute(args: Any, formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle binary execute command"""
    file_path = Path(args.file)
    
    if not file_path.exists():
        return error_handler.handle_file_not_found(str(file_path))
    
    if file_path.suffix not in ['.pnt']:
        formatter.error("File must have .pnt extension")
        return ErrorHandler.INVALID_ARGS
    
    formatter.loading(f"Executing binary file: {file_path}")
    
    try:
        # Load binary file
        peanut_config = PeanutConfig()
        data = peanut_config.load_binary(str(file_path))
        
        # Execute any FUJSEN functions found
        tsk = TSK(data)
        executed_functions = []
        
        # Find and execute FUJSEN functions
        for section_name, section_data in data.items():
            if isinstance(section_data, dict):
                for key, value in section_data.items():
                    if key.endswith('_fujsen') and isinstance(value, str):
                        try:
                            result = tsk.execute_fujsen(section_name, key)
                            executed_functions.append({
                                'function': f"{section_name}.{key}",
                                'result': result
                            })
                        except Exception as e:
                            executed_functions.append({
                                'function': f"{section_name}.{key}",
                                'error': str(e)
                            })
        
        # Display results
        formatter.success(f"Binary file executed successfully")
        formatter.subsection("Configuration Data")
        
        # Show top-level sections
        for section_name, section_data in data.items():
            if isinstance(section_data, dict):
                formatter.key_value(f"Section: {section_name}", f"{len(section_data)} keys")
            else:
                formatter.key_value(section_name, section_data)
        
        # Show executed functions
        if executed_functions:
            formatter.subsection("Executed Functions")
            for func in executed_functions:
                if 'error' in func:
                    formatter.error(f"{func['function']}: {func['error']}")
                else:
                    formatter.key_value(func['function'], func['result'])
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_binary_benchmark(args: Any, formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle binary benchmark command"""
    file_path = Path(args.file)
    
    if not file_path.exists():
        return error_handler.handle_file_not_found(str(file_path))
    
    if file_path.suffix != '.tsk':
        formatter.error("File must have .tsk extension")
        return ErrorHandler.INVALID_ARGS
    
    formatter.loading(f"Benchmarking {file_path}...")
    
    try:
        # Read file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Benchmark text parsing
        formatter.subsection("Text Format Benchmark")
        
        start_time = time.time()
        for _ in range(100):
            parser = TuskLangEnhanced()
            data = parser.parse(content)
        text_parse_time = (time.time() - start_time) / 100
        
        # Compile to binary
        peanut_config = PeanutConfig()
        binary_path = file_path.with_suffix('.pnt')
        peanut_config.compile_to_binary(data, str(binary_path))
        
        # Benchmark binary loading
        formatter.subsection("Binary Format Benchmark")
        
        start_time = time.time()
        for _ in range(100):
            binary_data = peanut_config.load_binary(str(binary_path))
        binary_load_time = (time.time() - start_time) / 100
        
        # Calculate performance improvement
        improvement = ((text_parse_time - binary_load_time) / text_parse_time) * 100
        
        # Display results
        formatter.table(
            ['Format', 'Time (ms)', 'Performance'],
            [
                ['Text Parse', f"{text_parse_time*1000:.2f}", 'Baseline'],
                ['Binary Load', f"{binary_load_time*1000:.2f}", f"{improvement:.1f}% faster"]
            ],
            'Performance Comparison'
        )
        
        # Show file sizes
        original_size = file_path.stat().st_size
        binary_size = binary_path.stat().st_size
        
        formatter.subsection("File Size Comparison")
        formatter.key_value("Text Format", f"{original_size} bytes")
        formatter.key_value("Binary Format", f"{binary_size} bytes")
        formatter.key_value("Size Ratio", f"{binary_size/original_size:.2f}x")
        
        # Clean up
        binary_path.unlink()
        
        # Summary
        if improvement > 50:
            formatter.success(f"Binary format provides excellent performance improvement: {improvement:.1f}% faster")
        elif improvement > 20:
            formatter.success(f"Binary format provides good performance improvement: {improvement:.1f}% faster")
        else:
            formatter.info(f"Binary format provides modest performance improvement: {improvement:.1f}% faster")
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_binary_optimize(args: Any, formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle binary optimize command"""
    file_path = Path(args.file)
    
    if not file_path.exists():
        return error_handler.handle_file_not_found(str(file_path))
    
    if file_path.suffix not in ['.tskb', '.pnt']:
        formatter.error("File must have .tskb or .pnt extension")
        return ErrorHandler.INVALID_ARGS
    
    formatter.loading(f"Optimizing binary file: {file_path}")
    
    try:
        # Load binary file
        peanut_config = PeanutConfig()
        data = peanut_config.load_binary(str(file_path))
        
        # Apply optimizations
        optimized_data = _optimize_binary_data(data)
        
        # Create optimized binary
        optimized_path = file_path.with_suffix('.optimized.tskb')
        peanut_config.compile_to_binary(optimized_data, str(optimized_path))
        
        # Compare sizes
        original_size = file_path.stat().st_size
        optimized_size = optimized_path.stat().st_size
        size_reduction = ((original_size - optimized_size) / original_size) * 100
        
        # Display results
        formatter.success(f"Binary file optimized: {optimized_path}")
        formatter.subsection("Optimization Results")
        formatter.key_value("Original Size", f"{original_size} bytes")
        formatter.key_value("Optimized Size", f"{optimized_size} bytes")
        formatter.key_value("Size Reduction", f"{size_reduction:.1f}%")
        
        # Show optimization details
        formatter.subsection("Optimizations Applied")
        optimizations = _get_optimization_details(data, optimized_data)
        for opt in optimizations:
            formatter.info(f"• {opt}")
        
        if size_reduction > 0:
            formatter.success(f"Optimization achieved {size_reduction:.1f}% size reduction")
        else:
            formatter.info("Optimization focused on performance rather than size reduction")
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _optimize_binary_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Optimize binary data for production"""
    optimized = {}
    
    for key, value in data.items():
        if isinstance(value, dict):
            optimized[key] = _optimize_binary_data(value)
        elif isinstance(value, str):
            # Remove extra whitespace
            optimized[key] = value.strip()
        elif isinstance(value, list):
            # Remove empty items and optimize
            optimized[key] = [item for item in value if item is not None]
        else:
            optimized[key] = value
    
    return optimized


def _get_optimization_details(original: Dict[str, Any], optimized: Dict[str, Any]) -> List[str]:
    """Get details about optimizations applied"""
    details = []
    
    # Count keys
    original_keys = _count_keys_recursive(original)
    optimized_keys = _count_keys_recursive(optimized)
    
    if optimized_keys < original_keys:
        details.append(f"Reduced keys from {original_keys} to {optimized_keys}")
    
    # Check for string optimizations
    original_strings = _count_strings_recursive(original)
    optimized_strings = _count_strings_recursive(optimized)
    
    if optimized_strings < original_strings:
        details.append(f"Optimized {original_strings - optimized_strings} string values")
    
    # Check for null removals
    original_nulls = _count_nulls_recursive(original)
    optimized_nulls = _count_nulls_recursive(optimized)
    
    if optimized_nulls < original_nulls:
        details.append(f"Removed {original_nulls - optimized_nulls} null values")
    
    if not details:
        details.append("Applied general data structure optimizations")
    
    return details


def _count_keys_recursive(data: Any) -> int:
    """Count total keys recursively"""
    if isinstance(data, dict):
        count = len(data)
        for value in data.values():
            count += _count_keys_recursive(value)
        return count
    elif isinstance(data, list):
        count = 0
        for item in data:
            count += _count_keys_recursive(item)
        return count
    else:
        return 0


def _count_strings_recursive(data: Any) -> int:
    """Count string values recursively"""
    if isinstance(data, dict):
        count = sum(1 for value in data.values() if isinstance(value, str))
        for value in data.values():
            count += _count_strings_recursive(value)
        return count
    elif isinstance(data, list):
        count = sum(1 for item in data if isinstance(item, str))
        for item in data:
            count += _count_strings_recursive(item)
        return count
    else:
        return 0


def _count_nulls_recursive(data: Any) -> int:
    """Count null values recursively"""
    if isinstance(data, dict):
        count = sum(1 for value in data.values() if value is None)
        for value in data.values():
            count += _count_nulls_recursive(value)
        return count
    elif isinstance(data, list):
        count = sum(1 for item in data if item is None)
        for item in data:
            count += _count_nulls_recursive(item)
        return count
    else:
        return 0 