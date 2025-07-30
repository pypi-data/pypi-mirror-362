#!/usr/bin/env python3
"""
TuskLang Python CLI - Peanuts Commands
======================================
Peanut configuration operations
"""

import os
import json
import time
from typing import Dict, Any, Optional
from pathlib import Path

from ..utils import output_formatter, error_handler, config_loader


def handle_peanuts_command(args, cli):
    """Handle peanuts commands"""
    if args.peanuts_command == 'compile':
        return handle_compile_command(args, cli)
    elif args.peanuts_command == 'auto-compile':
        return handle_auto_compile_command(args, cli)
    elif args.peanuts_command == 'load':
        return handle_load_command(args, cli)
    else:
        output_formatter.print_error("Unknown peanuts command")
        return 1


def handle_compile_command(args, cli):
    """Handle peanuts compile command"""
    input_file = Path(args.file)
    if not input_file.exists():
        output_formatter.print_error(f"File not found: {args.file}")
        return 1
    
    try:
        # Import PeanutConfig
        from peanut_config import PeanutConfig
        
        # Determine output file
        if input_file.suffix.lower() == '.peanuts':
            output_file = input_file.with_suffix('.pnt')
        elif input_file.suffix.lower() == '.tsk':
            output_file = input_file.with_suffix('.pnt')
        else:
            output_formatter.print_error(f"Unsupported file type: {input_file.suffix}")
            return 1
        
        # Compile the file
        start_time = time.time()
        PeanutConfig.compile(str(input_file), str(output_file))
        compile_time = time.time() - start_time
        
        # Get file sizes
        input_size = input_file.stat().st_size
        output_size = output_file.stat().st_size
        
        # Prepare result
        result = {
            'input_file': str(input_file),
            'output_file': str(output_file),
            'input_size': input_size,
            'output_size': output_size,
            'compression_ratio': round((1 - output_size / input_size) * 100, 2),
            'compile_time': round(compile_time, 4),
            'success': True
        }
        
        if cli.json_output:
            output_formatter.print_json(result)
        else:
            print(f"✅ Compiled: {args.file} → {output_file.name}")
            print(f"   Input size: {input_size} bytes")
            print(f"   Output size: {output_size} bytes")
            print(f"   Compression: {result['compression_ratio']}%")
            print(f"   Compile time: {result['compile_time']}s")
        
        return 0
        
    except Exception as e:
        output_formatter.print_error(f"Compilation error: {str(e)}")
        return 1


def handle_auto_compile_command(args, cli):
    """Handle peanuts auto-compile command"""
    compile_path = Path(args.path) if args.path else Path.cwd()
    
    if not compile_path.exists():
        output_formatter.print_error(f"Path not found: {compile_path}")
        return 1
    
    try:
        # Import PeanutConfig
        from peanut_config import PeanutConfig
        
        # Find all .peanuts and .tsk files
        peanuts_files = list(compile_path.rglob("*.peanuts"))
        tsk_files = list(compile_path.rglob("*.tsk"))
        all_files = peanuts_files + tsk_files
        
        if not all_files:
            output_formatter.print_error(f"No .peanuts or .tsk files found in {compile_path}")
            return 1
        
        # Compile each file
        results = []
        total_start_time = time.time()
        
        for file_path in all_files:
            try:
                # Determine output file
                if file_path.suffix.lower() == '.peanuts':
                    output_file = file_path.with_suffix('.pnt')
                else:
                    output_file = file_path.with_suffix('.pnt')
                
                # Check if compilation is needed
                if output_file.exists():
                    input_mtime = file_path.stat().st_mtime
                    output_mtime = output_file.stat().st_mtime
                    if input_mtime <= output_mtime:
                        results.append({
                            'file': str(file_path),
                            'status': 'skipped',
                            'reason': 'up to date'
                        })
                        continue
                
                # Compile the file
                start_time = time.time()
                PeanutConfig.compile(str(file_path), str(output_file))
                compile_time = time.time() - start_time
                
                results.append({
                    'file': str(file_path),
                    'output': str(output_file),
                    'status': 'compiled',
                    'compile_time': round(compile_time, 4)
                })
                
            except Exception as e:
                results.append({
                    'file': str(file_path),
                    'status': 'error',
                    'error': str(e)
                })
        
        total_time = time.time() - total_start_time
        
        # Count results
        compiled_count = len([r for r in results if r['status'] == 'compiled'])
        skipped_count = len([r for r in results if r['status'] == 'skipped'])
        error_count = len([r for r in results if r['status'] == 'error'])
        
        # Prepare result
        result = {
            'path': str(compile_path),
            'total_files': len(all_files),
            'compiled': compiled_count,
            'skipped': skipped_count,
            'errors': error_count,
            'total_time': round(total_time, 4),
            'results': results
        }
        
        if cli.json_output:
            output_formatter.print_json(result)
        else:
            print(f"🔄 Auto-compiled: {compile_path}")
            print(f"   Total files: {len(all_files)}")
            print(f"   Compiled: {compiled_count}")
            print(f"   Skipped: {skipped_count}")
            print(f"   Errors: {error_count}")
            print(f"   Total time: {result['total_time']}s")
            
            if cli.verbose and results:
                print(f"\n📋 Details:")
                for r in results:
                    if r['status'] == 'compiled':
                        print(f"   ✅ {r['file']} → {r['output']} ({r['compile_time']}s)")
                    elif r['status'] == 'skipped':
                        print(f"   ⏭️  {r['file']} ({r['reason']})")
                    else:
                        print(f"   ❌ {r['file']} ({r['error']})")
        
        return 0 if error_count == 0 else 1
        
    except Exception as e:
        output_formatter.print_error(f"Auto-compile error: {str(e)}")
        return 1


def handle_load_command(args, cli):
    """Handle peanuts load command"""
    file_path = Path(args.file)
    if not file_path.exists():
        output_formatter.print_error(f"File not found: {args.file}")
        return 1
    
    try:
        # Import PeanutConfig
        from peanut_config import PeanutConfig
        
        # Load the binary file
        start_time = time.time()
        config = PeanutConfig.load(file_path.parent)
        load_time = time.time() - start_time
        
        # Get file info
        file_size = file_path.stat().st_size
        file_mtime = file_path.stat().st_mtime
        
        # Get configuration data
        config_data = config.get_all()
        
        # Prepare result
        result = {
            'file': str(file_path),
            'file_size': file_size,
            'file_modified': time.ctime(file_mtime),
            'load_time': round(load_time, 4),
            'config_data': config_data,
            'hierarchy': [str(f.path) for f in config._hierarchy] if hasattr(config, '_hierarchy') else []
        }
        
        if cli.json_output:
            output_formatter.print_json(result)
        else:
            print(f"📄 Loaded: {args.file}")
            print(f"   Size: {file_size} bytes")
            print(f"   Modified: {result['file_modified']}")
            print(f"   Load time: {result['load_time']}s")
            
            if hasattr(config, '_hierarchy') and config._hierarchy:
                print(f"   Hierarchy:")
                for f in config._hierarchy:
                    print(f"     - {f.path}")
            
            if cli.verbose:
                print(f"\n📋 Configuration Data:")
                print(json.dumps(config_data, indent=2))
        
        return 0
        
    except Exception as e:
        output_formatter.print_error(f"Load error: {str(e)}")
        return 1 