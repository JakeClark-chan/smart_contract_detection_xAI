#!/bin/bash
# Setup script for Smart Contract Vulnerability Detection with XAI

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║  Smart Contract Vulnerability Detection with XAI - Setup Script         ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check/Install uv
echo "🔍 Checking uv package manager..."
if ! command -v uv &> /dev/null; then
    echo "⚠️  uv is not installed. Installing now..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add uv to PATH for this session
    export PATH="$HOME/.local/bin:$PATH"
    
    # Verify installation
    if ! command -v uv &> /dev/null; then
        echo "❌ Error: Failed to install uv"
        echo "   Please install manually: https://github.com/astral-sh/uv"
        exit 1
    fi
    
    echo "✅ uv installed successfully"
fi
echo "✅ uv $(uv --version)"

# Check Python version
echo ""
echo "🔍 Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Create virtual environment and sync dependencies
echo ""
echo "📦 Setting up virtual environment and installing dependencies..."
echo "   This will create a virtual environment and install all dependencies from pyproject.toml"

# Run uv sync (creates venv if not exists and installs dependencies)
uv sync

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Setup completed successfully!"
    echo ""
    echo "📋 Virtual environment created at: .venv"
    echo ""
    echo "🔓 To activate the virtual environment:"
    echo "   source .venv/bin/activate"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Activate virtual environment: source .venv/bin/activate"
    echo "   2. Ensure soliaudit_dasp_v2.csv is in the project directory"
    echo "   3. Run: python main.py --subset 100  (for quick testing)"
    echo "   4. Run: python main.py  (for full training)"
    echo ""
    echo "💡 Tips:"
    echo "   - Use --help to see all available options"
    echo "   - Check README.md for detailed usage instructions"
    echo "   - Logs will be saved to logs/experiment.log"
    echo ""


    
    # Check GPU (activate venv first)
    echo "🖥️  GPU Status:"
    source .venv/bin/activate
    python3 -c "import torch; print(f'   CUDA available: {torch.cuda.is_available()}'); print(f'   GPU count: {torch.cuda.device_count()}') if torch.cuda.is_available() else None; [print(f'   GPU {i}: {torch.cuda.get_device_name(i)}') for i in range(torch.cuda.device_count())] if torch.cuda.is_available() else None" 2>/dev/null || echo "   (Activate venv to check GPU status)"
    
    echo ""
    echo "🚀 Ready to start!"
else
    echo ""
    echo "❌ Error: Setup failed"
    echo "   Please check the error messages above"
    exit 1
fi
