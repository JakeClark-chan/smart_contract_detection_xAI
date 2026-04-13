"""
Generate Experimental Optimized Dataset (80/50/20% of baseline nodes)
Handles the 80%, 50%, and 20% node optimization relative to the baseline nodes
from generate_optimized_dataset.py.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

import config
from data_loader import load_train_test_datasets

# Import general functions from the base script
from generate_optimized_dataset import (
    NUM_CORES,
    compute_node_importance,
    graph_to_sequence_string,
)
from graph_processor import parse_cfg_json
from utils import Timer, get_logger, set_seed, setup_logging

logger = get_logger(__name__)


def process_single_sample_exp(args: Tuple) -> Dict:
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
    importance_scores = compute_node_importance(graph)

    # 1. Get baseline sequence and nodes (max 512)
    row["before_optimized"], baseline_nodes = graph_to_sequence_string(
        graph, max_tokens=512, importance_scores=importance_scores
    )

    # 2. Generate optimized versions relative to baseline
    for keep_pct, name in [(0.80, "80p"), (0.50, "50p"), (0.20, "20p")]:
        # Optimization is relative to the NODES in before_optimized
        num_to_keep = max(1, int(len(baseline_nodes) * keep_pct))

        # Sort baseline nodes by importance to select the best ones
        sorted_baseline = sorted(
            baseline_nodes, key=lambda n: importance_scores.get(n, 0.5), reverse=True
        )
        important_nodes = sorted_baseline[:num_to_keep]

        # Create optimized subgraph from these nodes
        opt_graph = graph.subgraph(important_nodes).copy()

        # Generate sequence (no additional truncation needed as we limited nodes)
        opt_seq, _ = graph_to_sequence_string(
            opt_graph,
            max_tokens=None,
            importance_scores=importance_scores,
            reference_graph=graph,  # Keep original traversal order
        )
        row[f"optimized_{name}"] = opt_seq

    return row


def process_batch_exp(batch_args: List[Tuple]) -> List[Dict]:
    """Process a batch of samples for the experimental set."""
    return [process_single_sample_exp(args) for args in batch_args]


def generate_exp_dataset(
    dataset, output_path, force_reload=False, num_workers=0, batch_size=100
):
    """Generate the experimental dataset (baseline + 80/50/20 columns)."""
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
    with Timer(f"Experimental generation ({num_workers} workers)", logger):
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = {
                executor.submit(process_batch_exp, batch): i
                for i, batch in enumerate(batches)
            }
            for future in as_completed(futures):
                all_results.extend(future.result())

    # Order results by dataset addresses
    results_dict = {r["address"]: r for r in all_results}
    ordered_results = [
        results_dict[addr] for addr in dataset.addresses if addr in results_dict
    ]

    df = pd.DataFrame(ordered_results)

    # Column ordering
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
    logger.info(f"Saved experimental dataset to {output_path}")
    return df


def main():
    parser = argparse.ArgumentParser(
        description="Generate Experimental Optimized Datasets"
    )
    parser.add_argument(
        "--force-reload", action="store_true", help="Force regeneration"
    )
    parser.add_argument("--subset", type=int, default=None, help="Use subset of data")
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

    # Generate Train & Test Experimental Sets
    generate_exp_dataset(
        train_dataset,
        config.OUTPUT_DIR / "train_optimized_dataset.csv",
        force_reload=args.force_reload,
    )
    generate_exp_dataset(
        test_dataset,
        config.OUTPUT_DIR / "test_optimized_dataset.csv",
        force_reload=args.force_reload,
    )


if __name__ == "__main__":
    main()
