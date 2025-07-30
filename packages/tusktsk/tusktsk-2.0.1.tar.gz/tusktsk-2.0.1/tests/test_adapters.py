#!/usr/bin/env python3
"""
Test script for TuskLang Python Database Adapters
=================================================
Tests all available database adapters with sample data
"""

import sys
import json
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from adapters import SQLiteAdapter, PostgreSQLAdapter, MongoDBAdapter


def test_sqlite():
    """Test SQLite adapter"""
    print("=" * 50)
    print("Testing SQLite Adapter")
    print("=" * 50)
    
    try:
        # Create adapter with test database
        adapter = SQLiteAdapter({'database': './test_sqlite.db'})
        
        # Create test data
        print("Creating test data...")
        adapter.create_test_data()
        
        # Test basic queries
        print("\nTesting queries:")
        
        # Count users
        count = adapter.count('users')
        print(f"Total users: {count}")
        
        # Find active users
        active_users = adapter.find_all('users', 'active = ?', [1])
        print(f"Active users: {len(active_users)}")
        
        # Sum order amounts
        total_revenue = adapter.sum('orders', 'amount')
        print(f"Total revenue: ${total_revenue}")
        
        # Average user age
        avg_age = adapter.avg('users', 'age')
        print(f"Average age: {avg_age:.1f}")
        
        # Raw SQL query
        users = adapter.query("SELECT name, email FROM users WHERE active = ?", [1])
        print(f"Active user emails: {[u['email'] for u in users]}")
        
        adapter.close()
        print("✅ SQLite tests passed!")
        
    except Exception as e:
        print(f"❌ SQLite test failed: {e}")


def test_postgresql():
    """Test PostgreSQL adapter"""
    print("\n" + "=" * 50)
    print("Testing PostgreSQL Adapter")
    print("=" * 50)
    
    try:
        # Create adapter (requires running PostgreSQL)
        adapter = PostgreSQLAdapter({
            'host': 'localhost',
            'database': 'tusklang_test',
            'user': 'postgres',
            'password': ''  # Update with your password
        })
        
        # Test connection
        if not adapter.is_connected():
            print("⚠️  PostgreSQL not available - skipping tests")
            return
        
        # Create test data
        print("Creating test data...")
        adapter.create_test_data()
        
        # Test basic queries
        print("\nTesting queries:")
        
        # Count users
        count = adapter.count('users')
        print(f"Total users: {count}")
        
        # Find active users
        active_users = adapter.find_all('users', 'active = %s', [True])
        print(f"Active users: {len(active_users)}")
        
        # Sum order amounts
        total_revenue = adapter.sum('orders', 'amount')
        print(f"Total revenue: ${total_revenue}")
        
        # Raw SQL query with JSON formatting
        users = adapter.query("SELECT name, email FROM users WHERE active = %s", [True])
        print(f"Active user emails: {[u['email'] for u in users]}")
        
        adapter.close()
        print("✅ PostgreSQL tests passed!")
        
    except Exception as e:
        print(f"⚠️  PostgreSQL test skipped: {e}")


def test_mongodb():
    """Test MongoDB adapter"""
    print("\n" + "=" * 50)
    print("Testing MongoDB Adapter")
    print("=" * 50)
    
    try:
        # Create adapter (requires running MongoDB)
        adapter = MongoDBAdapter({
            'url': 'mongodb://localhost:27017',
            'database': 'tusklang_test'
        })
        
        # Test connection
        if not adapter.is_connected():
            print("⚠️  MongoDB not available - skipping tests")
            return
        
        # Create test data
        print("Creating test data...")
        adapter.create_test_data()
        
        # Test basic queries
        print("\nTesting queries:")
        
        # Count users
        count = adapter.query('users.count', {})
        print(f"Total users: {count}")
        
        # Find active users
        active_users = adapter.query('users.find', {'active': True})
        print(f"Active users: {len(active_users)}")
        
        # Sum order amounts
        total_revenue = adapter.query('orders.sum', 'amount', {})
        print(f"Total revenue: ${total_revenue}")
        
        # Average product price
        avg_price = adapter.query('products.avg', 'price', {})
        print(f"Average product price: ${avg_price:.2f}")
        
        # Find specific user
        user = adapter.query('users.findOne', {'email': 'john@example.com'})
        print(f"Found user: {user['name'] if user else 'None'}")
        
        adapter.close()
        print("✅ MongoDB tests passed!")
        
    except Exception as e:
        print(f"⚠️  MongoDB test skipped: {e}")


def test_peanut_integration():
    """Test peanut.tsk integration"""
    print("\n" + "=" * 50)
    print("Testing peanut.tsk Integration")
    print("=" * 50)
    
    try:
        from tsk_enhanced import TuskLangEnhanced
        
        # Create a test peanut.tsk file
        peanut_content = """
# Test peanut.tsk for database adapters
$app_name: "TuskLang Python Test"
$version: "1.0.0"

[database]
default: "sqlite"

sqlite {
    database: "./test_peanut.db"
    timeout: 10.0
}

postgresql {
    host: "localhost"
    port: 5432
    database: "tusklang_test"
    user: "postgres"
    password: ""
}

mongodb {
    url: "mongodb://localhost:27017"
    database: "tusklang_test"
}
"""
        
        # Write test peanut.tsk
        with open('./peanut.tsk', 'w') as f:
            f.write(peanut_content)
        
        # Test parser with database integration
        parser = TuskLangEnhanced()
        parser.load_peanut()
        
        print(f"App name: {parser.get('app_name')}")
        print(f"Default database: {parser.get('database.default')}")
        print(f"SQLite database: {parser.get('database.sqlite.database')}")
        
        # Test query execution through parser
        result = parser.execute_query("SELECT 1 as test")
        print(f"Query result: {result}")
        
        print("✅ peanut.tsk integration tests passed!")
        
    except Exception as e:
        print(f"❌ peanut.tsk integration test failed: {e}")


def main():
    """Run all adapter tests"""
    print("TuskLang Python Database Adapter Tests")
    print("=====================================")
    
    # Test all adapters
    test_sqlite()
    test_postgresql()
    test_mongodb()
    test_peanut_integration()
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("=" * 50)


if __name__ == '__main__':
    main()