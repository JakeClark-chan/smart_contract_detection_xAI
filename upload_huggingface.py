"""
Upload Dataset to HuggingFace Hub (Memory-Optimized for Low RAM)
Uploads smart contract vulnerability datasets using streaming to minimize memory usage
"""

import os
from pathlib import Path

from datasets import Dataset, DatasetDict
from dotenv import load_dotenv

import config
from utils import get_logger

logger = get_logger(__name__)


def upload_to_huggingface():
    """
    Upload train and test datasets to HuggingFace Hub
    Uses memory-efficient loading to work with limited RAM (8GB)
    """
    # Load environment variables
    load_dotenv()

    # Get HuggingFace token
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
    if not hf_token:
        raise ValueError("HUGGINGFACE_API_TOKEN not found in .env file")

    # Dataset name
    dataset_name = config.HUGGINGFACE_DATASET_NAME
    if not dataset_name:
        raise ValueError("HUGGINGFACE_DATASET_NAME not set in config.py")

    logger.info(f"Uploading to HuggingFace: {dataset_name}")
    logger.info(f"Memory-optimized mode (streaming CSV loading)")

    # Load datasets one at a time using HuggingFace's CSV loader (no pandas needed)
    logger.info(f"Loading train dataset from {config.TRAIN_DATASET_PATH.name}")
    train_ds = Dataset.from_csv(str(config.TRAIN_DATASET_PATH))
    logger.info(f"  Loaded {len(train_ds)} samples")

    logger.info(f"Loading test dataset from {config.TEST_DATASET_PATH.name}")
    test_ds = Dataset.from_csv(str(config.TEST_DATASET_PATH))
    logger.info(f"  Loaded {len(test_ds)} samples")

    # Create dataset dictionary
    dataset_dict = DatasetDict({"train": train_ds, "test": test_ds})

    # Upload to HuggingFace Hub
    logger.info(f"Uploading to HuggingFace Hub: {dataset_name}")
    dataset_dict.push_to_hub(
        dataset_name,
        token=hf_token,
        private=False,  # Set to True if you want private dataset
    )

    logger.info(
        f"✅ Successfully uploaded to https://huggingface.co/datasets/{dataset_name}"
    )

    # Print dataset info
    logger.info("\n" + "=" * 70)
    logger.info("Dataset Information:")
    logger.info("=" * 70)
    logger.info(f"Dataset Name: {dataset_name}")
    logger.info(f"Train samples: {len(train_ds):,}")
    logger.info(f"Test samples: {len(test_ds):,}")
    logger.info(f"Features: {train_ds.column_names}")
    logger.info(f"\nLabel columns: {config.DATASET_COLUMNS['labels']}")

    logger.info("=" * 70)
    logger.info("✅ Upload complete!")
    logger.info(f"\nTo use in config.py, set:")
    logger.info(f"  USE_HUGGINGFACE = True")
    logger.info(f"  HUGGINGFACE_DATASET_NAME = '{dataset_name}'")


if __name__ == "__main__":
    import argparse

    from utils import setup_logging

    # Setup logging
    setup_logging()

    # Parse arguments
    parser = argparse.ArgumentParser(description="Upload datasets to HuggingFace Hub")
    parser.add_argument(
        "--dataset-name",
        type=str,
        default="JakeClark/soliaudit-dasp-ast-graph",
        help="HuggingFace dataset name (default: JakeClark/soliaudit-dasp-ast-graph)",
    )
    args = parser.parse_args()

    # Set dataset name in config
    config.HUGGINGFACE_DATASET_NAME = args.dataset_name

    # Upload
    upload_to_huggingface()
