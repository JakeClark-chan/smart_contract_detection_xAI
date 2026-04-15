"""
Generate Experimental Optimized Dataset (80/50/20% of baseline nodes)
Handles both fast heuristic version and GNN Explainer version datasets.
"""

import argparse
import multiprocessing as mp
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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
    GNNClassifier,
    compute_node_importance_gnn,
    networkx_to_pyg,
    train_gnn_model,
)

logger = get_logger(__name__)


def process_single_sample_exp(
    args: Tuple, gnn_model: Optional[GNNClassifier] = None
) -> Dict:
    """Process a single sample with baseline-relative optimization (80/50/20)."""
    idx, address, ast_json, labels = args
    row = {
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
        importance_array = compute_node_importance_gnn(pyg_data, gnn_model)
        node_list = list(graph.nodes())
        importance_scores = {
            node_list[i]: float(importance_array[i]) for i in range(len(node_list))
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
) -> List[Dict]:
    """Process a batch of samples."""
    return [process_single_sample_exp(args, gnn_model) for args in batch_args]


def generate_exp_dataset(
    dataset,
    output_path,
    gnn_model=None,
    force_reload=False,
    num_workers=0,
    batch_size=100,
):
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

    all_results = []
    mode = "GNN" if gnn_model else "Heuristic"
    with Timer(f"Experimental {mode} generation ({num_workers} workers)", logger):
        # Note: GNN model can't easily be pickled for multi-process if not careful
        # But we can use threads or pass it if it's small.
        # Actually, for GNNExplainer, process pool might be slow due to CUDA/pickling.
        # If gnn_model is provided, we might want to use a smaller pool or serial for stability if needed.
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = {
                executor.submit(process_batch_exp, batch, gnn_model): i
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
    logger.info(f"Saved {mode} dataset to {output_path}")
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force-reload", action="store_true")
    parser.add_argument("--subset", type=int, default=None)
    parser.add_argument("--use-gnn", action="store_true", help="Use GNN Explainer")
    parser.add_argument(
        "--gnn-epochs", type=int, default=10, help="Epochs to train GNN"
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

    # Generate Heuristic Version
    logger.info("\n>>> GENERATING HEURISTIC VERSION <<<")
    generate_exp_dataset(
        train_dataset,
        config.OUTPUT_DIR / "train_optimized_heuristic.csv",
        force_reload=args.force_reload,
    )
    generate_exp_dataset(
        test_dataset,
        config.OUTPUT_DIR / "test_optimized_heuristic.csv",
        force_reload=args.force_reload,
    )

    # Generate GNN Version
    if args.use_gnn:
        logger.info("\n>>> GENERATING GNN EXPLAINER VERSION <<<")
        # 1. Process graphs for training
        train_graphs = process_dataset_to_graphs(train_dataset)

        # 2. Train/Load GNN
        gnn_path = config.MODELS_DIR / "gnn_explainer_model.pth"
        if gnn_path.exists() and not args.force_reload:
            logger.info(f"Loading GNN model from {gnn_path}")
            gnn_model = GNNClassifier(num_node_features=4, num_classes=5)
            gnn_model.load_state_dict(torch.load(gnn_path, weights_only=True))
        else:
            logger.info(f"Training GNN model for {args.gnn_epochs} epochs...")
            gnn_model = train_gnn_model(train_graphs, epochs=args.gnn_epochs)
            torch.save(gnn_model.state_dict(), gnn_path)
            logger.info(f"Saved GNN model to {gnn_path}")

        # 3. Generate dataset
        generate_exp_dataset(
            train_dataset,
            config.OUTPUT_DIR / "train_optimized_gnn.csv",
            gnn_model=gnn_model,
            force_reload=args.force_reload,
        )
        generate_exp_dataset(
            test_dataset,
            config.OUTPUT_DIR / "test_optimized_gnn.csv",
            gnn_model=gnn_model,
            force_reload=args.force_reload,
        )


if __name__ == "__main__":
    main()
