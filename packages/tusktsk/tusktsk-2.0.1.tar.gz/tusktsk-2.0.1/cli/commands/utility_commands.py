#!/usr/bin/env python3
"""
TuskLang Python CLI - Utility Commands
======================================
Utility operations for file manipulation and system information
"""

import json
import sys
import time
from typing import Dict, Any, Optional, Union
from pathlib import Path

from ..utils import output_formatter, error_handler, config_loader


def handle_utility_command(args, cli):
    """Handle utility commands"""
    if args.command == 'parse':
        return handle_parse_command(args, cli)
    elif args.command == 'validate':
        return handle_validate_command(args, cli)
    elif args.command == 'convert':
        return handle_convert_command(args, cli)
    elif args.command == 'get':
        return handle_get_command(args, cli)
    elif args.command == 'set':
        return handle_set_command(args, cli)
    elif args.command == 'version':
        return handle_version_command(args, cli)
    elif args.command == 'help':
        return handle_help_command(args, cli)
    else:
        output_formatter.print_error("Unknown utility command")
        return 1


def handle_parse_command(args, cli):
    """Handle parse command"""
    file_path = Path(args.file)
    if not file_path.exists():
        output_formatter.print_error(f"File not found: {args.file}")
        return 1
    
    try:
        # Read file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse using TuskLang parser
        from tsk import TSKParser
        parser = TSKParser()
        
        start_time = time.time()
        parsed_data = parser.parse(content)
        parse_time = time.time() - start_time
        
        # Prepare result
        result = {
            'file': str(file_path),
            'size': len(content),
            'parse_time': round(parse_time, 4),
            'parsed_data': parsed_data,
            'statistics': {
                'lines': len(content.split('\n')),
                'characters': len(content),
                'words': len(content.split()),
                'sections': len(parsed_data) if isinstance(parsed_data, dict) else 0
            }
        }
        
        if cli.json_output:
            output_formatter.print_json(result)
        else:
            print(f"📄 Parsed: {args.file}")
            print(f"   Size: {result['statistics']['characters']} characters")
            print(f"   Lines: {result['statistics']['lines']}")
            print(f"   Parse time: {result['parse_time']}s")
            print(f"   Sections: {result['statistics']['sections']}")
            
            if cli.verbose:
                print(f"\n📋 Parsed Content:")
                print(json.dumps(parsed_data, indent=2))
        
        return 0
        
    except Exception as e:
        output_formatter.print_error(f"Parse error: {str(e)}")
        return 1


def handle_validate_command(args, cli):
    """Handle validate command"""
    file_path = Path(args.file)
    if not file_path.exists():
        output_formatter.print_error(f"File not found: {args.file}")
        return 1
    
    try:
        # Read file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Validate using TuskLang parser
        from tsk import TSKParser
        parser = TSKParser()
        
        start_time = time.time()
        try:
            parsed_data = parser.parse(content)
            parse_time = time.time() - start_time
            is_valid = True
            errors = []
        except Exception as e:
            parse_time = time.time() - start_time
            is_valid = False
            errors = [str(e)]
        
        # Prepare result
        result = {
            'file': str(file_path),
            'valid': is_valid,
            'parse_time': round(parse_time, 4),
            'errors': errors,
            'statistics': {
                'lines': len(content.split('\n')),
                'characters': len(content),
                'words': len(content.split())
            }
        }
        
        if cli.json_output:
            output_formatter.print_json(result)
        else:
            if is_valid:
                print(f"✅ Valid: {args.file}")
                print(f"   Parse time: {result['parse_time']}s")
                print(f"   Lines: {result['statistics']['lines']}")
            else:
                print(f"❌ Invalid: {args.file}")
                print(f"   Errors:")
                for error in errors:
                    print(f"     - {error}")
        
        return 0 if is_valid else 1
        
    except Exception as e:
        output_formatter.print_error(f"Validation error: {str(e)}")
        return 1


def handle_convert_command(args, cli):
    """Handle convert command"""
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        output_formatter.print_error(f"Input file not found: {args.input}")
        return 1
    
    try:
        # Read input file
        with open(input_path, 'r') as f:
            content = f.read()
        
        # Determine conversion type based on file extensions
        input_ext = input_path.suffix.lower()
        output_ext = output_path.suffix.lower()
        
        if input_ext == '.tsk' and output_ext == '.json':
            # TSK to JSON conversion
            from tsk import TSKParser
            parser = TSKParser()
            parsed_data = parser.parse(content)
            
            with open(output_path, 'w') as f:
                json.dump(parsed_data, f, indent=2)
            
            conversion_type = "TSK to JSON"
            
        elif input_ext == '.json' and output_ext == '.tsk':
            # JSON to TSK conversion
            with open(input_path, 'r') as f:
                json_data = json.load(f)
            
            # Convert JSON back to TSK format
            tsk_content = _json_to_tsk(json_data)
            
            with open(output_path, 'w') as f:
                f.write(tsk_content)
            
            conversion_type = "JSON to TSK"
            
        elif input_ext == '.tsk' and output_ext == '.yaml':
            # TSK to YAML conversion
            from tsk import TSKParser
            import yaml
            
            parser = TSKParser()
            parsed_data = parser.parse(content)
            
            with open(output_path, 'w') as f:
                yaml.dump(parsed_data, f, default_flow_style=False)
            
            conversion_type = "TSK to YAML"
            
        elif input_ext == '.yaml' and output_ext == '.tsk':
            # YAML to TSK conversion
            import yaml
            
            with open(input_path, 'r') as f:
                yaml_data = yaml.safe_load(f)
            
            tsk_content = _json_to_tsk(yaml_data)
            
            with open(output_path, 'w') as f:
                f.write(tsk_content)
            
            conversion_type = "YAML to TSK"
            
        else:
            output_formatter.print_error(f"Unsupported conversion: {input_ext} to {output_ext}")
            return 1
        
        # Prepare result
        result = {
            'conversion': conversion_type,
            'input': str(input_path),
            'output': str(output_path),
            'success': True
        }
        
        if cli.json_output:
            output_formatter.print_json(result)
        else:
            print(f"🔄 Converted: {conversion_type}")
            print(f"   Input: {args.input}")
            print(f"   Output: {args.output}")
        
        return 0
        
    except Exception as e:
        output_formatter.print_error(f"Conversion error: {str(e)}")
        return 1


def _json_to_tsk(data: Any, indent: int = 0) -> str:
    """Convert JSON data back to TSK format"""
    if isinstance(data, dict):
        lines = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{'  ' * indent}{key}:")
                lines.append(_json_to_tsk(value, indent + 1))
            else:
                lines.append(f"{'  ' * indent}{key}: {value}")
        return '\n'.join(lines)
    elif isinstance(data, list):
        lines = []
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(_json_to_tsk(item, indent))
            else:
                lines.append(f"{'  ' * indent}- {item}")
        return '\n'.join(lines)
    else:
        return str(data)


def handle_get_command(args, cli):
    """Handle get command"""
    file_path = Path(args.file)
    if not file_path.exists():
        output_formatter.print_error(f"File not found: {args.file}")
        return 1
    
    try:
        # Read and parse file
        with open(file_path, 'r') as f:
            content = f.read()
        
        from tsk import TSKParser
        parser = TSKParser()
        parsed_data = parser.parse(content)
        
        # Navigate to the specified key path
        value = _get_nested_value(parsed_data, args.key_path)
        
        if value is None:
            output_formatter.print_error(f"Key path not found: {args.key_path}")
            return 1
        
        # Prepare result
        result = {
            'file': str(file_path),
            'key_path': args.key_path,
            'value': value,
            'type': type(value).__name__
        }
        
        if cli.json_output:
            output_formatter.print_json(result)
        else:
            print(f"🔍 Value at '{args.key_path}':")
            if isinstance(value, (dict, list)):
                print(json.dumps(value, indent=2))
            else:
                print(f"   {value}")
            print(f"   Type: {result['type']}")
        
        return 0
        
    except Exception as e:
        output_formatter.print_error(f"Get error: {str(e)}")
        return 1


def _get_nested_value(data: Any, key_path: str) -> Any:
    """Get nested value from data using dot notation"""
    keys = key_path.split('.')
    current = data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        elif isinstance(current, list):
            try:
                index = int(key)
                if 0 <= index < len(current):
                    current = current[index]
                else:
                    return None
            except ValueError:
                return None
        else:
            return None
    
    return current


def handle_set_command(args, cli):
    """Handle set command"""
    file_path = Path(args.file)
    if not file_path.exists():
        output_formatter.print_error(f"File not found: {args.file}")
        return 1
    
    try:
        # Read and parse file
        with open(file_path, 'r') as f:
            content = f.read()
        
        from tsk import TSKParser
        parser = TSKParser()
        parsed_data = parser.parse(content)
        
        # Convert value to appropriate type
        value = _parse_value(args.value)
        
        # Set the value at the specified key path
        success = _set_nested_value(parsed_data, args.key_path, value)
        
        if not success:
            output_formatter.print_error(f"Could not set value at key path: {args.key_path}")
            return 1
        
        # Convert back to TSK format and save
        tsk_content = _json_to_tsk(parsed_data)
        
        with open(file_path, 'w') as f:
            f.write(tsk_content)
        
        # Prepare result
        result = {
            'file': str(file_path),
            'key_path': args.key_path,
            'value': value,
            'success': True
        }
        
        if cli.json_output:
            output_formatter.print_json(result)
        else:
            print(f"✏️  Set '{args.key_path}' = {value}")
            print(f"   File: {args.file}")
        
        return 0
        
    except Exception as e:
        output_formatter.print_error(f"Set error: {str(e)}")
        return 1


def _parse_value(value_str: str) -> Any:
    """Parse string value to appropriate type"""
    # Try to parse as JSON first
    try:
        return json.loads(value_str)
    except json.JSONDecodeError:
        pass
    
    # Try to parse as number
    try:
        if '.' in value_str:
            return float(value_str)
        else:
            return int(value_str)
    except ValueError:
        pass
    
    # Try to parse as boolean
    if value_str.lower() in ['true', 'false']:
        return value_str.lower() == 'true'
    
    # Return as string
    return value_str


def _set_nested_value(data: Any, key_path: str, value: Any) -> bool:
    """Set nested value in data using dot notation"""
    keys = key_path.split('.')
    current = data
    
    # Navigate to the parent of the target key
    for i, key in enumerate(keys[:-1]):
        if isinstance(current, dict):
            if key not in current:
                current[key] = {}
            current = current[key]
        elif isinstance(current, list):
            try:
                index = int(key)
                while len(current) <= index:
                    current.append({})
                current = current[index]
            except ValueError:
                return False
        else:
            return False
    
    # Set the value
    final_key = keys[-1]
    if isinstance(current, dict):
        current[final_key] = value
        return True
    elif isinstance(current, list):
        try:
            index = int(final_key)
            while len(current) <= index:
                current.append(None)
            current[index] = value
            return True
        except ValueError:
            return False
    
    return False


def handle_version_command(args, cli):
    """Handle version command"""
    version_info = {
        'version': '2.0.0',
        'python_version': sys.version,
        'platform': sys.platform,
        'architecture': sys.maxsize > 2**32 and '64-bit' or '32-bit'
    }
    
    # Get package versions
    try:
        import tsk
        version_info['tsk_version'] = getattr(tsk, '__version__', 'unknown')
    except ImportError:
        version_info['tsk_version'] = 'not installed'
    
    try:
        import tsk_enhanced
        version_info['tsk_enhanced_version'] = getattr(tsk_enhanced, '__version__', 'unknown')
    except ImportError:
        version_info['tsk_enhanced_version'] = 'not installed'
    
    try:
        import peanut_config
        version_info['peanut_config_version'] = getattr(peanut_config, '__version__', 'unknown')
    except ImportError:
        version_info['peanut_config_version'] = 'not installed'
    
    if cli.json_output:
        output_formatter.print_json(version_info)
    else:
        print("📦 TuskLang Python SDK")
        print(f"   Version: {version_info['version']}")
        print(f"   Python: {version_info['python_version']}")
        print(f"   Platform: {version_info['platform']} ({version_info['architecture']})")
        print(f"\n📚 Package Versions:")
        print(f"   TSK: {version_info['tsk_version']}")
        print(f"   TSK Enhanced: {version_info['tsk_enhanced_version']}")
        print(f"   Peanut Config: {version_info['peanut_config_version']}")
    
    return 0


def handle_help_command(args, cli):
    """Handle help command"""
    if args.command:
        # Show help for specific command
        help_text = _get_command_help(args.command)
        if help_text:
            print(help_text)
        else:
            output_formatter.print_error(f"No help available for command: {args.command}")
            return 1
    else:
        # Show general help
        print("""
🔧 TuskLang Python SDK CLI - Help
=================================

Available Commands:

📊 Database Operations:
  tsk db status                    # Check database connection
  tsk db migrate <file>            # Run migration file
  tsk db console                   # Open interactive database console
  tsk db backup [file]             # Backup database
  tsk db restore <file>            # Restore from backup
  tsk db init                      # Initialize SQLite database

🚀 Development:
  tsk serve [port]                 # Start development server
  tsk compile <file>               # Compile .tsk file
  tsk optimize <file>              # Optimize .tsk file

🧪 Testing:
  tsk test [suite]                 # Run tests
  tsk test --all                   # Run all test suites
  tsk test --parser                # Test parser functionality
  tsk test --fujsen                # Test FUJSEN operators
  tsk test --sdk                   # Test SDK features
  tsk test --performance           # Run performance benchmarks

🔧 Services:
  tsk services start               # Start all services
  tsk services stop                # Stop all services
  tsk services restart             # Restart all services
  tsk services status              # Show service status

💾 Cache:
  tsk cache clear                  # Clear all caches
  tsk cache status                 # Show cache status
  tsk cache warm                   # Pre-warm caches
  tsk cache memcached status       # Check Memcached
  tsk cache memcached stats        # Show Memcached stats

⚙️  Configuration:
  tsk config get <key> [dir]       # Get configuration value
  tsk config check [path]          # Check configuration hierarchy
  tsk config validate [path]       # Validate configuration
  tsk config compile [path]        # Auto-compile peanu.tsk files
  tsk config docs [path]           # Generate documentation
  tsk config clear-cache [path]    # Clear configuration cache
  tsk config stats                 # Show performance statistics

🔢 Binary Operations:
  tsk binary compile <file>        # Compile to binary format
  tsk binary execute <file>        # Execute binary file
  tsk binary benchmark <file>      # Compare performance
  tsk binary optimize <file>       # Optimize binary

🤖 AI Operations:
  tsk ai claude <prompt>           # Query Claude AI
  tsk ai chatgpt <prompt>          # Query ChatGPT
  tsk ai custom <api> <prompt>     # Query custom AI API
  tsk ai config                    # Show AI configuration
  tsk ai setup                     # Interactive AI setup
  tsk ai test                      # Test AI connections
  tsk ai complete <file> [line] [col]  # AI code completion
  tsk ai analyze <file>            # AI code analysis
  tsk ai optimize <file>           # AI performance optimization
  tsk ai security <file>           # AI security scan

🛠️  Utilities:
  tsk parse <file>                 # Parse and display TSK file
  tsk validate <file>              # Validate TSK file syntax
  tsk convert -i <input> -o <output>  # Convert between formats
  tsk get <file> <key_path>        # Get value by key path
  tsk set <file> <key_path> <value>  # Set value by key path
  tsk version                      # Show version information
  tsk help [command]               # Show help

Global Options:
  --verbose, -v                    # Enable verbose output
  --quiet, -q                      # Suppress non-error output
  --json                           # Output in JSON format
  --config <file>                  # Use alternate config file

Examples:
  tsk db status                    # Check database
  tsk serve 3000                   # Start server on port 3000
  tsk test all                     # Run all tests
  tsk config get server.port       # Get server port
  tsk ai claude "Hello world"      # Query Claude
  tsk parse config.tsk             # Parse configuration file
        """)
    
    return 0


def _get_command_help(command: str) -> Optional[str]:
    """Get help text for specific command"""
    help_texts = {
        'db': """
📊 Database Commands
===================

tsk db status                    # Check database connection status
tsk db migrate <file>            # Run migration file
tsk db console                   # Open interactive database console
tsk db backup [file]             # Backup database (optional file path)
tsk db restore <file>            # Restore from backup file
tsk db init                      # Initialize SQLite database

Examples:
  tsk db status                  # Check if database is accessible
  tsk db migrate schema.sql      # Run database migration
  tsk db backup backup.sql       # Create backup file
  tsk db restore backup.sql      # Restore from backup
        """,
        
        'serve': """
🚀 Development Server
====================

tsk serve [port]                 # Start development server

Arguments:
  port                          # Port number (default: 8080)

Examples:
  tsk serve                      # Start server on default port 8080
  tsk serve 3000                 # Start server on port 3000
        """,
        
        'test': """
🧪 Testing Commands
==================

tsk test [suite]                 # Run test suite
tsk test --all                   # Run all test suites
tsk test --parser                # Test parser functionality only
tsk test --fujsen                # Test FUJSEN operators only
tsk test --sdk                   # Test SDK-specific features
tsk test --performance           # Run performance benchmarks

Examples:
  tsk test                       # Run default test suite
  tsk test all                   # Run all tests
  tsk test --parser              # Test parser only
  tsk test --performance         # Run performance tests
        """,
        
        'config': """
⚙️  Configuration Commands
==========================

tsk config get <key_path> [dir]  # Get configuration value by path
tsk config check [path]          # Check configuration hierarchy
tsk config validate [path]       # Validate entire configuration chain
tsk config compile [path]        # Auto-compile all peanu.tsk files
tsk config docs [path]           # Generate configuration documentation
tsk config clear-cache [path]    # Clear configuration cache
tsk config stats                 # Show configuration performance statistics

Examples:
  tsk config get server.port     # Get server port configuration
  tsk config check .             # Check current directory config
  tsk config validate            # Validate all configurations
  tsk config compile             # Compile all peanu.tsk files
        """,
        
        'ai': """
🤖 AI Commands
==============

tsk ai claude <prompt>           # Query Claude AI with prompt
tsk ai chatgpt <prompt>          # Query ChatGPT with prompt
tsk ai custom <api> <prompt>     # Query custom AI API endpoint
tsk ai config                    # Show current AI configuration
tsk ai setup                     # Interactive AI API key setup
tsk ai test                      # Test all configured AI connections
tsk ai complete <file> [line] [col]  # Get AI-powered auto-completion
tsk ai analyze <file>            # Analyze file for errors and improvements
tsk ai optimize <file>           # Get performance optimization suggestions
tsk ai security <file>           # Scan for security vulnerabilities

Examples:
  tsk ai claude "Hello world"    # Query Claude
  tsk ai setup                   # Set up API keys
  tsk ai complete app.tsk 10 5   # Get completion at line 10, column 5
  tsk ai analyze config.tsk      # Analyze configuration file
        """
    }
    
    return help_texts.get(command) 