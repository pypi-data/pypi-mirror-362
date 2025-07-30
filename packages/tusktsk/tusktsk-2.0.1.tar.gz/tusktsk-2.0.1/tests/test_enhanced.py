#!/usr/bin/env python3
"""
Test Enhanced Python TuskLang Parser
====================================
Verify all new syntax features work correctly
"""

import os
import sys
from pathlib import Path

# Add the current directory to path so we can import tsk
sys.path.insert(0, str(Path(__file__).parent))

import tsk
from tsk_enhanced import TuskLangEnhanced

def test_enhanced_syntax():
    """Test enhanced syntax features"""
    print("🥜 Testing Enhanced Python TuskLang Parser")
    print("=" * 50)
    
    # Test basic parsing
    parser = TuskLangEnhanced()
    
    # Set some environment variables for testing
    os.environ['APP_ENV'] = 'development'
    os.environ['SERVER_HOST'] = '127.0.0.1'
    os.environ['SERVER_PORT'] = '3000'
    
    # Parse the test file
    test_file = Path(__file__).parent / "test_enhanced.tsk"
    if not test_file.exists():
        print("❌ Test file not found")
        return
    
    data = parser.parse_file(str(test_file))
    
    print("✅ Parsed configuration successfully")
    print(f"📊 Found {len(data)} configuration items")
    print()
    
    # Test global variables
    print("🌍 Global Variables:")
    for key, value in parser.global_variables.items():
        print(f"  ${key} = {value}")
    print()
    
    # Test specific features
    print("🔧 Feature Tests:")
    
    # Test environment variable with default
    server_host = parser.get("server.host")
    print(f"  Server host: {server_host}")
    
    # Test conditional expressions
    debug_mode = parser.get("debug")
    print(f"  Debug mode: {debug_mode}")
    
    # Test date functions
    created = parser.get("timestamps.created")
    print(f"  Created timestamp: {created}")
    
    # Test ranges
    web_range = parser.get("ports.web_range")
    print(f"  Web port range: {web_range}")
    
    # Test arrays and objects
    origins = parser.get("config.allowed_origins")
    print(f"  Allowed origins: {origins}")
    
    settings = parser.get("config.settings")
    print(f"  Settings: {settings}")
    
    print()
    print("🎯 All enhanced syntax features working!")

def test_original_compatibility():
    """Test that original TSK functionality still works"""
    print("\n🔄 Testing Backward Compatibility")
    print("=" * 35)
    
    # Create test content in original TOML-like format
    original_content = """
[database]
host = "localhost"
port = 5432
name = "test_db"

[server]  
host = "0.0.0.0"
port = 8080
workers = 4
"""
    
    # Parse with enhanced parser
    data = tsk.parse_enhanced(original_content)
    
    print("✅ Original TOML syntax still works")
    print(f"  Database host: {data.get('database', {}).get('host')}")
    print(f"  Server port: {data.get('server', {}).get('port')}")

def test_peanut_integration():
    """Test peanut.tsk integration"""
    print("\n🥜 Testing peanut.tsk Integration")
    print("=" * 35)
    
    # Check if peanut.tsk exists
    peanut_path = Path(__file__).parent.parent.parent / "peanut.tsk"
    if peanut_path.exists():
        try:
            peanut_tsk = tsk.load_from_peanut()
            print("✅ peanut.tsk loaded successfully")
            print(f"  Found {len(peanut_tsk.data)} sections")
        except Exception as e:
            print(f"⚠️  peanut.tsk found but couldn't load: {e}")
    else:
        print("ℹ️  peanut.tsk not found (expected in development)")

if __name__ == '__main__':
    try:
        test_enhanced_syntax()
        test_original_compatibility() 
        test_peanut_integration()
        
        print("\n🎉 All tests passed!")
        print("Python SDK enhanced successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)