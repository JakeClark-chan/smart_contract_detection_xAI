"""
Generate Test/Train Dataset with XAI Optimizations
Optimized version with:
- Better token format (shorter tokens)
- Smart truncation with importance-weighted sampling
- Better threshold values
"""

import argparse
import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp
import networkx as nx

import config
from utils import setup_logging, get_logger, set_seed, Timer
from data_loader import load_train_test_datasets, VulnerabilityDataset
from graph_processor import parse_cfg_json


logger = get_logger(__name__)

NUM_CORES = max(1, mp.cpu_count())


def get_node_label(node_data: dict) -> str:
    """
    Extract short, meaningful label from node data.
    Prioritizes: nodeType > name > type
    """
    node_type = node_data.get(
        "nodeType", node_data.get("type", node_data.get("node_type", "Node"))
    )
    name = node_data.get("name", "")
    label = node_data.get("label", "")
    value = node_data.get("value", "")

    if value and len(value) <= 20:
        return f"{node_type}[{value}]"
    elif name and name != node_type:
        short_name = name[:15] if len(name) > 15 else name
        return f"{node_type}({short_name})"
    else:
        return node_type


def graph_to_sequence_string(
    graph: Optional[nx.DiGraph],
    traversal_method: str = "dfs",
    max_tokens: int = 512,
    importance_scores: Optional[Dict] = None,
) -> str:
    """
    Convert graph to optimized sequence string.

    Features:
    - Short token format: Type or Type[value] or Type(name)
    - Smart truncation: importance-weighted + position sampling
    - DFS traversal from entry nodes
    """
    if graph is None or graph.number_of_nodes() == 0:
        return ""

    traversal_order = _dfs_traversal(graph)

    if importance_scores is None:
        importance_scores = {}

    tokens = []
    for node in traversal_order:
        node_data = graph.nodes[node]
        token = get_node_label(node_data)
        importance = importance_scores.get(node, 0.5)
        tokens.append((token, importance))

    if max_tokens and len(tokens) > max_tokens:
        tokens = smart_truncate(tokens, max_tokens)

    return " ".join([t[0] for t in tokens])


def smart_truncate(
    tokens: List[Tuple[str, float]], max_tokens: int
) -> List[Tuple[str, float]]:
    """
    Smart truncation using importance-weighted + position sampling.

    Strategy:
    - 60% from high-importance nodes (first half of graph)
    - 30% from remaining important nodes
    - 10% from tail to capture function endings
    """
    n = len(tokens)

    if n <= max_tokens:
        return tokens

    high_importance = int(max_tokens * 0.6)
    medium_importance = int(max_tokens * 0.30)
    tail = max_tokens - high_importance - medium_importance

    sorted_tokens = sorted(tokens, key=lambda x: x[1], reverse=True)

    selected = []
    selected_tokens = set()

    for token, imp in sorted_tokens[:high_importance]:
        if token not in selected_tokens:
            selected.append((token, imp))
            selected_tokens.add(token)

    mid_start = high_importance
    mid_end = min(high_importance + medium_importance, n)
    for token, imp in sorted_tokens[mid_start:mid_end]:
        if token not in selected_tokens:
            selected.append((token, imp))
            selected_tokens.add(token)

    for token, imp in tokens[-tail:]:
        if token not in selected_tokens:
            selected.append((token, imp))
            selected_tokens.add(token)

    selected.sort(key=lambda x: tokens.index(x), reverse=False)

    return selected[:max_tokens]


def _dfs_traversal(graph: nx.DiGraph) -> List:
    """DFS traversal starting from entry nodes."""
    entry_nodes = [n for n in graph.nodes() if graph.in_degree(n) == 0]
    if not entry_nodes:
        entry_nodes = [list(graph.nodes())[0]] if graph.number_of_nodes() > 0 else []

    visited = set()
    traversal_order = []

    def dfs_recursive(node):
        if node in visited:
            return
        visited.add(node)
        traversal_order.append(node)
        for successor in graph.successors(node):
            if successor not in visited:
                dfs_recursive(successor)

    for start in entry_nodes:
        if start in graph.nodes():
            dfs_recursive(start)

    for node in graph.nodes():
        if node not in visited:
            traversal_order.append(node)

    return traversal_order


def compute_node_importance(nx_graph: Optional[nx.DiGraph]) -> Dict:
    """
    Fast node importance computation.
    Combines: degree centrality + structural role + position
    """
    importance = {}
    if nx_graph is None:
        return importance

    num_nodes = nx_graph.number_of_nodes()

    if num_nodes == 0:
        return importance

    entry_nodes = [n for n in nx_graph.nodes() if nx_graph.in_degree(n) == 0]
    exit_nodes = [n for n in nx_graph.nodes() if nx_graph.out_degree(n) == 0]

    nodes_list = list(nx_graph.nodes())

    for i, node in enumerate(nodes_list):
        in_deg = nx_graph.in_degree(node)
        out_deg = nx_graph.out_degree(node)

        base_score = (in_deg + out_deg) / max(1, 2 * num_nodes - 2)

        role_bonus = 0.0
        if node in entry_nodes:
            role_bonus = 0.3
        elif node in exit_nodes:
            role_bonus = 0.2
        elif out_deg > in_deg:
            role_bonus = 0.1

        position_score = 1.0 - (i / num_nodes) * 0.3

        importance[node] = base_score + role_bonus + position_score

    max_imp = max(importance.values()) if importance else 1.0
    if max_imp > 0:
        importance = {k: v / max_imp for k, v in importance.items()}

    return importance


def optimize_graph_by_percentage(
    graph: Optional[nx.DiGraph],
    keep_percentage: float,
    importance_scores: Optional[Dict] = None,
) -> Tuple[nx.DiGraph, Dict]:
    """
    Optimize graph by keeping only top N% most important nodes.
    Returns both optimized graph and its importance scores.
    """
    if graph is None or graph.number_of_nodes() == 0:
        return nx.DiGraph(), {}

    if importance_scores is None:
        importance_scores = compute_node_importance(graph)

    sorted_nodes = sorted(importance_scores.items(), key=lambda x: x[1], reverse=True)

    num_to_keep = max(1, int(len(sorted_nodes) * keep_percentage))
    important_nodes = [node for node, score in sorted_nodes[:num_to_keep]]

    sub_graph = graph.subgraph(important_nodes).copy().to_directed()

    sub_importance = {
        k: importance_scores[k] for k in important_nodes if k in importance_scores
    }

    return sub_graph, sub_importance


def process_single_sample(args: Tuple) -> Dict:
    """Process a single sample with optimized token format and truncation."""
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

    row["before_optimized"] = graph_to_sequence_string(
        graph, "dfs", max_tokens=512, importance_scores=importance_scores
    )

    for keep_pct, name in [(0.80, "80p"), (0.50, "50p"), (0.20, "20p")]:
        opt_graph, opt_importance = optimize_graph_by_percentage(
            graph, keep_pct, importance_scores
        )
        row[f"optimized_{name}"] = graph_to_sequence_string(
            opt_graph, "dfs", max_tokens=512, importance_scores=opt_importance
        )

    return row


def generate_dataset_sequences(
    dataset: VulnerabilityDataset,
    output_path: Path,
    force_reload: bool = False,
    num_workers: int = 0,
    batch_size: int = 100,
) -> pd.DataFrame:
    """Generate optimized dataset CSV."""
    if num_workers <= 0:
        num_workers = NUM_CORES

    logger.info(
        f"Generating dataset for {len(dataset)} samples using {num_workers} workers..."
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not force_reload and output_path.exists():
        logger.info(f"Loading existing dataset from {output_path}")
        return pd.read_csv(output_path)

    sample_args = [
        (i, dataset.addresses[i], dataset.asts[i], dataset.labels[i])
        for i in range(len(dataset))
    ]

    batches = [
        sample_args[i : i + batch_size] for i in range(0, len(sample_args), batch_size)
    ]
    logger.info(f"Split into {len(batches)} batches")

    all_results = []

    with Timer(f"Multi-process dataset generation ({num_workers} workers)", logger):
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = {
                executor.submit(process_batch, batch): i
                for i, batch in enumerate(batches)
            }

            for future in as_completed(futures):
                try:
                    batch_results = future.result()
                    all_results.extend(batch_results)

                    if len(all_results) % 1000 == 0:
                        pct = (len(all_results) / len(sample_args)) * 100
                        logger.info(
                            f"Progress: {len(all_results)}/{len(sample_args)} ({pct:.1f}%)"
                        )
                except Exception as e:
                    logger.error(f"Error: {e}")

    results_dict = {r["address"]: r for r in all_results}
    ordered_results = [
        results_dict[dataset.addresses[i]]
        for i in range(len(dataset))
        if dataset.addresses[i] in results_dict
    ]

    df = pd.DataFrame(ordered_results)

    col_order = [
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
    existing_cols = [c for c in col_order if c in df.columns]
    if existing_cols:
        df = df.loc[:, existing_cols]

    df.to_csv(output_path, index=False)
    logger.info(f"Saved: {output_path} ({len(df)} rows)")

    return df


def process_batch(batch_args: List[Tuple]) -> List[Dict]:
    """Process a batch of samples."""
    return [process_single_sample(args) for args in batch_args]


def main():
    parser = argparse.ArgumentParser(description="Generate optimized dataset CSVs")
    parser.add_argument(
        "--force-reload", action="store_true", help="Force regeneration"
    )
    parser.add_argument("--subset", type=int, default=None, help="Use subset of data")
    parser.add_argument("--workers", type=int, default=None, help="Number of workers")
    parser.add_argument("--batch-size", type=int, default=100, help="Batch size")
    args = parser.parse_args()

    num_workers = args.workers or NUM_CORES

    setup_logging()
    set_seed()
    logger = get_logger(__name__)

    logger.info("=" * 70)
    logger.info("Dataset Generation - Optimized Token Format & Smart Truncation")
    logger.info(f"Workers: {num_workers}, Batch size: {args.batch_size}")
    logger.info("=" * 70)

    with Timer("Complete dataset generation", logger):
        train_dataset, test_dataset = load_train_test_datasets(
            force_reload=args.force_reload
        )

        if args.subset:
            train_dataset.addresses = train_dataset.addresses[: args.subset]
            train_dataset.asts = train_dataset.asts[: args.subset]
            train_dataset.labels = train_dataset.labels[: args.subset]
            test_dataset.addresses = test_dataset.addresses[
                : min(args.subset, len(test_dataset.addresses))
            ]
            test_dataset.asts = test_dataset.asts[
                : min(args.subset, len(test_dataset.asts))
            ]
            test_dataset.labels = test_dataset.labels[
                : min(args.subset, len(test_dataset.labels))
            ]

        train_output = config.OUTPUT_DIR / "train_optimized_dataset.csv"
        test_output = config.OUTPUT_DIR / "test_optimized_dataset.csv"

        logger.info("\n--- Generating Train Dataset ---")
        train_df = generate_dataset_sequences(
            train_dataset,
            train_output,
            force_reload=args.force_reload,
            num_workers=num_workers,
            batch_size=args.batch_size,
        )

        logger.info("\n--- Generating Test Dataset ---")
        test_df = generate_dataset_sequences(
            test_dataset,
            test_output,
            force_reload=args.force_reload,
            num_workers=num_workers,
            batch_size=args.batch_size,
        )

        logger.info("\n" + "=" * 70)
        logger.info("Dataset Generation Complete!")
        logger.info("=" * 70)
        logger.info(f"Train: {train_output} ({len(train_df)} rows)")
        logger.info(f"Test: {test_output} ({len(test_df)} rows)")


if __name__ == "__main__":
    main()
