#!/bin/bash

# Resume Tailor AI - Project Setup Script
# This script sets up the development environment using UV package manager

set -e

echo "🚀 Setting up Resume Tailor AI development environment..."
echo ""

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV package manager is not installed."
    echo "📦 Installing UV..."

    # Install UV
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    else
        echo "Please install UV manually: https://github.com/astral-sh/uv#installation"
        exit 1
    fi

    # Reload shell to get UV in PATH
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "✅ UV package manager found"

# Sync dependencies
echo "📦 Installing dependencies..."
uv sync

echo "🔧 Setting up development tools..."
uv sync --group dev

echo ""
echo "🎉 Setup complete! You can now:"
echo "   • Run the development server: make run"
echo "   • Run tests: make test"  
echo "   • Format code: make format"
echo "   • View all commands: make help"
echo ""
echo "🌐 The application will be available at: http://127.0.0.1:8000"