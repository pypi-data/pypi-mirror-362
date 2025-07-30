#!/usr/bin/env python3
"""
MongoDB Adapter for TuskLang Enhanced Python
==========================================
Enables @query operations with MongoDB collections

DEFAULT CONFIG: peanut.tsk (the bridge of language grace)
"""

import json
from typing import Any, Dict, List, Union, Optional
from datetime import datetime

try:
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False


class MongoDBAdapter:
    """MongoDB database adapter for TuskLang"""
    
    def __init__(self, options: Dict[str, Any] = None):
        if not PYMONGO_AVAILABLE:
            raise Exception('MongoDB adapter requires pymongo. Install it with: pip install pymongo')
        
        self.config = {
            'url': 'mongodb://localhost:27017',
            'database': 'tusklang',
            'connectTimeoutMS': 10000,
            'serverSelectionTimeoutMS': 5000
        }
        
        if options:
            self.config.update(options)
        
        self.client = None
        self.database = None
    
    def connect(self):
        """Connect to MongoDB database"""
        if not self.client:
            try:
                self.client = MongoClient(
                    self.config['url'],
                    connectTimeoutMS=self.config['connectTimeoutMS'],
                    serverSelectionTimeoutMS=self.config['serverSelectionTimeoutMS']
                )
                self.database = self.client[self.config['database']]
                
                # Test connection
                self.client.server_info()
                
            except PyMongoError as e:
                raise Exception(f"MongoDB connection error: {str(e)}")
    
    def query(self, operation: str, *args) -> Any:
        """
        Execute MongoDB query
        MongoDB uses a special query syntax for TuskLang:
        @query("collection.find", {"active": True})
        @query("users.countDocuments", {})
        @query("orders.aggregate", [{"$group": {"_id": None, "total": {"$sum": "$amount"}}}])
        """
        self.connect()
        
        # Parse operation (collection.method)
        if '.' not in operation:
            raise Exception("MongoDB operation must be in format 'collection.method'")
        
        collection_name, method = operation.split('.', 1)
        collection = self.database[collection_name]
        
        try:
            if method == 'find':
                filter_dict = args[0] if args else {}
                options = args[1] if len(args) > 1 else {}
                cursor = collection.find(filter_dict, **options)
                return list(cursor)
                
            elif method == 'findOne':
                filter_dict = args[0] if args else {}
                options = args[1] if len(args) > 1 else {}
                result = collection.find_one(filter_dict, **options)
                return result
                
            elif method == 'countDocuments':
                filter_dict = args[0] if args else {}
                return collection.count_documents(filter_dict)
                
            elif method == 'estimatedDocumentCount':
                return collection.estimated_document_count()
                
            elif method == 'distinct':
                field = args[0] if args else '_id'
                filter_dict = args[1] if len(args) > 1 else {}
                return collection.distinct(field, filter_dict)
                
            elif method == 'aggregate':
                pipeline = args[0] if args else []
                cursor = collection.aggregate(pipeline)
                return list(cursor)
                
            # TuskLang-specific helpers
            elif method == 'count':
                # Alias for countDocuments
                filter_dict = args[0] if args else {}
                return collection.count_documents(filter_dict)
                
            elif method == 'sum':
                # Sum a specific field
                field = args[0] if args else 'amount'
                filter_dict = args[1] if len(args) > 1 else {}
                pipeline = [
                    {'$match': filter_dict},
                    {'$group': {'_id': None, 'total': {'$sum': f'${field}'}}}
                ]
                result = list(collection.aggregate(pipeline))
                return result[0]['total'] if result else 0
                
            elif method == 'avg':
                # Average of a specific field
                field = args[0] if args else 'amount'
                filter_dict = args[1] if len(args) > 1 else {}
                pipeline = [
                    {'$match': filter_dict},
                    {'$group': {'_id': None, 'average': {'$avg': f'${field}'}}}
                ]
                result = list(collection.aggregate(pipeline))
                return result[0]['average'] if result else 0
                
            elif method == 'max':
                # Maximum value of a specific field
                field = args[0] if args else 'amount'
                filter_dict = args[1] if len(args) > 1 else {}
                pipeline = [
                    {'$match': filter_dict},
                    {'$group': {'_id': None, 'maximum': {'$max': f'${field}'}}}
                ]
                result = list(collection.aggregate(pipeline))
                return result[0]['maximum'] if result else None
                
            elif method == 'min':
                # Minimum value of a specific field
                field = args[0] if args else 'amount'
                filter_dict = args[1] if len(args) > 1 else {}
                pipeline = [
                    {'$match': filter_dict},
                    {'$group': {'_id': None, 'minimum': {'$min': f'${field}'}}}
                ]
                result = list(collection.aggregate(pipeline))
                return result[0]['minimum'] if result else None
                
            else:
                raise Exception(f"Unsupported MongoDB method: {method}")
                
        except PyMongoError as e:
            raise Exception(f"MongoDB query error: {str(e)}")
    
    def create_test_data(self):
        """Create test data for MongoDB"""
        self.connect()
        
        # Clear existing collections
        self.database.drop_collection('users')
        self.database.drop_collection('orders')
        self.database.drop_collection('products')
        
        # Create users collection
        users = self.database['users']
        users.insert_many([
            {'name': 'John Doe', 'email': 'john@example.com', 'active': True, 'age': 30},
            {'name': 'Jane Smith', 'email': 'jane@example.com', 'active': True, 'age': 25},
            {'name': 'Bob Wilson', 'email': 'bob@example.com', 'active': False, 'age': 35}
        ])
        
        # Create orders collection
        orders = self.database['orders']
        orders.insert_many([
            {'user_id': 1, 'amount': 99.99, 'status': 'completed', 'created_at': datetime.now()},
            {'user_id': 2, 'amount': 149.50, 'status': 'completed', 'created_at': datetime.now()},
            {'user_id': 1, 'amount': 75.25, 'status': 'pending', 'created_at': datetime.now()}
        ])
        
        # Create products collection
        products = self.database['products']
        products.insert_many([
            {'name': 'Widget A', 'price': 29.99, 'category': 'electronics', 'in_stock': True},
            {'name': 'Widget B', 'price': 49.99, 'category': 'electronics', 'in_stock': True},
            {'name': 'Gadget C', 'price': 19.99, 'category': 'accessories', 'in_stock': False}
        ])
        
        print("MongoDB test data created successfully")
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        try:
            self.connect()
            self.client.server_info()
            return True
        except Exception:
            return False
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            self.client = None
            self.database = None
    
    @staticmethod
    def load_from_peanut():
        """Load MongoDB configuration from peanut.tsk"""
        # Import here to avoid circular imports
        from tsk_enhanced import TuskLangEnhanced
        
        parser = TuskLangEnhanced()
        parser.load_peanut()
        
        config = {}
        
        # Look for MongoDB configuration in peanut.tsk
        if parser.get('database.mongodb.url'):
            config['url'] = parser.get('database.mongodb.url')
        elif parser.get('database.mongo.url'):
            config['url'] = parser.get('database.mongo.url')
        
        if parser.get('database.mongodb.database'):
            config['database'] = parser.get('database.mongodb.database')
        elif parser.get('database.mongo.database'):
            config['database'] = parser.get('database.mongo.database')
        
        if parser.get('database.mongodb.connectTimeoutMS'):
            config['connectTimeoutMS'] = int(parser.get('database.mongodb.connectTimeoutMS'))
        elif parser.get('database.mongo.connectTimeoutMS'):
            config['connectTimeoutMS'] = int(parser.get('database.mongo.connectTimeoutMS'))
        
        if not config:
            raise Exception('No MongoDB configuration found in peanut.tsk')
        
        return MongoDBAdapter(config)


# Command line interface
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("""
MongoDB Adapter for TuskLang Python
===================================

Usage: python mongodb_adapter.py [command] [options]

Commands:
    test                     Create test data
    query <operation> [args] Execute MongoDB operation
    count <collection>       Count documents in collection
    sum <collection> <field> Sum field values
    
Examples:
    python mongodb_adapter.py test
    python mongodb_adapter.py query "users.find" "{}"
    python mongodb_adapter.py count users
    python mongodb_adapter.py sum orders amount

Requirements:
    pip install pymongo
""")
        sys.exit(1)
    
    # Load from peanut.tsk or use defaults
    try:
        adapter = MongoDBAdapter.load_from_peanut()
    except:
        adapter = MongoDBAdapter({
            'url': 'mongodb://localhost:27017',
            'database': 'tusklang_test'
        })
    
    command = sys.argv[1]
    
    if command == 'test':
        try:
            adapter.create_test_data()
        except Exception as e:
            print(f"Error: {e}")
    
    elif command == 'query':
        if len(sys.argv) < 3:
            print("Error: Operation required")
            sys.exit(1)
        
        try:
            operation = sys.argv[2]
            args = []
            
            # Parse additional arguments as JSON
            for arg in sys.argv[3:]:
                try:
                    args.append(json.loads(arg))
                except json.JSONDecodeError:
                    args.append(arg)
            
            result = adapter.query(operation, *args)
            print(json.dumps(result, indent=2, default=str))
        except Exception as e:
            print(f"Error: {e}")
    
    elif command == 'count':
        if len(sys.argv) < 3:
            print("Error: Collection name required")
            sys.exit(1)
        
        try:
            count = adapter.query(f"{sys.argv[2]}.count", {})
            print(f"Count: {count}")
        except Exception as e:
            print(f"Error: {e}")
    
    elif command == 'sum':
        if len(sys.argv) < 4:
            print("Error: Collection name and field required")
            sys.exit(1)
        
        try:
            total = adapter.query(f"{sys.argv[2]}.sum", sys.argv[3], {})
            print(f"Sum: {total}")
        except Exception as e:
            print(f"Error: {e}")
    
    else:
        print(f"Error: Unknown command: {command}")
        sys.exit(1)
    
    adapter.close()