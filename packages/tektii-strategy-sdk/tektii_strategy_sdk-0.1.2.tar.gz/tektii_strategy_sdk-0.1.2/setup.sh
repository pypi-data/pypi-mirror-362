#!/bin/bash
# Setup script for tektii-strategy-sdk

set -e  # Exit on error

echo "Setting up tektii-strategy-sdk..."

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.8 or higher is required. You have Python $python_version"
    exit 1
fi

echo "✓ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate  # Handle Windows

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -e ".[dev]"   # with dev dependencies

# Install protobuf tools
echo "Installing protobuf tools..."
pip install grpcio-tools mypy-protobuf

# Create proto output directory
echo "Creating proto output directory..."
mkdir -p tektii_sdk/proto

# Generate proto files
echo "Generating proto files..."
python -m grpc_tools.protoc \
    -Iproto \
    --python_out=tektii_sdk/proto \
    --grpc_python_out=tektii_sdk/proto \
    proto/strategy.proto

# Fix imports based on OS
echo "Fixing proto imports..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' 's/import strategy_pb2/from . import strategy_pb2/' tektii_sdk/proto/*_grpc.py 2>/dev/null || true
else
    # Linux and others
    sed -i 's/import strategy_pb2/from . import strategy_pb2/' tektii_sdk/proto/*_grpc.py 2>/dev/null || true
fi

# Create __init__.py in proto directory
touch tektii_sdk/proto/__init__.py

# Install pre-commit hooks
if command -v pre-commit &> /dev/null; then
    pre-commit install
    echo "✓ Pre-commit hooks installed"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo ""
echo "To run tests:"
echo "  pytest tests/"
echo ""
echo "To run an example:"
echo "  python examples/simple_ma_strategy.py"
echo ""
