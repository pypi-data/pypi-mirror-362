#!/usr/bin/env python3
"""
TuskLang Python SDK CLI Setup Script
====================================
Installs the CLI as a global command and sets up dependencies
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"   stdout: {e.stdout}")
        if e.stderr:
            print(f"   stderr: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True


def install_dependencies():
    """Install required dependencies"""
    requirements = [
        'requests>=2.25.0',
        'psutil>=5.8.0',
        'pyyaml>=6.0',
        'colorama>=0.4.4'
    ]
    
    for req in requirements:
        if not run_command(f"pip install {req}", f"Installing {req}"):
            return False
    
    return True


def create_cli_script():
    """Create the CLI executable script"""
    script_content = '''#!/usr/bin/env python3
"""
TuskLang CLI Entry Point
========================
Global command-line interface for TuskLang Python SDK
"""

import sys
from pathlib import Path

# Add the SDK directory to Python path
sdk_path = Path(__file__).parent / "sdk-pnt-test" / "python"
sys.path.insert(0, str(sdk_path))

# Import and run the CLI
from cli.main import main

if __name__ == '__main__':
    sys.exit(main())
'''
    
    # Create the script in the project root
    script_path = Path(__file__).parent / "tsk"
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Make it executable
    os.chmod(script_path, 0o755)
    print(f"✅ Created CLI script: {script_path}")
    
    return script_path


def install_global_command(script_path):
    """Install the CLI as a global command"""
    # Try to install to /usr/local/bin (requires sudo)
    global_bin = "/usr/local/bin/tsk"
    
    try:
        # Create symlink
        if os.path.exists(global_bin):
            os.remove(global_bin)
        
        os.symlink(script_path.absolute(), global_bin)
        print(f"✅ Installed global command: {global_bin}")
        return True
    except PermissionError:
        print("⚠️  Could not install to /usr/local/bin (requires sudo)")
        print(f"   CLI script available at: {script_path}")
        print("   You can add it to your PATH or run it directly")
        return False


def setup_ai_config():
    """Set up AI configuration directory"""
    ai_config_dir = Path.home() / '.tsk'
    ai_config_dir.mkdir(exist_ok=True)
    
    ai_config_file = ai_config_dir / 'ai_config.json'
    if not ai_config_file.exists():
        with open(ai_config_file, 'w') as f:
            f.write('{}\n')
        print(f"✅ Created AI config: {ai_config_file}")
    
    return True


def create_completion_script():
    """Create bash completion script"""
    completion_content = '''# TuskLang CLI bash completion
_tsk_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Main commands
    if [[ ${cur} == * ]] ; then
        opts="db serve compile optimize test services cache config binary ai parse validate convert get set version help"
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
    
    # Subcommands based on previous argument
    case "${prev}" in
        db)
            opts="status migrate console backup restore init"
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            ;;
        services)
            opts="start stop restart status"
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            ;;
        cache)
            opts="clear status warm memcached distributed"
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            ;;
        config)
            opts="get check validate compile docs clear-cache stats"
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            ;;
        binary)
            opts="compile execute benchmark optimize"
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            ;;
        ai)
            opts="claude chatgpt custom config setup test complete analyze optimize security"
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            ;;
    esac
}

complete -F _tsk_completion tsk
'''
    
    completion_path = Path.home() / '.tsk' / 'tsk-completion.bash'
    with open(completion_path, 'w') as f:
        f.write(completion_content)
    
    print(f"✅ Created completion script: {completion_path}")
    print("   Add 'source ~/.tsk/tsk-completion.bash' to your ~/.bashrc for auto-completion")
    
    return True


def main():
    """Main setup function"""
    print("🚀 TuskLang Python SDK CLI Setup")
    print("=================================")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create CLI script
    script_path = create_cli_script()
    
    # Install global command
    install_global_command(script_path)
    
    # Setup AI configuration
    setup_ai_config()
    
    # Create completion script
    create_completion_script()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Add 'source ~/.tsk/tsk-completion.bash' to your ~/.bashrc for auto-completion")
    print("   2. Run 'tsk ai setup' to configure AI services")
    print("   3. Run 'tsk help' to see all available commands")
    print("   4. Run 'tsk version' to verify installation")
    
    print(f"\n🔧 CLI script location: {script_path}")
    print("   You can run it directly or add it to your PATH")


if __name__ == '__main__':
    main() 