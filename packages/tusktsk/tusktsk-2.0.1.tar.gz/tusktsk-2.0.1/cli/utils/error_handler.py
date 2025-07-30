#!/usr/bin/env python3
"""
Error Handler for TuskLang Python CLI
=====================================
Handles errors consistently across all commands
"""

import sys
import traceback
from typing import Any, Optional


class ErrorHandler:
    """Handles CLI errors consistently"""
    
    # Exit codes
    SUCCESS = 0
    GENERAL_ERROR = 1
    INVALID_ARGS = 2
    FILE_NOT_FOUND = 3
    PERMISSION_DENIED = 4
    CONNECTION_ERROR = 5
    CONFIG_ERROR = 6
    LICENSE_ERROR = 7
    
    def __init__(self, json_output: bool = False, verbose: bool = False):
        self.json_output = json_output
        self.verbose = verbose
    
    def handle_error(self, error: Exception, cli_instance: Any = None) -> int:
        """Handle an error and return appropriate exit code"""
        error_type = type(error).__name__
        error_message = str(error)
        
        # Determine exit code based on error type
        exit_code = self._get_exit_code(error)
        
        # Format error output
        if self.json_output:
            self._output_json_error(error_type, error_message, exit_code)
        else:
            self._output_text_error(error_type, error_message, exit_code)
        
        # Show traceback in verbose mode
        if self.verbose:
            traceback.print_exc()
        
        return exit_code
    
    def _get_exit_code(self, error: Exception) -> int:
        """Get appropriate exit code for error type"""
        error_type = type(error).__name__
        
        if 'FileNotFound' in error_type or 'No such file' in str(error):
            return self.FILE_NOT_FOUND
        elif 'Permission' in error_type or 'Access denied' in str(error):
            return self.PERMISSION_DENIED
        elif 'Connection' in error_type or 'Network' in error_type:
            return self.CONNECTION_ERROR
        elif 'Config' in error_type or 'Configuration' in error_type:
            return self.CONFIG_ERROR
        elif 'License' in error_type:
            return self.LICENSE_ERROR
        elif 'Argument' in error_type or 'ValueError' in error_type:
            return self.INVALID_ARGS
        else:
            return self.GENERAL_ERROR
    
    def _output_json_error(self, error_type: str, message: str, exit_code: int) -> None:
        """Output error in JSON format"""
        import json
        
        error_data = {
            'status': 'error',
            'error_type': error_type,
            'message': message,
            'exit_code': exit_code
        }
        
        print(json.dumps(error_data, indent=2), file=sys.stderr)
    
    def _output_text_error(self, error_type: str, message: str, exit_code: int) -> None:
        """Output error in text format"""
        print(f"❌ Error ({error_type}): {message}", file=sys.stderr)
        print(f"Exit code: {exit_code}", file=sys.stderr)
    
    def handle_file_not_found(self, file_path: str) -> int:
        """Handle file not found error"""
        message = f"File not found: {file_path}"
        if self.json_output:
            self._output_json_error("FileNotFoundError", message, self.FILE_NOT_FOUND)
        else:
            print(f"❌ {message}", file=sys.stderr)
        return self.FILE_NOT_FOUND
    
    def handle_permission_error(self, operation: str, path: str) -> int:
        """Handle permission error"""
        message = f"Permission denied: Cannot {operation} {path}"
        if self.json_output:
            self._output_json_error("PermissionError", message, self.PERMISSION_DENIED)
        else:
            print(f"❌ {message}", file=sys.stderr)
        return self.PERMISSION_DENIED
    
    def handle_connection_error(self, service: str, details: str = "") -> int:
        """Handle connection error"""
        message = f"Connection failed to {service}"
        if details:
            message += f": {details}"
        
        if self.json_output:
            self._output_json_error("ConnectionError", message, self.CONNECTION_ERROR)
        else:
            print(f"❌ {message}", file=sys.stderr)
        return self.CONNECTION_ERROR
    
    def handle_config_error(self, message: str) -> int:
        """Handle configuration error"""
        if self.json_output:
            self._output_json_error("ConfigError", message, self.CONFIG_ERROR)
        else:
            print(f"❌ Configuration error: {message}", file=sys.stderr)
        return self.CONFIG_ERROR
    
    def handle_invalid_args(self, message: str) -> int:
        """Handle invalid arguments error"""
        if self.json_output:
            self._output_json_error("ArgumentError", message, self.INVALID_ARGS)
        else:
            print(f"❌ Invalid arguments: {message}", file=sys.stderr)
        return self.INVALID_ARGS


# Global error handler instance
error_handler = ErrorHandler() 