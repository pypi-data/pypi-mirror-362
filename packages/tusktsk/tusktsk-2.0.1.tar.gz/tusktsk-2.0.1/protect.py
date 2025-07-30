#!/usr/bin/env python3
"""
TuskLang Python SDK Protection Script
Uses PyArmor to protect and obfuscate the SDK
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyarmor():
    """Install PyArmor if not available"""
    try:
        import pyarmor
        print("✅ PyArmor already installed")
        return True
    except ImportError:
        print("📦 Installing PyArmor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyarmor"])
        return True

def protect_sdk():
    """Protect the Python SDK with PyArmor"""
    sdk_dir = Path(__file__).parent
    src_dir = sdk_dir / "src"
    protected_dir = sdk_dir / "protected"
    
    # Create protected directory
    protected_dir.mkdir(exist_ok=True)
    
    # Protect main SDK file
    print("🔒 Protecting Python SDK with PyArmor...")
    
    cmd = [
        sys.executable, "-m", "pyarmor", "obfuscate",
        "--recursive",
        "--output", str(protected_dir),
        str(src_dir / "tsk_protected.py")
    ]
    
    subprocess.check_call(cmd)
    
    # Create loader script
    loader_content = '''#!/usr/bin/env python3
"""
TuskLang Protected Python SDK Loader
Loads protected SDK with license validation
"""

import sys
import os

# Add protected directory to path
protected_dir = os.path.join(os.path.dirname(__file__), "protected")
sys.path.insert(0, protected_dir)

# Import protected SDK
from tsk_protected import init, is_licensed, parse, compile_code, validate

# Initialize with license
license_key = os.environ.get("TUSKLANG_LICENSE")
if not init(license_key):
    print("❌ TuskLang SDK license validation failed")
    sys.exit(1)

print("✅ TuskLang Protected Python SDK loaded successfully")

if __name__ == "__main__":
    print("TuskLang Python SDK - Protected Version")
    print("License Status:", "Valid" if is_licensed() else "Invalid")
'''
    
    with open(protected_dir / "loader.py", "w") as f:
        f.write(loader_content)
    
    # Make loader executable
    os.chmod(protected_dir / "loader.py", 0o755)
    
    print("✅ Python SDK protection complete")
    print(f"Protected files: {protected_dir}")
    print("Run with: python protected/loader.py")

if __name__ == "__main__":
    install_pyarmor()
    protect_sdk() 