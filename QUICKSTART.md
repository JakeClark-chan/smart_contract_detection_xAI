# Quick Start Guide

## Installation (5 minutes)

1. **Install pydot** (required for CFG parsing):
```bash
# If using uv (recommended)
uv pip install pydot

# Or using pip
pip install pydot
```

2. **Install other dependencies**:
```bash
# Run the setup script
./setup.sh

# Or install manually
pip install -r requirements.txt
```

3. **Verify installation**:
```bash
python test_system.py
```

## Quick Test (2 minutes)

Test with a small subset to ensure everything works:

```bash
python main.py --subset 100 --epochs 1
```

Expected output:
- ✅ Dataset loaded and cached
- ✅ Graphs parsed from DOT format
- ✅ XAI optimization completed
- ✅ Sequences generated
- ✅ Model training started

## Full Run (~30-60 minutes depending on GPU)

```bash
python main.py
```

This will:
1. Load full SoliAudit dataset (~17,980 samples)
2. Process all CFGs (GraphViz DOT format → NetworkX)
3. Optimize graphs using XAI
4. Train BERT model for vulnerability detection
5. Save results to `output/` directory

## Common Commands

### Compare Models
```bash
python main.py --compare-models
```

### Use Different Model
```bash
python main.py --model distilbert  # Faster
python main.py --model codebert    # Code-specific
```

### Skip Optimization (Baseline)
```bash
python main.py --skip-optimization
```

### Force Reload (Clear Cache)
```bash
python main.py --force-reload
```

## Expected Results Location

After running, check:
- `output/experiment_results.json` - Full results
- `output/comparison_results.csv` - Model comparison
- `logs/experiment.log` - Detailed logs
- `models/bert/` - Trained model files
- `cache/*.pkl` - Cached data for faster reruns

## Troubleshooting

### "No module named 'pydot'"
```bash
pip install pydot
```

### Out of Memory
```bash
python main.py --subset 5000
```

### CUDA Out of Memory
Edit `config.py`:
```python
TRAINING_ARGS['per_device_train_batch_size'] = 4  # Reduce from 8
```

## Performance Tips

1. **Use cache**: Don't use `--force-reload` unless necessary
2. **Start small**: Test with `--subset 1000` first
3. **Use DistilBERT**: 40% faster than BERT
4. **Multiple GPUs**: Automatically detected and used

## Next Steps

After successful run:
1. Check `output/comparison_results.csv` for metrics
2. Review `logs/experiment.log` for timing details
3. Compare before/after optimization statistics
4. Try different models with `--model` flag
