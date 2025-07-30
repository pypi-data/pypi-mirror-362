#!/usr/bin/env python3
"""
Database Commands for TuskLang Python CLI
=========================================
Implements all database-related commands
"""

import os
import sqlite3
import subprocess
import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from adapters import SQLiteAdapter, PostgreSQLAdapter, MongoDBAdapter, RedisAdapter
from ..utils.output_formatter import OutputFormatter
from ..utils.error_handler import ErrorHandler
from ..utils.config_loader import ConfigLoader


def handle_db_command(args: Any, cli: Any) -> int:
    """Handle database commands"""
    formatter = OutputFormatter(cli.json_output, cli.quiet, cli.verbose)
    error_handler = ErrorHandler(cli.json_output, cli.verbose)
    config_loader = ConfigLoader(cli.config_path)
    
    try:
        if args.db_command == 'status':
            return _handle_db_status(formatter, config_loader)
        elif args.db_command == 'migrate':
            return _handle_db_migrate(args, formatter, error_handler)
        elif args.db_command == 'console':
            return _handle_db_console(formatter, config_loader)
        elif args.db_command == 'backup':
            return _handle_db_backup(args, formatter, error_handler, config_loader)
        elif args.db_command == 'restore':
            return _handle_db_restore(args, formatter, error_handler)
        elif args.db_command == 'init':
            return _handle_db_init(formatter, config_loader)
        else:
            formatter.error("Unknown database command")
            return ErrorHandler.INVALID_ARGS
            
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_db_status(formatter: OutputFormatter, config_loader: ConfigLoader) -> int:
    """Handle db status command"""
    formatter.loading("Checking database connections...")
    
    # Load configuration
    config = config_loader.load_config()
    db_config = config.get('database', {})
    default_db = db_config.get('default', 'sqlite')
    
    status_results = []
    
    # Check SQLite
    if 'sqlite' in db_config or default_db == 'sqlite':
        try:
            sqlite_config = db_config.get('sqlite', {})
            db_path = sqlite_config.get('database', './tusklang.db')
            
            adapter = SQLiteAdapter({'database': db_path})
            if adapter.is_connected():
                status_results.append(['SQLite', '✅ Connected', db_path])
            else:
                status_results.append(['SQLite', '❌ Disconnected', db_path])
        except Exception as e:
            status_results.append(['SQLite', f'❌ Error: {str(e)}', 'N/A'])
    
    # Check PostgreSQL
    if 'postgresql' in db_config or default_db == 'postgresql':
        try:
            pg_config = db_config.get('postgresql', {})
            adapter = PostgreSQLAdapter(pg_config)
            if adapter.is_connected():
                status_results.append(['PostgreSQL', '✅ Connected', f"{pg_config.get('host', 'localhost')}:{pg_config.get('port', 5432)}"])
            else:
                status_results.append(['PostgreSQL', '❌ Disconnected', f"{pg_config.get('host', 'localhost')}:{pg_config.get('port', 5432)}"])
        except Exception as e:
            status_results.append(['PostgreSQL', f'❌ Error: {str(e)}', 'N/A'])
    
    # Check MongoDB
    if 'mongodb' in db_config or default_db == 'mongodb':
        try:
            mongo_config = db_config.get('mongodb', {})
            adapter = MongoDBAdapter(mongo_config)
            if adapter.is_connected():
                status_results.append(['MongoDB', '✅ Connected', mongo_config.get('url', 'mongodb://localhost:27017')])
            else:
                status_results.append(['MongoDB', '❌ Disconnected', mongo_config.get('url', 'mongodb://localhost:27017')])
        except Exception as e:
            status_results.append(['MongoDB', f'❌ Error: {str(e)}', 'N/A'])
    
    # Check Redis
    if 'redis' in db_config or default_db == 'redis':
        try:
            redis_config = db_config.get('redis', {})
            adapter = RedisAdapter(redis_config)
            adapter.connect()
            status_results.append(['Redis', '✅ Connected', f"{redis_config.get('host', 'localhost')}:{redis_config.get('port', 6379)}"])
        except Exception as e:
            status_results.append(['Redis', f'❌ Error: {str(e)}', 'N/A'])
    
    # Display results
    formatter.table(
        ['Database', 'Status', 'Connection'],
        status_results,
        'Database Connection Status'
    )
    
    return ErrorHandler.SUCCESS


def _handle_db_migrate(args: Any, formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle db migrate command"""
    migration_file = Path(args.file)
    
    if not migration_file.exists():
        return error_handler.handle_file_not_found(str(migration_file))
    
    formatter.loading(f"Running migration: {migration_file}")
    
    try:
        # Read migration file
        with open(migration_file, 'r') as f:
            migration_sql = f.read()
        
        # Execute migration (using SQLite as default)
        adapter = SQLiteAdapter({'database': './tusklang.db'})
        adapter.connect()
        
        # Split SQL statements
        statements = [stmt.strip() for stmt in migration_sql.split(';') if stmt.strip()]
        
        for statement in statements:
            adapter.query(statement)
        
        formatter.success(f"Migration completed successfully: {len(statements)} statements executed")
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_db_console(formatter: OutputFormatter, config_loader: ConfigLoader) -> int:
    """Handle db console command"""
    formatter.info("Starting interactive database console...")
    formatter.info("Type 'exit' to quit, 'help' for commands")
    
    # Load configuration
    config = config_loader.load_config()
    db_config = config.get('database', {})
    default_db = db_config.get('default', 'sqlite')
    
    try:
        if default_db == 'sqlite':
            adapter = SQLiteAdapter({'database': './tusklang.db'})
        elif default_db == 'postgresql':
            adapter = PostgreSQLAdapter(db_config.get('postgresql', {}))
        elif default_db == 'mongodb':
            adapter = MongoDBAdapter(db_config.get('mongodb', {}))
        elif default_db == 'redis':
            adapter = RedisAdapter(db_config.get('redis', {}))
        else:
            formatter.error(f"Unsupported database type: {default_db}")
            return ErrorHandler.CONFIG_ERROR
        
        adapter.connect()
        
        # Simple console loop
        while True:
            try:
                query = input(f"{default_db}> ").strip()
                
                if query.lower() in ['exit', 'quit']:
                    break
                elif query.lower() == 'help':
                    print("Available commands: SELECT, INSERT, UPDATE, DELETE, exit, help")
                    continue
                elif not query:
                    continue
                
                # Execute query
                if default_db in ['sqlite', 'postgresql']:
                    result = adapter.query(query)
                    for row in result:
                        print(row)
                elif default_db == 'mongodb':
                    # Simple MongoDB query parsing
                    if query.startswith('find'):
                        collection = query.split()[1] if len(query.split()) > 1 else 'test'
                        result = adapter.query(f"{collection}.find", {})
                        for doc in result:
                            print(doc)
                    else:
                        print("MongoDB commands: find <collection>, exit, help")
                elif default_db == 'redis':
                    # Simple Redis command parsing
                    parts = query.split()
                    if parts[0].upper() in ['GET', 'SET', 'DEL', 'KEYS']:
                        result = adapter.query(parts[0].upper(), *parts[1:])
                        print(result)
                    else:
                        print("Redis commands: GET <key>, SET <key> <value>, DEL <key>, KEYS <pattern>")
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
        
        adapter.close()
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        formatter.error(f"Failed to start database console: {e}")
        return ErrorHandler.CONNECTION_ERROR


def _handle_db_backup(args: Any, formatter: OutputFormatter, error_handler: ErrorHandler, config_loader: ConfigLoader) -> int:
    """Handle db backup command"""
    # Generate backup filename if not provided
    if args.file:
        backup_file = Path(args.file)
    else:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = Path(f"tusklang_backup_{timestamp}.sql")
    
    formatter.loading(f"Creating database backup: {backup_file}")
    
    try:
        # Load configuration
        config = config_loader.load_config()
        db_config = config.get('database', {})
        default_db = db_config.get('default', 'sqlite')
        
        if default_db == 'sqlite':
            # SQLite backup
            source_db = db_config.get('sqlite', {}).get('database', './tusklang.db')
            
            if not Path(source_db).exists():
                formatter.warning(f"Source database not found: {source_db}")
                return ErrorHandler.FILE_NOT_FOUND
            
            # Use SQLite backup API
            source_conn = sqlite3.connect(source_db)
            backup_conn = sqlite3.connect(str(backup_file))
            
            source_conn.backup(backup_conn)
            source_conn.close()
            backup_conn.close()
            
        elif default_db == 'postgresql':
            # PostgreSQL backup using pg_dump
            pg_config = db_config.get('postgresql', {})
            host = pg_config.get('host', 'localhost')
            port = pg_config.get('port', 5432)
            database = pg_config.get('database', 'tusklang')
            user = pg_config.get('user', 'postgres')
            
            cmd = [
                'pg_dump',
                f'--host={host}',
                f'--port={port}',
                f'--dbname={database}',
                f'--username={user}',
                '--no-password',
                f'--file={backup_file}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"pg_dump failed: {result.stderr}")
        
        else:
            formatter.error(f"Backup not supported for database type: {default_db}")
            return ErrorHandler.CONFIG_ERROR
        
        formatter.success(f"Database backup created successfully: {backup_file}")
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_db_restore(args: Any, formatter: OutputFormatter, error_handler: ErrorHandler) -> int:
    """Handle db restore command"""
    backup_file = Path(args.file)
    
    if not backup_file.exists():
        return error_handler.handle_file_not_found(str(backup_file))
    
    formatter.loading(f"Restoring database from backup: {backup_file}")
    
    try:
        # Determine backup type and restore
        if backup_file.suffix == '.sql':
            # SQL backup file
            with open(backup_file, 'r') as f:
                restore_sql = f.read()
            
            adapter = SQLiteAdapter({'database': './tusklang.db'})
            adapter.connect()
            
            # Split and execute SQL statements
            statements = [stmt.strip() for stmt in restore_sql.split(';') if stmt.strip()]
            
            for statement in statements:
                adapter.query(statement)
            
            adapter.close()
            
        elif backup_file.suffix == '.db':
            # SQLite database file
            import shutil
            shutil.copy2(backup_file, './tusklang.db')
            
        else:
            formatter.error(f"Unsupported backup file format: {backup_file.suffix}")
            return ErrorHandler.INVALID_ARGS
        
        formatter.success(f"Database restored successfully from: {backup_file}")
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        return error_handler.handle_error(e)


def _handle_db_init(formatter: OutputFormatter, config_loader: ConfigLoader) -> int:
    """Handle db init command"""
    formatter.loading("Initializing SQLite database...")
    
    try:
        # Create SQLite database with basic schema
        adapter = SQLiteAdapter({'database': './tusklang.db'})
        adapter.connect()
        
        # Create basic tables
        init_sql = """
        CREATE TABLE IF NOT EXISTS config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            value TEXT,
            expires_at DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        statements = [stmt.strip() for stmt in init_sql.split(';') if stmt.strip()]
        
        for statement in statements:
            adapter.query(statement)
        
        adapter.close()
        
        formatter.success("SQLite database initialized successfully")
        formatter.info("Created tables: config, migrations, cache")
        
        return ErrorHandler.SUCCESS
        
    except Exception as e:
        formatter.error(f"Failed to initialize database: {e}")
        return ErrorHandler.CONNECTION_ERROR 