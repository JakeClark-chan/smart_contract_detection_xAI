# UV Run Guide - Smart Contract Detection with XAI

This guide explains how to use `uv run` to execute the various scripts in this project. `uv` is a fast Python package and project manager that makes it easy to run scripts with proper dependency management.

## Quick Start

### Prerequisites
Make sure you have `uv` installed:
```bash
# On macOS/Linux with Homebrew
brew install uv

# Or install from https://github.com/astral-sh/uv
```

### Initial Setup
```bash
# Sync dependencies (one time setup)
uv sync
```

### Run the GNN Explainer (Recommended for GPU)
```bash
# Quick test (5 epochs, ~5 minutes on GPU)
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 5

# Standard run (10 epochs, ~10 minutes on GPU)
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 10

# Full comprehensive run (200 epochs, ~40+ minutes on GPU)
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 200
```

## Available Commands

### Experimental Dataset Generation

#### 1. **Quick GNN Explainer Test**
```bash
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 5
```
- **Use case**: Testing the pipeline on your device
- **Epochs**: 5
- **Time**: ~5 minutes (GPU) / ~30 minutes (CPU)
- **Output**: 
  - `JakeClark/soliaudit-dasp-ast-sequence-heuristic/train_optimized_heuristic.csv`
  - `JakeClark/soliaudit-dasp-ast-sequence-gnn-explainer/train_optimized_gnn.csv`

#### 2. **Standard GNN Explainer Run**
```bash
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 10
```
- **Use case**: Balanced quality and speed for experimentation
- **Epochs**: 10
- **Time**: ~10 minutes (GPU) / ~60 minutes (CPU)
- **Output**: Complete optimized datasets for both approaches

#### 3. **Full Comprehensive GNN Explainer**
```bash
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 200
```
- **Use case**: Final experimental run for research/publication
- **Epochs**: 200
- **Time**: ~40+ minutes (GPU) / Several hours (CPU)
- **Output**: High-quality explanations with maximum epochs

#### 4. **Quick Subset Test**
```bash
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 5 --subset 100
```
- **Use case**: Rapid testing with small dataset (100 samples)
- **Epochs**: 5
- **Time**: ~1 minute
- **Output**: Limited datasets for validation

#### 5. **Force Regenerate All**
```bash
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 10 --force-reload
```
- **Use case**: Regenerate even if files already exist
- **Epochs**: 10
- **Use when**: You want to overwrite existing results

#### 6. **Heuristic Only (No GNN)**
```bash
uv run python generate_optimized_exp_set.py
```
- **Use case**: Fast baseline without GPU requirement
- **Epochs**: N/A (uses heuristic method)
- **Time**: ~10-15 seconds
- **Output**: Heuristic baseline datasets only

#### 7. **With HuggingFace Upload**
```bash
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 10 --upload-to-hf
```
- **Use case**: Generate and directly upload to HuggingFace Hub
- **Requirements**: 
  - Set `HUGGINGFACE_API_TOKEN` in `.env`
  - Set `HUGGINGFACE_DATASET_NAME` in `config.py`
- **Epochs**: 10
- **Output**: Datasets uploaded to HuggingFace

### Other Scripts

#### Generate Optimized Dataset (Baseline)
```bash
uv run python generate_optimized_dataset.py
```
- Generates the baseline optimized dataset without GNN Explainer
- Useful for comparison experiments

#### Train LLM Model
```bash
uv run python model_trainer.py
```
- Trains the vulnerability detection model
- Requires prepared datasets

#### Test System Setup
```bash
uv run python test_system.py
```
- Verifies GPU availability, dependencies, and configuration
- Run this first to ensure everything is set up correctly

#### Generate Token Counts
```bash
uv run python generate_token_counts.py
```
- Analyzes token counts in datasets

## Command-Line Arguments Guide

### Common Arguments for `generate_optimized_exp_set.py`:

```bash
# Specify number of GNN epochs
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 20

# Use subset of data (faster testing)
uv run python generate_optimized_exp_set.py --use-gnn --subset 500

# Force regenerate (overwrite existing files)
uv run python generate_optimized_exp_set.py --use-gnn --force-reload

# Combine multiple arguments
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 15 --subset 200 --force-reload

# Upload to HuggingFace after generation
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 10 --upload-to-hf
```

### Argument Details:

- `--use-gnn`: Enable GNN Explainer (without it, only heuristic is generated)
- `--gnn-epochs <N>`: Number of epochs for GNN training (default: 10)
- `--subset <N>`: Use only N samples from dataset (for testing)
- `--force-reload`: Regenerate datasets even if files exist
- `--upload-to-hf`: Upload to HuggingFace after generation

## Performance Expectations

### GPU-Accelerated (NVIDIA CUDA)
- **5 epochs**: ~5 minutes
- **10 epochs**: ~10 minutes  
- **200 epochs**: ~40 minutes

### CPU-Only
- **5 epochs**: ~30 minutes
- **10 epochs**: ~60 minutes
- **200 epochs**: ~Several hours

### Recommended GPU Configuration
- NVIDIA RTX 3060 (12GB VRAM) or better
- Minimum 6GB free VRAM

## Output Files

After running the explainer, you'll find:

```
JakeClark/soliaudit-dasp-ast-sequence-heuristic/
  ├── train_optimized_heuristic.csv
  └── test_optimized_heuristic.csv

JakeClark/soliaudit-dasp-ast-sequence-gnn-explainer/
  ├── train_optimized_gnn.csv
  └── test_optimized_gnn.csv
```

Each CSV contains:
- `address`: Smart contract address
- `before_optimized`: Full AST sequence
- `optimized_80p`: 80% of important nodes
- `optimized_50p`: 50% of important nodes
- `optimized_20p`: 20% of important nodes
- Vulnerability labels: Arithmetic, Reentrancy, etc.

## Monitoring GPU Usage

While the explainer runs, monitor GPU usage in another terminal:

```bash
# Watch GPU stats continuously
watch -n 1 nvidia-smi

# Or use individual check
nvidia-smi
```

Expected output during GNN Explainer:
```
| GPU Memory-Usage | 400MiB / 12288MiB |
| GPU-Util         | 3-5%              |
```

**Note**: 3-5% GPU utilization is normal for GNN Explainer due to algorithm bottlenecks, but the computation IS GPU-accelerated.

## Troubleshooting

### Issue: `TOML parse error` or `unknown field`
**Solution**: Make sure `pyproject.toml` is correctly formatted. The file has been fixed.
```bash
uv sync
```

### Issue: `ModuleNotFoundError: No module named 'torch'`
**Solution**: Run `uv sync` to install dependencies
```bash
uv sync
```

### Issue: CUDA out of memory
**Solution**: Use smaller dataset
```bash
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 5 --subset 100
```

### Issue: Very slow performance
**Solution**: Check if running on CPU instead of GPU
```bash
uv run python test_system.py
```

### Issue: Permission denied or command not found
**Solution**: Make sure you're in the project directory
```bash
cd /path/to/smart_contract_detection_xAI
uv sync
uv run python test_system.py
```

## Advanced Usage

### Run Custom Python Commands
```bash
# Direct Python execution
uv run python -c "import torch; print(torch.cuda.is_available())"

# Interactive Python shell
uv run python
```

### View Project Structure
```bash
# List all Python files
uv run python -c "import os; print([f for f in os.listdir() if f.endswith('.py')])"
```

## Environment Variables

Create a `.env` file in the project root for HuggingFace:

```bash
HUGGINGFACE_API_TOKEN=hf_your_token_here
```

Also update `config.py`:
```python
HUGGINGFACE_DATASET_NAME = "your-username/your-dataset-name"
USE_HUGGINGFACE = True
```

## Recommended Workflow

### For Development/Testing:
```bash
# 1. Test system first
uv run python test_system.py

# 2. Quick validation with subset
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 5 --subset 100

# 3. Standard run for experimentation
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 10
```

### For Production/Final Results:
```bash
# 1. Full comprehensive run
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 200

# 2. Optional: Upload to HuggingFace
uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 10 --upload-to-hf
```

### For Baseline Comparison:
```bash
# 1. Generate heuristic baseline
uv run python generate_optimized_exp_set.py

# 2. Generate traditional optimized dataset
uv run python generate_optimized_dataset.py

# 3. Then compare results
```

## Sync and Update Dependencies

```bash
# Initial sync (installs all dependencies)
uv sync

# Update lock file
uv lock --upgrade

# Install with specific Python version
uv sync --python 3.12
```

## Additional Resources

- See `README.md` for project overview
- See `config.py` for configuration options
- See `QUICKSTART.md` for initial setup
- Check logs in `logs/` directory for detailed execution info
- See `UV_MIGRATION.md` for migration details

## Quick Reference Commands

| Task | Command |
|------|---------|
| Setup | `uv sync` |
| Test System | `uv run python test_system.py` |
| Quick Test | `uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 5` |
| Standard Run | `uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 10` |
| Full Run | `uv run python generate_optimized_exp_set.py --use-gnn --gnn-epochs 200` |
| Small Dataset | `uv run python generate_optimized_exp_set.py --use-gnn --subset 100` |
| Regenerate | `uv run python generate_optimized_exp_set.py --use-gnn --force-reload` |
| Baseline | `uv run python generate_optimized_exp_set.py` |
| Upload to HF | `uv run python generate_optimized_exp_set.py --use-gnn --upload-to-hf` |

## Need Help?

1. Check `test_system.py` output for diagnostic information
2. Review logs in `logs/` directory
3. Ensure CUDA is available: `nvidia-smi`
4. Verify dependencies: `uv sync`
5. Check GPU memory: `nvidia-smi`
