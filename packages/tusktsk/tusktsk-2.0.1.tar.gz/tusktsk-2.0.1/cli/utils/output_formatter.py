#!/usr/bin/env python3
"""
Output Formatter for TuskLang Python CLI
========================================
Handles consistent output formatting across all commands
"""

import json
import sys
from typing import Any, Dict, List, Optional


class OutputFormatter:
    """Formats CLI output consistently"""
    
    # Status symbols
    SUCCESS = "✅"
    ERROR = "❌"
    WARNING = "⚠️"
    LOADING = "🔄"
    LOCATION = "📍"
    
    def __init__(self, json_output: bool = False, quiet: bool = False, verbose: bool = False):
        self.json_output = json_output
        self.quiet = quiet
        self.verbose = verbose
    
    def success(self, message: str, data: Any = None) -> None:
        """Output success message"""
        if self.quiet:
            return
        
        if self.json_output:
            self._output_json({
                'status': 'success',
                'message': message,
                'data': data
            })
        else:
            print(f"{self.SUCCESS} {message}")
            if data and self.verbose:
                self._print_data(data)
    
    def error(self, message: str, error_code: int = 1, data: Any = None) -> None:
        """Output error message"""
        if self.json_output:
            self._output_json({
                'status': 'error',
                'message': message,
                'error_code': error_code,
                'data': data
            })
        else:
            print(f"{self.ERROR} {message}", file=sys.stderr)
            if data and self.verbose:
                self._print_data(data, file=sys.stderr)
    
    def warning(self, message: str, data: Any = None) -> None:
        """Output warning message"""
        if self.quiet:
            return
        
        if self.json_output:
            self._output_json({
                'status': 'warning',
                'message': message,
                'data': data
            })
        else:
            print(f"{self.WARNING} {message}")
            if data and self.verbose:
                self._print_data(data)
    
    def info(self, message: str, data: Any = None) -> None:
        """Output info message"""
        if self.quiet:
            return
        
        if self.json_output:
            self._output_json({
                'status': 'info',
                'message': message,
                'data': data
            })
        else:
            print(f"ℹ️  {message}")
            if data and self.verbose:
                self._print_data(data)
    
    def loading(self, message: str) -> None:
        """Output loading message"""
        if self.quiet or self.json_output:
            return
        print(f"{self.LOADING} {message}")
    
    def table(self, headers: List[str], rows: List[List[Any]], title: str = None) -> None:
        """Output data as a formatted table"""
        if self.quiet:
            return
        
        if self.json_output:
            self._output_json({
                'status': 'success',
                'type': 'table',
                'title': title,
                'headers': headers,
                'rows': rows
            })
        else:
            if title:
                print(f"\n{title}")
            
            # Calculate column widths
            col_widths = []
            for i, header in enumerate(headers):
                max_width = len(str(header))
                for row in rows:
                    if i < len(row):
                        max_width = max(max_width, len(str(row[i])))
                col_widths.append(max_width)
            
            # Print header
            header_line = " | ".join(str(h).ljust(w) for h, w in zip(headers, col_widths))
            print(header_line)
            print("-" * len(header_line))
            
            # Print rows
            for row in rows:
                row_line = " | ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths))
                print(row_line)
    
    def list_items(self, items: List[Any], title: str = None) -> None:
        """Output list of items"""
        if self.quiet:
            return
        
        if self.json_output:
            self._output_json({
                'status': 'success',
                'type': 'list',
                'title': title,
                'items': items
            })
        else:
            if title:
                print(f"\n{title}:")
            
            for i, item in enumerate(items, 1):
                print(f"  {i}. {item}")
    
    def key_value(self, key: str, value: Any) -> None:
        """Output key-value pair"""
        if self.quiet:
            return
        
        if self.json_output:
            self._output_json({
                'status': 'success',
                'type': 'key_value',
                'key': key,
                'value': value
            })
        else:
            print(f"{key}: {value}")
    
    def section(self, title: str) -> None:
        """Output section header"""
        if self.quiet or self.json_output:
            return
        print(f"\n{title}")
        print("=" * len(title))
    
    def subsection(self, title: str) -> None:
        """Output subsection header"""
        if self.quiet or self.json_output:
            return
        print(f"\n{title}")
        print("-" * len(title))
    
    def _output_json(self, data: Dict[str, Any]) -> None:
        """Output data as JSON"""
        print(json.dumps(data, indent=2, default=str))
    
    def _print_data(self, data: Any, file=sys.stdout) -> None:
        """Print data in a readable format"""
        if isinstance(data, dict):
            for key, value in data.items():
                print(f"  {key}: {value}", file=file)
        elif isinstance(data, list):
            for item in data:
                print(f"  - {item}", file=file)
        else:
            print(f"  {data}", file=file)


# Global formatter instance
output_formatter = OutputFormatter() 