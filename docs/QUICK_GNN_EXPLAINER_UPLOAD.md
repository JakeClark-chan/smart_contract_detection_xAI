# Quick Start: Upload GNN Explainer Dataset to HuggingFace

## TL;DR - 3 Steps

### 1. Generate the Dataset
```bash
python generate_optimized_exp_set.py --use-gnn --upload-to-hf
```

### 2. Wait for Upload
The script will automatically upload the dataset to HuggingFace Hub.

### 3. Verify
Visit: https://huggingface.co/datasets/JakeClark/soliaudit-dasp-sequence-gnn-explainer

You should see `train-00000-of-00001.parquet` and `test-00000-of-00001.parquet` files.

---

## If You Already Have CSV Files

### Skip generation and upload directly:
```bash
python upload_gnn_explainer_to_hf.py
```

Or upload all variants at once:
```bash
python upload_gcn_gnn_ne_to_hf.py
```

---

## Requirements

✅ `.env` file with `HUGGINGFACE_API_TOKEN=your_token_here`

✅ Local CSV files in: `JakeClark/soliaudit-dasp-sequence-gnn-explainer/`

---

## What Gets Created

After successful upload, the HuggingFace repository will contain:

| Feature | Description |
|---------|-------------|
| `address` | Contract address |
| `before_optimized` | Full sequence (all nodes, ≤512 tokens) |
| `optimized_80p` | 80% of important nodes (GNN-identified) |
| `optimized_50p` | 50% of important nodes |
| `optimized_20p` | 20% of important nodes |
| `Arithmetic` | Label (0/1) |
| `Unchecked Return Values For Low Level Calls` | Label (0/1) |
| `Denial of Service` | Label (0/1) |
| `Time manipulation` | Label (0/1) |
| `Reentrancy` | Label (0/1) |

---

## Advanced Options

### Retrain the GNN model and generate dataset:
```bash
python generate_optimized_exp_set.py --use-gnn --retrain-model --gnn-epochs 50 --upload-to-hf
```

### Generate subset (faster for testing):
```bash
python generate_optimized_exp_set.py --use-gnn --subset 1000 --upload-to-hf
```

### Force regenerate if files already exist:
```bash
python generate_optimized_exp_set.py --use-gnn --force-reload --upload-to-hf
```

---

## Load Dataset After Upload

```python
from datasets import load_dataset

ds = load_dataset("JakeClark/soliaudit-dasp-sequence-gnn-explainer")

# Access splits
train_ds = ds["train"]
test_ds = ds["test"]

# Check a sample
print(train_ds[0])
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "HUGGINGFACE_API_TOKEN not found" | Create `.env` file with your token from https://huggingface.co/settings/tokens |
| "CSV files not found" | Run `python generate_optimized_exp_set.py --use-gnn` to generate them first |
| "Dataset viewer still not available" | Wait 5-10 minutes and refresh browser, or check `.gitattributes` in repo |
| Memory issues | Use `--subset 1000` to process smaller dataset |

---

## Files Updated

- **`upload_gcn_gnn_ne_to_hf.py`** - Now includes GNN Explainer dataset
- **`upload_gnn_explainer_to_hf.py`** - New standalone script (easier to use)
- **`generate_optimized_exp_set.py`** - Can directly upload with `--upload-to-hf`

---

For full documentation, see: `FIX_GNN_EXPLAINER_DATASET.md`
