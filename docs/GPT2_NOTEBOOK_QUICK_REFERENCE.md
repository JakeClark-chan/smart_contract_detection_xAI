# GPT-2 Notebook - Quick Reference Guide

## 📋 Configuration Checklist

Before running the notebook:

```python
# Cell 3 - EDIT THESE CONSTANTS
MODEL_NAME = "gpt2"                          # ✓ Pre-configured
DATASET_DIR = "/workspace/dataset"           # 🔧 Edit if needed
OUTPUT_BASE = "/workspace/output"            # 🔧 Edit if needed
RESUME_FROM_CHECKPOINT = True                # ✓ Auto-resume enabled
SKIP_COMPLETED = True                        # ✓ Skip finished experiments
```

## 🚀 Running the Notebook

### Quick Start (5 minutes)
```
Cell 0: Setup environment
   ↓
Cell 1-2: Install dependencies
   ↓
Cell 3: Load constants (see experiment status)
   ↓
Cell 4: Load dataset
   ↓
Cell 5: Define helpers
   ↓
Cell 6: Run training (auto-resumes if interrupted!)
   ↓
Cell 7: Show results
```

### If Interrupted
```
✓ Just re-run Cell 6
✓ It will automatically resume from checkpoint
✓ No manual recovery needed
```

## 🔄 Constants & Features

| Constant | Purpose | Default |
|----------|---------|---------|
| `MODEL_NAME` | HuggingFace model ID | `"gpt2"` |
| `DATASET_DIR` | Path to train/test CSV files | `"/workspace/dataset"` |
| `OUTPUT_BASE` | Where to save models & results | `"/workspace/output"` |
| `NUM_EPOCHS` | Training epochs per experiment | `10` |
| `LEARNING_RATE` | AdamW learning rate | `2e-5` |
| `TRAIN_BATCH_SIZE` | Batch size for training | `8` |
| `RESUME_FROM_CHECKPOINT` | Auto-resume from checkpoint | `True` |
| `SKIP_COMPLETED` | Skip already-trained experiments | `True` |

## 📊 Helper Functions in Cell 3

### Checkpoint Management
```python
get_checkpoint_path(column_name)      # → Path to checkpoint directory
checkpoint_exists(column_name)        # → True/False if checkpoint exists
get_latest_checkpoint(column_name)    # → Latest checkpoint path or None
```

### Experiment Tracking
```python
is_experiment_completed(column_name)  # → True/False if model saved
save_experiment_metadata(col, results) # → Saves metadata as JSON
cleanup_checkpoint(column_name)       # → Deletes checkpoint after training
```

## 📁 Output Structure

```
/workspace/output/
├── checkpoints/
│   ├── before_optimized_checkpoint/
│   ├── optimized_80p_checkpoint/
│   ├── optimized_50p_checkpoint/
│   └── optimized_20p_checkpoint/
├── before_optimized/           ← Final model
│   ├── pytorch_model.bin
│   ├── tokenizer.json
│   └── config.json
├── optimized_80p/              ← Final model
├── optimized_50p/              ← Final model
├── optimized_20p/              ← Final model
├── comparison_results.csv
├── experiment_results.json
├── before_optimized_metadata.json
├── optimized_80p_metadata.json
├── optimized_50p_metadata.json
└── optimized_20p_metadata.json
```

## ✅ What Happens at Startup (Cell 3)

When you run Cell 3, it displays:
```
Checking experiment status:
------------------------------------------------------------
  [✓ COMPLETED] before_optimized     ← Already done, will skip
  [⟳ CHECKPOINT] optimized_80p       ← Interrupted, will resume
  [○ NOT STARTED] optimized_50p      ← Will train fresh
  [○ NOT STARTED] optimized_20p      ← Will train fresh
```

## 🎯 Common Scenarios

### Scenario 1: First Run
```
All experiments show "○ NOT STARTED"
→ Cell 6 will train all 4 experiments
→ Each takes ~30-60 min
→ Total time: 2-4 hours
```

### Scenario 2: Interrupted Training
```
Some show "⟳ CHECKPOINT"
→ Cell 6 will resume those experiments
→ Checkpoint automatically detected
→ Seamless recovery, no data loss
```

### Scenario 3: Partial Run
```
Some show "✓ COMPLETED", some "⟳ CHECKPOINT"
→ Cell 6 resumes checkpoints, skips completed
→ Only unfinished work is done
```

### Scenario 4: Start Fresh
```
Set in Cell 3:
RESUME_FROM_CHECKPOINT = False
SKIP_COMPLETED = False
→ Re-trains everything from scratch
```

## 🔧 Advanced Configuration

### For Lower Memory Systems
```python
TRAIN_BATCH_SIZE = 4              # ← Reduce batch size
EVAL_BATCH_SIZE = 4
GRADIENT_ACCUMULATION_STEPS = 4   # ← Or increase accumulation
```

### For Faster Training
```python
NUM_EPOCHS = 3                    # ← Fewer epochs (trade accuracy)
```

### For Debugging
```python
SKIP_COMPLETED = False            # ← Re-run even if completed
RESUME_FROM_CHECKPOINT = False    # ← Start from scratch
```

## 📈 Interpreting Results

After Cell 7, you'll see:
```
Results for before_optimized:
  Train Samples: X, Test Samples: Y
  Train Time: Z min
  Precision: 0.8923    ← Higher is better
  Recall: 0.7654       ← Higher is better
  F1: 0.8234           ← Balanced metric
  Hamming Score: 0.95  ← Lower is better
  Hamming Loss: 0.05
```

Then a comparison CSV:
```
Dataset        | Precision | Recall | F1
before_opt     | 0.8923    | 0.7654 | 0.8234
optimized_80p  | 0.9012    | 0.8123 | 0.8542
...
```

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| "FileNotFoundError: dataset" | Update `DATASET_DIR` in Cell 3 |
| "CUDA out of memory" | Reduce `TRAIN_BATCH_SIZE` in Cell 3 |
| "Skipping all experiments" | Set `SKIP_COMPLETED = False` in Cell 3 |
| "Checkpoint not found" | Check `CHECKPOINT_DIR` exists and is writable |

## 📝 Metadata Files

Each experiment creates a metadata JSON:
```json
{
  "column": "optimized_80p",
  "timestamp": "2024-01-15T10:30:45.123456",
  "model": "gpt2",
  "hyperparameters": {
    "num_epochs": 10,
    "batch_size": 8,
    "learning_rate": 0.00002,
    "max_token_length": 1024
  },
  "results": {
    "train_time": 1234.56,
    "precision": 0.8923,
    "recall": 0.7654,
    "f1": 0.8234,
    "hamming_score": 0.95,
    "hamming_loss": 0.05
  }
}
```

## 🎓 Key Differences from Original

| Aspect | Original | Updated |
|--------|----------|---------|
| Configuration | Hardcoded in cells | Cell 3 constants |
| Interruption | Restart from scratch | Auto-resume |
| Completed experiments | Retrain every time | Skip if done |
| Output paths | Scattered | Centralized |
| Metadata | None | JSON per experiment |
| Status tracking | Manual | Automatic |

## 🔗 Related Files

- `smart-contract-vulnerability-detection-training.ipynb` - Similar pattern, for CodeBERT
- `NOTEBOOK_UPDATE_SUMMARY.md` - Detailed documentation
- `NCKHSV_Graph_SmartContract_Nov2024/` - Research proposal

---

**Need help?** Check the full documentation in `NOTEBOOK_UPDATE_SUMMARY.md`
