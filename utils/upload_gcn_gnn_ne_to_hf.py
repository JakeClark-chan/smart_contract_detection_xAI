"""One-off: upload GCN, GNN Explainer, and GNN-no-explainer datasets to HuggingFace Hub."""

import os
from pathlib import Path

import pandas as pd
from datasets import Dataset, DatasetDict
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
token = os.getenv("HUGGINGFACE_API_TOKEN")
if not token:
    raise RuntimeError("HUGGINGFACE_API_TOKEN not found in .env")

datasets_to_upload = [
    {
        "local_dir": Path("JakeClark/soliaudit-dasp-sequence-gcn-explainer"),
        "train_csv": "train_optimized_gcn.csv",
        "test_csv": "test_optimized_gcn.csv",
        "repo_id": "JakeClark/soliaudit-dasp-sequence-gcn-explainer",
    },
    {
        "local_dir": Path("JakeClark/soliaudit-dasp-sequence-gnn-explainer"),
        "train_csv": "train_optimized_gnn.csv",
        "test_csv": "test_optimized_gnn.csv",
        "repo_id": "JakeClark/soliaudit-dasp-sequence-gnn-explainer",
    },
    {
        "local_dir": Path("JakeClark/soliaudit-dasp-sequence-gnn-no-explainer"),
        "train_csv": "train_optimized_gnn_ne.csv",
        "test_csv": "test_optimized_gnn_ne.csv",
        "repo_id": "JakeClark/soliaudit-dasp-sequence-gnn-no-explainer",
    },
]

for ds in datasets_to_upload:
    print(f"\n{'=' * 60}")
    print(f"Uploading: {ds['repo_id']}")

    train_path = ds["local_dir"] / ds["train_csv"]
    test_path = ds["local_dir"] / ds["test_csv"]

    if not train_path.exists() or not test_path.exists():
        print(f"  ERROR: CSV files not found in {ds['local_dir']}")
        print(f"    Expected: {train_path.name}, {test_path.name}")
        continue

    print(f"  Reading {train_path.name} ...", end=" ", flush=True)
    train_df = pd.read_csv(train_path)
    print(f"{len(train_df):,} rows")

    print(f"  Reading {test_path.name}  ...", end=" ", flush=True)
    test_df = pd.read_csv(test_path)
    print(f"{len(test_df):,} rows")

    print(f"  Columns: {list(train_df.columns)}")

    dd = DatasetDict(
        {
            "train": Dataset.from_pandas(train_df, preserve_index=False),
            "test": Dataset.from_pandas(test_df, preserve_index=False),
        }
    )

    print(f"  Pushing to Hub as Parquet ...", flush=True)
    dd.push_to_hub(ds["repo_id"], token=token, private=False)
    print(f"  ✅ Done → https://huggingface.co/datasets/{ds['repo_id']}")

print("\n✅ All uploads complete.")
