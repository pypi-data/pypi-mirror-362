#!/usr/bin/env python3
"""
SQLite Adapter for TuskLang Enhanced Python
==========================================
Enables @query operations with SQLite database

DEFAULT CONFIG: peanut.tsk (the bridge of language grace)
"""

import sqlite3
import os
from typing import Any, Dict, List, Union, Optional
from pathlib import Path


class SQLiteAdapter:
    """SQLite database adapter for TuskLang"""
    
    def __init__(self, options: Dict[str, Any] = None):
        self.config = {
            'database': ':memory:',
            'timeout': 10.0,
            'check_same_thread': False
        }
        
        if options:
            self.config.update(options)
        
        self.connection = None
    
    def connect(self):
        """Connect to SQLite database"""
        if not self.connection:
            self.connection = sqlite3.connect(
                self.config['database'],
                timeout=self.config['timeout'],
                check_same_thread=self.config['check_same_thread']
            )
            self.connection.row_factory = sqlite3.Row  # Dictionary-like access
    
    def query(self, sql: str, params: List[Any] = None) -> List[Dict[str, Any]]:
        """Execute SQL query and return results"""
        self.connect()
        
        if params is None:
            params = []
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            
            # Handle different query types
            if sql.strip().upper().startswith(('SELECT', 'WITH')):
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
            else:
                # INSERT, UPDATE, DELETE, etc.
                self.connection.commit()
                return [{
                    'affected_rows': cursor.rowcount,
                    'last_insert_id': cursor.lastrowid
                }]
                
        except sqlite3.Error as e:
            raise Exception(f"SQLite error: {str(e)}")
    
    def count(self, table: str, where: str = None, params: List[Any] = None) -> int:
        """Count rows in table with optional WHERE clause"""
        sql = f"SELECT COUNT(*) as count FROM {table}"
        
        if where:
            sql += f" WHERE {where}"
        
        result = self.query(sql, params or [])
        return result[0]['count'] if result else 0
    
    def find_all(self, table: str, where: str = None, params: List[Any] = None) -> List[Dict[str, Any]]:
        """Find all rows in table with optional WHERE clause"""
        sql = f"SELECT * FROM {table}"
        
        if where:
            sql += f" WHERE {where}"
        
        return self.query(sql, params or [])
    
    def find_one(self, table: str, where: str = None, params: List[Any] = None) -> Optional[Dict[str, Any]]:
        """Find one row in table with optional WHERE clause"""
        sql = f"SELECT * FROM {table}"
        
        if where:
            sql += f" WHERE {where}"
        
        sql += " LIMIT 1"
        
        result = self.query(sql, params or [])
        return result[0] if result else None
    
    def sum(self, table: str, column: str, where: str = None, params: List[Any] = None) -> float:
        """Sum values in a column with optional WHERE clause"""
        sql = f"SELECT SUM({column}) as total FROM {table}"
        
        if where:
            sql += f" WHERE {where}"
        
        result = self.query(sql, params or [])
        return float(result[0]['total'] or 0) if result else 0.0
    
    def avg(self, table: str, column: str, where: str = None, params: List[Any] = None) -> float:
        """Average values in a column with optional WHERE clause"""
        sql = f"SELECT AVG({column}) as average FROM {table}"
        
        if where:
            sql += f" WHERE {where}"
        
        result = self.query(sql, params or [])
        return float(result[0]['average'] or 0) if result else 0.0
    
    def max(self, table: str, column: str, where: str = None, params: List[Any] = None) -> Any:
        """Find maximum value in a column with optional WHERE clause"""
        sql = f"SELECT MAX({column}) as maximum FROM {table}"
        
        if where:
            sql += f" WHERE {where}"
        
        result = self.query(sql, params or [])
        return result[0]['maximum'] if result else None
    
    def min(self, table: str, column: str, where: str = None, params: List[Any] = None) -> Any:
        """Find minimum value in a column with optional WHERE clause"""
        sql = f"SELECT MIN({column}) as minimum FROM {table}"
        
        if where:
            sql += f" WHERE {where}"
        
        result = self.query(sql, params or [])
        return result[0]['minimum'] if result else None
    
    def create_test_data(self):
        """Create test data for SQLite"""
        self.connect()
        
        # Drop existing tables
        self.query("DROP TABLE IF EXISTS users")
        self.query("DROP TABLE IF EXISTS orders")
        self.query("DROP TABLE IF EXISTS products")
        
        # Create tables
        self.query("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                active BOOLEAN DEFAULT 1,
                age INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.query("""
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount DECIMAL(10,2),
                status TEXT DEFAULT 'pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        self.query("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price DECIMAL(10,2),
                category TEXT,
                in_stock BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert test data
        self.query("""
            INSERT INTO users (name, email, active, age) VALUES
            ('John Doe', 'john@example.com', 1, 30),
            ('Jane Smith', 'jane@example.com', 1, 25),
            ('Bob Wilson', 'bob@example.com', 0, 35)
        """)
        
        self.query("""
            INSERT INTO orders (user_id, amount, status) VALUES
            (1, 99.99, 'completed'),
            (2, 149.50, 'completed'),
            (1, 75.25, 'pending')
        """)
        
        self.query("""
            INSERT INTO products (name, price, category, in_stock) VALUES
            ('Widget A', 29.99, 'electronics', 1),
            ('Widget B', 49.99, 'electronics', 1),
            ('Gadget C', 19.99, 'accessories', 0)
        """)
        
        print("SQLite test data created successfully")
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        try:
            self.connect()
            self.connection.execute("SELECT 1")
            return True
        except Exception:
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    @staticmethod
    def load_from_peanut():
        """Load SQLite configuration from peanut.tsk"""
        # Import here to avoid circular imports
        from tsk_enhanced import TuskLangEnhanced
        
        parser = TuskLangEnhanced()
        parser.load_peanut()
        
        config = {}
        
        # Look for SQLite configuration in peanut.tsk
        if parser.get('database.sqlite.database'):
            config['database'] = parser.get('database.sqlite.database')
        elif parser.get('database.sqlite.filename'):
            config['database'] = parser.get('database.sqlite.filename')
        
        if parser.get('database.sqlite.timeout'):
            config['timeout'] = float(parser.get('database.sqlite.timeout'))
        
        if not config:
            raise Exception('No SQLite configuration found in peanut.tsk')
        
        return SQLiteAdapter(config)


# Command line interface
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("""
SQLite Adapter for TuskLang Python
==================================

Usage: python sqlite_adapter.py [command] [options]

Commands:
    test                Create test data
    query <sql>         Execute SQL query
    count <table>       Count rows in table
    sum <table> <col>   Sum column values
    
Examples:
    python sqlite_adapter.py test
    python sqlite_adapter.py query "SELECT * FROM users"
    python sqlite_adapter.py count users
    python sqlite_adapter.py sum orders amount
""")
        sys.exit(1)
    
    # Load from peanut.tsk or use defaults
    try:
        adapter = SQLiteAdapter.load_from_peanut()
    except:
        adapter = SQLiteAdapter({'database': './test.db'})
    
    command = sys.argv[1]
    
    if command == 'test':
        adapter.create_test_data()
    
    elif command == 'query':
        if len(sys.argv) < 3:
            print("Error: SQL query required")
            sys.exit(1)
        
        try:
            results = adapter.query(sys.argv[2])
            for row in results:
                print(row)
        except Exception as e:
            print(f"Error: {e}")
    
    elif command == 'count':
        if len(sys.argv) < 3:
            print("Error: Table name required")
            sys.exit(1)
        
        try:
            count = adapter.count(sys.argv[2])
            print(f"Count: {count}")
        except Exception as e:
            print(f"Error: {e}")
    
    elif command == 'sum':
        if len(sys.argv) < 4:
            print("Error: Table name and column required")
            sys.exit(1)
        
        try:
            total = adapter.sum(sys.argv[2], sys.argv[3])
            print(f"Sum: {total}")
        except Exception as e:
            print(f"Error: {e}")
    
    else:
        print(f"Error: Unknown command: {command}")
        sys.exit(1)
    
    adapter.close()