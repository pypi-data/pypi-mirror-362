#!/usr/bin/env python3
"""
TuskLang Enhanced for Python - The Freedom Parser
=================================================
"We don't bow to any king" - Support ALL syntax styles

Features:
- Multiple grouping: [], {}, <>
- $global vs section-local variables
- Cross-file communication
- Database queries (placeholder adapters)
- All @ operators
- Maximum flexibility

DEFAULT CONFIG: peanut.tsk (the bridge of language grace)
"""

import re
import json
import os
import time
import hashlib
import gzip
import struct
from typing import Any, Dict, List, Union, Optional, Tuple
from datetime import datetime
from pathlib import Path


class TuskLangEnhanced:
    """Enhanced TuskLang parser with full syntax flexibility"""
    
    def __init__(self):
        self.data = {}
        self.global_variables = {}
        self.section_variables = {}
        self.cache = {}
        self.cross_file_cache = {}
        self.current_section = ""
        self.in_object = False
        self.object_key = ""
        self.peanut_loaded = False
        
        # Standard peanut.tsk locations
        self.peanut_locations = [
            "./peanut.tsk",
            "../peanut.tsk", 
            "../../peanut.tsk",
            "/etc/tusklang/peanut.tsk",
            os.path.expanduser("~/.config/tusklang/peanut.tsk"),
            os.environ.get('TUSKLANG_CONFIG', '')
        ]
    
    def load_peanut(self):
        """Load peanut.tsk if available"""
        if self.peanut_loaded:
            return
            
        for location in self.peanut_locations:
            if location and Path(location).exists():
                print(f"# Loading universal config from: {location}")
                self.parse_file(location)
                self.peanut_loaded = True
                return
    
    def parse_value(self, value: str) -> Any:
        """Parse TuskLang value with all syntax support"""
        value = value.strip()
        
        # Remove optional semicolon
        if value.endswith(';'):
            value = value[:-1].strip()
        
        # Basic types
        if value == 'true':
            return True
        elif value == 'false':
            return False
        elif value == 'null':
            return None
        
        # Numbers
        if re.match(r'^-?\d+$', value):
            return int(value)
        elif re.match(r'^-?\d+\.\d+$', value):
            return float(value)
        
        # $variable references (global)
        if re.match(r'^\$([a-zA-Z_][a-zA-Z0-9_]*)$', value):
            var_name = value[1:]
            return self.global_variables.get(var_name, '')
        
        # Section-local variable references
        if self.current_section and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', value):
            section_key = f"{self.current_section}.{value}"
            if section_key in self.section_variables:
                return self.section_variables[section_key]
        
        # @date function
        date_match = re.match(r'^@date\(["\'](.*)["\']\)$', value)
        if date_match:
            format_str = date_match.group(1)
            return self.execute_date(format_str)
        
        # @env function with default
        env_match = re.match(r'^@env\(["\']([^"\']*)["\'](?:,\s*(.+))?\)$', value)
        if env_match:
            env_var = env_match.group(1)
            default_val = env_match.group(2)
            if default_val:
                default_val = default_val.strip('"\'')
            return os.environ.get(env_var, default_val or '')
        
        # Ranges: 8000-9000
        range_match = re.match(r'^(\d+)-(\d+)$', value)
        if range_match:
            return {
                "min": int(range_match.group(1)),
                "max": int(range_match.group(2)),
                "type": "range"
            }
        
        # Arrays
        if value.startswith('[') and value.endswith(']'):
            return self.parse_array(value)
        
        # Objects
        if value.startswith('{') and value.endswith('}'):
            return self.parse_object(value)
        
        # Cross-file references: @file.tsk.get('key')
        cross_get_match = re.match(r'^@([a-zA-Z0-9_-]+)\.tsk\.get\(["\'](.*)["\']\)$', value)
        if cross_get_match:
            file_name = cross_get_match.group(1)
            key = cross_get_match.group(2)
            return self.cross_file_get(file_name, key)
        
        # Cross-file set: @file.tsk.set('key', value)
        cross_set_match = re.match(r'^@([a-zA-Z0-9_-]+)\.tsk\.set\(["\']([^"\']*)["\'],\s*(.+)\)$', value)
        if cross_set_match:
            file_name = cross_set_match.group(1)
            key = cross_set_match.group(2)
            val = cross_set_match.group(3)
            return self.cross_file_set(file_name, key, val)
        
        # @query function
        query_match = re.match(r'^@query\(["\'](.*)["\'](.*)\)$', value)
        if query_match:
            query = query_match.group(1)
            return self.execute_query(query)
        
        # @ operators
        operator_match = re.match(r'^@([a-zA-Z_][a-zA-Z0-9_]*)\((.+)\)$', value)
        if operator_match:
            operator = operator_match.group(1)
            params = operator_match.group(2)
            return self.execute_operator(operator, params)
        
        # String concatenation
        if ' + ' in value:
            parts = value.split(' + ')
            result = ""
            for part in parts:
                part = part.strip().strip('"\'')
                parsed_part = self.parse_value(part) if not part.startswith('"') else part[1:-1]
                result += str(parsed_part)
            return result
        
        # Conditional/ternary: condition ? true_val : false_val
        ternary_match = re.match(r'(.+?)\s*\?\s*(.+?)\s*:\s*(.+)', value)
        if ternary_match:
            condition = ternary_match.group(1).strip()
            true_val = ternary_match.group(2).strip()
            false_val = ternary_match.group(3).strip()
            
            if self.evaluate_condition(condition):
                return self.parse_value(true_val)
            else:
                return self.parse_value(false_val)
        
        # Remove quotes from strings
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
        
        # Return as-is
        return value
    
    def parse_array(self, value: str) -> List[Any]:
        """Parse array syntax"""
        content = value[1:-1].strip()
        if not content:
            return []
        
        items = []
        current = ""
        depth = 0
        in_string = False
        quote_char = None
        
        for char in content:
            if char in ['"', "'"] and not in_string:
                in_string = True
                quote_char = char
            elif char == quote_char and in_string:
                in_string = False
                quote_char = None
            
            if not in_string:
                if char in '[{':
                    depth += 1
                elif char in ']}':
                    depth -= 1
                elif char == ',' and depth == 0:
                    items.append(self.parse_value(current.strip()))
                    current = ""
                    continue
            
            current += char
        
        if current.strip():
            items.append(self.parse_value(current.strip()))
        
        return items
    
    def parse_object(self, value: str) -> Dict[str, Any]:
        """Parse object syntax"""
        content = value[1:-1].strip()
        if not content:
            return {}
        
        pairs = []
        current = ""
        depth = 0
        in_string = False
        quote_char = None
        
        for char in content:
            if char in ['"', "'"] and not in_string:
                in_string = True
                quote_char = char
            elif char == quote_char and in_string:
                in_string = False
                quote_char = None
            
            if not in_string:
                if char in '[{':
                    depth += 1
                elif char in ']}':
                    depth -= 1
                elif char == ',' and depth == 0:
                    pairs.append(current.strip())
                    current = ""
                    continue
            
            current += char
        
        if current.strip():
            pairs.append(current.strip())
        
        obj = {}
        for pair in pairs:
            if ':' in pair:
                key, val = pair.split(':', 1)
                key = key.strip().strip('"\'')
                val = val.strip()
                obj[key] = self.parse_value(val)
            elif '=' in pair:
                key, val = pair.split('=', 1)
                key = key.strip().strip('"\'')
                val = val.strip()
                obj[key] = self.parse_value(val)
        
        return obj
    
    def evaluate_condition(self, condition: str) -> bool:
        """Evaluate conditions for ternary expressions"""
        condition = condition.strip()
        
        # Simple equality check
        eq_match = re.match(r'(.+?)\s*==\s*(.+)', condition)
        if eq_match:
            left = self.parse_value(eq_match.group(1).strip())
            right = self.parse_value(eq_match.group(2).strip())
            return str(left) == str(right)
        
        # Not equal
        ne_match = re.match(r'(.+?)\s*!=\s*(.+)', condition)
        if ne_match:
            left = self.parse_value(ne_match.group(1).strip())
            right = self.parse_value(ne_match.group(2).strip())
            return str(left) != str(right)
        
        # Greater than
        gt_match = re.match(r'(.+?)\s*>\s*(.+)', condition)
        if gt_match:
            left = self.parse_value(gt_match.group(1).strip())
            right = self.parse_value(gt_match.group(2).strip())
            try:
                return float(left) > float(right)
            except:
                return str(left) > str(right)
        
        # Default: check if truthy
        value = self.parse_value(condition)
        return bool(value) and value not in [False, None, 0, '0', 'false', 'null']
    
    def cross_file_get(self, file_name: str, key: str) -> Any:
        """Get value from another TSK file"""
        cache_key = f"{file_name}:{key}"
        
        # Check cache
        if cache_key in self.cross_file_cache:
            return self.cross_file_cache[cache_key]
        
        # Find file
        file_path = None
        for directory in ['.', './config', '..', '../config']:
            potential_path = Path(directory) / f"{file_name}.tsk"
            if potential_path.exists():
                file_path = str(potential_path)
                break
        
        if not file_path:
            return ""
        
        # Parse file and get value
        temp_parser = TuskLangEnhanced()
        temp_parser.parse_file(file_path)
        
        value = temp_parser.data.get(key, "")
        
        # Cache result
        self.cross_file_cache[cache_key] = value
        
        return value
    
    def cross_file_set(self, file_name: str, key: str, value: str) -> Any:
        """Set value in another TSK file (cache only for now)"""
        cache_key = f"{file_name}:{key}"
        parsed_value = self.parse_value(value)
        self.cross_file_cache[cache_key] = parsed_value
        return parsed_value
    
    def execute_date(self, format_str: str) -> str:
        """Execute @date function"""
        now = datetime.now()
        
        # Convert PHP-style format to Python
        format_map = {
            'Y': '%Y',  # 4-digit year
            'Y-m-d': '%Y-%m-%d',
            'Y-m-d H:i:s': '%Y-%m-%d %H:%M:%S',
            'c': '%Y-%m-%dT%H:%M:%S%z'
        }
        
        if format_str in format_map:
            return now.strftime(format_map[format_str])
        else:
            return now.strftime('%Y-%m-%d %H:%M:%S')
    
    def execute_query(self, query: str) -> Any:
        """Execute database query using appropriate adapter"""
        self.load_peanut()
        
        # Determine database type
        db_type = self.data.get('database.default', 'sqlite')
        
        try:
            # Import adapters (delayed to avoid circular imports)
            from adapters import get_adapter, load_adapter_from_peanut
            
            # Load appropriate adapter
            adapter = load_adapter_from_peanut(db_type)
            
            # Execute query
            return adapter.query(query)
            
        except Exception as e:
            # Fallback to placeholder if adapters not available
            return f"[Query: {query} on {db_type}] - Error: {str(e)}"
    
    def execute_operator(self, operator: str, params: str) -> Any:
        """Execute @ operators"""
        if operator == 'cache':
            # Simple cache implementation
            parts = params.split(',', 1)
            if len(parts) == 2:
                ttl = parts[0].strip().strip('"\'')
                value = parts[1].strip()
                parsed_value = self.parse_value(value)
                return parsed_value
            return ""
        elif operator in ['learn', 'optimize', 'metrics', 'feature']:
            # Placeholders for advanced features
            return f"@{operator}({params})"
        else:
            return f"@{operator}({params})"
    
    def parse_line(self, line: str):
        """Parse a single line"""
        trimmed = line.strip()
        
        # Skip empty lines and comments
        if not trimmed or trimmed.startswith('#'):
            return
        
        # Remove optional semicolon
        if trimmed.endswith(';'):
            trimmed = trimmed[:-1].strip()
        
        # Check for section declaration []
        section_match = re.match(r'^\[([a-zA-Z_][a-zA-Z0-9_]*)\]$', trimmed)
        if section_match:
            self.current_section = section_match.group(1)
            self.in_object = False
            return
        
        # Check for angle bracket object >
        angle_open_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*>$', trimmed)
        if angle_open_match:
            self.in_object = True
            self.object_key = angle_open_match.group(1)
            return
        
        # Check for closing angle bracket <
        if trimmed == '<':
            self.in_object = False
            self.object_key = ""
            return
        
        # Check for curly brace object {
        brace_open_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*\{$', trimmed)
        if brace_open_match:
            self.in_object = True
            self.object_key = brace_open_match.group(1)
            return
        
        # Check for closing curly brace }
        if trimmed == '}':
            self.in_object = False
            self.object_key = ""
            return
        
        # Parse key-value pairs (both : and = supported)
        kv_match = re.match(r'^([\$]?[a-zA-Z_][a-zA-Z0-9_-]*)\s*[:=]\s*(.+)$', trimmed)
        if kv_match:
            key = kv_match.group(1)
            value = kv_match.group(2)
            parsed_value = self.parse_value(value)
            
            # Determine storage location
            if self.in_object and self.object_key:
                if self.current_section:
                    storage_key = f"{self.current_section}.{self.object_key}.{key}"
                else:
                    storage_key = f"{self.object_key}.{key}"
            elif self.current_section:
                storage_key = f"{self.current_section}.{key}"
            else:
                storage_key = key
            
            # Store the value
            self.data[storage_key] = parsed_value
            
            # Handle global variables
            if key.startswith('$'):
                var_name = key[1:]
                self.global_variables[var_name] = parsed_value
            elif self.current_section and not key.startswith('$'):
                # Store section-local variable
                section_key = f"{self.current_section}.{key}"
                self.section_variables[section_key] = parsed_value
    
    def parse(self, content: str) -> Dict[str, Any]:
        """Parse TuskLang content"""
        lines = content.split('\n')
        
        for line in lines:
            self.parse_line(line)
        
        return self.data
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a TSK file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self.parse(content)
    
    def get(self, key: str) -> Any:
        """Get a value by key"""
        return self.data.get(key, None)
    
    def set(self, key: str, value: Any):
        """Set a value"""
        self.data[key] = value
    
    def keys(self) -> List[str]:
        """Get all keys"""
        return sorted(self.data.keys())
    
    def items(self) -> List[Tuple[str, Any]]:
        """Get all key-value pairs"""
        return [(key, self.data[key]) for key in self.keys()]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.data.copy()


def parse(content: str) -> Dict[str, Any]:
    """Parse TuskLang content with enhanced syntax"""
    parser = TuskLangEnhanced()
    return parser.parse(content)


def parse_file(file_path: str) -> Dict[str, Any]:
    """Parse a TuskLang file with enhanced syntax"""
    parser = TuskLangEnhanced()
    return parser.parse_file(file_path)


def load_from_peanut():
    """Load configuration from peanut.tsk"""
    parser = TuskLangEnhanced()
    parser.load_peanut()
    return parser


# CLI interface
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("""
TuskLang Enhanced for Python - The Freedom Parser
=================================================

Usage: python tsk_enhanced.py [command] [options]

Commands:
    parse <file>     Parse a .tsk file
    get <file> <key> Get a value by key
    keys <file>      List all keys
    peanut           Load from peanut.tsk
    
Examples:
    python tsk_enhanced.py parse config.tsk
    python tsk_enhanced.py get config.tsk database.host
    python tsk_enhanced.py keys config.tsk
    python tsk_enhanced.py peanut

Features:
    - Multiple syntax styles: [], {}, <>
    - Global variables with $
    - Cross-file references: @file.tsk.get()
    - Database queries: @query()
    - Date functions: @date()
    - Environment variables: @env()

Default config file: peanut.tsk
""")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'parse':
        if len(sys.argv) < 3:
            print("Error: File path required")
            sys.exit(1)
        
        parser = TuskLangEnhanced()
        data = parser.parse_file(sys.argv[2])
        
        for key, value in parser.items():
            print(f"{key} = {value}")
    
    elif command == 'get':
        if len(sys.argv) < 4:
            print("Error: File path and key required")
            sys.exit(1)
        
        parser = TuskLangEnhanced()
        parser.parse_file(sys.argv[2])
        value = parser.get(sys.argv[3])
        print(value if value is not None else "")
    
    elif command == 'keys':
        if len(sys.argv) < 3:
            print("Error: File path required")
            sys.exit(1)
        
        parser = TuskLangEnhanced()
        parser.parse_file(sys.argv[2])
        
        for key in parser.keys():
            print(key)
    
    elif command == 'peanut':
        parser = load_from_peanut()
        print(f"Loaded {len(parser.data)} configuration items")
        
        for key, value in parser.items():
            print(f"{key} = {value}")
    
    else:
        print(f"Error: Unknown command: {command}")
        sys.exit(1)