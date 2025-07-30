#!/usr/bin/env python3
"""
Cache Commands for TuskLang Python CLI
======================================
Implements cache-related commands
"""

import os
import sys
import time
import subprocess
import socket
from pathlib import Path
from typing import Any, Dict, List, Optional

from adapters import RedisAdapter
from ..utils.output_formatter import OutputFormatter
from ..utils.error_handler import ErrorHandler
from ..utils.config_loader import ConfigLoader


def handle_cache_command(args: Any, cli: Any) -> int:
    """Handle cache commands"""
    formatter = OutputFormatter(cli.json_output, cli.quiet, cli.verbose)
    error_handler = ErrorHandler(cli.json_output, cli.verbose)
    
    try:
        if args.cache_command == 'clear':
            return _handle_cache_clear(formatter, error_handler)
        elif args.cache_command == 'status':
            return _handle_cache_status(formatter, error_handler)
        elif args.cache_command == 'warm':
            return _handle_cache_warm(formatter, error_handler)
        elif args.cache_command == 'memcached':
            return _handle_memcached_command(args, formatter, error_handler)
        elif args.cache_command == 'distributed':
            return _handle_distributed_cache(formatter, error_handler)
        else:
            formatter.error("Unknown cache command")
            return ErrorHandler.INVALID_ARGS
            
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_cache_clear(formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle cache clear command"""
    formatter.loading("Clearing all caches...")
    
    try:
        cleared_caches = []
        failed_caches = []
        
        # Clear Redis cache
        try:
            redis_adapter = RedisAdapter()
            redis_adapter.connect()
            redis_adapter.delete('*')  # Clear all keys
            cleared_caches.append('Redis')
        except Exception as e:
            failed_caches.append(f"Redis: {str(e)}")
        
        # Clear file system cache
        try:
            cache_dirs = [
                Path('.cache'),
                Path('.tsk_cache'),
                Path('cache'),
                Path.home() / '.cache' / 'tusklang'
            ]
            
            for cache_dir in cache_dirs:
                if cache_dir.exists():
                    import shutil
                    shutil.rmtree(cache_dir)
                    cleared_caches.append(f"File cache ({cache_dir})")
        except Exception as e:
            failed_caches.append(f"File cache: {str(e)}")
        
        # Clear Python cache
        try:
            import glob
            cache_files = glob.glob('**/__pycache__', recursive=True)
            cache_files.extend(glob.glob('**/*.pyc', recursive=True))
            
            for cache_file in cache_files:
                if os.path.isdir(cache_file):
                    import shutil
                    shutil.rmtree(cache_file)
                else:
                    os.remove(cache_file)
            
            if cache_files:
                cleared_caches.append(f"Python cache ({len(cache_files)} items)")
        except Exception as e:
            failed_caches.append(f"Python cache: {str(e)}")
        
        # Display results
        if cleared_caches:
            formatter.success(f"Cleared {len(cleared_caches)} caches")
            formatter.list_items(cleared_caches, "Cleared Caches")
        
        if failed_caches:
            formatter.warning(f"Failed to clear {len(failed_caches)} caches")
            formatter.list_items(failed_caches, "Failed Caches")
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_cache_status(formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle cache status command"""
    formatter.loading("Checking cache status...")
    
    try:
        cache_status = []
        
        # Check Redis cache
        try:
            redis_adapter = RedisAdapter()
            redis_adapter.connect()
            
            # Get Redis info
            info = redis_adapter.query("INFO")
            if isinstance(info, str):
                # Parse INFO output
                lines = info.split('\n')
                redis_stats = {}
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        redis_stats[key] = value.strip()
                
                cache_status.append([
                    'Redis',
                    '✅ Connected',
                    redis_stats.get('connected_clients', 'N/A'),
                    redis_stats.get('used_memory_human', 'N/A'),
                    redis_stats.get('keyspace_hits', 'N/A')
                ])
            else:
                cache_status.append(['Redis', '✅ Connected', 'N/A', 'N/A', 'N/A'])
        except Exception as e:
            cache_status.append(['Redis', f'❌ Error: {str(e)}', 'N/A', 'N/A', 'N/A'])
        
        # Check file system cache
        try:
            cache_dirs = [
                Path('.cache'),
                Path('.tsk_cache'),
                Path('cache'),
                Path.home() / '.cache' / 'tusklang'
            ]
            
            total_size = 0
            total_files = 0
            
            for cache_dir in cache_dirs:
                if cache_dir.exists():
                    for root, dirs, files in os.walk(cache_dir):
                        for file in files:
                            file_path = Path(root) / file
                            total_size += file_path.stat().st_size
                            total_files += 1
            
            if total_files > 0:
                size_str = f"{total_size / 1024 / 1024:.1f}MB"
                cache_status.append(['File Cache', '✅ Active', total_files, size_str, 'N/A'])
            else:
                cache_status.append(['File Cache', '⚠️ Empty', 0, '0B', 'N/A'])
        except Exception as e:
            cache_status.append(['File Cache', f'❌ Error: {str(e)}', 'N/A', 'N/A', 'N/A'])
        
        # Check Python cache
        try:
            import glob
            pycache_dirs = glob.glob('**/__pycache__', recursive=True)
            pyc_files = glob.glob('**/*.pyc', recursive=True)
            
            if pycache_dirs or pyc_files:
                cache_status.append(['Python Cache', '✅ Active', len(pycache_dirs) + len(pyc_files), 'N/A', 'N/A'])
            else:
                cache_status.append(['Python Cache', '⚠️ Empty', 0, 'N/A', 'N/A'])
        except Exception as e:
            cache_status.append(['Python Cache', f'❌ Error: {str(e)}', 'N/A', 'N/A', 'N/A'])
        
        # Display results
        formatter.table(
            ['Cache Type', 'Status', 'Items', 'Size', 'Hits'],
            cache_status,
            'Cache Status'
        )
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_cache_warm(formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle cache warm command"""
    formatter.loading("Warming caches...")
    
    try:
        warmed_caches = []
        failed_caches = []
        
        # Warm Redis cache
        try:
            redis_adapter = RedisAdapter()
            redis_adapter.connect()
            
            # Add some common cache entries
            warm_data = {
                'config:app': '{"name": "TuskLang", "version": "2.0.0"}',
                'config:database': '{"host": "localhost", "port": 5432}',
                'stats:requests': '0',
                'stats:errors': '0',
                'cache:warmed': str(time.time())
            }
            
            for key, value in warm_data.items():
                redis_adapter.set(key, value, ex=3600)  # 1 hour TTL
            
            warmed_caches.append(f"Redis ({len(warm_data)} items)")
        except Exception as e:
            failed_caches.append(f"Redis: {str(e)}")
        
        # Warm file system cache
        try:
            cache_dir = Path('.tsk_cache')
            cache_dir.mkdir(exist_ok=True)
            
            # Create some cache files
            cache_files = [
                ('config.json', '{"warmed": true, "timestamp": ' + str(time.time()) + '}'),
                ('stats.json', '{"requests": 0, "errors": 0}'),
                ('cache.info', f"Warmed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            ]
            
            for filename, content in cache_files:
                cache_file = cache_dir / filename
                with open(cache_file, 'w') as f:
                    f.write(content)
            
            warmed_caches.append(f"File cache ({len(cache_files)} files)")
        except Exception as e:
            failed_caches.append(f"File cache: {str(e)}")
        
        # Display results
        if warmed_caches:
            formatter.success(f"Warmed {len(warmed_caches)} caches")
            formatter.list_items(warmed_caches, "Warmed Caches")
        
        if failed_caches:
            formatter.warning(f"Failed to warm {len(failed_caches)} caches")
            formatter.list_items(failed_caches, "Failed Caches")
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_memcached_command(args: Any, formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle memcached subcommands"""
    try:
        if args.memcached_command == 'status':
            return _handle_memcached_status(formatter, error_handler)
        elif args.memcached_command == 'stats':
            return _handle_memcached_stats(formatter, error_handler)
        elif args.memcached_command == 'flush':
            return _handle_memcached_flush(formatter, error_handler)
        elif args.memcached_command == 'restart':
            return _handle_memcached_restart(formatter, error_handler)
        elif args.memcached_command == 'test':
            return _handle_memcached_test(formatter, error_handler)
        else:
            formatter.error("Unknown memcached command")
            return ErrorHandler.INVALID_ARGS
            
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_memcached_status(formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle memcached status command"""
    formatter.loading("Checking Memcached connection status...")
    
    try:
        # Try to connect to memcached
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        result = sock.connect_ex(('localhost', 11211))
        sock.close()
        
        if result == 0:
            formatter.success("Memcached is running and accessible")
            return ErrorHandler.SUCCESS
        else:
            formatter.error("Memcached is not accessible")
            return ErrorHandler.CONNECTION_ERROR
            
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_memcached_stats(formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle memcached stats command"""
    formatter.loading("Getting Memcached statistics...")
    
    try:
        # Connect to memcached and get stats
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(('localhost', 11211))
        
        # Send stats command
        sock.send(b'stats\r\n')
        
        # Read response
        response = b''
        while True:
            data = sock.recv(1024)
            if not data:
                break
            response += data
            if b'END\r\n' in response:
                break
        
        sock.close()
        
        # Parse stats
        stats_lines = response.decode('utf-8').split('\r\n')
        stats_data = []
        
        for line in stats_lines:
            if line.startswith('STAT ') and not line.startswith('STAT END'):
                parts = line.split(' ')
                if len(parts) >= 3:
                    stat_name = parts[1]
                    stat_value = parts[2]
                    stats_data.append([stat_name, stat_value])
        
        # Display results
        formatter.table(
            ['Statistic', 'Value'],
            stats_data,
            'Memcached Statistics'
        )
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_memcached_flush(formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle memcached flush command"""
    formatter.loading("Flushing Memcached data...")
    
    try:
        # Connect to memcached and send flush_all command
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(('localhost', 11211))
        
        # Send flush_all command
        sock.send(b'flush_all\r\n')
        
        # Read response
        response = sock.recv(1024).decode('utf-8')
        sock.close()
        
        if 'OK' in response:
            formatter.success("Memcached data flushed successfully")
            return ErrorHandler.SUCCESS
        else:
            formatter.error("Failed to flush Memcached data")
            return ErrorHandler.GENERAL_ERROR
            
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_memcached_restart(formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle memcached restart command"""
    formatter.loading("Restarting Memcached service...")
    
    try:
        # Try to restart memcached using systemctl
        result = subprocess.run(['systemctl', 'restart', 'memcached'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            formatter.success("Memcached service restarted successfully")
            return ErrorHandler.SUCCESS
        else:
            # Try alternative restart methods
            try:
                # Try service command
                result = subprocess.run(['service', 'memcached', 'restart'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    formatter.success("Memcached service restarted successfully")
                    return ErrorHandler.SUCCESS
            except FileNotFoundError:
                pass
            
            formatter.error("Failed to restart Memcached service")
            formatter.info("You may need to restart Memcached manually")
            return ErrorHandler.GENERAL_ERROR
            
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_memcached_test(formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle memcached test command"""
    formatter.loading("Testing Memcached connection...")
    
    try:
        # Test basic operations
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(('localhost', 11211))
        
        # Test set operation
        sock.send(b'set test_key 0 60 11\r\nhello world\r\n')
        response = sock.recv(1024).decode('utf-8')
        
        if 'STORED' not in response:
            raise Exception("Set operation failed")
        
        # Test get operation
        sock.send(b'get test_key\r\n')
        response = sock.recv(1024).decode('utf-8')
        
        if 'hello world' not in response:
            raise Exception("Get operation failed")
        
        # Test delete operation
        sock.send(b'delete test_key\r\n')
        response = sock.recv(1024).decode('utf-8')
        
        sock.close()
        
        formatter.success("Memcached connection test passed")
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        formatter.error(f"Memcached connection test failed: {e}")
        return ErrorHandler.CONNECTION_ERROR


def _handle_distributed_cache(formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle distributed cache command"""
    formatter.loading("Checking distributed cache status...")
    
    try:
        # Check various cache backends
        cache_backends = []
        
        # Check Redis
        try:
            redis_adapter = RedisAdapter()
            redis_adapter.connect()
            cache_backends.append(['Redis', '✅ Available', 'localhost:6379'])
        except Exception:
            cache_backends.append(['Redis', '❌ Unavailable', 'N/A'])
        
        # Check Memcached
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', 11211))
            sock.close()
            
            if result == 0:
                cache_backends.append(['Memcached', '✅ Available', 'localhost:11211'])
            else:
                cache_backends.append(['Memcached', '❌ Unavailable', 'N/A'])
        except Exception:
            cache_backends.append(['Memcached', '❌ Unavailable', 'N/A'])
        
        # Check local file cache
        cache_dirs = [Path('.cache'), Path('.tsk_cache'), Path('cache')]
        local_cache_available = any(cache_dir.exists() for cache_dir in cache_dirs)
        
        if local_cache_available:
            cache_backends.append(['Local File', '✅ Available', 'File System'])
        else:
            cache_backends.append(['Local File', '⚠️ Empty', 'File System'])
        
        # Display results
        formatter.table(
            ['Backend', 'Status', 'Location'],
            cache_backends,
            'Distributed Cache Status'
        )
        
        # Summary
        available_backends = [backend for backend in cache_backends if '✅' in backend[1]]
        if available_backends:
            formatter.success(f"{len(available_backends)} cache backends available")
        else:
            formatter.warning("No cache backends available")
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e) 