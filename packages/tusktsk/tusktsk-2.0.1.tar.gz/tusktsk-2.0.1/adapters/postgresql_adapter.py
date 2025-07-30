#!/usr/bin/env python3
"""
PostgreSQL Adapter for TuskLang Enhanced Python
=============================================
Enables @query operations with PostgreSQL database

DEFAULT CONFIG: peanut.tsk (the bridge of language grace)
"""

import json
from typing import Any, Dict, List, Union, Optional

try:
    import psycopg2
    import psycopg2.extras
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False


class PostgreSQLAdapter:
    """PostgreSQL database adapter for TuskLang"""
    
    def __init__(self, options: Dict[str, Any] = None):
        if not PSYCOPG2_AVAILABLE:
            raise Exception('PostgreSQL adapter requires psycopg2. Install it with: pip install psycopg2-binary')
        
        self.config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'tusklang',
            'user': 'postgres',
            'password': '',
            'sslmode': 'prefer',
            'connect_timeout': 10
        }
        
        if options:
            self.config.update(options)
        
        self.connection = None
    
    def connect(self):
        """Connect to PostgreSQL database"""
        if not self.connection:
            try:
                self.connection = psycopg2.connect(
                    host=self.config['host'],
                    port=self.config['port'],
                    database=self.config['database'],
                    user=self.config['user'],
                    password=self.config['password'],
                    sslmode=self.config['sslmode'],
                    connect_timeout=self.config['connect_timeout']
                )
                self.connection.autocommit = True
            except psycopg2.Error as e:
                raise Exception(f"PostgreSQL connection error: {str(e)}")
    
    def query(self, sql: str, params: List[Any] = None) -> List[Dict[str, Any]]:
        """Execute SQL query and return results"""
        self.connect()
        
        if params is None:
            params = []
        
        try:
            with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql, params)
                
                # Handle different query types
                if sql.strip().upper().startswith(('SELECT', 'WITH', 'SHOW')):
                    rows = cursor.fetchall()
                    return [dict(row) for row in rows]
                else:
                    # INSERT, UPDATE, DELETE, etc.
                    return [{
                        'affected_rows': cursor.rowcount,
                        'last_insert_id': getattr(cursor, 'lastrowid', None)
                    }]
                    
        except psycopg2.Error as e:
            raise Exception(f"PostgreSQL error: {str(e)}")
    
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
        """Create test data for PostgreSQL"""
        self.connect()
        
        # Drop existing tables (with CASCADE)
        self.query("DROP TABLE IF EXISTS orders CASCADE")
        self.query("DROP TABLE IF EXISTS products CASCADE")
        self.query("DROP TABLE IF EXISTS users CASCADE")
        
        # Create tables
        self.query("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE,
                active BOOLEAN DEFAULT TRUE,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.query("""
            CREATE TABLE orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                amount DECIMAL(10,2),
                status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.query("""
            CREATE TABLE products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10,2),
                category VARCHAR(100),
                in_stock BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert test data
        self.query("""
            INSERT INTO users (name, email, active, age) VALUES
            ('John Doe', 'john@example.com', TRUE, 30),
            ('Jane Smith', 'jane@example.com', TRUE, 25),
            ('Bob Wilson', 'bob@example.com', FALSE, 35)
        """)
        
        self.query("""
            INSERT INTO orders (user_id, amount, status) VALUES
            (1, 99.99, 'completed'),
            (2, 149.50, 'completed'),
            (1, 75.25, 'pending')
        """)
        
        self.query("""
            INSERT INTO products (name, price, category, in_stock) VALUES
            ('Widget A', 29.99, 'electronics', TRUE),
            ('Widget B', 49.99, 'electronics', TRUE),
            ('Gadget C', 19.99, 'accessories', FALSE)
        """)
        
        print("PostgreSQL test data created successfully")
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1")
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
        """Load PostgreSQL configuration from peanut.tsk"""
        # Import here to avoid circular imports
        from tsk_enhanced import TuskLangEnhanced
        
        parser = TuskLangEnhanced()
        parser.load_peanut()
        
        config = {}
        
        # Look for PostgreSQL configuration in peanut.tsk
        if parser.get('database.postgresql.host'):
            config['host'] = parser.get('database.postgresql.host')
        elif parser.get('database.postgres.host'):
            config['host'] = parser.get('database.postgres.host')
        
        if parser.get('database.postgresql.port'):
            config['port'] = int(parser.get('database.postgresql.port'))
        elif parser.get('database.postgres.port'):
            config['port'] = int(parser.get('database.postgres.port'))
        
        if parser.get('database.postgresql.database'):
            config['database'] = parser.get('database.postgresql.database')
        elif parser.get('database.postgres.database'):
            config['database'] = parser.get('database.postgres.database')
        
        if parser.get('database.postgresql.user'):
            config['user'] = parser.get('database.postgresql.user')
        elif parser.get('database.postgres.user'):
            config['user'] = parser.get('database.postgres.user')
        
        if parser.get('database.postgresql.password'):
            config['password'] = parser.get('database.postgresql.password')
        elif parser.get('database.postgres.password'):
            config['password'] = parser.get('database.postgres.password')
        
        if not config:
            raise Exception('No PostgreSQL configuration found in peanut.tsk')
        
        return PostgreSQLAdapter(config)


# Command line interface
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("""
PostgreSQL Adapter for TuskLang Python
=====================================

Usage: python postgresql_adapter.py [command] [options]

Commands:
    test                Create test data
    query <sql>         Execute SQL query
    count <table>       Count rows in table
    sum <table> <col>   Sum column values
    
Examples:
    python postgresql_adapter.py test
    python postgresql_adapter.py query "SELECT * FROM users"
    python postgresql_adapter.py count users
    python postgresql_adapter.py sum orders amount

Requirements:
    pip install psycopg2-binary
""")
        sys.exit(1)
    
    # Load from peanut.tsk or use defaults
    try:
        adapter = PostgreSQLAdapter.load_from_peanut()
    except:
        adapter = PostgreSQLAdapter({
            'host': 'localhost',
            'database': 'tusklang_test',
            'user': 'postgres',
            'password': 'password'
        })
    
    command = sys.argv[1]
    
    if command == 'test':
        try:
            adapter.create_test_data()
        except Exception as e:
            print(f"Error: {e}")
    
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