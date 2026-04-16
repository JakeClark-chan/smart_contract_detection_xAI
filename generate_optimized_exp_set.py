"""
Generate Experimental Optimized Dataset (80/50/20% of baseline nodes)
Handles both fast heuristic version and GNN Explainer version datasets.
Integrates both versions into one combined dataset and optionally uploads to HuggingFace.
"""

import argparse
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import torch

import config
from data_loader import VulnerabilityDataset, load_train_test_datasets

# Import general functions from the base script
from generate_optimized_dataset import (
    NUM_CORES,
    compute_node_importance,
    graph_to_sequence_string,
)
from graph_processor import parse_cfg_json, process_dataset_to_graphs
from utils import Timer, get_logger, set_seed, setup_logging
from xai_optimizer import (
    HAS_TORCH_GEOMETRIC,
    GNNClassifier,
    compute_node_importance_gnn,
    networkx_to_pyg,
    train_gnn_model,
)

logger = get_logger(__name__)


def process_single_sample_exp(
    args: Tuple, gnn_model: Optional[GNNClassifier] = None
) -> Dict[str, Any]:
    """Process a single sample with baseline-relative optimization (80/50/20)."""
    idx, address, ast_json, labels = args
    row: Dict[str, Any] = {
        "address": address,
        "Arithmetic": int(labels[0]),
        "Unchecked Return Values For Low Level Calls": int(labels[1]),
        "Denial of Service": int(labels[2]),
        "Time manipulation": int(labels[3]),
        "Reentrancy": int(labels[4]),
    }

    graph = parse_cfg_json(ast_json, address)

    # 1. Compute importance scores
    if gnn_model is not None:
        # GNN Explainer path
        pyg_data = networkx_to_pyg(graph, labels)
        logger.debug(
            f"Computing GNN importance for graph {address} with {pyg_data.x.size(0)} nodes"
        )
        importance_array = compute_node_importance_gnn(pyg_data, gnn_model)
        node_list = list(graph.nodes())
        importance_scores = {
            node_list[i]: float(
                importance_array[i].item()
                if hasattr(importance_array[i], "item")
                else importance_array[i]
            )
            for i in range(len(node_list))
        }
    else:
        # Fast heuristic path
        importance_scores = compute_node_importance(graph)

    # 2. Get baseline sequence and nodes (max 512)
    row["before_optimized"], baseline_nodes = graph_to_sequence_string(
        graph, max_tokens=512, importance_scores=importance_scores
    )

    # 3. Generate optimized versions relative to baseline
    for keep_pct, name in [(0.80, "80p"), (0.50, "50p"), (0.20, "20p")]:
        num_to_keep = max(1, int(len(baseline_nodes) * keep_pct))
        sorted_baseline = sorted(
            baseline_nodes, key=lambda n: importance_scores.get(n, 0.5), reverse=True
        )
        important_nodes = sorted_baseline[:num_to_keep]
        opt_graph = graph.subgraph(important_nodes).copy()

        opt_seq, _ = graph_to_sequence_string(
            opt_graph,
            max_tokens=None,
            importance_scores=importance_scores,
            reference_graph=graph,
        )
        row[f"optimized_{name}"] = opt_seq

    return row


def process_batch_exp(
    batch_args: List[Tuple], gnn_model: Optional[GNNClassifier] = None
) -> List[Dict[str, Any]]:
    """Process a batch of samples."""
    return [process_single_sample_exp(args, gnn_model) for args in batch_args]


def generate_exp_dataset(
    dataset: VulnerabilityDataset,
    output_path: Path,
    gnn_model: Optional[GNNClassifier] = None,
    force_reload: bool = False,
    num_workers: int = 0,
    batch_size: int = 100,
) -> pd.DataFrame:
    """Generate experimental dataset."""
    if num_workers <= 0:
        num_workers = NUM_CORES
    output_path = Path(output_path)
    if not force_reload and output_path.exists():
        logger.info(f"Loading existing experimental dataset from {output_path}")
        return pd.read_csv(output_path)

    sample_args = [
        (i, dataset.addresses[i], dataset.asts[i], dataset.labels[i])
        for i in range(len(dataset))
    ]
    batches = [
        sample_args[i : i + batch_size] for i in range(0, len(sample_args), batch_size)
    ]

    all_results: List[Dict[str, Any]] = []
    mode = "GNN" if gnn_model else "Heuristic"

    # For GNN model, use serial processing to avoid pickle/CUDA issues
    if gnn_model is not None:
        logger.info(
            f"Using serial processing for {mode} mode (GNN model pickle limitation)"
        )
        for i, batch in enumerate(batches):
            logger.info(
                f"Processing batch {i + 1}/{len(batches)} for GNN explainer ({len(batch)} samples)"
            )
            batch_results = process_batch_exp(batch, gnn_model)
            all_results.extend(batch_results)
            logger.info(f"Completed batch {i + 1}/{len(batches)} for GNN explainer")
    else:
        with Timer(f"Experimental {mode} generation ({num_workers} workers)", logger):
            with ProcessPoolExecutor(max_workers=num_workers) as executor:
                futures = {
                    executor.submit(process_batch_exp, batch): i
                    for i, batch in enumerate(batches)
                }
                for future in as_completed(futures):
                    all_results.extend(future.result())

    results_dict = {r["address"]: r for r in all_results}
    ordered_results = [
        results_dict[addr] for addr in dataset.addresses if addr in results_dict
    ]
    df = pd.DataFrame(ordered_results)

    cols = [
        "address",
        "before_optimized",
        "optimized_80p",
        "optimized_50p",
        "optimized_20p",
        "Arithmetic",
        "Unchecked Return Values For Low Level Calls",
        "Denial of Service",
        "Time manipulation",
        "Reentrancy",
    ]
    df = df[[c for c in cols if c in df.columns]]
    df.to_csv(output_path, index=False)
    logger.info(f"Saved {mode} dataset to {output_path} ({len(df)} samples)")
    return df


def upload_optimized_to_huggingface(
    train_heuristic_df: pd.DataFrame,
    test_heuristic_df: pd.DataFrame,
    train_gnn_df: Optional[pd.DataFrame] = None,
    test_gnn_df: Optional[pd.DataFrame] = None,
) -> None:
    """
    Upload optimized datasets to HuggingFace Hub.
    If GNN version is not available, only uploads heuristic version.
    """
    from datasets import Dataset, DatasetDict

    dataset_name = config.HUGGINGFACE_DATASET_NAME
    if not dataset_name:
        logger.warning("HUGGINGFACE_DATASET_NAME not set, skipping upload")
        return

    logger.info(f"Uploading optimized datasets to HuggingFace: {dataset_name}")

    # Load environment variables for token
    import os

    from dotenv import load_dotenv

    load_dotenv()

    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
    if not hf_token:
        logger.error("HUGGINGFACE_API_TOKEN not found in .env file")
        return

    # Create combined dataset with both versions
    # Structure: train/test splits, each with heuristic and optional gnn columns
    train_ds = Dataset.from_pandas(train_heuristic_df)
    test_ds = Dataset.from_pandas(test_heuristic_df)

    # Add GNN columns if available
    if train_gnn_df is not None and test_gnn_df is not None:
        logger.info("Including GNN Explainer version in dataset")
        # Merge GNN columns into heuristic dataframe
        # Rename GNN columns to have _gnn suffix
        gnn_cols = [
            "before_optimized_gnn",
            "optimized_80p_gnn",
            "optimized_50p_gnn",
            "optimized_20p_gnn",
        ]

        for col, gnn_col in zip(
            ["before_optimized", "optimized_80p", "optimized_50p", "optimized_20p"],
            gnn_cols,
        ):
            if gnn_col in train_gnn_df.columns:
                train_ds = train_ds.add_column(gnn_col, train_gnn_df[gnn_col].tolist())
                test_ds = test_ds.add_column(gnn_col, test_gnn_df[gnn_col].tolist())

    dataset_dict = DatasetDict(
        {
            "train": train_ds,
            "test": test_ds,
        }
    )

    logger.info(f"Train samples: {len(train_ds)}, Test samples: {len(test_ds)}")
    logger.info(f"Features: {train_ds.column_names}")

    # Upload to HuggingFace
    dataset_dict.push_to_hub(
        dataset_name,
        token=hf_token,
        private=False,
    )

    logger.info(
        f"✅ Successfully uploaded to https://huggingface.co/datasets/{dataset_name}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate optimized datasets with 80/50/20% variants"
    )
    parser.add_argument(
        "--force-reload", action="store_true", help="Force regeneration"
    )
    parser.add_argument("--subset", type=int, default=None, help="Use subset of data")
    parser.add_argument(
        "--use-gnn", action="store_true", help="Generate GNN Explainer version"
    )
    parser.add_argument(
        "--gnn-epochs", type=int, default=10, help="Epochs to train GNN model"
    )
    parser.add_argument(
        "--upload-to-hf",
        action="store_true",
        help="Upload to HuggingFace if USE_HUGGINGFACE is True",
    )
    args = parser.parse_args()

    setup_logging()
    set_seed()

    train_dataset, test_dataset = load_train_test_datasets(
        force_reload=args.force_reload
    )

    if args.subset:
        train_dataset.addresses = train_dataset.addresses[: args.subset]
        train_dataset.asts = train_dataset.asts[: args.subset]
        train_dataset.labels = train_dataset.labels[: args.subset]
        test_dataset.addresses = test_dataset.addresses[: args.subset]
        test_dataset.asts = test_dataset.asts[: args.subset]
        test_dataset.labels = test_dataset.labels[: args.subset]

    # Generate Heuristic Version (always)
    logger.info("\n>>> GENERATING HEURISTIC VERSION <<<")
    train_heuristic_path = (
        Path("JakeClark/soliaudit-dasp-ast-sequence-heuristic")
        / "train_optimized_heuristic.csv"
    )
    test_heuristic_path = (
        Path("JakeClark/soliaudit-dasp-ast-sequence-heuristic")
        / "test_optimized_heuristic.csv"
    )
    # Create directories if they don't exist
    train_heuristic_path.parent.mkdir(parents=True, exist_ok=True)
    test_heuristic_path.parent.mkdir(parents=True, exist_ok=True)

    train_heuristic_df = generate_exp_dataset(
        train_dataset,
        train_heuristic_path,
        force_reload=args.force_reload,
    )
    test_heuristic_df = generate_exp_dataset(
        test_dataset,
        test_heuristic_path,
        force_reload=args.force_reload,
    )

    # Generate GNN Version (optional)
    train_gnn_df = None
    test_gnn_df = None

    if args.use_gnn:
        if not HAS_TORCH_GEOMETRIC:
            logger.warning("torch-geometric not available, skipping GNN generation")
        else:
            logger.info("\n>>> GENERATING GNN EXPLAINER VERSION <<<")
            # 1. Process graphs for training
            train_graphs = process_dataset_to_graphs(train_dataset)

            # 2. Train/Load GNN
            gnn_path = config.MODELS_DIR / "gnn_explainer_model.pth"
            gnn_model = None

            if gnn_path.exists() and not args.force_reload:
                logger.info(f"Loading GNN model from {gnn_path}")
                gnn_model = GNNClassifier(num_node_features=4, num_classes=5)
                gnn_model.load_state_dict(
                    torch.load(gnn_path, weights_only=True, map_location="cpu")
                )
            else:
                logger.info(f"Training GNN model for {args.gnn_epochs} epochs...")
                gnn_model = train_gnn_model(train_graphs, epochs=args.gnn_epochs)
                torch.save(gnn_model.state_dict(), gnn_path)
                logger.info(f"Saved GNN model to {gnn_path}")

            # 3. Generate dataset
            train_gnn_path = (
                Path("JakeClark/soliaudit-dasp-ast-sequence-gnn-explainer")
                / "train_optimized_gnn.csv"
            )
            test_gnn_path = (
                Path("JakeClark/soliaudit-dasp-ast-sequence-gnn-explainer")
                / "test_optimized_gnn.csv"
            )
            # Create directories if they don't exist
            train_gnn_path.parent.mkdir(parents=True, exist_ok=True)
            test_gnn_path.parent.mkdir(parents=True, exist_ok=True)

            train_gnn_df = generate_exp_dataset(
                train_dataset,
                train_gnn_path,
                gnn_model=gnn_model,
                force_reload=args.force_reload,
            )
            test_gnn_df = generate_exp_dataset(
                test_dataset,
                test_gnn_path,
                gnn_model=gnn_model,
                force_reload=args.force_reload,
            )

    # Upload to HuggingFace if configured
    if config.USE_HUGGINGFACE and args.upload_to_hf:
        logger.info("\n>>> UPLOADING TO HUGGINGFACE <<<")
        upload_optimized_to_huggingface(
            train_heuristic_df,
            test_heuristic_df,
            train_gnn_df,
            test_gnn_df,
        )
    elif config.USE_HUGGINGFACE:
        logger.info("\n💡 To upload to HuggingFace, add --upload-to-hf flag")
        logger.info(f"Or manually set USE_HUGGINGFACE=True in config.py")
    else:
        logger.info("\n💡 USE_HUGGINGFACE is False, skipping upload")
        logger.info("Generated datasets saved locally in output/ directory")


if __name__ == "__main__":
    main()
