# Fixing GNN Explainer Dataset Upload to HuggingFace Hub

## Problem

The repository `JakeClark/soliaudit-dasp-sequence-gnn-explainer` is showing:

```
The dataset viewer is not available because its heuristics could not detect any supported data files. You can try uploading some data files, or configuring the data files location manually.
```

While the working reference dataset `JakeClark/soliaudit-dasp-sequence-gnn-no-explainer` correctly displays `test-00000-of-00001.parquet` and `train-00000-of-00001.parquet`.

## Root Cause

HuggingFace Hub automatically converts CSV files to Parquet format when you push datasets using the `datasets` library. However, the GNN Explainer dataset was likely:

1. **Missing local CSV files**: The `train_optimized_gnn.csv` and `test_optimized_gnn.csv` files were never generated or uploaded
2. **Incorrect upload method**: Manual file uploads without using the proper HuggingFace `datasets` library format
3. **Incomplete push**: Upload process failed or was interrupted, leaving the repository in a broken state

## Solution

### Step 1: Generate the GNN Explainer Dataset Locally

If you haven't already generated the optimized dataset files, run:

```bash
python generate_optimized_exp_set.py --use-gnn --upload-to-hf
```

This will:
- Train (or load) a GNN model
- Process all train/test samples using GNN Explainer
- Generate `train_optimized_gnn.csv` and `test_optimized_gnn.csv`
- Save them to `JakeClark/soliaudit-dasp-sequence-gnn-explainer/`

**Parameters:**
- `--use-gnn`: Enable GNN Explainer optimization
- `--upload-to-hf`: Automatically upload to HuggingFace after generation
- `--retrain-model`: Force retrain the GNN model (optional, use if you want fresh model)
- `--gnn-epochs 50`: Increase training epochs for better results (optional, default: 10)

**Example with full setup:**

```bash
python generate_optimized_exp_set.py \
    --use-gnn \
    --retrain-model \
    --gnn-epochs 50 \
    --upload-to-hf
```

### Step 2: Verify Local CSV Files Exist

After generation, verify the files were created:

```bash
ls -lh JakeClark/soliaudit-dasp-sequence-gnn-explainer/
```

You should see:
```
train_optimized_gnn.csv    (~50-100 MB)
test_optimized_gnn.csv     (~10-20 MB)
```

### Step 3: Upload to HuggingFace Hub

If you already have the CSV files but need to upload them, use the standalone upload script:

```bash
python upload_gnn_explainer_to_hf.py
```

Or use the combined upload script for all variants (GCN, GNN Explainer, GNN-no-explainer):

```bash
python upload_gcn_gnn_ne_to_hf.py
```

**Requirements:**
- `.env` file with `HUGGINGFACE_API_TOKEN=your_token_here`
- Local CSV files in correct directories

### Step 4: Verify Upload Success

Check the repository on HuggingFace:
- Go to: https://huggingface.co/datasets/JakeClark/soliaudit-dasp-sequence-gnn-explainer
- You should see:
  - `train-00000-of-00001.parquet` (Parquet file, not CSV)
  - `test-00000-of-00001.parquet`
  - Dataset preview showing rows and columns
  - "Dataset viewer is available" message

### Step 5: Test Loading the Dataset

Verify the dataset loads correctly:

```python
from datasets import load_dataset

# Load the full dataset
ds = load_dataset("JakeClark/soliaudit-dasp-sequence-gnn-explainer")

print(ds)
# Output should show:
# DatasetDict({
#     train: Dataset({features: [...], num_rows: X})
#     test:  Dataset({features: [...], num_rows: Y})
# })

# Access splits
train_ds = ds["train"]
test_ds = ds["test"]

# Check sample
print(train_ds[0])
```

## File Reference

### Key Files Updated

1. **`upload_gcn_gnn_ne_to_hf.py`** (Updated)
   - Now includes GNN Explainer dataset in upload list
   - Handles all three variants: GCN, GNN Explainer, GNN-no-explainer

2. **`upload_gnn_explainer_to_hf.py`** (New)
   - Standalone script for GNN Explainer dataset only
   - Better error messages and validation
   - User-friendly output

3. **`generate_optimized_exp_set.py`** (Existing)
   - Generates GNN Explainer dataset with `--use-gnn` flag
   - Can directly upload with `--upload-to-hf` flag

## Expected Output Structure

After successful upload, the HuggingFace repository should have:

```
JakeClark/soliaudit-dasp-sequence-gnn-explainer/
├── train-00000-of-00001.parquet    # Auto-converted from CSV
├── test-00000-of-00001.parquet     # Auto-converted from CSV
├── README.md                        # Auto-generated dataset card
└── .gitattributes                   # HuggingFace metadata
```

Dataset features should include:
- `address` - Contract address
- `before_optimized` - Full sequence (baseline)
- `optimized_80p` - 80% of important nodes
- `optimized_50p` - 50% of important nodes
- `optimized_20p` - 20% of important nodes
- `Arithmetic` - Label column
- `Unchecked Return Values For Low Level Calls` - Label column
- `Denial of Service` - Label column
- `Time manipulation` - Label column
- `Reentrancy` - Label column

## Comparison with Working Dataset

The `JakeClark/soliaudit-dasp-sequence-gnn-no-explainer` repository works correctly because it:

✅ Has properly converted Parquet files  
✅ Was uploaded using `push_to_hub()` from the `datasets` library  
✅ Has correct dataset structure recognized by HuggingFace heuristics  

Your GNN Explainer dataset will match this format after using the corrected upload scripts.

## Troubleshooting

### Problem: "CSV files not found"

**Solution:** Generate the dataset first:

```bash
python generate_optimized_exp_set.py --use-gnn --force-reload
```

### Problem: "HUGGINGFACE_API_TOKEN not found"

**Solution:** Create `.env` file:

```bash
echo 'HUGGINGFACE_API_TOKEN=hf_your_token_here' > .env
```

Get your token from: https://huggingface.co/settings/tokens

### Problem: "Dataset viewer still not available after upload"

**Solution:** Wait 5-10 minutes for HuggingFace to refresh, then:
1. Clear your browser cache
2. Check the `.gitattributes` file exists in the repo
3. Verify Parquet files are named: `train-00000-of-00001.parquet` (exact naming)

### Problem: Memory issues during generation

**Solution:** Use smaller batches:

```bash
python generate_optimized_exp_set.py --use-gnn --subset 1000
```

## Next Steps

1. Run: `python generate_optimized_exp_set.py --use-gnn --upload-to-hf`
2. Wait 5-10 minutes for processing
3. Visit: https://huggingface.co/datasets/JakeClark/soliaudit-dasp-sequence-gnn-explainer
4. Verify the dataset viewer is now available ✅

## Additional Resources

- HuggingFace Datasets Documentation: https://huggingface.co/docs/datasets/
- Parquet Format Info: https://parquet.apache.org/
- Dataset Push Guide: https://huggingface.co/docs/datasets/upload_dataset