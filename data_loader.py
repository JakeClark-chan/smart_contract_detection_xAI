"""
Data Loader for Smart Contract Vulnerability Detection
Handles CSV loading with separate train/test files containing all 5 vulnerability labels
"""

from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

import config
from utils import Timer, get_logger, load_pickle, pickle_exists, save_pickle, timeit

logger = get_logger(__name__)


class VulnerabilityDataset:
    """
    Dataset class for smart contract vulnerability detection
    Stores addresses, AST data, and multi-label vulnerability annotations
    """

    def __init__(self, addresses: List[str], asts: List[str], labels: np.ndarray):
        """
        Initialize dataset

        Args:
            addresses: List of contract addresses
            asts: List of AST JSON strings
            labels: Multi-label array (N x num_labels)
        """
        self.addresses = addresses
        self.asts = asts  # Changed from cfgs to asts
        self.labels = labels

        # Validate sizes
        assert len(addresses) == len(asts) == len(labels), (
            f"Size mismatch: addresses={len(addresses)}, asts={len(asts)}, labels={len(labels)}"
        )

    def __len__(self):
        return len(self.addresses)

    def __getitem__(self, idx):
        return {
            "address": self.addresses[idx],
            "ast": self.asts[idx],  # Changed from cfg to ast
            "labels": self.labels[idx],
        }

    def get_label_distribution(self) -> Dict:
        """Get distribution of each vulnerability label"""
        label_names = config.DATASET_COLUMNS["labels"]
        distribution = {}

        for i, label_name in enumerate(label_names):
            count = np.sum(self.labels[:, i])
            percentage = (count / len(self)) * 100
            display_name = config.LABEL_DISPLAY_NAMES.get(label_name, label_name)
            distribution[display_name] = {"count": int(count), "percentage": percentage}

        return distribution

    def print_statistics(self):
        """Print dataset statistics"""
        logger.info(f"\n{'=' * 70}")
        logger.info(f"Dataset Statistics:")
        logger.info(f"{'=' * 70}")
        logger.info(f"Total samples: {len(self)}")
        logger.info(f"Label distribution:")

        dist = self.get_label_distribution()
        for label_name, stats in dist.items():
            logger.info(
                f"  - {label_name}: {stats['count']} ({stats['percentage']:.2f}%)"
            )

        # Multi-label statistics
        samples_with_labels = np.sum(np.sum(self.labels, axis=1) > 0)
        samples_with_multiple = np.sum(np.sum(self.labels, axis=1) > 1)

        logger.info(f"\nMulti-label statistics:")
        logger.info(
            f"  - Samples with at least 1 vulnerability: {samples_with_labels} ({samples_with_labels / len(self) * 100:.2f}%)"
        )
        logger.info(
            f"  - Samples with multiple vulnerabilities: {samples_with_multiple} ({samples_with_multiple / len(self) * 100:.2f}%)"
        )
        logger.info(f"{'=' * 70}\n")


def load_reentrancy_mapping() -> Dict[str, int]:
    """
    Load Reentrancy labels from DASP v2 file and create address->label mapping

    Returns:
        Dictionary mapping address to Reentrancy label (0 or 1)
    """
    logger.info(
        f"Loading Reentrancy mapping from {config.REENTRANCY_MAPPING_PATH.name}"
    )

    if not config.REENTRANCY_MAPPING_PATH.exists():
        logger.warning(
            f"Reentrancy mapping file not found: {config.REENTRANCY_MAPPING_PATH}"
        )
        return {}

    try:
        # Load only address and Reentrancy columns
        df = pd.read_csv(config.REENTRANCY_MAPPING_PATH, usecols=["Addr", "Reentrancy"])

        # Create mapping dictionary
        mapping = {}
        for _, row in df.iterrows():
            addr = str(row["Addr"]).strip().lower()
            reentrancy = int(row["Reentrancy"]) if not pd.isna(row["Reentrancy"]) else 0
            mapping[addr] = reentrancy

        logger.info(f"Loaded Reentrancy mapping for {len(mapping)} addresses")
        logger.info(f"  - Reentrancy positives: {sum(mapping.values())}")

        return mapping

    except Exception as e:
        logger.error(f"Error loading Reentrancy mapping: {e}")
        return {}


@timeit
def load_dataset_from_file(file_path: Path) -> VulnerabilityDataset:
    """
    Load dataset from a single CSV file (train or test)
    All 5 labels are loaded directly from the CSV file

    Args:
        file_path: Path to CSV file

    Returns:
        VulnerabilityDataset object
    """
    logger.info(f"Loading dataset from: {file_path.name}")

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    with Timer(f"Loading {file_path.name}", logger):
        # Load only required columns
        required_cols = [
            config.DATASET_COLUMNS["address"],
            config.DATASET_COLUMNS["ast"],
        ]
        # Add all 5 label columns (now all are directly in the CSV)
        required_cols.extend(config.DATASET_COLUMNS["labels"])

        df = pd.read_csv(file_path, usecols=required_cols)

    logger.info(f"Loaded {len(df)} rows from CSV")

    # Extract data
    logger.info("Extracting data...")

    # Get addresses
    addresses = df[config.DATASET_COLUMNS["address"]].astype(str).tolist()

    # Get AST data
    asts = df[config.DATASET_COLUMNS["ast"]].astype(str).tolist()

    # Get all 5 labels directly from the CSV
    labels_list = []
    for col in config.DATASET_COLUMNS["labels"]:
        labels_list.append(df[col].values)

    # Stack into 2D array
    labels = np.column_stack(labels_list).astype(np.float32)

    # Handle NaN values in labels (treat as 0)
    labels = np.nan_to_num(labels, nan=0.0)

    # Remove samples with invalid AST
    valid_indices = []
    for i, ast in enumerate(asts):
        if ast and ast != "nan" and ast != "None" and len(ast) > 50:
            valid_indices.append(i)

    logger.info(f"Valid samples (with AST): {len(valid_indices)} / {len(df)}")

    # Filter data
    addresses = [addresses[i] for i in valid_indices]
    asts = [asts[i] for i in valid_indices]
    labels = labels[valid_indices]

    # Create dataset
    dataset = VulnerabilityDataset(addresses, asts, labels)

    return dataset


@timeit
def load_dataset_from_huggingface(split: str) -> VulnerabilityDataset:
    """
    Load dataset from HuggingFace Hub

    Args:
        split: 'train' or 'test'

    Returns:
        VulnerabilityDataset object
    """
    from datasets import load_dataset

    logger.info(
        f"Loading {split} dataset from HuggingFace: {config.HUGGINGFACE_DATASET_NAME}"
    )

    # Load dataset from HuggingFace Hub
    ds = load_dataset(config.HUGGINGFACE_DATASET_NAME, split=split)

    logger.info(f"  Loaded {len(ds)} samples from HuggingFace")

    # Extract data
    logger.info("Extracting data...")

    # Get addresses
    addresses = ds[config.DATASET_COLUMNS["address"]]

    # Get AST data
    asts = ds[config.DATASET_COLUMNS["ast"]]

    # Get all 5 labels directly from the dataset
    labels_list = []
    for col in config.DATASET_COLUMNS["labels"]:
        labels_list.append(np.array(ds[col]))

    # Stack into 2D array
    labels = np.column_stack(labels_list).astype(np.float32)

    # Handle NaN values in labels (treat as 0)
    labels = np.nan_to_num(labels, nan=0.0)

    # Remove samples with invalid AST
    valid_indices = []
    for i, ast in enumerate(asts):
        if ast and ast != "nan" and ast != "None" and len(str(ast)) > 50:
            valid_indices.append(i)

    logger.info(f"Valid samples (with AST): {len(valid_indices)} / {len(ds)}")

    # Filter data
    addresses = [addresses[i] for i in valid_indices]
    asts = [asts[i] for i in valid_indices]
    labels = labels[valid_indices]

    # Create dataset
    dataset = VulnerabilityDataset(addresses, asts, labels)

    return dataset


@timeit
def load_train_test_datasets(
    force_reload: bool = False,
) -> Tuple[VulnerabilityDataset, VulnerabilityDataset]:
    """
    Load train and test datasets from separate CSV files or HuggingFace Hub

    Args:
        force_reload: Force reload from CSV even if pickle exists

    Returns:
        Tuple of (train_dataset, test_dataset)
    """
    # Check if pickle cache exists
    if (
        not force_reload
        and pickle_exists(config.PICKLE_TRAIN_DATASET)
        and pickle_exists(config.PICKLE_TEST_DATASET)
    ):
        logger.info("Loading train/test datasets from pickle cache")
        train_dataset = load_pickle(config.PICKLE_TRAIN_DATASET, logger)
        test_dataset = load_pickle(config.PICKLE_TEST_DATASET, logger)

        if train_dataset and test_dataset:
            logger.info(f"Train set: {len(train_dataset)} samples")
            logger.info(f"Test set: {len(test_dataset)} samples")

            # Print statistics
            logger.info("\n=== Train Set Statistics ===")
            train_dataset.print_statistics()

            logger.info("\n=== Test Set Statistics ===")
            test_dataset.print_statistics()

            return train_dataset, test_dataset

    # Check if using HuggingFace
    if config.USE_HUGGINGFACE:
        logger.info(f"Loading from HuggingFace Hub: {config.HUGGINGFACE_DATASET_NAME}")

        # Load train dataset
        train_dataset = load_dataset_from_huggingface("train")

        # Load test dataset
        test_dataset = load_dataset_from_huggingface("test")
    else:
        # Load from local CSV files
        # Load train dataset
        logger.info(f"Loading train dataset from {config.TRAIN_DATASET_PATH.name}")
        train_dataset = load_dataset_from_file(config.TRAIN_DATASET_PATH)

        # Load test dataset
        logger.info(f"Loading test dataset from {config.TEST_DATASET_PATH.name}")
        test_dataset = load_dataset_from_file(config.TEST_DATASET_PATH)

    logger.info(f"Train set: {len(train_dataset)} samples")
    logger.info(f"Test set: {len(test_dataset)} samples")

    # Save to pickle cache
    logger.info("Saving train/test datasets to pickle cache")
    save_pickle(train_dataset, config.PICKLE_TRAIN_DATASET, logger)
    save_pickle(test_dataset, config.PICKLE_TEST_DATASET, logger)

    # Print statistics
    logger.info("\n=== Train Set Statistics ===")
    train_dataset.print_statistics()

    logger.info("\n=== Test Set Statistics ===")
    test_dataset.print_statistics()

    return train_dataset, test_dataset


def get_label_names() -> List[str]:
    """Get list of vulnerability label names (display format)"""
    return [
        config.LABEL_DISPLAY_NAMES.get(l, l) for l in config.DATASET_COLUMNS["labels"]
    ]


def get_num_labels() -> int:
    """Get number of vulnerability labels"""
    return len(config.DATASET_COLUMNS["labels"])


# ============================================================================
# MAIN (for testing)
# ============================================================================
if __name__ == "__main__":
    import argparse

    from utils import set_seed, setup_logging

    # Setup
    setup_logging()
    set_seed()

    # Parse arguments
    parser = argparse.ArgumentParser(description="Explore dataset and view samples")
    parser.add_argument(
        "--sample", type=int, help="Sample number to view (1-based index)"
    )
    parser.add_argument(
        "--dataset", choices=["train", "test"], default="train", help="Dataset to use"
    )
    parser.add_argument("--show-ast", action="store_true", help="Show full AST content")
    parser.add_argument(
        "--max-ast-chars", type=int, default=500, help="Max AST characters to show"
    )
    parser.add_argument(
        "--range", type=str, help='Sample range to analyze (e.g., "1-100")'
    )
    parser.add_argument(
        "--force-reload",
        action="store_true",
        help="Force reload from CSV ignoring pickle cache",
    )
    args = parser.parse_args()

    logger.info("=" * 70)
    logger.info("Dataset Explorer")
    logger.info("=" * 70)

    # Load datasets
    train_dataset, test_dataset = load_train_test_datasets(
        force_reload=args.force_reload
    )
    dataset = train_dataset if args.dataset == "train" else test_dataset

    # If specific sample requested
    if args.sample is not None:
        # Validate sample number
        if args.sample < 1 or args.sample > len(dataset):
            logger.error(f"Sample number must be between 1 and {len(dataset)}")
            exit(1)

        sample_idx = args.sample - 1  # Convert to 0-based

        logger.info(f"\n{'=' * 70}")
        logger.info(f"Sample #{args.sample} from {args.dataset.upper()} set")
        logger.info(f"{'=' * 70}")

        # Get sample data
        sample = dataset[sample_idx]

        # Display all columns
        logger.info(f"\n📋 Sample Details:")
        logger.info(f"  Address: {sample['address']}")

        # Labels
        label_names = get_label_names()
        active_labels = [
            label_names[i] for i, val in enumerate(sample["labels"]) if val == 1
        ]
        logger.info(f"\n  Labels ({sample['labels'].sum():.0f} vulnerabilities):")
        for i, label_name in enumerate(label_names):
            status = "✓" if sample["labels"][i] == 1 else "✗"
            logger.info(f"    {status} {label_name}: {sample['labels'][i]:.0f}")

        if active_labels:
            logger.info(f"\n  Active vulnerabilities: {', '.join(active_labels)}")
        else:
            logger.info(f"\n  Active vulnerabilities: None")

        # AST content
        logger.info(f"\n  AST Statistics:")
        logger.info(f"    - Total characters: {len(sample['ast']):,}")
        logger.info(f"    - Total lines: {sample['ast'].count(chr(10)) + 1:,}")

        # Try to parse AST to get node count
        try:
            import json

            ast_obj = json.loads(sample["ast"])

            def count_nodes(node):
                if not isinstance(node, dict):
                    return 0
                count = 1
                for key in ["children", "body", "statements", "nodes"]:
                    if key in node and isinstance(node[key], list):
                        for child in node[key]:
                            count += count_nodes(child)
                return count

            node_count = count_nodes(ast_obj)
            logger.info(f"    - Estimated AST nodes: {node_count:,}")
            logger.info(f"    - Root node type: {ast_obj.get('nodeType', 'Unknown')}")
        except:
            logger.info(f"    - Could not parse AST structure")

        # Show AST content
        if args.show_ast:
            logger.info(f"\n📝 Full AST Content:")
            logger.info("=" * 70)
            print(sample["ast"])
            logger.info("=" * 70)
        else:
            logger.info(f"\n📝 AST Content Preview (first {args.max_ast_chars} chars):")
            logger.info("=" * 70)
            print(sample["ast"][: args.max_ast_chars])
            if len(sample["ast"]) > args.max_ast_chars:
                logger.info(
                    f"\n... (truncated, showing {args.max_ast_chars}/{len(sample['ast']):,} characters)"
                )
                logger.info(f"    Use --show-ast to see full content")
            logger.info("=" * 70)

        logger.info(f"\n✅ Done! Use --help to see all options")

    # If range specified
    elif args.range:
        try:
            start, end = map(int, args.range.split("-"))
            if start < 1 or end > len(dataset) or start > end:
                logger.error(f"Invalid range. Must be 1-{len(dataset)}")
                exit(1)

            start_idx = start - 1
            end_idx = end

            logger.info(f"\n{'=' * 70}")
            logger.info(
                f"Analyzing Samples {start}-{end} from {args.dataset.upper()} set"
            )
            logger.info(f"{'=' * 70}")

            # Collect statistics
            logger.info(f"\n📊 Range Statistics:")
            logger.info(f"  Total samples: {end_idx - start_idx}")

            # Label distribution in range
            labels_in_range = dataset.labels[start_idx:end_idx]
            logger.info(f"\n  Label Distribution:")
            label_names = get_label_names()
            for i, label_name in enumerate(label_names):
                count = np.sum(labels_in_range[:, i])
                percentage = (count / len(labels_in_range)) * 100
                logger.info(f"    - {label_name}: {count:.0f} ({percentage:.1f}%)")

            # AST size statistics
            ast_sizes = [len(dataset.asts[i]) for i in range(start_idx, end_idx)]
            logger.info(f"\n  AST Size Statistics:")
            logger.info(f"    - Min: {min(ast_sizes):,} characters")
            logger.info(f"    - Max: {max(ast_sizes):,} characters")
            logger.info(f"    - Mean: {np.mean(ast_sizes):,.0f} characters")
            logger.info(f"    - Median: {np.median(ast_sizes):,.0f} characters")

            # Multi-label statistics
            samples_with_labels = np.sum(labels_in_range, axis=1)
            logger.info(f"\n  Multi-label Statistics:")
            logger.info(
                f"    - Samples with 0 vulnerabilities: {np.sum(samples_with_labels == 0)}"
            )
            logger.info(
                f"    - Samples with 1 vulnerability: {np.sum(samples_with_labels == 1)}"
            )
            logger.info(
                f"    - Samples with 2+ vulnerabilities: {np.sum(samples_with_labels >= 2)}"
            )
            logger.info(
                f"    - Max vulnerabilities per sample: {int(np.max(samples_with_labels))}"
            )
            logger.info(
                f"    - Avg vulnerabilities per sample: {np.mean(samples_with_labels):.2f}"
            )

        except ValueError:
            logger.error("Invalid range format. Use: --range 1-100")
            exit(1)

    # Default: show overall dataset statistics
    else:
        logger.info(f"\n{'=' * 70}")
        logger.info(f"Dataset Overview")
        logger.info(f"{'=' * 70}")

        logger.info(f"\n📊 Dataset Sizes:")
        logger.info(f"  Train set: {len(train_dataset):,} samples")
        logger.info(f"  Test set: {len(test_dataset):,} samples")
        logger.info(f"  Total: {len(train_dataset) + len(test_dataset):,} samples")

        logger.info(f"\n📋 Dataset Columns:")
        logger.info(f"  - address: Smart contract address (string)")
        logger.info(f"  - ast: Abstract Syntax Tree (JSON string)")
        logger.info(f"  - labels: Vulnerability labels (5 binary values)")

        logger.info(f"\n🏷️  Label Names:")
        label_names = get_label_names()
        for i, label_name in enumerate(label_names):
            original_name = config.DATASET_COLUMNS["labels"][i]
            if label_name != original_name:
                logger.info(f"  {i + 1}. {label_name} (from '{original_name}')")
            else:
                logger.info(f"  {i + 1}. {label_name}")

        # Check for null/missing data
        logger.info(f"\n🔍 Data Quality Check:")

        for dataset_obj, dataset_name in [
            (train_dataset, "Train"),
            (test_dataset, "Test"),
        ]:
            logger.info(f"\n  {dataset_name} Set:")

            # Check addresses
            null_addresses = sum(
                1 for addr in dataset_obj.addresses if not addr or addr == ""
            )
            logger.info(f"    - Null addresses: {null_addresses}")

            # Check ASTs
            null_asts = sum(1 for ast in dataset_obj.asts if not ast or ast == "")
            logger.info(f"    - Null ASTs: {null_asts}")

            # Check duplicate addresses
            unique_addresses = len(set(dataset_obj.addresses))
            duplicates = len(dataset_obj.addresses) - unique_addresses
            logger.info(f"    - Unique addresses: {unique_addresses:,}")
            logger.info(f"    - Duplicate addresses: {duplicates}")

            # AST size range
            ast_sizes = [len(ast) for ast in dataset_obj.asts]
            logger.info(
                f"    - AST size range: {min(ast_sizes):,} - {max(ast_sizes):,} characters"
            )
            logger.info(f"    - AST size mean: {np.mean(ast_sizes):,.0f} characters")

        # Train set detailed statistics
        logger.info(f"\n📈 Train Set Label Distribution:")
        for i, label_name in enumerate(label_names):
            count = np.sum(train_dataset.labels[:, i])
            percentage = (count / len(train_dataset)) * 100
            logger.info(f"  - {label_name}: {count:.0f} ({percentage:.1f}%)")

        # Multi-label statistics
        train_samples_with_labels = np.sum(train_dataset.labels, axis=1)
        logger.info(f"\n  Multi-label Statistics:")
        logger.info(
            f"    - Samples with at least 1 vulnerability: {np.sum(train_samples_with_labels > 0)} ({(np.sum(train_samples_with_labels > 0) / len(train_dataset) * 100):.1f}%)"
        )
        logger.info(
            f"    - Samples with multiple vulnerabilities: {np.sum(train_samples_with_labels > 1)} ({(np.sum(train_samples_with_labels > 1) / len(train_dataset) * 100):.1f}%)"
        )
        logger.info(
            f"    - Average vulnerabilities per sample: {np.mean(train_samples_with_labels):.2f}"
        )

        # Test set detailed statistics
        logger.info(f"\n📈 Test Set Label Distribution:")
        for i, label_name in enumerate(label_names):
            count = np.sum(test_dataset.labels[:, i])
            percentage = (count / len(test_dataset)) * 100
            logger.info(f"  - {label_name}: {count:.0f} ({percentage:.1f}%)")

        # Multi-label statistics
        test_samples_with_labels = np.sum(test_dataset.labels, axis=1)
        logger.info(f"\n  Multi-label Statistics:")
        logger.info(
            f"    - Samples with at least 1 vulnerability: {np.sum(test_samples_with_labels > 0)} ({(np.sum(test_samples_with_labels > 0) / len(test_dataset) * 100):.1f}%)"
        )
        logger.info(
            f"    - Samples with multiple vulnerabilities: {np.sum(test_samples_with_labels > 1)} ({(np.sum(test_samples_with_labels > 1) / len(test_dataset) * 100):.1f}%)"
        )
        logger.info(
            f"    - Average vulnerabilities per sample: {np.mean(test_samples_with_labels):.2f}"
        )

        logger.info(f"\n💡 Usage Tips:")
        logger.info(f"  - View specific sample: python data_loader.py --sample 10")
        logger.info(f"  - Analyze range: python data_loader.py --range 1-100")
        logger.info(
            f"  - View test set: python data_loader.py --sample 5 --dataset test"
        )
        logger.info(f"  - Show full AST: python data_loader.py --sample 1 --show-ast")
        logger.info(f"\n✅ Use --help to see all options")
