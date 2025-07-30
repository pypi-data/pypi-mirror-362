#!/usr/bin/env python3
"""
Setup script for Federated Learning Client CLI
"""
from pathlib import Path
import os
import sys

def create_directories():
    """Create necessary directories for the federated learning client."""
    directories = [
        "models",
        "logs", 
        "results",
        "data"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        "pandas",
        "sklearn",
        "typer",
        "rich",
        "requests",
        "numpy"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is missing")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install them with: pip install -r requirements.txt")
        return False
    
    return True

def make_executable():
    """Make the CLI script executable."""
    cli_path = Path("cli.py")
    if cli_path.exists():
        os.chmod(cli_path, 0o755)
        print("✓ Made cli.py executable")
    else:
        print("✗ cli.py not found")

def main():
    """Main setup function."""
    print("🚀 Setting up Federated Learning Client CLI")
    print("=" * 50)
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    deps_ok = check_dependencies()
    
    # Make executable
    print("\n🔧 Setting permissions...")
    make_executable()
    
    print("\n" + "=" * 50)
    if deps_ok:
        print("✅ Setup completed successfully!")
        print("\nYou can now use the CLI:")
        print("  python cli.py info")
        print("  python cli.py train ./data/sample_diabetes_client1.csv")
    else:
        print("❌ Setup incomplete - please install missing dependencies")
        sys.exit(1)

if __name__ == "__main__":
    main()
