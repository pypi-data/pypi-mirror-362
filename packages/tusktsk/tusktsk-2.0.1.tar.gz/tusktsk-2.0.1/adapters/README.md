# 🐘 TuskLang Python Database Adapters

Complete database adapter collection for TuskLang Enhanced Python, enabling the **killer feature**: configuration files that can query your databases!

## ✨ Available Adapters

### 1. **SQLiteAdapter** - Built-in, zero configuration
Perfect for development, testing, and embedded applications.

### 2. **PostgreSQLAdapter** - Professional SQL database
Enterprise-grade relational database with full SQL support.

### 3. **MongoDBAdapter** - Document database
Flexible NoSQL database for modern applications.

### 4. **RedisAdapter** - In-memory data store
High-performance key-value store for caching and real-time data.

## 🚀 Quick Start

### Installation

```bash
# Basic (SQLite only - no extra dependencies)
pip install tusklang

# With PostgreSQL support
pip install tusklang[postgres]

# With MongoDB support  
pip install tusklang[mongo]

# With Redis support
pip install tusklang[redis]

# Everything
pip install tusklang[all]
```

### Basic Usage

```python
from tsk_enhanced import TuskLangEnhanced
from adapters import SQLiteAdapter, PostgreSQLAdapter, MongoDBAdapter, RedisAdapter

# Use any adapter
db = SQLiteAdapter({'database': 'myapp.db'})
users = db.find_all('users', 'active = ?', [True])

# Or let TuskLang handle it via @query
parser = TuskLangEnhanced()
config = '''
stats {
    total_users: @query("SELECT COUNT(*) FROM users")
    active_users: @query("SELECT COUNT(*) FROM users WHERE active = 1")
}
'''
result = parser.parse(config)
```

## 📝 Adapter Details

### SQLiteAdapter

```python
from adapters import SQLiteAdapter

# Configuration options
db = SQLiteAdapter({
    'database': 'path/to/database.db',  # or ':memory:'
    'timeout': 10.0,
    'check_same_thread': False
})

# Execute queries
results = db.query("SELECT * FROM users WHERE age > ?", [18])

# Convenience methods
count = db.count('users', 'active = ?', [True])
users = db.find_all('users', 'role = ?', ['admin'])
user = db.find_one('users', 'id = ?', [123])
```

### PostgreSQLAdapter

```python
from adapters import PostgreSQLAdapter

# Configuration options
db = PostgreSQLAdapter({
    'host': 'localhost',
    'port': 5432,
    'database': 'myapp',
    'user': 'postgres',
    'password': 'secret'
})

# Same interface as SQLite
products = db.find_all('products', 'price < %s', [100])
```

### MongoDBAdapter

```python
from adapters import MongoDBAdapter

# Configuration options
db = MongoDBAdapter({
    'host': 'localhost',
    'port': 27017,
    'database': 'myapp',
    'username': None,
    'password': None
})

# MongoDB queries
db.query("INSERT", "users", {"name": "Alice", "age": 30})
users = db.find_all('users', {'age': {'$gte': 18}})
count = db.count('users', {'active': True})
```

### RedisAdapter

```python
from adapters import RedisAdapter

# Configuration options
db = RedisAdapter({
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'password': None
})

# Redis operations
db.set('user:1', {'name': 'Alice', 'score': 100})
user = db.get('user:1')

# Pattern matching
user_keys = db.find_all('user:*')
count = db.count('session:*')

# Redis-specific methods
db.expire('cache:results', 300)  # 5 minutes
db.hset('stats', 'visits', 1500)
db.lpush('queue', 'task1', 'task2')
```

## 🥜 peanut.tsk Integration

All adapters automatically load configuration from `peanut.tsk`:

```tsk
# peanut.tsk - Universal TuskLang configuration
database {
    default: "sqlite"
    
    sqlite {
        database: "./data/app.db"
    }
    
    postgresql {
        host: @env("DB_HOST", "localhost")
        port: @env("DB_PORT", "5432")
        database: @env("DB_NAME", "myapp")
        user: @env("DB_USER", "postgres")
        password: @env("DB_PASS", "")
    }
    
    mongodb {
        host: @env("MONGO_HOST", "localhost")
        port: @env("MONGO_PORT", "27017")
        database: "myapp"
    }
    
    redis {
        host: @env("REDIS_HOST", "localhost")
        port: @env("REDIS_PORT", "6379")
        password: @env("REDIS_PASS", null)
    }
}
```

Then in your code:

```python
# Adapters automatically use peanut.tsk configuration
db = SQLiteAdapter.load_from_peanut()
db = PostgreSQLAdapter.load_from_peanut()
db = MongoDBAdapter.load_from_peanut()
db = RedisAdapter.load_from_peanut()
```

## 🎯 The Killer Feature: @query in Configs!

This is what makes TuskLang revolutionary:

```tsk
# config.tsk - Your app configuration
app_name: "My TuskLang App"
version: "2.0.0"

# Static configs are boring. Make them DYNAMIC!
settings {
    # Adjust settings based on database state
    max_upload_size: @query("SELECT value FROM settings WHERE key = 'max_upload'")
    
    # Feature flags from database
    features {
        new_dashboard: @query("SELECT enabled FROM features WHERE name = 'dashboard_v2'")
        ai_mode: @learn("ai_enabled", false)
    }
    
    # Auto-scaling based on metrics
    scaling {
        current_users: @query("SELECT COUNT(*) FROM active_sessions")
        server_count: current_users > 1000 ? 10 : 5
    }
}

# Cache expensive operations
analytics {
    daily_revenue: @cache("5m", @query("SELECT SUM(amount) FROM orders WHERE date = CURRENT_DATE"))
    top_products: @cache("1h", @query("SELECT * FROM products ORDER BY sales DESC LIMIT 10"))
}

# Real-time configuration
rate_limiting {
    # Different limits based on time
    requests_per_minute: @query("SELECT limit FROM rate_limits WHERE hour = EXTRACT(HOUR FROM NOW())")
    
    # Or use Redis for real-time counters
    current_rpm: @query("GET api:requests:minute")
    at_limit: current_rpm > requests_per_minute
}
```

## 🔧 Advanced Usage

### Query Builder Pattern

```python
# SQLite/PostgreSQL style
db = SQLiteAdapter.load_from_peanut()
users = db.where("users").where("age > ?", [18]).order_by("name").limit(10).find()

# MongoDB style
db = MongoDBAdapter.load_from_peanut()
users = db.where("users").where({"age": {"$gt": 18}}).sort("name").limit(10).find()

# Redis style
db = RedisAdapter.load_from_peanut()
sessions = db.where("session:*").type("hash").find()
```

### Connection Pooling

```python
# PostgreSQL with connection pooling
db = PostgreSQLAdapter({
    'host': 'localhost',
    'database': 'myapp',
    'pool_size': 20,
    'max_overflow': 5
})
```

### Async Support (Coming Soon)

```python
# Future async support
async def get_users():
    db = AsyncPostgreSQLAdapter(config)
    return await db.find_all('users', 'active = ?', [True])
```

## 🧪 Testing

```bash
# Run adapter tests
python test_all_adapters.py

# Test specific adapter
python -m pytest test_adapters.py::test_sqlite
python -m pytest test_adapters.py::test_postgresql
python -m pytest test_adapters.py::test_mongodb
python -m pytest test_adapters.py::test_redis
```

## 🐛 Troubleshooting

### "Module not found" errors
- Install required dependencies: `pip install psycopg2-binary pymongo redis`

### Connection refused
- Ensure database server is running
- Check connection parameters in peanut.tsk
- Verify firewall/network settings

### @query returning raw strings
- Make sure you're using `TuskLangEnhanced`, not basic `TuskLang`
- Check that database adapters are properly imported
- Verify adapter configuration is correct

## 🚀 Real-World Examples

### Dynamic Pricing
```tsk
pricing {
    base_price: 99.99
    
    # Adjust price based on demand
    current_stock: @query("SELECT quantity FROM inventory WHERE sku = 'TSK-001'")
    demand_multiplier: current_stock < 10 ? 1.5 : 1.0
    
    final_price: base_price * demand_multiplier
}
```

### A/B Testing
```tsk
experiments {
    # Get experiment config from database
    button_color: @cache("10m", @query("SELECT variant FROM ab_tests WHERE test = 'cta_color' AND user_id = $user_id"))
    
    # Track metrics
    conversion_rate: @metrics("conversion_rate", 0.0)
}
```

### Auto-scaling
```tsk
infrastructure {
    # Scale based on real metrics
    cpu_usage: @query("SELECT AVG(cpu) FROM metrics WHERE time > NOW() - INTERVAL '5 minutes'")
    memory_usage: @query("SELECT AVG(memory) FROM metrics WHERE time > NOW() - INTERVAL '5 minutes'")
    
    needed_instances: cpu_usage > 80 || memory_usage > 90 ? 10 : 5
}
```

## 📚 API Reference

### Common Methods (All Adapters)

- `query(sql, params)` - Execute raw query
- `count(table, where, params)` - Count records
- `find_all(table, where, params)` - Find multiple records
- `find_one(table, where, params)` - Find single record
- `connect()` - Establish connection
- `close()` - Close connection
- `load_from_peanut()` - Load config from peanut.tsk

### Adapter-Specific Methods

See individual adapter files for database-specific methods.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Add tests for new adapters
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**Remember**: With TuskLang, your configuration files are no longer static - they're alive, intelligent, and connected to your data! 🐘