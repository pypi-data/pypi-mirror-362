#!/usr/bin/env python3
"""
Service Commands for TuskLang Python CLI
========================================
Implements service management commands
"""

import os
import sys
import time
import subprocess
import signal
import psutil
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..utils.output_formatter import OutputFormatter
from ..utils.error_handler import ErrorHandler
from ..utils.config_loader import ConfigLoader


def handle_service_command(args: Any, cli: Any) -> int:
    """Handle service commands"""
    formatter = OutputFormatter(cli.json_output, cli.quiet, cli.verbose)
    error_handler = ErrorHandler(cli.json_output, cli.verbose)
    
    try:
        if args.service_command == 'start':
            return _handle_service_start(formatter, error_handler)
        elif args.service_command == 'stop':
            return _handle_service_stop(formatter, error_handler)
        elif args.service_command == 'restart':
            return _handle_service_restart(formatter, error_handler)
        elif args.service_command == 'status':
            return _handle_service_status(formatter, error_handler)
        else:
            formatter.error("Unknown service command")
            return ErrorHandler.INVALID_ARGS
            
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_service_start(formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle service start command"""
    formatter.loading("Starting TuskLang services...")
    
    try:
        services = _get_tusklang_services()
        started_services = []
        failed_services = []
        
        for service_name, service_config in services.items():
            try:
                if _start_service(service_name, service_config):
                    started_services.append(service_name)
                else:
                    failed_services.append(service_name)
            except Exception as e:
                failed_services.append(f"{service_name}: {str(e)}")
        
        # Display results
        if started_services:
            formatter.success(f"Started {len(started_services)} services")
            formatter.list_items(started_services, "Started Services")
        
        if failed_services:
            formatter.error(f"Failed to start {len(failed_services)} services")
            formatter.list_items(failed_services, "Failed Services")
            return ErrorHandler.GENERAL_ERROR
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_service_stop(formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle service stop command"""
    formatter.loading("Stopping TuskLang services...")
    
    try:
        services = _get_running_tusklang_services()
        stopped_services = []
        failed_services = []
        
        for service_name, process in services.items():
            try:
                if _stop_service(service_name, process):
                    stopped_services.append(service_name)
                else:
                    failed_services.append(service_name)
            except Exception as e:
                failed_services.append(f"{service_name}: {str(e)}")
        
        # Display results
        if stopped_services:
            formatter.success(f"Stopped {len(stopped_services)} services")
            formatter.list_items(stopped_services, "Stopped Services")
        
        if failed_services:
            formatter.error(f"Failed to stop {len(failed_services)} services")
            formatter.list_items(failed_services, "Failed Services")
            return ErrorHandler.GENERAL_ERROR
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_service_restart(formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle service restart command"""
    formatter.loading("Restarting TuskLang services...")
    
    try:
        # Stop services first
        stop_result = _handle_service_stop(formatter, error_handler)
        if stop_result != ErrorHandler.SUCCESS:
            formatter.warning("Some services failed to stop")
        
        # Wait a moment
        time.sleep(2)
        
        # Start services
        start_result = _handle_service_start(formatter, error_handler)
        if start_result != ErrorHandler.SUCCESS:
            formatter.error("Some services failed to start")
            return ErrorHandler.GENERAL_ERROR
        
        formatter.success("All services restarted successfully")
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_service_status(formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle service status command"""
    formatter.loading("Checking TuskLang service status...")
    
    try:
        services = _get_tusklang_services()
        running_services = _get_running_tusklang_services()
        
        status_results = []
        
        for service_name, service_config in services.items():
            if service_name in running_services:
                process = running_services[service_name]
                status = "✅ Running"
                pid = process.pid
                uptime = _get_process_uptime(process)
                memory = _get_process_memory(process)
                status_results.append([service_name, status, pid, uptime, memory])
            else:
                status_results.append([service_name, "❌ Stopped", "N/A", "N/A", "N/A"])
        
        # Display results
        formatter.table(
            ['Service', 'Status', 'PID', 'Uptime', 'Memory'],
            status_results,
            'TuskLang Service Status'
        )
        
        # Summary
        running_count = len(running_services)
        total_count = len(services)
        
        if running_count == total_count:
            formatter.success(f"All {total_count} services are running")
        elif running_count > 0:
            formatter.warning(f"{running_count}/{total_count} services are running")
        else:
            formatter.error("No services are running")
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _get_tusklang_services() -> Dict[str, Dict[str, Any]]:
    """Get list of TuskLang services"""
    return {
        'tusklang-api': {
            'command': 'python -m tsk.api',
            'port': 8080,
            'description': 'TuskLang API Server'
        },
        'tusklang-worker': {
            'command': 'python -m tsk.worker',
            'port': None,
            'description': 'TuskLang Background Worker'
        },
        'tusklang-cache': {
            'command': 'python -m tsk.cache',
            'port': 6379,
            'description': 'TuskLang Cache Service'
        },
        'tusklang-db': {
            'command': 'python -m tsk.database',
            'port': 5432,
            'description': 'TuskLang Database Service'
        }
    }


def _get_running_tusklang_services() -> Dict[str, psutil.Process]:
    """Get currently running TuskLang services"""
    running_services = {}
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
            if 'tsk' in cmdline or 'tusklang' in cmdline:
                service_name = _identify_service_from_process(proc)
                if service_name:
                    running_services[service_name] = proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return running_services


def _identify_service_from_process(process: psutil.Process) -> Optional[str]:
    """Identify service name from process"""
    try:
        cmdline = ' '.join(process.cmdline())
        
        if 'tsk.api' in cmdline:
            return 'tusklang-api'
        elif 'tsk.worker' in cmdline:
            return 'tusklang-worker'
        elif 'tsk.cache' in cmdline:
            return 'tusklang-cache'
        elif 'tsk.database' in cmdline:
            return 'tusklang-db'
        else:
            return None
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None


def _start_service(service_name: str, service_config: Dict[str, Any]) -> bool:
    """Start a service"""
    try:
        # Check if service is already running
        running_services = _get_running_tusklang_services()
        if service_name in running_services:
            return True  # Already running
        
        # Start service
        cmd = service_config['command'].split()
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True
        )
        
        # Wait a moment to see if it starts successfully
        time.sleep(1)
        
        if process.poll() is None:
            return True  # Process is running
        else:
            return False  # Process failed to start
            
    except Exception:
        return False


def _stop_service(service_name: str, process: psutil.Process) -> bool:
    """Stop a service"""
    try:
        # Try graceful shutdown first
        process.terminate()
        
        # Wait for graceful shutdown
        try:
            process.wait(timeout=10)
            return True
        except psutil.TimeoutExpired:
            # Force kill if graceful shutdown fails
            process.kill()
            process.wait()
            return True
            
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return True  # Process already stopped
    except Exception:
        return False


def _get_process_uptime(process: psutil.Process) -> str:
    """Get process uptime as string"""
    try:
        create_time = process.create_time()
        uptime_seconds = time.time() - create_time
        
        if uptime_seconds < 60:
            return f"{int(uptime_seconds)}s"
        elif uptime_seconds < 3600:
            return f"{int(uptime_seconds // 60)}m"
        else:
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return "N/A"


def _get_process_memory(process: psutil.Process) -> str:
    """Get process memory usage as string"""
    try:
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024
        
        if memory_mb < 1024:
            return f"{memory_mb:.1f}MB"
        else:
            return f"{memory_mb / 1024:.1f}GB"
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return "N/A"


def _check_port_availability(port: int) -> bool:
    """Check if a port is available"""
    import socket
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False


def _get_service_logs(service_name: str, lines: int = 50) -> List[str]:
    """Get service logs (placeholder implementation)"""
    # This would typically read from log files
    # For now, return placeholder
    return [
        f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {service_name}: Service started",
        f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {service_name}: Ready to accept connections"
    ] 