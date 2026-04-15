"""
Generate Test/Train Dataset with XAI Optimizations
General purpose script for AST sequence generation and optimization.
"""

import argparse
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import networkx as nx
import numpy as np
import pandas as pd

import config
from data_loader import VulnerabilityDataset, load_train_test_datasets
from graph_processor import parse_cfg_json
from utils import Timer, get_logger, set_seed, setup_logging

logger = get_logger(__name__)

NUM_CORES = max(1, mp.cpu_count())


def get_node_label(node_data: dict) -> str:
    """Extract short, meaningful label from node data."""
    node_type = node_data.get(
        "nodeType", node_data.get("type", node_data.get("node_type", "Node"))
    )
    name = node_data.get("name", "")
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
    max_tokens: int = 512,
    importance_scores: Optional[Dict] = None,
    reference_graph: Optional[nx.DiGraph] = None,
) -> Tuple[str, List]:
    """
    Convert graph to sequence string.
    Returns (sequence_string, list_of_node_ids_kept)
    """
    if graph is None or graph.number_of_nodes() == 0:
        return "", []

    if reference_graph is not None:
        traversal_order = _dfs_traversal(reference_graph)
        current_nodes = set(graph.nodes())
        traversal_order = [n for n in traversal_order if n in current_nodes]
    else:
        traversal_order = _dfs_traversal(graph)

    importance_scores = importance_scores or {}
    tokens = []
    for node in traversal_order:
        node_data = graph.nodes[node]
        token = get_node_label(node_data)
        importance = importance_scores.get(node, 0.5)
        tokens.append((token, importance, node))

    if max_tokens and len(tokens) > max_tokens:
        tokens = smart_truncate(tokens, max_tokens)

    return " ".join([t[0] for t in tokens]), [t[2] for t in tokens]


def smart_truncate(tokens: List[Tuple], max_tokens: int) -> List[Tuple]:
    """Truncate tokens keeping high importance and tail."""
    n = len(tokens)
    if n <= max_tokens:
        return tokens

    high_importance = int(max_tokens * 0.6)
    medium_importance = int(max_tokens * 0.30)
    tail = max_tokens - high_importance - medium_importance

    indices_to_keep = set()
    sorted_indices = sorted(range(n), key=lambda i: tokens[i][1], reverse=True)
    indices_to_keep.update(sorted_indices[: high_importance + medium_importance])
    indices_to_keep.update(range(n - tail, n))

    final_indices = sorted(list(indices_to_keep))
    return [tokens[i] for i in final_indices[:max_tokens]]


def _dfs_traversal(graph: nx.DiGraph) -> List:
    """DFS traversal from entry nodes."""
    entry_nodes = [n for n in graph.nodes() if graph.in_degree(n) == 0]
    if not entry_nodes:
        entry_nodes = [list(graph.nodes())[0]] if graph.number_of_nodes() > 0 else []

    visited, traversal_order = set(), []

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
    """Fast node importance computation."""
    if nx_graph is None:
        return {}
    num_nodes = nx_graph.number_of_nodes()
    if num_nodes == 0:
        return {}

    entry_nodes = [n for n in nx_graph.nodes() if nx_graph.in_degree(n) == 0]
    exit_nodes = [n for n in nx_graph.nodes() if nx_graph.out_degree(n) == 0]
    nodes_list = list(nx_graph.nodes())

    importance = {}
    for i, node in enumerate(nodes_list):
        in_deg, out_deg = nx_graph.in_degree(node), nx_graph.out_degree(node)
        base_score = (in_deg + out_deg) / max(1, 2 * num_nodes - 2)
        role_bonus = (
            0.3
            if node in entry_nodes
            else (0.2 if node in exit_nodes else (0.1 if out_deg > in_deg else 0))
        )
        position_score = 1.0 - (i / num_nodes) * 0.3
        importance[node] = base_score + role_bonus + position_score

    max_imp = max(importance.values()) if importance else 1.0
    return {k: v / max_imp for k, v in importance.items()}


def process_single_sample(args: Tuple, keep_percentage: float = 1.0) -> Dict:
    """Process a single sample with a specific optimization percentage."""
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

    # Generate sequence
    if keep_percentage < 1.0:
        sorted_nodes = sorted(
            importance_scores.items(), key=lambda x: x[1], reverse=True
        )
        num_keep = max(1, int(len(sorted_nodes) * keep_percentage))
        important_nodes = [node for node, _ in sorted_nodes[:num_keep]]
        opt_graph = graph.subgraph(important_nodes).copy()
        seq, _ = graph_to_sequence_string(
            opt_graph,
            max_tokens=512,
            importance_scores=importance_scores,
            reference_graph=graph,
        )
    else:
        seq, _ = graph_to_sequence_string(
            graph, max_tokens=512, importance_scores=importance_scores
        )

    row["sequence"] = seq
    return row


def generate_dataset(
    dataset,
    output_path,
    keep_percentage=1.0,
    force_reload=False,
    num_workers=0,
    batch_size=100,
):
    if num_workers <= 0:
        num_workers = NUM_CORES
    output_path = Path(output_path)
    if not force_reload and output_path.exists():
        return pd.read_csv(output_path)

    sample_args = [
        (i, dataset.addresses[i], dataset.asts[i], dataset.labels[i])
        for i in range(len(dataset))
    ]
    batches = [
        sample_args[i : i + batch_size] for i in range(0, len(sample_args), batch_size)
    ]

    all_results = []
    with Timer(f"Dataset generation ({num_workers} workers)", logger):
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = {
                executor.submit(process_batch, batch, keep_percentage): i
                for i, batch in enumerate(batches)
            }
            for future in as_completed(futures):
                all_results.extend(future.result())

    results_dict = {r["address"]: r for r in all_results}
    ordered_results = [
        results_dict[addr] for addr in dataset.addresses if addr in results_dict
    ]
    df = pd.DataFrame(ordered_results)
    df.to_csv(output_path, index=False)
    return df


def process_batch(batch_args, keep_percentage):
    return [process_single_sample(args, keep_percentage) for args in batch_args]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force-reload", action="store_true")
    parser.add_argument(
        "--percentage", type=float, default=1.0, help="Node retention percentage"
    )
    parser.add_argument("--output", type=str, default="dataset.csv")
    args = parser.parse_args()

    setup_logging()
    set_seed()
    train_dataset, test_dataset = load_train_test_datasets(
        force_reload=args.force_reload
    )

    generate_dataset(
        train_dataset,
        args.output,
        keep_percentage=args.percentage,
        force_reload=args.force_reload,
    )


if __name__ == "__main__":
    main()
