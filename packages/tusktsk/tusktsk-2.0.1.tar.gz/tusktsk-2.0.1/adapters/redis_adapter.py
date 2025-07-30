#!/usr/bin/env python3
"""
Redis Adapter for TuskLang Enhanced Python
=========================================
Enables @query operations with Redis key-value store

DEFAULT CONFIG: peanut.tsk (the bridge of language grace)
"""

import redis
import json
from typing import Any, Dict, List, Union, Optional
from datetime import datetime


class RedisAdapter:
    """Redis database adapter for TuskLang"""
    
    def __init__(self, options: Dict[str, Any] = None):
        self.config = {
            'host': 'localhost',
            'port': 6379,
            'db': 0,
            'password': None,
            'decode_responses': True,
            'socket_timeout': 5.0
        }
        
        if options:
            self.config.update(options)
        
        self.connection = None
    
    def connect(self):
        """Connect to Redis server"""
        if not self.connection:
            self.connection = redis.Redis(
                host=self.config['host'],
                port=self.config['port'],
                db=self.config['db'],
                password=self.config['password'],
                decode_responses=self.config['decode_responses'],
                socket_timeout=self.config['socket_timeout']
            )
            # Test connection
            self.connection.ping()
    
    def query(self, operation: str, *args) -> Any:
        """Execute Redis operation
        
        Examples:
            query("GET", "mykey")
            query("SET", "mykey", "value")
            query("HGET", "myhash", "field")
            query("ZADD", "myset", 1, "member1")
        """
        self.connect()
        
        try:
            # Get the Redis command method
            command = getattr(self.connection, operation.lower())
            result = command(*args)
            
            # Handle different result types
            if isinstance(result, bytes):
                try:
                    # Try to decode JSON
                    return json.loads(result.decode())
                except:
                    return result.decode() if self.config['decode_responses'] else result
            
            return result
            
        except redis.RedisError as e:
            raise Exception(f"Redis error: {str(e)}")
    
    def count(self, pattern: str = "*", type_filter: str = None) -> int:
        """Count keys matching pattern"""
        self.connect()
        
        try:
            if pattern == "*" and not type_filter:
                # Use DBSIZE for total count
                return self.connection.dbsize()
            
            # Use SCAN to count matching keys
            count = 0
            cursor = 0
            
            while True:
                cursor, keys = self.connection.scan(cursor, match=pattern, count=1000)
                
                if type_filter:
                    # Filter by type if specified
                    for key in keys:
                        if self.connection.type(key) == type_filter:
                            count += 1
                else:
                    count += len(keys)
                
                if cursor == 0:
                    break
            
            return count
            
        except redis.RedisError as e:
            raise Exception(f"Redis error: {str(e)}")
    
    def find_all(self, pattern: str = "*", type_filter: str = None, limit: int = None) -> List[Dict[str, Any]]:
        """Find all keys matching pattern with their values"""
        self.connect()
        
        try:
            results = []
            cursor = 0
            found = 0
            
            while True:
                cursor, keys = self.connection.scan(cursor, match=pattern, count=1000)
                
                for key in keys:
                    if limit and found >= limit:
                        return results
                    
                    key_type = self.connection.type(key)
                    
                    if type_filter and key_type != type_filter:
                        continue
                    
                    # Get value based on type
                    if key_type == 'string':
                        value = self.connection.get(key)
                        try:
                            value = json.loads(value)
                        except:
                            pass
                    elif key_type == 'hash':
                        value = self.connection.hgetall(key)
                    elif key_type == 'list':
                        value = self.connection.lrange(key, 0, -1)
                    elif key_type == 'set':
                        value = list(self.connection.smembers(key))
                    elif key_type == 'zset':
                        value = self.connection.zrange(key, 0, -1, withscores=True)
                    else:
                        value = None
                    
                    results.append({
                        'key': key,
                        'type': key_type,
                        'value': value
                    })
                    found += 1
                
                if cursor == 0:
                    break
            
            return results
            
        except redis.RedisError as e:
            raise Exception(f"Redis error: {str(e)}")
    
    def find_one(self, key: str) -> Optional[Dict[str, Any]]:
        """Find one key and its value"""
        self.connect()
        
        try:
            if not self.connection.exists(key):
                return None
            
            key_type = self.connection.type(key)
            
            # Get value based on type
            if key_type == 'string':
                value = self.connection.get(key)
                try:
                    value = json.loads(value)
                except:
                    pass
            elif key_type == 'hash':
                value = self.connection.hgetall(key)
            elif key_type == 'list':
                value = self.connection.lrange(key, 0, -1)
            elif key_type == 'set':
                value = list(self.connection.smembers(key))
            elif key_type == 'zset':
                value = self.connection.zrange(key, 0, -1, withscores=True)
            else:
                value = None
            
            return {
                'key': key,
                'type': key_type,
                'value': value
            }
            
        except redis.RedisError as e:
            raise Exception(f"Redis error: {str(e)}")
    
    # Convenience methods for common operations
    
    def get(self, key: str) -> Any:
        """Get value by key"""
        return self.query("GET", key)
    
    def set(self, key: str, value: Any, ex: int = None) -> bool:
        """Set key-value with optional expiration in seconds"""
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        if ex:
            return self.query("SETEX", key, ex, value)
        else:
            return self.query("SET", key, value)
    
    def delete(self, *keys) -> int:
        """Delete one or more keys"""
        return self.query("DEL", *keys)
    
    def expire(self, key: str, seconds: int) -> bool:
        """Set expiration time for a key"""
        return self.query("EXPIRE", key, seconds)
    
    def ttl(self, key: str) -> int:
        """Get time to live for a key"""
        return self.query("TTL", key)
    
    def hget(self, key: str, field: str) -> Any:
        """Get hash field value"""
        return self.query("HGET", key, field)
    
    def hset(self, key: str, field: str, value: Any) -> int:
        """Set hash field value"""
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return self.query("HSET", key, field, value)
    
    def hgetall(self, key: str) -> Dict[str, Any]:
        """Get all hash fields and values"""
        return self.query("HGETALL", key)
    
    def lpush(self, key: str, *values) -> int:
        """Push values to list"""
        return self.query("LPUSH", key, *values)
    
    def lrange(self, key: str, start: int = 0, end: int = -1) -> List[str]:
        """Get list range"""
        return self.query("LRANGE", key, start, end)
    
    def sadd(self, key: str, *members) -> int:
        """Add members to set"""
        return self.query("SADD", key, *members)
    
    def smembers(self, key: str) -> set:
        """Get all set members"""
        return self.query("SMEMBERS", key)
    
    def zadd(self, key: str, mapping: Dict[str, float]) -> int:
        """Add members to sorted set"""
        args = []
        for member, score in mapping.items():
            args.extend([score, member])
        return self.query("ZADD", key, *args)
    
    def zrange(self, key: str, start: int = 0, end: int = -1, withscores: bool = False) -> Union[List[str], List[tuple]]:
        """Get sorted set range"""
        if withscores:
            return self.query("ZRANGE", key, start, end, "WITHSCORES")
        else:
            return self.query("ZRANGE", key, start, end)
    
    def close(self):
        """Close Redis connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def __del__(self):
        """Cleanup connection on deletion"""
        self.close()
    
    @classmethod
    def load_from_peanut(cls) -> 'RedisAdapter':
        """Load configuration from peanut.tsk"""
        try:
            from tsk_enhanced import TuskLangEnhanced
            parser = TuskLangEnhanced()
            parser.load_peanut()
            
            # Get Redis configuration from peanut.tsk
            config = {
                'host': parser.get('database.redis.host', 'localhost'),
                'port': parser.get('database.redis.port', 6379),
                'db': parser.get('database.redis.db', 0),
                'password': parser.get('database.redis.password', None)
            }
            
            return cls(config)
            
        except Exception as e:
            # If peanut.tsk not found or error, use defaults
            return cls()
    
    # Query builder pattern for TuskLang @query syntax
    
    def where(self, pattern: str) -> 'RedisQueryBuilder':
        """Start a query builder"""
        return RedisQueryBuilder(self, pattern)


class RedisQueryBuilder:
    """Query builder for Redis operations"""
    
    def __init__(self, adapter: RedisAdapter, pattern: str = "*"):
        self.adapter = adapter
        self.pattern = pattern
        self._type_filter = None
        self._limit = None
    
    def type(self, type_filter: str) -> 'RedisQueryBuilder':
        """Filter by key type"""
        self._type_filter = type_filter
        return self
    
    def limit(self, limit: int) -> 'RedisQueryBuilder':
        """Limit results"""
        self._limit = limit
        return self
    
    def count(self) -> int:
        """Count matching keys"""
        return self.adapter.count(self.pattern, self._type_filter)
    
    def find(self) -> List[Dict[str, Any]]:
        """Find all matching keys"""
        return self.adapter.find_all(self.pattern, self._type_filter, self._limit)
    
    def first(self) -> Optional[Dict[str, Any]]:
        """Find first matching key"""
        results = self.adapter.find_all(self.pattern, self._type_filter, 1)
        return results[0] if results else None
    
    def delete(self) -> int:
        """Delete all matching keys"""
        # Get all matching keys
        results = self.adapter.find_all(self.pattern, self._type_filter)
        if not results:
            return 0
        
        keys = [r['key'] for r in results]
        return self.adapter.delete(*keys)
    
    def expire(self, seconds: int) -> int:
        """Set expiration for all matching keys"""
        results = self.adapter.find_all(self.pattern, self._type_filter)
        count = 0
        
        for result in results:
            if self.adapter.expire(result['key'], seconds):
                count += 1
        
        return count