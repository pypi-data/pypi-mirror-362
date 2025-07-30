#!/usr/bin/env python3
"""
TSK (TuskLang Configuration) Parser and Generator for Python
Enhanced with flexible syntax support and peanut.tsk integration

Features:
- Multiple syntax styles: [], {}, <>
- $global and section-local variables  
- Cross-file communication
- Database queries via adapters
- peanut.tsk universal config
"""

import re
import json
import struct
import gzip
import hashlib
import time
import os
from pathlib import Path
from typing import Any, Dict, List, Union, Callable, Optional, Tuple
from datetime import datetime


class ShellStorage:
    """Shell format storage for binary data"""
    MAGIC = b'FLEX'
    VERSION = 1
    
    @staticmethod
    def pack(data: Dict[str, Any]) -> bytes:
        """Pack data into Shell binary format"""
        # Compress data if it's not already compressed
        if isinstance(data['data'], str):
            compressed_data = gzip.compress(data['data'].encode('utf-8'))
        elif isinstance(data['data'], bytes):
            compressed_data = gzip.compress(data['data'])
        else:
            compressed_data = gzip.compress(str(data['data']).encode('utf-8'))
        
        id_bytes = data['id'].encode('utf-8')
        
        # Build binary format
        # Magic (4) + Version (1) + ID Length (4) + ID + Data Length (4) + Data
        header = ShellStorage.MAGIC
        header += struct.pack('B', ShellStorage.VERSION)
        header += struct.pack('>I', len(id_bytes))
        header += id_bytes
        header += struct.pack('>I', len(compressed_data))
        
        return header + compressed_data
    
    @staticmethod
    def unpack(shell_data: bytes) -> Dict[str, Any]:
        """Unpack Shell binary format"""
        offset = 0
        
        # Check magic bytes
        magic = shell_data[offset:offset+4]
        if magic != ShellStorage.MAGIC:
            raise ValueError('Invalid shell format')
        offset += 4
        
        # Read version
        version = struct.unpack('B', shell_data[offset:offset+1])[0]
        offset += 1
        
        # Read ID
        id_length = struct.unpack('>I', shell_data[offset:offset+4])[0]
        offset += 4
        storage_id = shell_data[offset:offset+id_length].decode('utf-8')
        offset += id_length
        
        # Read data
        data_length = struct.unpack('>I', shell_data[offset:offset+4])[0]
        offset += 4
        compressed_data = shell_data[offset:offset+data_length]
        
        # Decompress
        data = gzip.decompress(compressed_data).decode('utf-8')
        
        return {
            'version': version,
            'id': storage_id,
            'data': data
        }


class TSKParser:
    """Parse and generate TSK format files"""
    
    def __init__(self):
        self.global_variables = {}
        self.section_variables = {}
        self.cross_file_cache = {}
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
    
    @staticmethod
    def parse(content: str) -> Dict[str, Any]:
        """Parse TSK content into Python dictionary"""
        parser = TSKParser()
        # Load peanut.tsk first if available
        try:
            parser.load_peanut()
        except:
            pass  # Ignore errors loading peanut.tsk
        data, _ = parser.parse_with_comments(content)
        return data
    
    def load_peanut(self) -> None:
        """Load peanut.tsk if available"""
        if self.peanut_loaded:
            return
            
        # Mark as loaded first to prevent recursion
        self.peanut_loaded = True
            
        for location in self.peanut_locations:
            if location and Path(location).exists():
                print(f"# Loading universal config from: {location}")
                try:
                    with open(location, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # Use basic parsing to avoid recursion
                    self._parse_peanut_basic(content)
                    return
                except Exception as e:
                    print(f"# Warning: Could not load {location}: {e}")
                    continue
    
    def _parse_peanut_basic(self, content: str) -> None:
        """Basic parsing for peanut.tsk to avoid recursion"""
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            trimmed = line.strip()
            if not trimmed or trimmed.startswith('#'):
                continue
                
            # Section headers
            section_match = re.match(r'^\[([^\]]+)\]$', trimmed)
            if section_match:
                current_section = section_match.group(1)
                continue
            
            # Key-value pairs with basic parsing only
            if current_section and ('=' in trimmed or ':' in trimmed):
                separator = '=' if '=' in trimmed else ':'
                key, value = trimmed.split(separator, 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                
                # Store in section variables for reference
                section_key = f"{current_section}.{key}"
                self.section_variables[section_key] = value
    
    def parse_with_comments(self, content: str) -> Tuple[Dict[str, Any], Dict[int, str]]:
        """Parse TSK content into Python dictionary with enhanced syntax"""
        lines = content.split('\n')
        result = {}
        comments = {}
        current_section = None
        in_multiline_string = False
        multiline_key = None
        multiline_content = []
        in_object = False
        object_key = ""
        
        for i, line in enumerate(lines):
            trimmed_line = line.strip()
            
            # Handle multiline strings
            if in_multiline_string:
                if trimmed_line == '"""':
                    if current_section and multiline_key:
                        result[current_section][multiline_key] = '\n'.join(multiline_content)
                    in_multiline_string = False
                    multiline_key = None
                    multiline_content = []
                    continue
                multiline_content.append(line)
                continue
            
            # Capture comments
            if trimmed_line.startswith('#'):
                comments[i] = trimmed_line
                continue
            
            # Skip empty lines
            if not trimmed_line:
                continue
            
            # Section header []
            section_match = re.match(r'^\[([a-zA-Z_][a-zA-Z0-9_]*)\]$', trimmed_line)
            if section_match:
                current_section = section_match.group(1)
                result[current_section] = {}
                in_object = False
                continue
            
            # Angle bracket object >
            angle_open_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*>$', trimmed_line)
            if angle_open_match:
                in_object = True
                object_key = angle_open_match.group(1)
                continue
            
            # Closing angle bracket <
            if trimmed_line == '<':
                in_object = False
                object_key = ""
                continue
            
            # Curly brace object {
            brace_open_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*\{$', trimmed_line)
            if brace_open_match:
                in_object = True
                object_key = brace_open_match.group(1)
                continue
            
            # Closing curly brace }
            if trimmed_line == '}':
                in_object = False
                object_key = ""
                continue
            
            # Key-value pair (both : and = supported)
            kv_match = re.match(r'^([\$]?[a-zA-Z_][a-zA-Z0-9_-]*)\s*[:=]\s*(.+)$', trimmed_line)
            if kv_match:
                key = kv_match.group(1)
                value_str = kv_match.group(2)
                
                # Remove optional semicolon
                if value_str.endswith(';'):
                    value_str = value_str[:-1].strip()
                
                # Check for multiline string start
                if value_str == '"""':
                    in_multiline_string = True
                    multiline_key = key
                    continue
                
                value = self._parse_value_enhanced(value_str, current_section)
                
                # Determine storage location
                if in_object and object_key:
                    if current_section:
                        storage_key = f"{current_section}.{object_key}.{key}"
                        if current_section not in result:
                            result[current_section] = {}
                        if object_key not in result[current_section]:
                            result[current_section][object_key] = {}
                        result[current_section][object_key][key] = value
                    else:
                        if object_key not in result:
                            result[object_key] = {}
                        result[object_key][key] = value
                elif current_section:
                    if current_section not in result:
                        result[current_section] = {}
                    result[current_section][key] = value
                else:
                    result[key] = value
                
                # Handle global variables
                if key.startswith('$'):
                    var_name = key[1:]
                    self.global_variables[var_name] = value
                elif current_section and not key.startswith('$'):
                    # Store section-local variable
                    section_key = f"{current_section}.{key}"
                    self.section_variables[section_key] = value
        
        return result, comments
    
    def _parse_value_enhanced(self, value_str: str, current_section: str = "") -> Any:
        """Parse a TSK value string with enhanced syntax support"""
        # Note: peanut.tsk loading is done at the class level, not during value parsing
        
        value = value_str.strip()
        
        # $variable references (global)
        if re.match(r'^\$([a-zA-Z_][a-zA-Z0-9_]*)$', value):
            var_name = value[1:]
            return self.global_variables.get(var_name, '')
        
        # Section-local variable references
        if current_section and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', value):
            section_key = f"{current_section}.{value}"
            if section_key in self.section_variables:
                return self.section_variables[section_key]
        
        # @date function with format
        date_match = re.match(r'^@date\(["\'](.*)["\'\)]$', value)
        if date_match:
            format_str = date_match.group(1)
            return self._execute_date(format_str)
        
        # @env function with default
        env_match = re.match(r'^@env\(["\']([^"\']*)["\'\](?:,\s*(.+))?\)$', value)
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
        
        # Cross-file references: @file.tsk.get('key')
        cross_get_match = re.match(r'^@([a-zA-Z0-9_-]+)\.tsk\.get\(["\'](.*)["\'\)]$', value)
        if cross_get_match:
            file_name = cross_get_match.group(1)
            key = cross_get_match.group(2)
            return self._cross_file_get(file_name, key)
        
        # Conditional/ternary: condition ? true_val : false_val
        ternary_match = re.match(r'(.+?)\s*\?\s*(.+?)\s*:\s*(.+)', value)
        if ternary_match:
            condition = ternary_match.group(1).strip()
            true_val = ternary_match.group(2).strip()
            false_val = ternary_match.group(3).strip()
            
            if self._evaluate_condition(condition, current_section):
                return self._parse_value_enhanced(true_val, current_section)
            else:
                return self._parse_value_enhanced(false_val, current_section)
        
        # Fall back to original parsing
        return self._parse_value(value_str)
    
    def _execute_date(self, format_str: str) -> str:
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
    
    def _cross_file_get(self, file_name: str, key: str) -> Any:
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
        temp_parser = TSKParser()
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        data, _ = temp_parser.parse_with_comments(content)
        
        # Navigate to key
        keys = key.split('.')
        value = data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                value = ""
                break
        
        # Cache result
        self.cross_file_cache[cache_key] = value
        
        return value
    
    def _evaluate_condition(self, condition: str, current_section: str = "") -> bool:
        """Evaluate conditions for ternary expressions"""
        condition = condition.strip()
        
        # Simple equality check
        eq_match = re.match(r'(.+?)\s*==\s*(.+)', condition)
        if eq_match:
            left = self._parse_value_enhanced(eq_match.group(1).strip(), current_section)
            right = self._parse_value_enhanced(eq_match.group(2).strip(), current_section)
            return str(left) == str(right)
        
        # Not equal
        ne_match = re.match(r'(.+?)\s*!=\s*(.+)', condition)
        if ne_match:
            left = self._parse_value_enhanced(ne_match.group(1).strip(), current_section)
            right = self._parse_value_enhanced(ne_match.group(2).strip(), current_section)
            return str(left) != str(right)
        
        # Greater than
        gt_match = re.match(r'(.+?)\s*>\s*(.+)', condition)
        if gt_match:
            left = self._parse_value_enhanced(gt_match.group(1).strip(), current_section)
            right = self._parse_value_enhanced(gt_match.group(2).strip(), current_section)
            try:
                return float(left) > float(right)
            except:
                return str(left) > str(right)
        
        # Default: check if truthy
        value = self._parse_value_enhanced(condition, current_section)
        return bool(value) and value not in [False, None, 0, '0', 'false', 'null']
    
    @staticmethod
    def _parse_value(value_str: str) -> Any:
        """Parse a TSK value string into appropriate Python type (original method)"""
        # Null
        if value_str == 'null':
            return None
        
        # Boolean
        if value_str == 'true':
            return True
        if value_str == 'false':
            return False
        
        # Number
        if re.match(r'^-?\d+$', value_str):
            return int(value_str)
        if re.match(r'^-?\d+\.\d+$', value_str):
            return float(value_str)
        
        # String
        if value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1].replace('\\"', '"').replace('\\\\', '\\')
        
        # Array
        if value_str.startswith('[') and value_str.endswith(']'):
            array_content = value_str[1:-1].strip()
            if not array_content:
                return []
            
            items = TSKParser._split_array_items(array_content)
            return [TSKParser._parse_value(item.strip()) for item in items]
        
        # Object/Dict
        if value_str.startswith('{') and value_str.endswith('}'):
            obj_content = value_str[1:-1].strip()
            if not obj_content:
                return {}
            
            pairs = TSKParser._split_object_pairs(obj_content)
            obj = {}
            
            for pair in pairs:
                if '=' in pair:
                    eq_index = pair.index('=')
                    key = pair[:eq_index].strip()
                    value = pair[eq_index + 1:].strip()
                    # Remove quotes from key if present
                    clean_key = key[1:-1] if key.startswith('"') and key.endswith('"') else key
                    obj[clean_key] = TSKParser._parse_value(value)
            
            return obj
        
        # @ operators (FUJSEN-style)
        # @Query operator: @Query("Users").where("active", true).find()
        if value_str.startswith('@Query('):
            return {'__operator': 'Query', 'expression': value_str}
        
        # @q shorthand: @q("Users").where("active", true).find()
        if value_str.startswith('@q('):
            return {'__operator': 'Query', 'expression': value_str.replace('@q(', '@Query(')}
        
        # @cache operator: @cache("ttl", value)
        if value_str.startswith('@cache('):
            return {'__operator': 'cache', 'expression': value_str}
        
        # @metrics operator: @metrics("name", value)
        if value_str.startswith('@metrics('):
            return {'__operator': 'metrics', 'expression': value_str}
        
        # @if operator: @if(condition, true_val, false_val)
        if value_str.startswith('@if('):
            return {'__operator': 'if', 'expression': value_str}
        
        # @date operator: @date("format")
        if value_str.startswith('@date('):
            return {'__operator': 'date', 'expression': value_str}
        
        # @optimize operator: @optimize("param", initial)
        if value_str.startswith('@optimize('):
            return {'__operator': 'optimize', 'expression': value_str}
        
        # @learn operator: @learn("key", default)
        if value_str.startswith('@learn('):
            return {'__operator': 'learn', 'expression': value_str}
        
        # @feature operator: @feature("name")
        if value_str.startswith('@feature('):
            return {'__operator': 'feature', 'expression': value_str}
        
        # @json operator: @json(data)
        if value_str.startswith('@json('):
            return {'__operator': 'json', 'expression': value_str}
        
        # @request operator: @request or @request.method
        if value_str == '@request' or value_str.startswith('@request.'):
            return {'__operator': 'request', 'expression': value_str}
        
        # env() function: env("VAR_NAME", "default")
        if value_str.startswith('env('):
            return {'__function': 'env', 'expression': value_str}
        
        # php() function: php(expression)
        if value_str.startswith('php('):
            return {'__function': 'php', 'expression': value_str}
        
        # file() function: file("path")
        if value_str.startswith('file('):
            return {'__function': 'file', 'expression': value_str}
        
        # query() function: query("Class").find()
        if value_str.startswith('query('):
            return {'__function': 'query', 'expression': value_str}
        
        # Return as string if no other type matches
        return value_str
    
    @staticmethod
    def _split_array_items(content: str) -> List[str]:
        """Split array items considering nested structures"""
        items = []
        current = ''
        depth = 0
        in_string = False
        
        for i, char in enumerate(content):
            if char == '"' and (i == 0 or content[i - 1] != '\\'):
                in_string = not in_string
            
            if not in_string:
                if char in '[{':
                    depth += 1
                if char in ']}':
                    depth -= 1
                
                if char == ',' and depth == 0:
                    items.append(current.strip())
                    current = ''
                    continue
            
            current += char
        
        if current.strip():
            items.append(current.strip())
        
        return items
    
    @staticmethod
    def _split_object_pairs(content: str) -> List[str]:
        """Split object pairs considering nested structures"""
        pairs = []
        current = ''
        depth = 0
        in_string = False
        
        for i, char in enumerate(content):
            if char == '"' and (i == 0 or content[i - 1] != '\\'):
                in_string = not in_string
            
            if not in_string:
                if char in '[{':
                    depth += 1
                if char in ']}':
                    depth -= 1
                
                if char == ',' and depth == 0:
                    pairs.append(current.strip())
                    current = ''
                    continue
            
            current += char
        
        if current.strip():
            pairs.append(current.strip())
        
        return pairs
    
    @staticmethod
    def stringify(data: Dict[str, Any]) -> str:
        """Generate TSK content from Python dictionary"""
        content = '# Generated by Flexchain TSK Python SDK\n'
        content += f'# {datetime.now().isoformat()}\n\n'
        
        for section, values in data.items():
            content += f'[{section}]\n'
            
            if isinstance(values, dict):
                for key, value in values.items():
                    content += f'{key} = {TSKParser._format_value(value)}\n'
            
            content += '\n'
        
        return content.strip()
    
    @staticmethod
    def _format_value(value: Any) -> str:
        """Format a Python value for TSK"""
        # Null
        if value is None:
            return 'null'
        
        # Boolean
        if isinstance(value, bool):
            return 'true' if value else 'false'
        
        # Number
        if isinstance(value, (int, float)):
            return str(value)
        
        # String
        if isinstance(value, str):
            # Multiline string
            if '\n' in value:
                return '"""\n' + value + '\n"""'
            # Regular string
            return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'
        
        # List
        if isinstance(value, list):
            items = [TSKParser._format_value(item) for item in value]
            return '[ ' + ', '.join(items) + ' ]'
        
        # Dict
        if isinstance(value, dict):
            pairs = []
            for k, v in value.items():
                pairs.append(f'"{k}" = {TSKParser._format_value(v)}')
            return '{ ' + ', '.join(pairs) + ' }'
        
        return '""'


class TSK:
    """Helper class for working with TSK files"""
    
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        self.data = data or {}
        self._fujsen_cache = {}
        self.comments = {}
        self.metadata = {}
        self._parser = None  # Will be set when parsing
    
    @classmethod
    def from_string(cls, content: str) -> 'TSK':
        """Load TSK from string content"""
        parser = TSKParser()
        data, comments = parser.parse_with_comments(content)
        tsk = cls(data)
        tsk.comments = comments
        tsk._parser = parser  # Keep reference to access enhanced features
        return tsk
    
    @classmethod
    def from_file(cls, filepath: str) -> 'TSK':
        """Load TSK from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return cls.from_string(content)
    
    def get_section(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a section"""
        return self.data.get(name)
    
    def get_value(self, section: str, key: str) -> Any:
        """Get a value from a section"""
        return self.data.get(section, {}).get(key)
    
    def set_section(self, name: str, values: Dict[str, Any]) -> None:
        """Set a section"""
        self.data[name] = values
    
    def set_value(self, section: str, key: str, value: Any) -> None:
        """Set a value in a section"""
        if section not in self.data:
            self.data[section] = {}
        self.data[section][key] = value
    
    def to_string(self) -> str:
        """Convert to string"""
        return TSKParser.stringify(self.data)
    
    def to_file(self, filepath: str) -> None:
        """Save to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_string())
    
    def to_dict(self) -> Dict[str, Any]:
        """Get raw data as dictionary"""
        return self.data
    
    def execute_fujsen(self, section: str, key: str = 'fujsen', *args, **kwargs) -> Any:
        """Execute a fujsen (serialized function) from the TSK data"""
        fujsen_code = self.get_value(section, key)
        
        if not fujsen_code or not isinstance(fujsen_code, str):
            raise ValueError(f"No fujsen found at {section}.{key}")
        
        # Check cache first
        cache_key = f"{section}.{key}"
        if cache_key not in self._fujsen_cache:
            # Compile the function
            self._fujsen_cache[cache_key] = self._compile_fujsen(fujsen_code)
        
        fn = self._fujsen_cache[cache_key]
        return fn(*args, **kwargs)
    
    def execute_fujsen_with_context(self, section: str, key: str, context: Dict[str, Any], *args, **kwargs) -> Any:
        """Execute fujsen with custom context"""
        fujsen_code = self.get_value(section, key or 'fujsen')
        
        if not fujsen_code or not isinstance(fujsen_code, str):
            raise ValueError(f"No fujsen found at {section}.{key or 'fujsen'}")
        
        cache_key = f"{section}.{key or 'fujsen'}"
        if cache_key not in self._fujsen_cache:
            self._fujsen_cache[cache_key] = self._compile_fujsen(fujsen_code)
        
        fn = self._fujsen_cache[cache_key]
        
        # Create a wrapper that binds the context
        def bound_fn(*args, **kwargs):
            # Inject context into function's globals
            fn_globals = fn.__globals__.copy()
            fn_globals.update(context)
            
            # Create new function with updated globals
            import types
            bound = types.FunctionType(
                fn.__code__,
                fn_globals,
                fn.__name__,
                fn.__defaults__,
                fn.__closure__
            )
            return bound(*args, **kwargs)
        
        return bound_fn(*args, **kwargs)
    
    def _compile_fujsen(self, code: str) -> Callable:
        """Compile fujsen code into executable function"""
        trimmed_code = code.strip()
        
        # Function declaration pattern
        func_match = re.match(r'^function\s+(\w+)?\s*\((.*?)\)\s*{([\s\S]*)}$', trimmed_code)
        if func_match:
            _, params, body = func_match.groups()
            # Create function string
            param_list = [p.strip() for p in params.split(',') if p.strip()] if params else []
            func_str = f"def _fujsen_func({', '.join(param_list)}):\n"
            # Indent body
            indented_body = '\n'.join('    ' + line for line in body.split('\n'))
            func_str += indented_body
            
            # Execute and return function
            local_scope = {}
            exec(func_str, {'__builtins__': __builtins__}, local_scope)
            return local_scope['_fujsen_func']
        
        # Arrow function pattern (convert JS to Python)
        arrow_match = re.match(r'^\s*\((.*?)\)\s*=>\s*{?([\s\S]*)}?$', trimmed_code)
        if arrow_match:
            params, body = arrow_match.groups()
            param_list = [p.strip() for p in params.split(',') if p.strip()] if params else []
            
            # Convert JS-style code to Python
            py_body = self._js_to_python(body.strip())
            
            if '{' in body:
                # Block body
                func_str = f"def _fujsen_func({', '.join(param_list)}):\n"
                indented_body = '\n'.join('    ' + line for line in py_body.split('\n'))
                func_str += indented_body
            else:
                # Expression body
                func_str = f"lambda {', '.join(param_list)}: {py_body}"
                return eval(func_str)
            
            local_scope = {}
            exec(func_str, {'__builtins__': __builtins__}, local_scope)
            return local_scope['_fujsen_func']
        
        # Try as Python code directly
        try:
            # Try to evaluate as lambda
            if trimmed_code.startswith('lambda'):
                return eval(trimmed_code)
            
            # Try as function definition
            local_scope = {}
            exec(trimmed_code, {'__builtins__': __builtins__}, local_scope)
            # Find the function in local scope
            for value in local_scope.values():
                if callable(value):
                    return value
            
            raise ValueError("No callable found in fujsen code")
        except Exception as e:
            raise ValueError(f"Failed to compile fujsen: {str(e)}")
    
    def _js_to_python(self, js_code: str) -> str:
        """Basic JS to Python conversion for common patterns"""
        py_code = js_code
        
        # Replace common JS patterns with Python equivalents
        replacements = [
            (r'\bconsole\.log\b', 'print'),
            (r'\bconst\b', ''),
            (r'\blet\b', ''),
            (r'\bvar\b', ''),
            (r'\bnew Error\b', 'Exception'),
            (r'\bDate\.now\(\)', 'int(time.time() * 1000)'),
            (r'\btypeof\s+(\w+)\s*===\s*["\']number["\']', 'isinstance(\\1, (int, float))'),
            (r'\btypeof\s+(\w+)\s*!==\s*["\']number["\']', 'not isinstance(\\1, (int, float))'),
            (r'\b(\w+)\.length\b', 'len(\\1)'),
            (r'\bMath\.min\b', 'min'),
            (r'\bMath\.max\b', 'max'),
            (r'\bMath\.floor\b', 'int'),
            (r'\bthrow\b', 'raise'),
            (r'===', '=='),
            (r'!==', '!='),
            (r'\|\|', 'or'),
            (r'&&', 'and'),
            (r'!(\w+)', 'not \\1'),
            (r'`([^`]*)\$\{([^}]+)\}([^`]*)`', r"f'\\1{\\2}\\3'"),  # Template literals
        ]
        
        for pattern, replacement in replacements:
            py_code = re.sub(pattern, replacement, py_code)
        
        # Import time if needed
        if 'time.time()' in py_code:
            py_code = 'import time\n' + py_code
        
        return py_code
    
    def get_fujsen_map(self, section: str) -> Dict[str, Callable]:
        """Get all fujsen functions in a section"""
        section_data = self.get_section(section)
        if not section_data:
            return {}
        
        fujsen_map = {}
        
        for key, value in section_data.items():
            if key == 'fujsen' or key.endswith('_fujsen'):
                try:
                    fujsen_map[key] = self._compile_fujsen(value)
                except Exception as e:
                    print(f"Warning: Failed to compile fujsen at {section}.{key}: {e}")
        
        return fujsen_map
    
    def set_fujsen(self, section: str, key: Optional[str], fn: Callable) -> None:
        """Add a function as fujsen to the TSK data"""
        import inspect
        
        if not callable(fn):
            raise ValueError("Fujsen value must be a callable")
        
        # Get function source
        try:
            fn_source = inspect.getsource(fn).strip()
        except:
            # Fallback for lambdas or built-ins
            fn_source = str(fn)
        
        self.set_value(section, key or 'fujsen', fn_source)
    
    def store_with_shell(self, data: Union[str, bytes], metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Store binary data with TSK metadata and .shell file"""
        storage_id = f"flex_{int(time.time() * 1000)}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"
        
        # Detect type
        content_type = self.detect_type(data)
        size = len(data) if isinstance(data, (str, bytes)) else 0
        
        # Create TSK metadata
        self.set_section('storage', {
            'id': storage_id,
            'type': content_type,
            'size': size,
            'created': int(time.time()),
            'chunks': (size // 65536) + 1  # 64KB chunks
        })
        
        if metadata:
            self.set_section('metadata', metadata)
        
        # Generate hash
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
        else:
            data_bytes = data
        
        data_hash = hashlib.sha256(data_bytes).hexdigest()
        
        self.set_section('verification', {
            'hash': f'sha256:{data_hash}',
            'checksum': 'sha256'
        })
        
        # Pack shell data
        shell_data = ShellStorage.pack({
            'version': 1,
            'type': 'flexchain_storage',
            'id': storage_id,
            'compression': 'gzip',
            'data': data
        })
        
        return {
            'storage_id': storage_id,
            'tsk_data': self.to_string(),
            'shell_data': shell_data,
            'type': content_type,
            'size': size
        }
    
    def retrieve_from_shell(self, shell_data: bytes) -> Dict[str, Any]:
        """Retrieve data from shell storage"""
        unpacked = ShellStorage.unpack(shell_data)
        storage_info = self.get_section('storage')
        
        return {
            'data': unpacked['data'],
            'metadata': self.get_section('metadata'),
            'verification': self.get_section('verification'),
            'storage_info': storage_info
        }
    
    def detect_type(self, data: Union[str, bytes]) -> str:
        """Detect content type from data"""
        if isinstance(data, str):
            return 'text/plain'
        
        # Check magic bytes for common formats
        if len(data) >= 4:
            if data[0:3] == b'\xFF\xD8\xFF':
                return 'image/jpeg'
            elif data[0:4] == b'\x89PNG':
                return 'image/png'
            elif data[0:4] == b'%PDF':
                return 'application/pdf'
            elif data[0:2] == b'PK':
                return 'application/zip'
        
        # Check if it's text
        try:
            data.decode('utf-8')
            return 'text/plain'
        except:
            return 'application/octet-stream'
    
    async def execute_operators(self, value: Any, context: Dict[str, Any] = None) -> Any:
        """Execute @ operators and functions in TSK data"""
        if context is None:
            context = {}
        
        # If it's a dict with __operator or __function, execute it
        if isinstance(value, dict):
            if '__operator' in value:
                return await self.execute_operator(value['__operator'], value['expression'], context)
            if '__function' in value:
                return await self.execute_function(value['__function'], value['expression'], context)
        
        # Recursively process dicts and lists
        if isinstance(value, dict):
            result = {}
            for key, val in value.items():
                result[key] = await self.execute_operators(val, context)
            return result
        elif isinstance(value, list):
            result = []
            for item in value:
                result.append(await self.execute_operators(item, context))
            return result
        
        return value
    
    async def execute_operator(self, operator: str, expression: str, context: Dict[str, Any]) -> Any:
        """Execute a specific @ operator"""
        if operator == 'Query':
            return await self.execute_query(expression, context)
        elif operator == 'cache':
            return await self.execute_cache(expression, context)
        elif operator == 'metrics':
            return self.execute_metrics(expression, context)
        elif operator == 'if':
            return self.execute_if(expression, context)
        elif operator == 'date':
            return self.execute_date(expression, context)
        elif operator == 'optimize':
            return self.execute_optimize(expression, context)
        elif operator == 'learn':
            return self.execute_learn(expression, context)
        elif operator == 'feature':
            return self.execute_feature(expression, context)
        elif operator == 'json':
            return self.execute_json(expression, context)
        elif operator == 'request':
            return self.execute_request(expression, context)
        else:
            print(f"Warning: Unknown operator: {operator}")
            return expression
    
    async def execute_function(self, func: str, expression: str, context: Dict[str, Any]) -> Any:
        """Execute a function (env, php, file, query)"""
        if func == 'env':
            return self.execute_env(expression, context)
        elif func == 'php':
            # In Python, we can't execute PHP
            return f"[PHP: {expression}]"
        elif func == 'file':
            return await self.execute_file(expression, context)
        elif func == 'query':
            return await self.execute_query(expression, context)
        else:
            print(f"Warning: Unknown function: {func}")
            return expression
    
    async def execute_query(self, expression: str, context: Dict[str, Any]) -> Any:
        """Execute @Query/@q operator"""
        import re
        match = re.match(r'@?[Qq]uery\("([^"]+)"\)(.*)', expression)
        if not match:
            return None
        
        class_name = match.group(1)
        chain_str = match.group(2)
        
        # Try to make API call
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post('/api/tusk/query', json={
                    'className': class_name,
                    'chain': chain_str
                }) as response:
                    if response.status == 200:
                        return await response.json()
        except:
            pass
        
        # Return mock data
        return {
            '__query': class_name,
            '__chain': chain_str,
            '__result': 'Query execution not available in this environment'
        }
    
    async def execute_cache(self, expression: str, context: Dict[str, Any]) -> Any:
        """Execute @cache operator"""
        import re
        match = re.match(r'@cache\("([^"]+)"\s*,\s*(.+)\)', expression)
        if not match:
            return None
        
        ttl = match.group(1)
        value_expr = match.group(2)
        
        # Simple in-memory cache
        cache_key = f"cache_{expression}"
        if not hasattr(self, '_cache'):
            self._cache = {}
        
        cached = self._cache.get(cache_key)
        if cached and cached['expires'] > time.time():
            return cached['value']
        
        # Execute the value expression
        value = await self.execute_operators(TSKParser._parse_value(value_expr), context)
        
        # Store in cache
        ttl_seconds = self.parse_ttl(ttl)
        self._cache[cache_key] = {
            'value': value,
            'expires': time.time() + ttl_seconds
        }
        
        return value
    
    def execute_metrics(self, expression: str, context: Dict[str, Any]) -> float:
        """Execute @metrics operator"""
        import re
        match = re.match(r'@metrics\("([^"]+)"\s*,\s*(.+)\)', expression)
        if not match:
            return 0
        
        name = match.group(1)
        value = float(match.group(2)) if match.group(2).replace('.', '').isdigit() else 1
        
        # Store metric
        if not hasattr(self, '_metrics'):
            self._metrics = {}
        
        if name not in self._metrics:
            self._metrics[name] = 0
        
        self._metrics[name] += value
        return self._metrics[name]
    
    def execute_if(self, expression: str, context: Dict[str, Any]) -> Any:
        """Execute @if operator"""
        import re
        match = re.match(r'@if\((.+?)\s*,\s*(.+?)\s*,\s*(.+)\)', expression)
        if not match:
            return None
        
        condition = match.group(1).strip()
        true_value = match.group(2).strip()
        false_value = match.group(3).strip()
        
        # Evaluate condition
        cond_result = False
        if condition == 'true':
            cond_result = True
        elif condition == 'false':
            cond_result = False
        elif condition.startswith('@'):
            # Variable reference
            var_name = condition[1:]
            cond_result = bool(context.get(var_name))
        else:
            cond_result = bool(condition)
        
        return TSKParser._parse_value(true_value if cond_result else false_value)
    
    def execute_date(self, expression: str, context: Dict[str, Any]) -> str:
        """Execute @date operator"""
        import re
        from datetime import datetime
        
        match = re.match(r'@date\("?([^"\)]+)"?\)', expression)
        if not match:
            return datetime.now().isoformat()
        
        format_str = match.group(1)
        now = datetime.now()
        
        if format_str == 'now':
            return now.strftime('%Y-%m-%d %H:%M:%S')
        
        # Simple format replacements (PHP-style to Python)
        format_map = {
            'Y': '%Y',  # 4-digit year
            'm': '%m',  # 2-digit month
            'd': '%d',  # 2-digit day
            'H': '%H',  # 24-hour format hour
            'i': '%M',  # Minutes
            's': '%S'   # Seconds
        }
        
        py_format = format_str
        for php_fmt, py_fmt in format_map.items():
            py_format = py_format.replace(php_fmt, py_fmt)
        
        try:
            return now.strftime(py_format)
        except:
            return now.strftime('%Y-%m-%d %H:%M:%S')
    
    def execute_env(self, expression: str, context: Dict[str, Any]) -> Optional[str]:
        """Execute env() function"""
        import re
        import os
        
        # Enhanced env() with @env syntax support
        match = re.match(r'@?env\(["\']([^"\']*)["\'\](?:,\s*["\']?([^"\']*)["\'\])?\)', expression)
        if not match:
            return None
        
        var_name = match.group(1)
        default_value = match.group(2)
        
        # Check context first, then environment
        if var_name in context:
            return context[var_name]
        
        return os.environ.get(var_name, default_value)
    
    def parse_ttl(self, ttl: str) -> float:
        """Parse TTL string to seconds"""
        import re
        match = re.match(r'(\d+)([smhd])', ttl)
        if not match:
            return 60  # Default 1 minute
        
        value = int(match.group(1))
        unit = match.group(2)
        
        if unit == 's':
            return value
        elif unit == 'm':
            return value * 60
        elif unit == 'h':
            return value * 3600
        elif unit == 'd':
            return value * 86400
        else:
            return 60
    
    # Placeholder implementations
    def execute_optimize(self, expression: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {'__optimize': expression}
    
    def execute_learn(self, expression: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {'__learn': expression}
    
    def execute_feature(self, expression: str, context: Dict[str, Any]) -> bool:
        import re
        match = re.match(r'@feature\("([^"]+)"\)', expression)
        if not match:
            return False
        
        feature = match.group(1).lower()
        # Check common Python features
        features = {
            'async': True,
            'typing': True,
            'dataclasses': True,
            'pathlib': True,
            'asyncio': True,
            'json': True,
            'sqlite': True
        }
        
        return features.get(feature, False)
    
    def execute_json(self, expression: str, context: Dict[str, Any]) -> str:
        import re
        import json
        
        match = re.match(r'@json\((.+)\)', expression)
        if not match:
            return '{}'
        
        try:
            data = TSKParser._parse_value(match.group(1))
            return json.dumps(data)
        except:
            return '{}'
    
    def execute_request(self, expression: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # In Python, return mock request data
        request = {
            'method': 'GET',
            'path': '/',
            'headers': {}
        }
        
        if expression == '@request':
            return request
        
        import re
        match = re.match(r'@request\.(.+)', expression)
        if match:
            return request.get(match.group(1))
        
        return request
    
    async def execute_file(self, expression: str, context: Dict[str, Any]) -> Optional[str]:
        import re
        match = re.match(r'file\("([^"]+)"\)', expression)
        if not match:
            return None
        
        file_path = match.group(1)
        
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except:
            return f"[File: {file_path}]"


# Convenience functions
def parse(content: str) -> Dict[str, Any]:
    """Parse TSK content"""
    return TSKParser.parse(content)


def stringify(data: Dict[str, Any]) -> str:
    """Generate TSK content"""
    return TSKParser.stringify(data)


def load(filepath: str) -> TSK:
    """Load TSK from file"""
    return TSK.from_file(filepath)


def load_from_peanut() -> TSK:
    """Load configuration from peanut.tsk"""
    parser = TSKParser()
    parser.load_peanut()
    
    # Convert parser data to TSK format
    tsk_data = {}
    for key, value in parser.section_variables.items():
        parts = key.split('.')
        if len(parts) >= 2:
            section = parts[0]
            subkey = '.'.join(parts[1:])
            if section not in tsk_data:
                tsk_data[section] = {}
            tsk_data[section][subkey] = value
    
    tsk = TSK(tsk_data)
    tsk._parser = parser
    return tsk


def save(tsk: TSK, filepath: str) -> None:
    """Save TSK to file"""
    tsk.to_file(filepath)


def parse_with_comments(content: str) -> Tuple[Dict[str, Any], Dict[int, str]]:
    """Parse TSK content and preserve comments"""
    parser = TSKParser()
    return parser.parse_with_comments(content)


def parse_enhanced(content: str) -> Dict[str, Any]:
    """Parse TSK content with enhanced syntax support"""
    parser = TSKParser()
    data, _ = parser.parse_with_comments(content)
    return data


# Example usage
if __name__ == '__main__':
    # Example TSK content
    example_tsk = """
[storage]
id = "flex_123"
type = "image/jpeg"
tags = [ "sunset", "beach" ]

[contract]
name = "PaymentProcessor"
fujsen = \"\"\"
(amount, recipient) => {
  if (amount <= 0) throw new Error("Invalid amount");
  return {
    success: true,
    amount: amount,
    recipient: recipient,
    id: 'tx_' + Date.now()
  };
}
\"\"\"

[validation]
check_amount_fujsen = \"\"\"
lambda amount: isinstance(amount, (int, float)) and 0 < amount <= 1000000
\"\"\"
"""
    
    # Parse and use
    tsk = TSK.from_string(example_tsk)
    print("Storage ID:", tsk.get_value('storage', 'id'))
    print("Tags:", tsk.get_value('storage', 'tags'))
    
    # Execute fujsen
    try:
        result = tsk.execute_fujsen('validation', 'check_amount_fujsen', 100)
        print("Amount valid:", result)
    except Exception as e:
        print("Validation error:", e)