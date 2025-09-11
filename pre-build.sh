#!/usr/bin/env bash

echo "🔧 Pre-build: Ensuring Python 3.9 environment..."

# Set Python version explicitly
export PYTHON_VERSION="3.9.19"

# Check if we have Python 3.9
if command -v python3.9 &> /dev/null; then
    echo "✅ Found python3.9, creating symlink..."
    ln -sf $(which python3.9) ./python
    export PATH="$PWD:$PATH"
elif python --version | grep -q "3.9"; then
    echo "✅ Current python is 3.9"
else
    echo "❌ Python 3.9 not found!"
    echo "Available Python versions:"
    ls -la /usr/bin/python* 2>/dev/null || echo "No python binaries found in /usr/bin/"
    
    # Try to find any Python 3.9 installation
    find /usr -name "python3.9*" -type f 2>/dev/null | head -5
    
    echo "Environment variables:"
    env | grep -i python || echo "No Python-related environment variables"
    
    echo "Current Python version:"
    python --version
    
    exit 1
fi

echo "✅ Pre-build Python setup complete"
