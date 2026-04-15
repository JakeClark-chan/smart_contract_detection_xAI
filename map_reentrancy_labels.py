"""
Script to map Reentrancy labels from soliaudit_dasp_v2.csv
and add them to soliaudit_graph_train.csv and soliaudit_graph_test.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd

# File paths
PROJECT_ROOT = Path(__file__).parent
DASP_V2_FILE = PROJECT_ROOT / "soliaudit_dasp_v2.csv"
GRAPH_TRAIN_FILE = PROJECT_ROOT / "soliaudit_graph_train.csv"
GRAPH_TEST_FILE = PROJECT_ROOT / "soliaudit_graph_test.csv"

# Output files (backup original and create new version)
OUTPUT_TRAIN_FILE = PROJECT_ROOT / "soliaudit_graph_train_with_reentrancy.csv"
OUTPUT_TEST_FILE = PROJECT_ROOT / "soliaudit_graph_test_with_reentrancy.csv"


def load_reentrancy_labels():
    """Load Reentrancy labels from DASP v2 dataset"""
    print(f"Loading Reentrancy labels from {DASP_V2_FILE.name}...")

    # Load only Addr and Reentrancy columns
    df_dasp = pd.read_csv(DASP_V2_FILE, usecols=["Addr", "Reentrancy"])

    # Create mapping: address -> reentrancy_label
    reentrancy_map = {}
    for _, row in df_dasp.iterrows():
        addr = str(row["Addr"]).strip().lower()
        label = int(row["Reentrancy"]) if pd.notna(row["Reentrancy"]) else 0
        reentrancy_map[addr] = label

    print(f"  ✓ Loaded {len(reentrancy_map)} addresses")
    print(f"  ✓ Reentrancy positives: {sum(reentrancy_map.values())}")
    print(
        f"  ✓ Reentrancy negatives: {len(reentrancy_map) - sum(reentrancy_map.values())}"
    )

    return reentrancy_map


def add_reentrancy_to_graph_file(graph_file_path, reentrancy_map, output_file_path):
    """Add Reentrancy column to a graph dataset CSV"""
    print(f"\nProcessing {graph_file_path.name}...")

    # Load the graph dataset
    df_graph = pd.read_csv(graph_file_path)
    print(f"  ✓ Loaded {len(df_graph)} rows")

    # Extract addresses and map Reentrancy labels
    addresses = df_graph["address"].astype(str).str.strip().str.lower()

    # Create Reentrancy column
    df_graph["Reentrancy"] = addresses.apply(lambda addr: reentrancy_map.get(addr, 0))

    # Statistics
    reentrancy_count = df_graph["Reentrancy"].sum()
    total_count = len(df_graph)
    matched_count = sum(1 for addr in addresses if addr in reentrancy_map)

    print(f"  ✓ Matched addresses: {matched_count}/{total_count}")
    print(f"  ✓ Reentrancy positives: {reentrancy_count}")
    print(f"  ✓ Reentrancy negatives: {total_count - reentrancy_count}")
    print(
        f"  ✓ Reentrancy distribution: {reentrancy_count / total_count * 100:.2f}% positive"
    )

    # Save to new file
    df_graph.to_csv(output_file_path, index=False)
    print(f"  ✓ Saved to {output_file_path.name}")

    return df_graph


def verify_columns(file_path):
    """Verify the columns in the output file"""
    print(f"\nVerifying {file_path.name}...")

    # Read just the header to check columns
    df = pd.read_csv(file_path, nrows=0)

    # Check for expected columns
    expected_label_cols = [
        "Denial of Service",
        "Time manipulation",
        "Unchecked Return Values For Low Level Calls",
        "Arithmetic",
        "Reentrancy",
    ]

    print(f"  Columns in file:")
    for col in df.columns:
        print(f"    - {col}")

    print(f"\n  Expected label columns:")
    for col in expected_label_cols:
        exists = col in df.columns
        status = "✓" if exists else "✗"
        print(f"    {status} {col}")

    return all(col in df.columns for col in expected_label_cols)


def main():
    print("=" * 70)
    print("Adding Reentrancy Labels to Graph Datasets")
    print("=" * 70)

    # Step 1: Load Reentrancy mapping from DASP v2
    print("\n[Step 1] Loading Reentrancy labels...")
    reentrancy_map = load_reentrancy_labels()

    # Step 2: Add Reentrancy to train set
    print("\n[Step 2] Processing train dataset...")
    df_train = add_reentrancy_to_graph_file(
        GRAPH_TRAIN_FILE, reentrancy_map, OUTPUT_TRAIN_FILE
    )

    # Step 3: Add Reentrancy to test set
    print("\n[Step 3] Processing test dataset...")
    df_test = add_reentrancy_to_graph_file(
        GRAPH_TEST_FILE, reentrancy_map, OUTPUT_TEST_FILE
    )

    # Step 4: Verify output files
    print("\n[Step 4] Verifying output files...")
    train_ok = verify_columns(OUTPUT_TRAIN_FILE)
    test_ok = verify_columns(OUTPUT_TEST_FILE)

    # Step 5: Summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)

    print(f"\nTrain dataset:")
    print(f"  - Total samples: {len(df_train)}")
    print(f"  - Reentrancy positive: {df_train['Reentrancy'].sum()}")
    print(f"  - Reentrancy negative: {len(df_train) - df_train['Reentrancy'].sum()}")
    print(f"  - Output file: {OUTPUT_TRAIN_FILE.name}")

    print(f"\nTest dataset:")
    print(f"  - Total samples: {len(df_test)}")
    print(f"  - Reentrancy positive: {df_test['Reentrancy'].sum()}")
    print(f"  - Reentrancy negative: {len(df_test) - df_test['Reentrancy'].sum()}")
    print(f"  - Output file: {OUTPUT_TEST_FILE.name}")

    print(f"\nVerification:")
    print(f"  - Train file columns: {'✓ PASS' if train_ok else '✗ FAIL'}")
    print(f"  - Test file columns: {'✓ PASS' if test_ok else '✗ FAIL'}")

    print("\n" + "=" * 70)
    print("✓ Completed successfully!")
    print("=" * 70)

    print("\nNext steps:")
    print("1. Review the output files")
    print("2. Replace original files or update config to use new files")
    print("3. Run: python main.py to train with 5 labels")


if __name__ == "__main__":
    main()
