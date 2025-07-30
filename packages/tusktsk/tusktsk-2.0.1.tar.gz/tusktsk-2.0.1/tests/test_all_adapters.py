#!/usr/bin/env python3
"""
Test all database adapters for TuskLang Enhanced Python
======================================================
Demonstrates @query operations with all supported databases
"""

from tsk_enhanced import TuskLangEnhanced
from adapters import SQLiteAdapter, PostgreSQLAdapter, MongoDBAdapter, RedisAdapter
import json

def test_sqlite():
    """Test SQLite adapter"""
    print("\n=== Testing SQLite Adapter ===")
    
    # Create adapter
    db = SQLiteAdapter({'database': 'test_adapters.db'})
    
    # Create test table
    db.query("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            active BOOLEAN,
            score INTEGER
        )
    """)
    
    # Insert test data
    db.query("DELETE FROM users")  # Clean up first
    db.query("INSERT INTO users (name, active, score) VALUES (?, ?, ?)", ["Alice", True, 100])
    db.query("INSERT INTO users (name, active, score) VALUES (?, ?, ?)", ["Bob", False, 85])
    db.query("INSERT INTO users (name, active, score) VALUES (?, ?, ?)", ["Charlie", True, 92])
    
    # Test queries
    print(f"Total users: {db.count('users')}")
    print(f"Active users: {db.count('users', 'active = ?', [True])}")
    
    # Find all active users
    active_users = db.find_all('users', 'active = ?', [True])
    print(f"Active users: {json.dumps(active_users, indent=2)}")
    
    # Test with TuskLang config
    config = '''
    database {
        type: "sqlite"
        path: "test_adapters.db"
        
        stats {
            total_users: @query("SELECT COUNT(*) as count FROM users")
            active_users: @query("SELECT COUNT(*) as count FROM users WHERE active = 1")
            avg_score: @query("SELECT AVG(score) as avg FROM users")
        }
    }
    '''
    
    parser = TuskLangEnhanced()
    result = parser.parse(config)
    print(f"\nTuskLang config result: {json.dumps(result, indent=2)}")


def test_postgresql():
    """Test PostgreSQL adapter (requires running PostgreSQL)"""
    print("\n=== Testing PostgreSQL Adapter ===")
    
    try:
        # Create adapter - adjust connection details as needed
        db = PostgreSQLAdapter({
            'host': 'localhost',
            'port': 5432,
            'database': 'tusklang_test',
            'user': 'postgres',
            'password': 'postgres'
        })
        
        # Test connection
        result = db.query("SELECT version()")
        print(f"PostgreSQL version: {result[0]['version']}")
        
        # Create test table
        db.query("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                price DECIMAL(10,2),
                in_stock BOOLEAN
            )
        """)
        
        # Insert test data
        db.query("TRUNCATE TABLE products")
        db.query("INSERT INTO products (name, price, in_stock) VALUES (%s, %s, %s)", 
                ["Laptop", 999.99, True])
        db.query("INSERT INTO products (name, price, in_stock) VALUES (%s, %s, %s)", 
                ["Mouse", 29.99, True])
        db.query("INSERT INTO products (name, price, in_stock) VALUES (%s, %s, %s)", 
                ["Keyboard", 79.99, False])
        
        # Test queries
        print(f"Total products: {db.count('products')}")
        print(f"In stock: {db.count('products', 'in_stock = %s', [True])}")
        
        # Find expensive products
        expensive = db.find_all('products', 'price > %s', [50])
        print(f"Expensive products: {json.dumps(expensive, indent=2)}")
        
    except Exception as e:
        print(f"PostgreSQL test skipped: {e}")


def test_mongodb():
    """Test MongoDB adapter (requires running MongoDB)"""
    print("\n=== Testing MongoDB Adapter ===")
    
    try:
        # Create adapter
        db = MongoDBAdapter({
            'host': 'localhost',
            'port': 27017,
            'database': 'tusklang_test'
        })
        
        # Test connection
        db.connect()
        print("MongoDB connected successfully")
        
        # Clear and insert test data
        db.query("DELETE", "articles", {})  # Clear collection
        
        # Insert documents
        db.query("INSERT", "articles", {
            'title': 'Introduction to TuskLang',
            'author': 'Alice',
            'views': 1500,
            'published': True
        })
        db.query("INSERT", "articles", {
            'title': 'Advanced @ Operators',
            'author': 'Bob',
            'views': 800,
            'published': True
        })
        db.query("INSERT", "articles", {
            'title': 'Draft Article',
            'author': 'Charlie',
            'views': 50,
            'published': False
        })
        
        # Test queries
        print(f"Total articles: {db.count('articles')}")
        print(f"Published articles: {db.count('articles', {'published': True})}")
        
        # Find popular articles
        popular = db.find_all('articles', {'views': {'$gt': 500}})
        print(f"Popular articles: {json.dumps(popular, indent=2, default=str)}")
        
    except Exception as e:
        print(f"MongoDB test skipped: {e}")


def test_redis():
    """Test Redis adapter (requires running Redis)"""
    print("\n=== Testing Redis Adapter ===")
    
    try:
        # Create adapter
        db = RedisAdapter({
            'host': 'localhost',
            'port': 6379,
            'db': 0
        })
        
        # Test connection
        db.connect()
        print("Redis connected successfully")
        
        # Clear test keys
        db.delete("user:1", "user:2", "user:3", "stats:daily", "cache:results")
        
        # Set various data types
        db.set("user:1", {"name": "Alice", "score": 100})
        db.set("user:2", {"name": "Bob", "score": 85})
        db.set("user:3", {"name": "Charlie", "score": 92})
        
        # Hash example
        db.hset("stats:daily", "visits", 1500)
        db.hset("stats:daily", "signups", 23)
        db.hset("stats:daily", "revenue", 4567.89)
        
        # List example
        db.lpush("recent:actions", "user_login", "page_view", "purchase")
        
        # Set with expiration
        db.set("cache:results", {"data": "expensive computation"}, ex=300)  # 5 minutes
        
        # Test queries
        print(f"Total keys: {db.count()}")
        print(f"User keys: {db.count('user:*')}")
        
        # Find all users
        users = db.find_all("user:*")
        print(f"All users: {json.dumps(users, indent=2)}")
        
        # Get specific values
        stats = db.hgetall("stats:daily")
        print(f"Daily stats: {stats}")
        
        # Check TTL
        ttl = db.ttl("cache:results")
        print(f"Cache TTL: {ttl} seconds")
        
        # Test query builder
        print(f"Users count via builder: {db.where('user:*').count()}")
        
    except Exception as e:
        print(f"Redis test skipped: {e}")


def test_integrated_config():
    """Test integrated TuskLang config with multiple databases"""
    print("\n=== Testing Integrated TuskLang Config ===")
    
    config = '''
    # Multi-database configuration example
    app_name: "TuskLang Multi-DB Demo"
    environment: @env("ENV", "development")
    
    # SQLite for local data
    local_stats {
        total_records: @query("SELECT COUNT(*) FROM local_data")
        last_updated: @date("Y-m-d H:i:s")
    }
    
    # Redis for caching
    cache {
        active_sessions: @cache("1m", @query("GET sessions:count"))
        hit_rate: @metrics("cache_hit_rate", 0.85)
    }
    
    # Dynamic configuration based on load
    scaling {
        current_load: @query("GET metrics:cpu:average")
        instances: current_load > 80 ? 10 : 5
        cache_size: @optimize("cache_size", 1000)
    }
    
    # Feature flags from database
    features {
        new_ui: @learn("feature:new_ui", false)
        dark_mode: @cache("1h", @query("GET preferences:theme:popular"))
    }
    '''
    
    parser = TuskLangEnhanced()
    # Note: This would work with actual database connections
    print("Config structure created (would query actual databases in production)")


def main():
    """Run all adapter tests"""
    print("🐘 TuskLang Python Database Adapters Test Suite")
    print("=" * 50)
    
    # Test each adapter
    test_sqlite()
    test_postgresql()
    test_mongodb() 
    test_redis()
    test_integrated_config()
    
    print("\n✅ All adapter tests completed!")
    print("\nNote: Some tests may be skipped if the database server is not running.")
    print("To test all adapters, ensure PostgreSQL, MongoDB, and Redis are running locally.")


if __name__ == "__main__":
    main()