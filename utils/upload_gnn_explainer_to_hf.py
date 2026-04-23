"""Standalone script to upload GNN Explainer dataset to HuggingFace Hub.

This script converts local CSV files from the GNN Explainer optimization process
into HuggingFace Parquet format and uploads them to the Hub.

Usage:
    python upload_gnn_explainer_to_hf.py

Requirements:
    - HUGGINGFACE_API_TOKEN in .env file
    - train_optimized_gnn.csv and test_optimized_gnn.csv in JakeClark/soliaudit-dasp-sequence-gnn-explainer/
"""

import os
from pathlib import Path

import pandas as pd
from datasets import Dataset, DatasetDict
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Get HuggingFace token
token = os.getenv("HUGGINGFACE_API_TOKEN")
if not token:
    raise RuntimeError(
        "HUGGINGFACE_API_TOKEN not found in .env file. "
        "Please create a .env file with your HuggingFace API token."
    )

# Dataset configuration
dataset_config = {
    "local_dir": Path("JakeClark/soliaudit-dasp-sequence-gnn-explainer"),
    "train_csv": "train_optimized_gnn.csv",
    "test_csv": "test_optimized_gnn.csv",
    "repo_id": "JakeClark/soliaudit-dasp-sequence-gnn-explainer",
}

print("\n" + "=" * 70)
print("GNN Explainer Dataset Upload to HuggingFace")
print("=" * 70)

# Validate paths
train_path = dataset_config["local_dir"] / dataset_config["train_csv"]
test_path = dataset_config["local_dir"] / dataset_config["test_csv"]

print(f"\nDataset: {dataset_config['repo_id']}")
print(f"Local directory: {dataset_config['local_dir']}")

if not train_path.exists():
    raise FileNotFoundError(f"Train CSV not found: {train_path}")
if not test_path.exists():
    raise FileNotFoundError(f"Test CSV not found: {test_path}")

print(f"  ✓ Train file exists: {train_path}")
print(f"  ✓ Test file exists: {test_path}")

# Read CSV files
print(f"\nReading {train_path.name} ...", end=" ", flush=True)
train_df = pd.read_csv(train_path)
print(f"✓ Loaded {len(train_df):,} rows")

print(f"Reading {test_path.name}  ...", end=" ", flush=True)
test_df = pd.read_csv(test_path)
print(f"✓ Loaded {len(test_df):,} rows")

# Display dataset info
print(f"\nDataset Information:")
print(f"  Train samples: {len(train_df):,}")
print(f"  Test samples: {len(test_df):,}")
print(f"  Columns ({len(train_df.columns)}): {list(train_df.columns)}")

# Create HuggingFace datasets
print(f"\nConverting to HuggingFace format ...", flush=True)
dd = DatasetDict(
    {
        "train": Dataset.from_pandas(train_df, preserve_index=False),
        "test": Dataset.from_pandas(test_df, preserve_index=False),
    }
)

print(f"  ✓ Train: {len(dd['train']):,} samples")
print(f"  ✓ Test: {len(dd['test']):,} samples")

# Upload to HuggingFace Hub
print(f"\nPushing to HuggingFace Hub as Parquet ...", flush=True)
dd.push_to_hub(dataset_config["repo_id"], token=token, private=False)

print(f"\n" + "=" * 70)
print("✅ Upload Complete!")
print("=" * 70)
print(f"\nDataset URL:")
print(f"  https://huggingface.co/datasets/{dataset_config['repo_id']}")
print(f"\nYou can now load this dataset with:")
print(f"  from datasets import load_dataset")
print(f"  ds = load_dataset('{dataset_config['repo_id']}')")
print("\n")
