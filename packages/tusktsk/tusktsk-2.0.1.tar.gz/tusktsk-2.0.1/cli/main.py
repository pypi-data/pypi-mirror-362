#!/usr/bin/env python3
"""
TuskLang Python CLI - Main Entry Point
======================================
Complete command-line interface following Universal CLI Command Specification
"""

import sys
import argparse
import json
from typing import Dict, Any, Optional
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tsk import TSK, TSKParser
from tsk_enhanced import TuskLangEnhanced
from peanut_config import PeanutConfig
from adapters import SQLiteAdapter, PostgreSQLAdapter, MongoDBAdapter, RedisAdapter

from cli.commands import (
    db_commands, dev_commands, test_commands, service_commands,
    cache_commands, config_commands, binary_commands
)
from cli.commands import ai_commands, utility_commands, peanuts_commands, css_commands, license_commands
from cli.utils import output_formatter, error_handler, config_loader


class TuskLangCLI:
    """Main CLI class for TuskLang Python SDK"""
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='tsk',
            description='TuskLang Python SDK - Strong. Secure. Scalable.',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  tsk db status                    # Check database connection
  tsk serve 3000                  # Start development server
  tsk test all                    # Run all tests
  tsk config get server.port      # Get configuration value
  tsk binary compile app.tsk      # Compile to binary format
            """
        )
        
        # Global options
        self.parser.add_argument('--version', '-v', action='version', version='TuskLang Python SDK 2.0.0')
        self.parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
        self.parser.add_argument('--quiet', '-q', action='store_true', help='Suppress non-error output')
        self.parser.add_argument('--json', action='store_true', help='Output in JSON format')
        self.parser.add_argument('--config', help='Use alternate config file')
        
        # Create subparsers for commands
        subparsers = self.parser.add_subparsers(dest='command', help='Available commands')
        
        # Add all command categories
        self._add_db_commands(subparsers)
        self._add_dev_commands(subparsers)
        self._add_test_commands(subparsers)
        self._add_service_commands(subparsers)
        self._add_cache_commands(subparsers)
        self._add_config_commands(subparsers)
        self._add_binary_commands(subparsers)
        self._add_peanuts_commands(subparsers)
        self._add_ai_commands(subparsers)
        self._add_css_commands(subparsers)
        self._add_license_commands(subparsers)
        self._add_utility_commands(subparsers)
    
    def _add_db_commands(self, subparsers):
        """Add database commands"""
        db_parser = subparsers.add_parser('db', help='Database operations')
        db_subparsers = db_parser.add_subparsers(dest='db_command', help='Database commands')
        
        # db status
        db_subparsers.add_parser('status', help='Check database connection status')
        
        # db migrate
        migrate_parser = db_subparsers.add_parser('migrate', help='Run migration file')
        migrate_parser.add_argument('file', help='Migration file path')
        
        # db console
        db_subparsers.add_parser('console', help='Open interactive database console')
        
        # db backup
        backup_parser = db_subparsers.add_parser('backup', help='Backup database')
        backup_parser.add_argument('file', nargs='?', help='Backup file path (optional)')
        
        # db restore
        restore_parser = db_subparsers.add_parser('restore', help='Restore from backup file')
        restore_parser.add_argument('file', help='Backup file path')
        
        # db init
        db_subparsers.add_parser('init', help='Initialize SQLite database')
    
    def _add_dev_commands(self, subparsers):
        """Add development commands"""
        dev_parser = subparsers.add_parser('serve', help='Start development server')
        dev_parser.add_argument('port', nargs='?', type=int, default=8080, help='Port number (default: 8080)')
        
        compile_parser = subparsers.add_parser('compile', help='Compile .tsk file')
        compile_parser.add_argument('file', help='TSK file to compile')
        
        optimize_parser = subparsers.add_parser('optimize', help='Optimize .tsk file')
        optimize_parser.add_argument('file', help='TSK file to optimize')
    
    def _add_test_commands(self, subparsers):
        """Add testing commands"""
        test_parser = subparsers.add_parser('test', help='Run tests')
        test_parser.add_argument('suite', nargs='?', help='Test suite to run')
        test_parser.add_argument('--all', action='store_true', help='Run all test suites')
        test_parser.add_argument('--parser', action='store_true', help='Test parser functionality only')
        test_parser.add_argument('--fujsen', action='store_true', help='Test FUJSEN operators only')
        test_parser.add_argument('--sdk', action='store_true', help='Test SDK-specific features')
        test_parser.add_argument('--performance', action='store_true', help='Run performance benchmarks')
    
    def _add_service_commands(self, subparsers):
        """Add service commands"""
        services_parser = subparsers.add_parser('services', help='Service management')
        services_subparsers = services_parser.add_subparsers(dest='service_command', help='Service commands')
        
        services_subparsers.add_parser('start', help='Start all TuskLang services')
        services_subparsers.add_parser('stop', help='Stop all TuskLang services')
        services_subparsers.add_parser('restart', help='Restart all services')
        services_subparsers.add_parser('status', help='Show status of all services')
    
    def _add_cache_commands(self, subparsers):
        """Add cache commands"""
        cache_parser = subparsers.add_parser('cache', help='Cache operations')
        cache_subparsers = cache_parser.add_subparsers(dest='cache_command', help='Cache commands')
        
        cache_subparsers.add_parser('clear', help='Clear all caches')
        cache_subparsers.add_parser('status', help='Show cache status and statistics')
        cache_subparsers.add_parser('warm', help='Pre-warm caches')
        
        # Memcached subcommands
        memcached_parser = cache_subparsers.add_parser('memcached', help='Memcached operations')
        memcached_subparsers = memcached_parser.add_subparsers(dest='memcached_command', help='Memcached commands')
        
        memcached_subparsers.add_parser('status', help='Check Memcached connection status')
        memcached_subparsers.add_parser('stats', help='Show detailed Memcached statistics')
        memcached_subparsers.add_parser('flush', help='Flush all Memcached data')
        memcached_subparsers.add_parser('restart', help='Restart Memcached service')
        memcached_subparsers.add_parser('test', help='Test Memcached connection')
        
        cache_subparsers.add_parser('distributed', help='Show distributed cache status')
    
    def _add_config_commands(self, subparsers):
        """Add configuration commands"""
        config_parser = subparsers.add_parser('config', help='Configuration operations')
        config_subparsers = config_parser.add_subparsers(dest='config_command', help='Configuration commands')
        
        # config get
        get_parser = config_subparsers.add_parser('get', help='Get configuration value by path')
        get_parser.add_argument('key_path', help='Configuration key path')
        get_parser.add_argument('dir', nargs='?', help='Directory to search (optional)')
        
        # config check
        check_parser = config_subparsers.add_parser('check', help='Check configuration hierarchy')
        check_parser.add_argument('path', nargs='?', help='Path to check (optional)')
        
        # config validate
        validate_parser = config_subparsers.add_parser('validate', help='Validate entire configuration chain')
        validate_parser.add_argument('path', nargs='?', help='Path to validate (optional)')
        
        # config compile
        compile_parser = config_subparsers.add_parser('compile', help='Auto-compile all peanu.tsk files')
        compile_parser.add_argument('path', nargs='?', help='Path to compile (optional)')
        
        # config docs
        docs_parser = config_subparsers.add_parser('docs', help='Generate configuration documentation')
        docs_parser.add_argument('path', nargs='?', help='Path for docs (optional)')
        
        # config clear-cache
        clear_cache_parser = config_subparsers.add_parser('clear-cache', help='Clear configuration cache')
        clear_cache_parser.add_argument('path', nargs='?', help='Path to clear cache for (optional)')
        
        # config stats
        config_subparsers.add_parser('stats', help='Show configuration performance statistics')
    
    def _add_binary_commands(self, subparsers):
        """Add binary performance commands"""
        binary_parser = subparsers.add_parser('binary', help='Binary operations')
        binary_subparsers = binary_parser.add_subparsers(dest='binary_command', help='Binary commands')
        
        # binary compile
        compile_parser = binary_subparsers.add_parser('compile', help='Compile to binary format (.tskb)')
        compile_parser.add_argument('file', help='TSK file to compile')
        
        # binary execute
        execute_parser = binary_subparsers.add_parser('execute', help='Execute binary file directly')
        execute_parser.add_argument('file', help='Binary file to execute')
        
        # binary benchmark
        benchmark_parser = binary_subparsers.add_parser('benchmark', help='Compare binary vs text performance')
        benchmark_parser.add_argument('file', help='File to benchmark')
        
        # binary optimize
        optimize_parser = binary_subparsers.add_parser('optimize', help='Optimize binary for production')
        optimize_parser.add_argument('file', help='Binary file to optimize')
    
    def _add_ai_commands(self, subparsers):
        """Add AI commands"""
        ai_parser = subparsers.add_parser('ai', help='AI operations')
        ai_subparsers = ai_parser.add_subparsers(dest='ai_command', help='AI commands')
        
        # ai claude
        claude_parser = ai_subparsers.add_parser('claude', help='Query Claude AI with prompt')
        claude_parser.add_argument('prompt', help='Prompt to send to Claude')
        
        # ai chatgpt
        chatgpt_parser = ai_subparsers.add_parser('chatgpt', help='Query ChatGPT with prompt')
        chatgpt_parser.add_argument('prompt', help='Prompt to send to ChatGPT')
        
        # ai custom
        custom_parser = ai_subparsers.add_parser('custom', help='Query custom AI API endpoint')
        custom_parser.add_argument('api', help='API endpoint')
        custom_parser.add_argument('prompt', help='Prompt to send')
        
        # ai config
        ai_subparsers.add_parser('config', help='Show current AI configuration')
        
        # ai setup
        ai_subparsers.add_parser('setup', help='Interactive AI API key setup')
        
        # ai test
        ai_subparsers.add_parser('test', help='Test all configured AI connections')
        
        # ai complete
        complete_parser = ai_subparsers.add_parser('complete', help='Get AI-powered auto-completion')
        complete_parser.add_argument('file', help='File to complete')
        complete_parser.add_argument('line', nargs='?', type=int, help='Line number (optional)')
        complete_parser.add_argument('column', nargs='?', type=int, help='Column number (optional)')
        
        # ai analyze
        analyze_parser = ai_subparsers.add_parser('analyze', help='Analyze file for errors and improvements')
        analyze_parser.add_argument('file', help='File to analyze')
        
        # ai optimize
        optimize_parser = ai_subparsers.add_parser('optimize', help='Get performance optimization suggestions')
        optimize_parser.add_argument('file', help='File to optimize')
        
        # ai security
        security_parser = ai_subparsers.add_parser('security', help='Scan for security vulnerabilities')
        security_parser.add_argument('file', help='File to scan')
    
    def _add_peanuts_commands(self, subparsers):
        """Add peanuts commands"""
        peanuts_parser = subparsers.add_parser('peanuts', help='Peanut configuration operations')
        peanuts_subparsers = peanuts_parser.add_subparsers(dest='peanuts_command', help='Peanuts commands')
        
        # peanuts compile
        compile_parser = peanuts_subparsers.add_parser('compile', help='Compile .peanuts to binary .pnt format')
        compile_parser.add_argument('file', help='Peanuts file to compile')
        
        # peanuts auto-compile
        auto_compile_parser = peanuts_subparsers.add_parser('auto-compile', help='Auto-compile all .peanuts files')
        auto_compile_parser.add_argument('path', nargs='?', help='Path to compile (optional)')
        
        # peanuts load
        load_parser = peanuts_subparsers.add_parser('load', help='Load and display binary peanuts file')
        load_parser.add_argument('file', help='Binary file to load')
    
    def _add_css_commands(self, subparsers):
        """Add CSS commands"""
        css_parser = subparsers.add_parser('css', help='CSS utilities')
        css_subparsers = css_parser.add_subparsers(dest='css_command', help='CSS commands')
        
        # css expand
        expand_parser = css_subparsers.add_parser('expand', help='Expand CSS shorthand properties')
        expand_parser.add_argument('file', help='CSS file to expand')
        
        # css map
        map_parser = css_subparsers.add_parser('map', help='Generate CSS source maps')
        map_parser.add_argument('file', help='CSS file to map')
    
    def _add_license_commands(self, subparsers):
        """Add license commands"""
        license_parser = subparsers.add_parser('license', help='License management')
        license_subparsers = license_parser.add_subparsers(dest='license_command', help='License commands')
        
        # license check
        license_subparsers.add_parser('check', help='Check license status')
        
        # license activate
        activate_parser = license_subparsers.add_parser('activate', help='Activate license')
        activate_parser.add_argument('key', help='License key')
    
    def _add_utility_commands(self, subparsers):
        """Add utility commands"""
        # parse
        parse_parser = subparsers.add_parser('parse', help='Parse and display TSK file contents')
        parse_parser.add_argument('file', help='TSK file to parse')
        
        # validate
        validate_parser = subparsers.add_parser('validate', help='Validate TSK file syntax')
        validate_parser.add_argument('file', help='TSK file to validate')
        
        # convert
        convert_parser = subparsers.add_parser('convert', help='Convert between formats')
        convert_parser.add_argument('-i', '--input', required=True, help='Input file')
        convert_parser.add_argument('-o', '--output', required=True, help='Output file')
        
        # get
        get_parser = subparsers.add_parser('get', help='Get specific value by key path')
        get_parser.add_argument('file', help='TSK file')
        get_parser.add_argument('key_path', help='Key path')
        
        # set
        set_parser = subparsers.add_parser('set', help='Set value by key path')
        set_parser.add_argument('file', help='TSK file')
        set_parser.add_argument('key_path', help='Key path')
        set_parser.add_argument('value', help='Value to set')
        
        # version
        subparsers.add_parser('version', help='Show version information')
        
        # help
        help_parser = subparsers.add_parser('help', help='Show help for command')
        help_parser.add_argument('command', nargs='?', help='Command to get help for')
    
    def run(self, args=None):
        """Run the CLI with given arguments"""
        if args is None:
            args = sys.argv[1:]
        
        # Handle no arguments (interactive mode)
        if not args:
            return self._interactive_mode()
        
        parsed_args = self.parser.parse_args(args)
        
        # Set global flags
        self.verbose = parsed_args.verbose
        self.quiet = parsed_args.quiet
        self.json_output = parsed_args.json
        self.config_path = parsed_args.config
        
        try:
            # Route to appropriate command handler
            if parsed_args.command == 'db':
                return db_commands.handle_db_command(parsed_args, self)
            elif parsed_args.command == 'serve':
                return dev_commands.handle_serve_command(parsed_args, self)
            elif parsed_args.command == 'compile':
                return dev_commands.handle_compile_command(parsed_args, self)
            elif parsed_args.command == 'optimize':
                return dev_commands.handle_optimize_command(parsed_args, self)
            elif parsed_args.command == 'test':
                return test_commands.handle_test_command(parsed_args, self)
            elif parsed_args.command == 'services':
                return service_commands.handle_service_command(parsed_args, self)
            elif parsed_args.command == 'cache':
                return cache_commands.handle_cache_command(parsed_args, self)
            elif parsed_args.command == 'config':
                return config_commands.handle_config_command(parsed_args, self)
            elif parsed_args.command == 'binary':
                return binary_commands.handle_binary_command(parsed_args, self)
            elif parsed_args.command == 'peanuts':
                return peanuts_commands.handle_peanuts_command(parsed_args, self)
            elif parsed_args.command == 'ai':
                return ai_commands.handle_ai_command(parsed_args, self)
            elif parsed_args.command == 'css':
                return css_commands.handle_css_command(parsed_args, self)
            elif parsed_args.command == 'license':
                return license_commands.handle_license_command(parsed_args, self)
            elif parsed_args.command in ['parse', 'validate', 'convert', 'get', 'set', 'version', 'help']:
                return utility_commands.handle_utility_command(parsed_args, self)
            else:
                self.parser.print_help()
                return 1
                
        except Exception as e:
            return error_handler.handle_error(e, self)
    
    def _interactive_mode(self):
        """Enter interactive REPL mode"""
        print("TuskLang v2.0.0 - Interactive Mode")
        print("Type 'exit' to quit, 'help' for commands")
        
        while True:
            try:
                command = input("tsk> ").strip()
                if command.lower() in ['exit', 'quit']:
                    break
                elif command.lower() == 'help':
                    print("Available commands: db status, serve, test, config get, etc.")
                    continue
                elif not command:
                    continue
                
                # Parse and execute command
                args = command.split()
                result = self.run(args)
                if result != 0:
                    break
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
        
        return 0


def main():
    """Main entry point"""
    cli = TuskLangCLI()
    return cli.run()


if __name__ == '__main__':
    sys.exit(main()) 