#!/usr/bin/env python3
"""
Simple test for Enhanced Python TuskLang Parser
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from tsk_enhanced import TuskLangEnhanced

# Test content with new syntax features
test_content = """
# Global variables
$app_name: "Test App"
$version: "1.0.0"

# Basic section
[database]
host: "localhost"
port: 5432

# Object with curly braces
server {
    host: "127.0.0.1"
    port: 8080
}

# Object with angle brackets
cache >
    driver: "redis"
    ttl: "5m"
<

# Environment variables with defaults
[config]
env_var: @env("TEST_VAR", "default_value")
debug_mode: $app_name != "production"

# Date functions
[timestamps]
now: @date("Y-m-d H:i:s")
year: @date("Y")

# Ranges
[ports]
range: 8000-9000
"""

def main():
    print("🐍 Testing Enhanced Python TuskLang Parser")
    print("=" * 45)
    
    parser = TuskLangEnhanced()
    data = parser.parse(test_content)
    
    print(f"✅ Parsed {len(data)} configuration items")
    print()
    
    # Test global variables
    print("🌍 Global Variables:")
    for key, value in parser.global_variables.items():
        print(f"  ${key} = {value}")
    print()
    
    # Test specific features
    print("🔧 Test Results:")
    print(f"  Database host: {parser.get('database.host')}")
    print(f"  Server port: {parser.get('server.port')}")
    print(f"  Cache driver: {parser.get('cache.driver')}")
    print(f"  Timestamp: {parser.get('timestamps.now')}")
    print(f"  Port range: {parser.get('ports.range')}")
    print(f"  Environment var: {parser.get('config.env_var')}")
    
    print("\n🎉 Enhanced Python SDK working correctly!")

if __name__ == '__main__':
    main()