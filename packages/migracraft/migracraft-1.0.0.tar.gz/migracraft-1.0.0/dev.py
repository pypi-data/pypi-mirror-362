#!/usr/bin/env python3
"""
MigraCraft Development Helper

This script provides common development tasks for MigraCraft.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description=""):
    """Run a shell command and return success status"""
    if description:
        print(f"🔧 {description}")
    print(f"   → {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0


def install_dev():
    """Install MigraCraft in development mode"""
    print("📦 Installing MigraCraft in development mode...")
    return run_command("pip install -e '.[dev]'", "Installing with development dependencies")


def run_tests():
    """Run the test suite"""
    print("🧪 Running test suite...")
    return run_command("python run_tests.py", "Running all tests with coverage")


def build_package():
    """Build the package for distribution"""
    print("🏗️ Building MigraCraft package...")
    
    # Clean previous builds
    run_command("rm -rf build/ dist/ *.egg-info/", "Cleaning previous builds")
    
    # Build source and wheel distributions
    success = run_command("python setup.py sdist bdist_wheel", "Building distributions")
    
    if success:
        print("✅ Package built successfully!")
        print("   Files created in dist/:")
        run_command("ls -la dist/", "")
    else:
        print("❌ Package build failed!")
    
    return success


def validate_package():
    """Validate the built package"""
    print("✅ Validating package...")
    return run_command("twine check dist/*", "Checking package with twine")


def lint_code():
    """Run code linting"""
    print("🔍 Linting code...")
    # You can add linting tools here like flake8, black, etc.
    print("   (Add your preferred linting tools here)")
    return True


def generate_entities_demo():
    """Generate demo entities in all supported languages"""
    print("🎨 Generating demo entities...")
    
    languages = ['typescript', 'python', 'dart', 'java', 'cpp', 'csharp', 'go']
    
    for lang in languages:
        cmd = f"python migrate.py --generate-entities {lang} --entities-dir demo_entities/{lang}"
        if not run_command(cmd, f"Generating {lang} entities"):
            return False
    
    print("✅ Demo entities generated in demo_entities/")
    return True


def clean_project():
    """Clean project artifacts"""
    print("🧹 Cleaning project...")
    
    patterns = [
        "__pycache__",
        "*.pyc",
        "*.pyo", 
        "*.egg-info",
        "build/",
        "dist/",
        ".pytest_cache/",
        "htmlcov/",
        ".coverage",
        "demo_entities/",
        "entities/",
        "*.tmp"
    ]
    
    for pattern in patterns:
        run_command(f"find . -name '{pattern}' -exec rm -rf {{}} + 2>/dev/null || true", f"Removing {pattern}")
    
    print("✅ Project cleaned!")
    return True


def show_help():
    """Show available commands"""
    print("""
🛠️ MigraCraft Development Helper

Available commands:
  install     Install MigraCraft in development mode
  test        Run the test suite with coverage
  build       Build the package for distribution
  validate    Validate the built package
  lint        Run code linting
  demo        Generate demo entities in all languages
  clean       Clean project artifacts
  help        Show this help message

Usage:
  python dev.py <command>

Examples:
  python dev.py install
  python dev.py test
  python dev.py build
""")


def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        'install': install_dev,
        'test': run_tests,
        'build': build_package,
        'validate': validate_package,
        'lint': lint_code,
        'demo': generate_entities_demo,
        'clean': clean_project,
        'help': show_help,
    }
    
    if command in commands:
        if command != 'help':
            print(f"🚀 MigraCraft Dev Helper - {command.title()}")
            print("=" * 50)
        
        success = commands[command]()
        
        if command != 'help':
            if success:
                print(f"\n✅ {command.title()} completed successfully!")
            else:
                print(f"\n❌ {command.title()} failed!")
                sys.exit(1)
    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
