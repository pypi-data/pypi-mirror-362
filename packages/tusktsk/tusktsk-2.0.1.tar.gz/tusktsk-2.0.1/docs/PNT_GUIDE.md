# 🥜 Peanut Binary Configuration Guide for Python

A comprehensive guide to using TuskLang's high-performance binary configuration system with Python.

## Table of Contents

- [What is Peanut Configuration?](#what-is-peanut-configuration)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [API Reference](#api-reference)
- [Advanced Usage](#advanced-usage)
- [Python-Specific Features](#python-specific-features)
- [Integration Examples](#integration-examples)
- [Binary Format Details](#binary-format-specification)
- [Performance Guide](#performance-optimization)
- [Troubleshooting](#troubleshooting)
- [Migration Guide](#migration-guide)
- [Complete Examples](#complete-examples)
- [Quick Reference](#quick-reference)

## What is Peanut Configuration?

Peanut Configuration is TuskLang's high-performance binary configuration system that provides:

- **85% faster loading** compared to text-based formats
- **Type-safe configuration** with automatic type inference
- **Hierarchical loading** with CSS-like cascading
- **Binary format** (.pnt) for production use
- **Human-readable** source formats (.peanuts, .tsk)

The system automatically compiles human-readable configuration files into optimized binary format, providing the best of both worlds: developer-friendly source files and production-ready performance.

## Installation

### Prerequisites

- Python 3.8 or higher
- TuskLang Python SDK installed

### Installing the SDK

```bash
# Install from PyPI
pip install tusklang-python

# Or install from source
git clone https://github.com/cyber-boost/python-sdk.git
cd python-sdk
pip install -e .
```

### Importing PeanutConfig

```python
from peanut_config import PeanutConfig
```

## Quick Start

### Your First Peanut Configuration

1. Create a `peanu.peanuts` file:

```ini
[app]
name: "My Python App"
version: "1.0.0"

[server]
host: "localhost"
port: 8080

[database]
url: "postgresql://localhost/mydb"
pool_size: 10
```

2. Load the configuration:

```python
from peanut_config import PeanutConfig

# Load configuration from current directory
config = PeanutConfig.load()

# Access values
app_name = config.get("app.name")
server_port = config.get("server.port", 3000)  # with default
db_url = config.get("database.url")
```

3. Access values with type safety:

```python
# Values are automatically typed
port: int = config.get("server.port")  # Type: int
name: str = config.get("app.name")     # Type: str
pool_size: int = config.get("database.pool_size")  # Type: int

print(f"Starting {name} on port {port}")
```

## Core Concepts

### File Types

- **`.peanuts`** - Human-readable configuration (INI-like syntax)
- **`.tsk`** - TuskLang syntax (advanced features, conditionals, imports)
- **`.pnt`** - Compiled binary format (85% faster loading)

### Hierarchical Loading

PeanutConfig uses CSS-like cascading to load configuration from multiple sources:

```python
# Configuration hierarchy (highest to lowest priority):
# 1. Environment variables
# 2. Command line arguments
# 3. Local peanu.pnt (binary)
# 4. Local peanu.tsk
# 5. Local peanu.peanuts
# 6. Parent directories (recursive)

config = PeanutConfig.load()  # Automatically finds and loads hierarchy
```

### Type System

PeanutConfig automatically infers types from values:

```python
# Type inference examples
config.get("app.port")        # int: 8080
config.get("app.name")        # str: "My App"
config.get("app.debug")       # bool: true
config.get("app.timeout")     # float: 30.5
config.get("app.features")    # list: ["auth", "logging"]
config.get("app.settings")    # dict: {"cache": true, "ssl": false}
```

## API Reference

### PeanutConfig Class

#### Constructor/Initialization

```python
# Basic initialization
config = PeanutConfig()

# With custom directory
config = PeanutConfig.load("/path/to/config")

# With options
config = PeanutConfig.load(
    directory="/path/to/config",
    auto_compile=True,  # Auto-compile .peanuts/.tsk to .pnt
    watch_changes=True  # Watch for file changes
)
```

#### Methods

##### load(directory=None, auto_compile=True, watch_changes=False)

Load configuration from directory hierarchy.

**Parameters:**
- `directory` (str, optional): Starting directory (default: current)
- `auto_compile` (bool): Auto-compile source files to binary (default: True)
- `watch_changes` (bool): Watch for file changes (default: False)

**Returns:** PeanutConfig instance

**Examples:**

```python
# Load from current directory
config = PeanutConfig.load()

# Load from specific directory
config = PeanutConfig.load("/etc/myapp")

# Load with custom options
config = PeanutConfig.load(
    directory="/app/config",
    auto_compile=True,
    watch_changes=True
)
```

##### get(key_path, default_value=None)

Get configuration value by dot-notation path.

**Parameters:**
- `key_path` (str): Configuration key path (e.g., "server.port")
- `default_value` (any): Default value if key not found

**Returns:** Configuration value with inferred type

**Examples:**

```python
# Basic usage
port = config.get("server.port")
name = config.get("app.name", "Default App")

# Nested access
db_host = config.get("database.connection.host")
cache_ttl = config.get("cache.ttl", 3600)

# Array access
first_feature = config.get("features.0")
api_key = config.get("api.keys.0")
```

##### compile(input_file, output_file=None)

Compile source file to binary format.

**Parameters:**
- `input_file` (str): Source file path (.peanuts or .tsk)
- `output_file` (str, optional): Output file path (default: auto-generated)

**Returns:** Output file path

**Examples:**

```python
# Compile .peanuts to .pnt
binary_file = PeanutConfig.compile("config.peanuts")

# Compile with custom output
PeanutConfig.compile("config.peanuts", "production.pnt")

# Compile .tsk file
PeanutConfig.compile("advanced_config.tsk")
```

##### watch(callback)

Watch for configuration file changes.

**Parameters:**
- `callback` (callable): Function called when files change

**Returns:** None

**Examples:**

```python
def on_config_change():
    print("Configuration changed, reloading...")
    config.reload()

# Watch for changes
config.watch(on_config_change)
```

##### reload()

Reload configuration from files.

**Returns:** None

**Examples:**

```python
# Manual reload
config.reload()

# Reload after file changes
def on_change():
    config.reload()
    print("Configuration reloaded")
```

##### get_all()

Get all configuration as dictionary.

**Returns:** dict

**Examples:**

```python
# Get all configuration
all_config = config.get_all()
print(all_config)

# Access nested values
server_config = all_config.get("server", {})
```

##### validate()

Validate configuration against schema.

**Returns:** bool

**Examples:**

```python
# Validate configuration
if config.validate():
    print("Configuration is valid")
else:
    print("Configuration has errors")
```

## Advanced Usage

### File Watching

```python
import time
from peanut_config import PeanutConfig

def on_config_change():
    print("Configuration changed!")
    # Reload configuration
    config.reload()
    # Update application settings
    update_app_settings()

# Load with file watching
config = PeanutConfig.load(watch_changes=True)
config.watch(on_config_change)

# Keep watching
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping file watch")
```

### Custom Serialization

```python
from dataclasses import dataclass
from typing import List, Dict, Any
from peanut_config import PeanutConfig

@dataclass
class ServerConfig:
    host: str
    port: int
    ssl: bool

@dataclass
class AppConfig:
    name: str
    version: str
    servers: List[ServerConfig]
    settings: Dict[str, Any]

# Load and deserialize to custom classes
config = PeanutConfig.load()

# Manual deserialization
server_config = ServerConfig(
    host=config.get("server.host"),
    port=config.get("server.port"),
    ssl=config.get("server.ssl", False)
)

# Or use a helper function
def load_server_config(config: PeanutConfig) -> ServerConfig:
    return ServerConfig(
        host=config.get("server.host"),
        port=config.get("server.port"),
        ssl=config.get("server.ssl", False)
    )
```

### Performance Optimization

```python
from peanut_config import PeanutConfig
import time

# Singleton pattern for shared configuration
class ConfigManager:
    _instance = None
    _config = None
    
    @classmethod
    def get_config(cls):
        if cls._config is None:
            cls._config = PeanutConfig.load()
        return cls._config

# Usage
config = ConfigManager.get_config()

# Caching frequently accessed values
class CachedConfig:
    def __init__(self, config: PeanutConfig):
        self.config = config
        self._cache = {}
    
    def get(self, key: str, default=None):
        if key not in self._cache:
            self._cache[key] = self.config.get(key, default)
        return self._cache[key]
    
    def clear_cache(self):
        self._cache.clear()

# Usage
cached_config = CachedConfig(config)
port = cached_config.get("server.port")  # Cached after first access
```

### Thread Safety

```python
import threading
from peanut_config import PeanutConfig
from typing import Dict, Any

class ThreadSafeConfig:
    def __init__(self, config: PeanutConfig):
        self.config = config
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
    
    def get(self, key: str, default=None):
        with self._lock:
            if key not in self._cache:
                self._cache[key] = self.config.get(key, default)
            return self._cache[key]
    
    def reload(self):
        with self._lock:
            self.config.reload()
            self._cache.clear()

# Usage in multi-threaded applications
config = ThreadSafeConfig(PeanutConfig.load())

def worker():
    port = config.get("server.port")
    print(f"Worker using port: {port}")

# Start multiple threads
threads = [threading.Thread(target=worker) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

## Python-Specific Features

### Async/Await Support

```python
import asyncio
from peanut_config import PeanutConfig

async def load_config_async():
    """Load configuration asynchronously"""
    # Simulate async loading
    await asyncio.sleep(0.1)
    return PeanutConfig.load()

async def main():
    config = await load_config_async()
    port = config.get("server.port")
    print(f"Server port: {port}")

# Run async function
asyncio.run(main())
```

### Type Hints

```python
from typing import Dict, Any, Optional, Union
from peanut_config import PeanutConfig

def get_config_value(key: str, default: Optional[Any] = None) -> Any:
    """Get configuration value with type hints"""
    return PeanutConfig.load().get(key, default)

def get_server_config() -> Dict[str, Union[str, int, bool]]:
    """Get server configuration with specific types"""
    config = PeanutConfig.load()
    return {
        "host": config.get("server.host"),
        "port": config.get("server.port"),
        "ssl": config.get("server.ssl", False)
    }

# Usage with type checking
server_config: Dict[str, Union[str, int, bool]] = get_server_config()
```

### Context Managers

```python
from contextlib import contextmanager
from peanut_config import PeanutConfig

@contextmanager
def config_context(directory: str = None):
    """Context manager for configuration loading"""
    config = PeanutConfig.load(directory)
    try:
        yield config
    finally:
        # Cleanup if needed
        pass

# Usage
with config_context("/app/config") as config:
    port = config.get("server.port")
    print(f"Using port: {port}")
```

### Dataclass Integration

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any
from peanut_config import PeanutConfig

@dataclass
class DatabaseConfig:
    url: str
    pool_size: int = 10
    timeout: float = 30.0
    ssl: bool = False

@dataclass
class AppConfig:
    name: str
    version: str
    debug: bool = False
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    features: List[str] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=dict)

def load_app_config() -> AppConfig:
    """Load configuration into dataclass"""
    config = PeanutConfig.load()
    
    return AppConfig(
        name=config.get("app.name"),
        version=config.get("app.version"),
        debug=config.get("app.debug", False),
        database=DatabaseConfig(
            url=config.get("database.url"),
            pool_size=config.get("database.pool_size", 10),
            timeout=config.get("database.timeout", 30.0),
            ssl=config.get("database.ssl", False)
        ),
        features=config.get("app.features", []),
        settings=config.get("app.settings", {})
    )

# Usage
app_config = load_app_config()
print(f"App: {app_config.name} v{app_config.version}")
print(f"Database: {app_config.database.url}")
```

## Integration Examples

### Flask Integration

```python
from flask import Flask, jsonify
from peanut_config import PeanutConfig

# Load configuration
config = PeanutConfig.load()

# Create Flask app
app = Flask(__name__)

# Configure Flask from PeanutConfig
app.config['SECRET_KEY'] = config.get("app.secret_key", "default-secret")
app.config['DEBUG'] = config.get("app.debug", False)

@app.route('/config')
def get_config():
    """API endpoint to view configuration"""
    return jsonify({
        "app_name": config.get("app.name"),
        "server_port": config.get("server.port"),
        "database_url": config.get("database.url")
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "version": config.get("app.version")
    })

if __name__ == '__main__':
    port = config.get("server.port", 5000)
    app.run(host=config.get("server.host", "localhost"), port=port)
```

### Django Integration

```python
# settings.py
from peanut_config import PeanutConfig

# Load configuration
config = PeanutConfig.load()

# Django settings
SECRET_KEY = config.get("django.secret_key")
DEBUG = config.get("django.debug", False)
ALLOWED_HOSTS = config.get("django.allowed_hosts", [])

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config.get("database.name"),
        'USER': config.get("database.user"),
        'PASSWORD': config.get("database.password"),
        'HOST': config.get("database.host"),
        'PORT': config.get("database.port", 5432),
    }
}

# Static files
STATIC_URL = config.get("static.url", "/static/")
STATIC_ROOT = config.get("static.root")

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': config.get("logging.level", "INFO"),
            'class': 'logging.FileHandler',
            'filename': config.get("logging.file"),
        },
    },
    'root': {
        'handlers': ['file'],
        'level': config.get("logging.level", "INFO"),
    },
}
```

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from peanut_config import PeanutConfig
import uvicorn

# Load configuration
config = PeanutConfig.load()

# Create FastAPI app
app = FastAPI(
    title=config.get("app.name"),
    version=config.get("app.version"),
    debug=config.get("app.debug", False)
)

# Pydantic models
class ConfigResponse(BaseModel):
    app_name: str
    server_port: int
    database_url: str

@app.get("/config", response_model=ConfigResponse)
async def get_config():
    """Get application configuration"""
    return ConfigResponse(
        app_name=config.get("app.name"),
        server_port=config.get("server.port"),
        database_url=config.get("database.url")
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": config.get("app.version"),
        "environment": config.get("app.environment", "development")
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.get("server.host", "localhost"),
        port=config.get("server.port", 8000),
        reload=config.get("app.debug", False)
    )
```

## Binary Format Specification

### File Structure

| Offset | Size | Description |
|--------|------|-------------|
| 0 | 4 | Magic: "PNUT" |
| 4 | 4 | Version (LE) |
| 8 | 8 | Timestamp (LE) |
| 16 | 8 | SHA256 checksum |
| 24 | N | Serialized data |

### Serialization Format

The Python implementation uses a custom binary serialization format optimized for configuration data:

```python
# Binary format structure
struct BinaryHeader {
    magic: bytes[4],      # "PNUT"
    version: uint32,      # Format version
    timestamp: uint64,    # Creation timestamp
    checksum: bytes[32],  # SHA256 of data
}

struct BinaryData {
    header: BinaryHeader,
    data: bytes[],        # Serialized configuration
}
```

### Type Serialization

```python
# Type mapping for serialization
TYPE_MAP = {
    str: 0x01,
    int: 0x02,
    float: 0x03,
    bool: 0x04,
    list: 0x05,
    dict: 0x06,
    None: 0x00
}

# Serialization example
def serialize_value(value):
    if value is None:
        return b'\x00'
    elif isinstance(value, str):
        return b'\x01' + len(value).to_bytes(4, 'little') + value.encode('utf-8')
    elif isinstance(value, int):
        return b'\x02' + value.to_bytes(8, 'little')
    # ... other types
```

## Performance Optimization

### Benchmarks

```python
import time
import json
import yaml
from peanut_config import PeanutConfig

def benchmark_loading():
    """Benchmark different configuration formats"""
    
    # Test data
    test_data = {
        "app": {
            "name": "Test App",
            "version": "1.0.0",
            "debug": True
        },
        "server": {
            "host": "localhost",
            "port": 8080,
            "ssl": False
        },
        "database": {
            "url": "postgresql://localhost/testdb",
            "pool_size": 10,
            "timeout": 30.0
        }
    }
    
    # Create test files
    with open("test.json", "w") as f:
        json.dump(test_data, f)
    
    with open("test.yaml", "w") as f:
        yaml.dump(test_data, f)
    
    with open("test.peanuts", "w") as f:
        f.write("""
[app]
name: "Test App"
version: "1.0.0"
debug: true

[server]
host: "localhost"
port: 8080
ssl: false

[database]
url: "postgresql://localhost/testdb"
pool_size: 10
timeout: 30.0
        """)
    
    # Compile to binary
    PeanutConfig.compile("test.peanuts", "test.pnt")
    
    # Benchmark loading
    iterations = 1000
    
    # JSON loading
    start = time.time()
    for _ in range(iterations):
        with open("test.json", "r") as f:
            json.load(f)
    json_time = time.time() - start
    
    # YAML loading
    start = time.time()
    for _ in range(iterations):
        with open("test.yaml", "r") as f:
            yaml.safe_load(f)
    yaml_time = time.time() - start
    
    # PeanutConfig loading
    start = time.time()
    for _ in range(iterations):
        PeanutConfig.load(".")
    peanut_time = time.time() - start
    
    print(f"JSON loading: {json_time:.4f}s")
    print(f"YAML loading: {yaml_time:.4f}s")
    print(f"PeanutConfig loading: {peanut_time:.4f}s")
    print(f"PeanutConfig is {json_time/peanut_time:.1f}x faster than JSON")
    print(f"PeanutConfig is {yaml_time/peanut_time:.1f}x faster than YAML")

# Run benchmark
benchmark_loading()
```

### Best Practices

1. **Always use .pnt in production**
   ```python
   # Development: Use .peanuts files
   # Production: Use compiled .pnt files
   config = PeanutConfig.load(auto_compile=True)
   ```

2. **Cache configuration objects**
   ```python
   # Singleton pattern
   class Config:
       _instance = None
       
       @classmethod
       def get(cls):
           if cls._instance is None:
               cls._instance = PeanutConfig.load()
           return cls._instance
   ```

3. **Use file watching wisely**
   ```python
   # Only in development
   if os.getenv("ENVIRONMENT") == "development":
       config = PeanutConfig.load(watch_changes=True)
   else:
       config = PeanutConfig.load(watch_changes=False)
   ```

4. **Optimize for your use case**
   ```python
   # For frequently accessed values
   class CachedConfig:
       def __init__(self, config):
           self.config = config
           self._cache = {}
       
       def get(self, key, default=None):
           if key not in self._cache:
               self._cache[key] = self.config.get(key, default)
           return self._cache[key]
   ```

## Troubleshooting

### Common Issues

#### File Not Found

**Problem:** Configuration files not found

**Solution:**
```python
# Check current directory
import os
print(f"Current directory: {os.getcwd()}")

# Specify explicit path
config = PeanutConfig.load("/path/to/config")

# Check file existence
import pathlib
config_dir = pathlib.Path("/path/to/config")
if (config_dir / "peanu.peanuts").exists():
    print("peanu.peanuts found")
if (config_dir / "peanu.pnt").exists():
    print("peanu.pnt found")
```

#### Checksum Mismatch

**Problem:** Binary file corruption

**Solution:**
```python
# Recompile source files
PeanutConfig.compile("config.peanuts")

# Or delete binary and reload
import os
if os.path.exists("peanu.pnt"):
    os.remove("peanu.pnt")
config = PeanutConfig.load()
```

#### Performance Issues

**Problem:** Slow configuration loading

**Solution:**
```python
# Use binary format
config = PeanutConfig.load(auto_compile=True)

# Cache frequently accessed values
class OptimizedConfig:
    def __init__(self):
        self.config = PeanutConfig.load()
        self._cache = {}
    
    def get(self, key, default=None):
        if key not in self._cache:
            self._cache[key] = self.config.get(key, default)
        return self._cache[key]
```

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Load with debug information
config = PeanutConfig.load()
print(f"Loaded from: {config._loaded_files}")
print(f"Hierarchy: {config._hierarchy}")
```

## Migration Guide

### From JSON

```python
import json
from peanut_config import PeanutConfig

# Convert JSON to .peanuts
def json_to_peanuts(json_file, peanuts_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    with open(peanuts_file, 'w') as f:
        for section, values in data.items():
            f.write(f"[{section}]\n")
            for key, value in values.items():
                if isinstance(value, str):
                    f.write(f"{key}: \"{value}\"\n")
                else:
                    f.write(f"{key}: {value}\n")
            f.write("\n")

# Usage
json_to_peanuts("config.json", "config.peanuts")
config = PeanutConfig.load()
```

### From YAML

```python
import yaml
from peanut_config import PeanutConfig

# Convert YAML to .peanuts
def yaml_to_peanuts(yaml_file, peanuts_file):
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    
    with open(peanuts_file, 'w') as f:
        for section, values in data.items():
            f.write(f"[{section}]\n")
            for key, value in values.items():
                if isinstance(value, str):
                    f.write(f"{key}: \"{value}\"\n")
                else:
                    f.write(f"{key}: {value}\n")
            f.write("\n")

# Usage
yaml_to_peanuts("config.yaml", "config.peanuts")
config = PeanutConfig.load()
```

### From .env

```python
import os
from peanut_config import PeanutConfig

# Convert .env to .peanuts
def env_to_peanuts(env_file, peanuts_file):
    with open(env_file, 'r') as f:
        env_vars = {}
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key] = value
    
    with open(peanuts_file, 'w') as f:
        f.write("[app]\n")
        for key, value in env_vars.items():
            if value.isdigit():
                f.write(f"{key}: {value}\n")
            elif value.lower() in ('true', 'false'):
                f.write(f"{key}: {value.lower()}\n")
            else:
                f.write(f"{key}: \"{value}\"\n")

# Usage
env_to_peanuts(".env", "config.peanuts")
config = PeanutConfig.load()
```

## Complete Examples

### Web Application Configuration

**File Structure:**
```
myapp/
├── config/
│   ├── peanu.peanuts
│   ├── peanu.pnt (auto-generated)
│   └── production.peanuts
├── app.py
└── requirements.txt
```

**config/peanu.peanuts:**
```ini
[app]
name: "My Web App"
version: "1.0.0"
debug: true
secret_key: "your-secret-key-here"

[server]
host: "localhost"
port: 8080
workers: 4
timeout: 30

[database]
url: "postgresql://localhost/myapp"
pool_size: 10
max_connections: 100
ssl: false

[redis]
host: "localhost"
port: 6379
db: 0
password: ""

[logging]
level: "INFO"
file: "logs/app.log"
max_size: "10MB"
backup_count: 5
```

**app.py:**
```python
from flask import Flask, jsonify
from peanut_config import PeanutConfig
import logging

# Load configuration
config = PeanutConfig.load("config")

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.get("logging.level", "INFO")),
    filename=config.get("logging.file"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config.get("app.secret_key")
app.config['DEBUG'] = config.get("app.debug", False)

@app.route('/')
def index():
    return jsonify({
        "app": config.get("app.name"),
        "version": config.get("app.version"),
        "status": "running"
    })

@app.route('/config')
def get_config():
    return jsonify({
        "server": {
            "host": config.get("server.host"),
            "port": config.get("server.port")
        },
        "database": {
            "url": config.get("database.url"),
            "pool_size": config.get("database.pool_size")
        }
    })

if __name__ == '__main__':
    app.run(
        host=config.get("server.host"),
        port=config.get("server.port"),
        debug=config.get("app.debug")
    )
```

### Microservice Configuration

**File Structure:**
```
microservice/
├── config/
│   ├── base.peanuts
│   ├── development.peanuts
│   ├── production.peanuts
│   └── peanu.pnt (auto-generated)
├── service.py
└── requirements.txt
```

**config/base.peanuts:**
```ini
[service]
name: "user-service"
version: "1.0.0"

[api]
host: "0.0.0.0"
port: 8000
timeout: 30
rate_limit: 1000

[database]
url: "postgresql://localhost/users"
pool_size: 5
max_connections: 20

[redis]
host: "localhost"
port: 6379
db: 1

[monitoring]
enabled: true
metrics_port: 9090
health_check_interval: 30
```

**service.py:**
```python
from fastapi import FastAPI, HTTPException
from peanut_config import PeanutConfig
import uvicorn
import asyncio

# Load configuration
config = PeanutConfig.load("config")

# Create FastAPI app
app = FastAPI(
    title=config.get("service.name"),
    version=config.get("service.version")
)

@app.get("/health")
async def health_check():
    return {
        "service": config.get("service.name"),
        "version": config.get("service.version"),
        "status": "healthy"
    }

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Simulate database query
    return {
        "id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com"
    }

if __name__ == "__main__":
    uvicorn.run(
        "service:app",
        host=config.get("api.host"),
        port=config.get("api.port"),
        timeout_keep_alive=config.get("api.timeout")
    )
```

### CLI Tool Configuration

**File Structure:**
```
cli-tool/
├── config/
│   ├── peanu.peanuts
│   └── peanu.pnt (auto-generated)
├── cli.py
└── requirements.txt
```

**config/peanu.peanuts:**
```ini
[cli]
name: "My CLI Tool"
version: "1.0.0"
description: "A powerful command-line tool"

[output]
format: "text"
color: true
verbose: false
quiet: false

[api]
base_url: "https://api.example.com"
timeout: 30
retries: 3
api_key: ""

[files]
input_dir: "./input"
output_dir: "./output"
temp_dir: "./temp"
```

**cli.py:**
```python
import click
from peanut_config import PeanutConfig
import os

# Load configuration
config = PeanutConfig.load("config")

@click.group()
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.option('--quiet', is_flag=True, help='Suppress output')
def cli(verbose, quiet):
    """My CLI Tool - A powerful command-line tool"""
    # Override config with command line options
    if verbose:
        config._cache["output.verbose"] = True
    if quiet:
        config._cache["output.quiet"] = True

@cli.command()
@click.argument('input_file')
def process(input_file):
    """Process an input file"""
    if config.get("output.verbose"):
        click.echo(f"Processing {input_file}")
    
    # Process file logic here
    click.echo(f"Processed {input_file}")

@cli.command()
def status():
    """Show tool status"""
    click.echo(f"Tool: {config.get('cli.name')}")
    click.echo(f"Version: {config.get('cli.version')}")
    click.echo(f"API URL: {config.get('api.base_url')}")

if __name__ == '__main__':
    cli()
```

## Quick Reference

### Common Operations

```python
# Load config
config = PeanutConfig.load()

# Get value
value = config.get("key.path", defaultValue)

# Compile to binary
PeanutConfig.compile("config.peanuts", "config.pnt")

# Watch for changes
config.watch(onChange)

# Reload config
config.reload()

# Get all config
all_config = config.get_all()
```

### File Extensions

- `.peanuts` - Human-readable configuration
- `.tsk` - TuskLang syntax (advanced)
- `.pnt` - Binary format (production)

### Type Inference

- `"value"` → str
- `123` → int
- `123.45` → float
- `true/false` → bool
- `[1, 2, 3]` → list
- `{key: value}` → dict

### Performance Tips

1. Use `.pnt` files in production
2. Cache frequently accessed values
3. Use singleton pattern for shared config
4. Enable auto-compilation in development
5. Use file watching only when needed

### Error Handling

```python
try:
    config = PeanutConfig.load()
    value = config.get("required.key")
except FileNotFoundError:
    print("Configuration file not found")
except ValueError as e:
    print(f"Configuration error: {e}")
```

This comprehensive guide provides everything you need to use Peanut Configuration effectively with Python! 