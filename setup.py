#!/usr/bin/env python3
"""
Quick setup script for Certificate Management Portal
This script helps set up the development environment
"""

import os
import subprocess
import sys
import time

def run_command(command, cwd=None, shell=False):
    """Run a command and return success status"""
    try:
        if shell:
            result = subprocess.run(command, cwd=cwd, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command.split(), cwd=cwd, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_python():
    """Check if Python 3.8+ is available"""
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✅ Python {version.major}.{version.minor} found")
            return True
        else:
            print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
            return False
    except:
        print("❌ Python not found")
        return False

def check_node():
    """Check if Node.js is available"""
    success, output = run_command("node --version")
    if success:
        version = output.strip()
        print(f"✅ Node.js {version} found")
        return True
    else:
        print("❌ Node.js not found. Please install Node.js 16+")
        return False

def setup_backend():
    """Set up the backend environment"""
    print("\n🔧 Setting up backend...")
    
    # Check if virtual environment exists
    venv_path = os.path.join("backend", "venv")
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        success, output = run_command("python -m venv venv", cwd="backend")
        if not success:
            print(f"❌ Failed to create virtual environment: {output}")
            return False
    
    # Determine activation script based on OS
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
        pip_path = os.path.join(venv_path, "Scripts", "pip")
    else:  # Unix/Linux/macOS
        activate_script = os.path.join(venv_path, "bin", "activate")
        pip_path = os.path.join(venv_path, "bin", "pip")
    
    # Install dependencies
    print("Installing Python dependencies...")
    success, output = run_command(f"{pip_path} install -r requirements.txt", cwd="backend", shell=True)
    if not success:
        print(f"❌ Failed to install dependencies: {output}")
        return False
    
    print("✅ Backend setup complete")
    return True

def setup_frontend():
    """Set up the frontend environment"""
    print("\n🔧 Setting up frontend...")
    
    # Install dependencies
    print("Installing Node.js dependencies...")
    success, output = run_command("npm install", cwd="frontend")
    if not success:
        print(f"❌ Failed to install dependencies: {output}")
        return False
    
    # Create .env file if it doesn't exist
    env_file = os.path.join("frontend", ".env")
    if not os.path.exists(env_file):
        print("Creating .env file...")
        with open(env_file, 'w') as f:
            f.write("REACT_APP_API_URL=http://localhost:8000\n")
            f.write("REACT_APP_WS_URL=ws://localhost:8000\n")
    
    print("✅ Frontend setup complete")
    return True

def main():
    """Main setup function"""
    print("🚀 Certificate Management Portal Setup")
    print("=====================================")
    
    # Check prerequisites
    if not check_python():
        return False
    
    if not check_node():
        return False
    
    # Setup backend
    if not setup_backend():
        return False
    
    # Setup frontend
    if not setup_frontend():
        return False
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Start the backend server:")
    print("   cd backend")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("   uvicorn main:app --reload")
    print("\n2. In another terminal, create admin user:")
    print("   cd backend")
    print("   python create_admin.py")
    print("\n3. In another terminal, start the frontend:")
    print("   cd frontend")
    print("   npm start")
    print("\n4. Open http://localhost:3000 in your browser")
    print("   Login with: admin / admin123456")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)





