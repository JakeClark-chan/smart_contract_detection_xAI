# UV Package Manager Migration Guide

This project has been migrated from `pip` to `uv` for faster package installation and better dependency resolution.

## What Changed

### Setup Scripts
- **`setup.sh`**: Now uses `uv pip` instead of `pip` and `uv venv` for virtual environment creation
- **`setup_windows.ps1`** (NEW): Native PowerShell script for Windows users

### Performance Improvements
- **10-100x faster** package installation
- **Better dependency resolution** with more accurate conflict detection
- **Faster virtual environment creation** with `uv venv`

## Installing uv

### Windows (PowerShell)
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

### macOS/Linux (Bash)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Alternative: Using pipx
```bash
pipx install uv
```

## Using the Setup Scripts

### Windows
```powershell
.\setup_windows.ps1
```

### Linux/macOS/WSL/Git Bash
```bash
bash setup.sh
```

## Command Equivalents

| Old (pip) | New (uv) |
|-----------|----------|
| `pip install <package>` | `uv pip install <package>` |
| `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| `pip list` | `uv pip list` |
| `pip freeze` | `uv pip freeze` |
| `pip uninstall <package>` | `uv pip uninstall <package>` |
| `python -m venv venv` | `uv venv venv` |

## Manual Installation (Without Setup Script)

If you prefer to install manually:

```bash
# Create virtual environment
uv venv venv

# Activate (Linux/macOS/WSL)
source venv/bin/activate

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install PyTorch (CPU)
uv pip install torch torchvision

# Or with CUDA 11.8
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Install PyTorch Geometric
uv pip install torch-geometric torch-scatter torch-sparse

# Install other dependencies
uv pip install -r requirements.txt
```

## Troubleshooting

### uv command not found
- Make sure uv is installed and in your PATH
- On Windows, restart your terminal after installation
- Verify with: `uv --version`

### Virtual environment activation issues
- **Windows Git Bash**: Use `source venv/Scripts/activate` instead of PowerShell activation
- **PowerShell execution policy**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Package installation failures
- Check your internet connection
- Try adding `--no-cache` flag: `uv pip install --no-cache -r requirements.txt`
- For PyTorch CUDA, ensure the CUDA index URL is correct for your GPU

## Benefits of uv

✅ **Speed**: 10-100x faster than pip for most operations  
✅ **Reliability**: Better dependency resolution and conflict detection  
✅ **Compatibility**: Drop-in replacement, works with existing requirements.txt  
✅ **Modern**: Written in Rust, actively maintained by Astral (creators of Ruff)  
✅ **Cross-platform**: Works on Windows, macOS, Linux  

## Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [uv GitHub Repository](https://github.com/astral-sh/uv)
- [Astral Blog](https://astral.sh/blog)
