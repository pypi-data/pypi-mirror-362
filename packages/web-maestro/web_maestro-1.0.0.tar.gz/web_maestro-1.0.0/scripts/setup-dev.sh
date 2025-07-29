#!/bin/bash
set -e

echo "🌐 Setting up Web Maestro development environment..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Not in web-maestro root directory"
    echo "Please run this script from the web-maestro root directory"
    exit 1
fi

# Check Python version
python_version=$(python --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
if [[ $(echo "$python_version >= 3.9" | bc -l) -eq 0 ]]; then
    echo "❌ Error: Python 3.9+ required (found $python_version)"
    exit 1
fi

echo "✅ Python $python_version detected"

# Install or upgrade Hatch
echo "📦 Installing/upgrading Hatch..."
pip install --upgrade hatch

# Create Hatch environment and install dependencies
echo "🔧 Setting up Hatch environment..."
hatch env create

# Install Playwright browsers
echo "🎭 Installing Playwright browsers..."
hatch run playwright install chromium firefox
hatch run playwright install-deps

# Install pre-commit hooks
echo "🪝 Setting up pre-commit hooks..."
hatch run pre-commit install
hatch run pre-commit install --hook-type commit-msg

# Run initial quality checks
echo "🔍 Running initial quality checks..."
hatch run format
echo "✅ Code formatted"

hatch run lint
if [ $? -eq 0 ]; then
    echo "✅ Linting passed"
else
    echo "⚠️  Some linting issues found - run 'hatch run format' to fix automatically"
fi

# Test installation
echo "🧪 Testing package installation..."
if hatch run python -c "import web_maestro; print(f'✅ Web Maestro {web_maestro.__version__} imported successfully')"; then
    echo "✅ Package installation verified"
else
    echo "❌ Package installation failed"
    exit 1
fi

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "Available commands:"
echo "  hatch run format    - Format code with Black and Ruff"
echo "  hatch run lint      - Run linting checks"
echo "  hatch run check     - Run all quality checks"
echo "  hatch run test      - Run tests"
echo "  hatch run test-cov  - Run tests with coverage"
echo ""
echo "Or use Make commands:"
echo "  make format         - Format code"
echo "  make lint           - Run linting"
echo "  make check          - Run all checks"
echo "  make test           - Run tests"
echo ""
echo "To test the installation:"
echo "  python test_streaming.py"
echo "  python test_chelsea_final.py"
echo ""
echo "Happy coding! 🚀"
