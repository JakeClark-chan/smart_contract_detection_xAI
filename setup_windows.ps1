# Setup script for Smart Contract Vulnerability Detection with XAI
# Windows PowerShell version using uv package manager and pyproject.toml

Write-Host "╔══════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Smart Contract Vulnerability Detection with XAI - Setup Script         ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check/Install uv
Write-Host "🔍 Checking uv package manager..." -ForegroundColor Yellow
try {
    $uvVersion = uv --version 2>&1
    Write-Host "✅ $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️  uv is not installed. Installing now..." -ForegroundColor Yellow
    
    try {
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
        
        # Refresh PATH for current session
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        # Verify installation
        $uvVersion = uv --version 2>&1
        Write-Host "✅ uv installed successfully: $uvVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error: Failed to install uv" -ForegroundColor Red
        Write-Host "   Please install manually: irm https://astral.sh/uv/install.ps1 | iex" -ForegroundColor Yellow
        exit 1
    }
}

# Check Python version
Write-Host ""
Write-Host "🔍 Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host $pythonVersion -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Create virtual environment and sync dependencies
Write-Host ""
Write-Host "📦 Setting up virtual environment and installing dependencies..." -ForegroundColor Yellow
Write-Host "   This will create a virtual environment and install all dependencies from pyproject.toml" -ForegroundColor Gray

# Run uv sync (creates venv if not exists and installs dependencies)
uv sync

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Setup completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Virtual environment created at: .venv" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🔓 To activate the virtual environment:" -ForegroundColor Cyan
    Write-Host "   .\.venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 Next steps:" -ForegroundColor Cyan
    Write-Host "   1. Activate virtual environment: .\.venv\Scripts\Activate.ps1"
    Write-Host "   2. Ensure soliaudit_dasp_v2.csv is in the project directory"
    Write-Host "   3. Run: python main.py --subset 100  (for quick testing)"
    Write-Host "   4. Run: python main.py  (for full training)"
    Write-Host ""
    Write-Host "💡 Tips:" -ForegroundColor Cyan
    Write-Host "   - Use --help to see all available options"
    Write-Host "   - Check README.md for detailed usage instructions"
    Write-Host "   - Logs will be saved to logs/experiment.log"
    Write-Host ""
    
    # Check GPU (activate venv first)
    Write-Host "🖥️  GPU Status:" -ForegroundColor Yellow
    & ".\.venv\Scripts\Activate.ps1"
    python -c "import torch; print(f'   CUDA available: {torch.cuda.is_available()}'); print(f'   GPU count: {torch.cuda.device_count()}') if torch.cuda.is_available() else None; [print(f'   GPU {i}: {torch.cuda.get_device_name(i)}') for i in range(torch.cuda.device_count())] if torch.cuda.is_available() else None" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   (Activate venv to check GPU status)" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "🚀 Ready to start!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Error: Setup failed" -ForegroundColor Red
    Write-Host "   Please check the error messages above"
    exit 1
}
