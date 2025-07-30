#!/usr/bin/env python3
"""
Development Commands for TuskLang Python CLI
============================================
Implements development-related commands
"""

import os
import sys
import time
import threading
import http.server
import socketserver
from pathlib import Path
from typing import Any, Dict, Optional

from tsk import TSK, TSKParser
from tsk_enhanced import TuskLangEnhanced
from peanut_config import PeanutConfig
from ..utils.output_formatter import OutputFormatter
from ..utils.error_handler import ErrorHandler
from ..utils.config_loader import ConfigLoader


def handle_serve_command(args: Any, cli: Any) -> int:
    """Handle serve command"""
    formatter = OutputFormatter(cli.json_output, cli.quiet, cli.verbose)
    error_handler = ErrorHandler(cli.json_output, cli.verbose)
    
    try:
        port = args.port
        return _start_dev_server(port, formatter, error_handler)
    except Exception as e:
        return error_handler.handle_error(e)


def handle_compile_command(args: Any, cli: Any) -> int:
    """Handle compile command"""
    formatter = OutputFormatter(cli.json_output, cli.quiet, cli.verbose)
    error_handler = ErrorHandler(cli.json_output, cli.verbose)
    
    try:
        file_path = Path(args.file)
        return _compile_tsk_file(file_path, formatter, error_handler)
    except Exception as e:
        return error_handler.handle_error(e)


def handle_optimize_command(args: Any, cli: Any) -> int:
    """Handle optimize command"""
    formatter = OutputFormatter(cli.json_output, cli.quiet, cli.verbose)
    error_handler = ErrorHandler(cli.json_output, cli.verbose)
    
    try:
        file_path = Path(args.file)
        return _optimize_tsk_file(file_path, formatter, error_handler)
    except Exception as e:
        return error_handler.handle_error(e)


def _start_dev_server(port: int, formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Start development server"""
    formatter.loading(f"Starting development server on port {port}...")
    
    try:
        # Create simple HTTP server
        class TuskLangHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=os.getcwd(), **kwargs)
            
            def end_headers(self):
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                super().end_headers()
            
            def do_GET(self):
                if self.path == '/':
                    self.path = '/index.html'
                elif self.path == '/api/status':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "running", "timestamp": "' + str(time.time()).encode() + b'"}')
                    return
                super().do_GET()
        
        with socketserver.TCPServer(("", port), TuskLangHandler) as httpd:
            formatter.success(f"Development server started at http://localhost:{port}")
            formatter.info("Press Ctrl+C to stop the server")
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                formatter.info("Shutting down development server...")
                httpd.shutdown()
                formatter.success("Development server stopped")
        
        return ErrorHandler.SUCCESS
        
    except OSError as e:
        if "Address already in use" in str(e):
            formatter.error(f"Port {port} is already in use")
            return ErrorHandler.CONNECTION_ERROR
        else:
            return error_handler.handle_error(e)
    except Exception as e:
        return error_handler.handle_error(e)


def _compile_tsk_file(file_path: Path, formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Compile TSK file to optimized format"""
    if not file_path.exists():
        return error_handler.handle_file_not_found(str(file_path))
    
    if file_path.suffix != '.tsk':
        formatter.error("File must have .tsk extension")
        return ErrorHandler.INVALID_ARGS
    
    formatter.loading(f"Compiling {file_path}...")
    
    try:
        # Parse TSK file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse with enhanced parser
        parser = TuskLangEnhanced()
        data = parser.parse(content)
        
        # Create optimized version
        optimized_content = _create_optimized_tsk(data)
        
        # Write optimized file
        optimized_path = file_path.with_suffix('.optimized.tsk')
        with open(optimized_path, 'w') as f:
            f.write(optimized_content)
        
        # Also compile to binary if peanut_config is available
        try:
            peanut_config = PeanutConfig()
            binary_path = file_path.with_suffix('.pnt')
            peanut_config.compile_to_binary(data, str(binary_path))
            formatter.success(f"Compiled to {optimized_path} and {binary_path}")
        except Exception as e:
            formatter.warning(f"Binary compilation failed: {e}")
            formatter.success(f"Compiled to {optimized_path}")
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _optimize_tsk_file(file_path: Path, formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Optimize TSK file for production"""
    if not file_path.exists():
        return error_handler.handle_file_not_found(str(file_path))
    
    if file_path.suffix != '.tsk':
        formatter.error("File must have .tsk extension")
        return ErrorHandler.INVALID_ARGS
    
    formatter.loading(f"Optimizing {file_path} for production...")
    
    try:
        # Parse TSK file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse with enhanced parser
        parser = TuskLangEnhanced()
        data = parser.parse(content)
        
        # Apply optimizations
        optimized_data = _apply_optimizations(data)
        
        # Create optimized content
        optimized_content = _create_optimized_tsk(optimized_data)
        
        # Write optimized file
        optimized_path = file_path.with_suffix('.prod.tsk')
        with open(optimized_path, 'w') as f:
            f.write(optimized_content)
        
        # Show optimization statistics
        original_size = len(content)
        optimized_size = len(optimized_content)
        reduction = ((original_size - optimized_size) / original_size) * 100
        
        formatter.success(f"Optimized file saved to {optimized_path}")
        formatter.info(f"Size reduction: {reduction:.1f}% ({original_size} -> {optimized_size} bytes)")
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _create_optimized_tsk(data: Dict[str, Any]) -> str:
    """Create optimized TSK content"""
    lines = []
    
    # Add header comment
    lines.append("# Optimized TuskLang Configuration")
    lines.append(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    def format_section(section_data: Dict[str, Any], section_name: str = None, indent: int = 0):
        """Recursively format TSK sections"""
        if section_name:
            lines.append(f"{'  ' * indent}[{section_name}]")
        
        for key, value in section_data.items():
            if isinstance(value, dict):
                format_section(value, key, indent + 1)
            else:
                # Format value
                if isinstance(value, str):
                    if '\n' in value:
                        # Multiline string
                        lines.append(f"{'  ' * indent}{key} = \"\"\"")
                        lines.append(value)
                        lines.append(f"{'  ' * indent}\"\"\"")
                    else:
                        lines.append(f"{'  ' * indent}{key} = \"{value}\"")
                elif isinstance(value, bool):
                    lines.append(f"{'  ' * indent}{key} = {str(value).lower()}")
                elif value is None:
                    lines.append(f"{'  ' * indent}{key} = null")
                else:
                    lines.append(f"{'  ' * indent}{key} = {value}")
    
    format_section(data)
    return '\n'.join(lines)


def _apply_optimizations(data: Dict[str, Any]) -> Dict[str, Any]:
    """Apply production optimizations to configuration data"""
    optimized = {}
    
    for key, value in data.items():
        if isinstance(value, dict):
            optimized[key] = _apply_optimizations(value)
        elif isinstance(value, str):
            # Remove extra whitespace
            optimized[key] = value.strip()
        else:
            optimized[key] = value
    
    return optimized 