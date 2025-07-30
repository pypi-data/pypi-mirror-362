#!/usr/bin/env python3
"""
Database Adapters for TuskLang Enhanced Python
==============================================
Collection of database adapters for TuskLang Python SDK

Available Adapters:
- SQLiteAdapter - SQLite database support
- PostgreSQLAdapter - PostgreSQL database support  
- MongoDBAdapter - MongoDB document database support
- RedisAdapter - Redis key-value store support

Usage:
    from adapters import SQLiteAdapter, PostgreSQLAdapter, MongoDBAdapter, RedisAdapter
    
    # Load from peanut.tsk
    db = SQLiteAdapter.load_from_peanut()
    
    # Or configure manually
    db = SQLiteAdapter({'database': './myapp.db'})
    
    # Execute queries
    results = db.query("SELECT * FROM users")
    count = db.count("users", "active = ?", [True])
"""

from .sqlite_adapter import SQLiteAdapter
from .postgresql_adapter import PostgreSQLAdapter  
from .mongodb_adapter import MongoDBAdapter
from .redis_adapter import RedisAdapter

__all__ = ['SQLiteAdapter', 'PostgreSQLAdapter', 'MongoDBAdapter', 'RedisAdapter']

# Database adapter registry
ADAPTERS = {
    'sqlite': SQLiteAdapter,
    'postgresql': PostgreSQLAdapter,
    'postgres': PostgreSQLAdapter,
    'mongodb': MongoDBAdapter,
    'mongo': MongoDBAdapter,
    'redis': RedisAdapter
}


def get_adapter(db_type: str):
    """Get database adapter by type"""
    if db_type.lower() not in ADAPTERS:
        available = ', '.join(ADAPTERS.keys())
        raise Exception(f"Unknown database type: {db_type}. Available: {available}")
    
    return ADAPTERS[db_type.lower()]


def load_adapter_from_peanut(db_type: str = None):
    """Load database adapter from peanut.tsk configuration"""
    if not db_type:
        # Try to determine from peanut.tsk
        from tsk_enhanced import TuskLangEnhanced
        parser = TuskLangEnhanced()
        parser.load_peanut()
        
        db_type = parser.get('database.default', 'sqlite')
    
    adapter_class = get_adapter(db_type)
    return adapter_class.load_from_peanut()


# Convenience functions
def query(sql_or_operation: str, *args, db_type: str = None):
    """Execute a query using the default database adapter"""
    adapter = load_adapter_from_peanut(db_type)
    return adapter.query(sql_or_operation, *args)


def count(table_or_collection: str, where: str = None, params: list = None, db_type: str = None):
    """Count records using the default database adapter"""
    adapter = load_adapter_from_peanut(db_type)
    return adapter.count(table_or_collection, where, params)


def find_all(table_or_collection: str, where: str = None, params: list = None, db_type: str = None):
    """Find all records using the default database adapter"""
    adapter = load_adapter_from_peanut(db_type)
    return adapter.find_all(table_or_collection, where, params)


def find_one(table_or_collection: str, where: str = None, params: list = None, db_type: str = None):
    """Find one record using the default database adapter"""
    adapter = load_adapter_from_peanut(db_type)
    return adapter.find_one(table_or_collection, where, params)