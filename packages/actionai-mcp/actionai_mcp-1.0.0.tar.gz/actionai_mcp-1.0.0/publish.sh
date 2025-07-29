#!/bin/bash

# ActionAI MCP Python Package Publishing Script

set -e

echo "🚀 Publishing ActionAI MCP Python Package..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Build the package
echo "📦 Building package..."
python3 -m build

# Check the package
echo "🔍 Checking package..."
python3 -m twine check dist/*

# Upload to PyPI (test first)
echo "📤 Uploading to PyPI..."
if [ "$1" = "--test" ]; then
    echo "📤 Uploading to Test PyPI..."
    python3 -m twine upload --repository testpypi dist/*
else
    echo "📤 Uploading to PyPI..."
    python3 -m twine upload dist/*
fi

echo "✅ Package published successfully!"
echo ""
echo "📋 Usage:"
echo "  # Test connection:"
echo "  uvx actionai-mcp --test"
echo ""
echo "  # Use with Claude Desktop:"
echo '  {'
echo '    "mcpServers": {'
echo '      "actionai-mcp": {'
echo '        "command": "uvx",'
echo '        "args": ["actionai-mcp"],'
echo '        "env": {'
echo '          "MCP_SERVER_URL": "http://localhost:8089/mcp",'
echo '          "ACTIONAI_API_KEY": "client-access-key-2024"'
echo '        }'
echo '      }'
echo '    }'
echo '  }'
