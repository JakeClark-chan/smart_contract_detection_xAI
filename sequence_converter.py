"""
Sequence Converter for Graph-to-Sequence Transformation
Performs DFS traversal on optimized CFG graphs to generate sequences for BERT models

Optimizations:
- Compact token format: Type instead of Type:Type
- Smart truncation: Importance-weighted + position sampling for BERT 512 token limit
- Node importance: Degree centrality + structural role + position scoring
"""

import networkx as nx
import numpy as np
from typing import List, Dict, Tuple, Optional
from collections import deque

import config
from utils import get_logger, save_pickle, load_pickle, pickle_exists, timeit, Timer
from graph_processor import CFGGraph, get_function_entry_points, get_entry_nodes


logger = get_logger(__name__)


# ============================================================================
# NODE IMPORTANCE COMPUTATION
# ============================================================================
def compute_node_importance(nx_graph: nx.DiGraph) -> Dict:
    """
    Fast node importance computation.
    Combines: degree centrality + structural role + position

    Args:
        nx_graph: NetworkX directed graph

    Returns:
        Dictionary mapping node -> importance score (0-1)
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


# ============================================================================
# TOKEN FORMATTING
# ============================================================================
def get_node_label(node_data: dict) -> str:
    """
    Extract short, meaningful label from node data.
    Optimized format: Type or Type[value] or Type(name)

    Args:
        node_data: Node attributes dictionary

    Returns:
        Compact token string
    """
    node_type = node_data.get(
        "nodeType", node_data.get("type", node_data.get("node_type", "Node"))
    )
    name = node_data.get("name", "")
    label = node_data.get("label", "")
    value = node_data.get("value", "")

    if value and len(str(value)) <= 20:
        return f"{node_type}[{value}]"
    elif name and name != node_type:
        short_name = name[:15] if len(name) > 15 else name
        return f"{node_type}({short_name})"
    else:
        return node_type


def node_to_token(graph: nx.DiGraph, node) -> str:
    """
    Convert a graph node to a compact token string.

    Args:
        graph: NetworkX graph
        node: Node ID

    Returns:
        Token string representing the node
    """
    node_data = graph.nodes[node]
    return get_node_label(node_data)


# ============================================================================
# SMART TRUNCATION
# ============================================================================
def smart_truncate(
    tokens: List[Tuple[str, float]], max_tokens: int
) -> List[Tuple[str, float]]:
    """
    Smart truncation using importance-weighted + position sampling.

    Strategy:
    - 60% from high-importance nodes (first half of graph)
    - 30% from remaining important nodes
    - 10% from tail to capture function endings

    Args:
        tokens: List of (token, importance) tuples
        max_tokens: Maximum tokens to keep

    Returns:
        Filtered list of (token, importance) tuples
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


# ============================================================================
# GRAPH TRAVERSAL
# ============================================================================
def dfs_traversal(
    graph: nx.DiGraph, start_nodes: List = None, max_depth: int = None
) -> List:
    """
    Perform Depth-First Search traversal on graph

    Args:
        graph: NetworkX graph
        start_nodes: Starting nodes for traversal (default: entry nodes)
        max_depth: Maximum depth for traversal

    Returns:
        List of nodes in DFS order
    """
    if start_nodes is None:
        start_nodes = get_entry_nodes(graph)

    if not start_nodes and graph.number_of_nodes() > 0:
        start_nodes = [list(graph.nodes())[0]]

    visited = set()
    traversal_order = []

    def dfs_recursive(node, depth=0):[@PROJECT_SUMMARY.md](file:///home/jc/scripts/smart_contract_detection_xAI/PROJECT_SUMMARY.md)
        if max_depth is not None and depth > max_depth:
            return

        if node in visited:
            return

        visited.add(node)
        traversal_order.append(node)

        # Visit successors
        for successor in graph.successors(node):
            if successor not in visited:
                dfs_recursive(successor, depth + 1)

    # Start DFS from each start node
    for start in start_nodes:
        if start in graph.nodes():
            dfs_recursive(start)

    # Include any unvisited nodes
    for node in graph.nodes():
        if node not in visited:
            traversal_order.append(node)

    return traversal_order


def bfs_traversal(
    graph: nx.DiGraph, start_nodes: List = None, max_depth: int = None
) -> List:
    """
    Perform Breadth-First Search traversal on graph

    Args:
        graph: NetworkX graph
        start_nodes: Starting nodes for traversal
        max_depth: Maximum depth for traversal

    Returns:
        List of nodes in BFS order
    """
    if start_nodes is None:
        start_nodes = get_entry_nodes(graph)

    if not start_nodes and graph.number_of_nodes() > 0:
        start_nodes = [list(graph.nodes())[0]]

    visited = set()
    traversal_order = []
    queue = deque([(node, 0) for node in start_nodes])

    while queue:
        node, depth = queue.popleft()

        if max_depth is not None and depth > max_depth:
            continue

        if node not in visited and node in graph.nodes():
            visited.add(node)
            traversal_order.append(node)

            # Add successors to queue
            for successor in graph.successors(node):
                if successor not in visited:
                    queue.append((successor, depth + 1))

    # Include any unvisited nodes
    for node in graph.nodes():
        if node not in visited:
            traversal_order.append(node)

    return traversal_order


# ============================================================================
# NODE TO TOKEN CONVERSION
# ============================================================================
def node_to_token(graph: nx.DiGraph, node) -> str:
    """
    Convert a graph node to a compact token string.
    Uses optimized format: Type or Type[value] or Type(name)

    Args:
        graph: NetworkX graph
        node: Node ID

    Returns:
        Compact token string
    """
    node_data = graph.nodes[node]
    return get_node_label(node_data)


def graph_to_sequence(
    graph: nx.DiGraph,
    traversal_method: str = "dfs",
    start_nodes: Optional[List] = None,
    include_edges: bool = False,
    max_tokens: Optional[int] = None,
    importance_scores: Optional[Dict] = None,
) -> str:
    """
    Convert graph to optimized sequence using traversal.

    Optimizations:
    - Compact token format (Type instead of Type:Type)
    - Smart truncation respecting BERT's 512 token limit
    - Importance-weighted token selection

    Args:
        graph: NetworkX graph
        traversal_method: 'dfs' or 'bfs'
        start_nodes: Starting nodes (default: function entry points)
        include_edges: Whether to include edge information (default: False)
        max_tokens: Maximum tokens to keep (default: config.MAX_SEQUENCE_LENGTH)
        importance_scores: Pre-computed node importance scores

    Returns:
        Optimized sequence string
    """
    if graph is None or graph.number_of_nodes() == 0:
        return ""

    if max_tokens is None:
        max_tokens = config.MAX_SEQUENCE_LENGTH

    if importance_scores is None:
        importance_scores = compute_node_importance(graph)

    if start_nodes is None and config.DFS_START_FROM_ENTRY:
        start_nodes = get_function_entry_points(graph)

    # Get traversal order
    if traversal_method == "dfs":
        traversal_order = dfs_traversal(graph, start_nodes)
    elif traversal_method == "bfs":
        traversal_order = bfs_traversal(graph, start_nodes)
    else:
        raise ValueError(f"Unknown traversal method: {traversal_method}")

    # Convert nodes to tokens with importance
    tokens = []

    for node in traversal_order:
        node_token = node_to_token(graph, node)
        importance = importance_scores.get(node, 0.5)
        tokens.append((node_token, importance))

    # Apply smart truncation
    if max_tokens and len(tokens) > max_tokens:
        tokens = smart_truncate(tokens, max_tokens)

    # Join tokens
    return " ".join([t[0] for t in tokens])


# ============================================================================
# BATCH CONVERSION
# ============================================================================
class GraphSequence:
    """
    Wrapper class for graph sequence with metadata
    """

    def __init__(
        self, sequence: str, address: str, labels: np.ndarray, graph_stats: Dict
    ):
        self.sequence = sequence
        self.address = address
        self.labels = labels
        self.graph_stats = graph_stats

    def __len__(self):
        return len(self.sequence.split())

    def __repr__(self):
        return f"GraphSequence(tokens={len(self)}, address={self.address[:10]}...)"


@timeit
def convert_graphs_to_sequences(
    cfg_graphs: List[CFGGraph],
    traversal_method: str = "dfs",
    include_edges: bool = True,
    force_reconvert: bool = False,
) -> List[GraphSequence]:
    """
    Convert multiple graphs to sequences

    Args:
        cfg_graphs: List of CFGGraph objects
        traversal_method: 'dfs' or 'bfs'
        include_edges: Whether to include edge information
        force_reconvert: Force re-conversion even if cache exists

    Returns:
        List of GraphSequence objects
    """
    # Check cache
    if not force_reconvert and pickle_exists(config.PICKLE_SEQUENCES):
        logger.info(f"Loading sequences from cache: {config.PICKLE_SEQUENCES.name}")
        sequences = load_pickle(config.PICKLE_SEQUENCES, logger)
        if sequences is not None:
            logger.info(f"Loaded {len(sequences)} sequences from cache")

            # Display statistics
            display_sequence_statistics(sequences)

            return sequences

    logger.info(
        f"Converting {len(cfg_graphs)} graphs to sequences using {traversal_method.upper()} traversal..."
    )

    sequences = []
    failed_count = 0

    with Timer("Graph to sequence conversion", logger):
        for i, cfg_graph in enumerate(cfg_graphs):
            if cfg_graph is None or cfg_graph.graph.number_of_nodes() == 0:
                # Create empty sequence for invalid graphs
                sequences.append(None)
                failed_count += 1
                continue

            try:
                # Convert graph to sequence
                sequence_str = graph_to_sequence(
                    cfg_graph.graph,
                    traversal_method=traversal_method,
                    include_edges=include_edges,
                )

                # Create GraphSequence object
                graph_seq = GraphSequence(
                    sequence=sequence_str,
                    address=cfg_graph.address,
                    labels=cfg_graph.labels,
                    graph_stats=cfg_graph.get_statistics(),
                )

                sequences.append(graph_seq)

            except Exception as e:
                logger.error(f"Error converting graph {i} to sequence: {e}")
                sequences.append(None)
                failed_count += 1

            # Progress logging
            if (i + 1) % 1000 == 0:
                logger.info(
                    f"Converted {i + 1}/{len(cfg_graphs)} graphs ({failed_count} failed)"
                )

    logger.info(
        f"Successfully converted {len(sequences) - failed_count}/{len(cfg_graphs)} graphs to sequences"
    )

    # Display statistics
    display_sequence_statistics(sequences)

    # Save to cache
    logger.info(f"Saving sequences to cache: {config.PICKLE_SEQUENCES.name}")
    save_pickle(sequences, config.PICKLE_SEQUENCES, logger)

    return sequences


def display_sequence_statistics(sequences: List[GraphSequence]):
    """Display statistics about sequences"""
    valid_sequences = [s for s in sequences if s is not None]

    if not valid_sequences:
        logger.warning("No valid sequences to analyze")
        return

    sequence_lengths = [len(s) for s in valid_sequences]

    logger.info(f"\n{'=' * 70}")
    logger.info(f"Sequence Statistics:")
    logger.info(f"{'=' * 70}")
    logger.info(f"Total sequences: {len(sequences)}")
    logger.info(f"Valid sequences: {len(valid_sequences)}")
    logger.info(f"Average sequence length: {np.mean(sequence_lengths):.2f} tokens")
    logger.info(f"Median sequence length: {np.median(sequence_lengths):.2f} tokens")
    logger.info(f"Min sequence length: {min(sequence_lengths)}")
    logger.info(f"Max sequence length: {max(sequence_lengths)}")
    logger.info(
        f"Sequences > {config.MAX_SEQUENCE_LENGTH} tokens: {sum(1 for l in sequence_lengths if l > config.MAX_SEQUENCE_LENGTH)}"
    )
    logger.info(f"{'=' * 70}\n")


def truncate_sequence(sequence: str, max_length: int = None) -> str:
    """
    Truncate sequence to maximum length

    Args:
        sequence: Sequence string
        max_length: Maximum number of tokens (default: config.MAX_SEQUENCE_LENGTH)

    Returns:
        Truncated sequence
    """
    if max_length is None:
        max_length = config.MAX_SEQUENCE_LENGTH

    tokens = sequence.split()

    if len(tokens) <= max_length:
        return sequence

    # Truncate to max_length
    truncated_tokens = tokens[:max_length]

    return " ".join(truncated_tokens)


# ============================================================================
# MAIN (for testing)
# ============================================================================
if __name__ == "__main__":
    import argparse
    from utils import setup_logging, set_seed
    from data_loader import load_train_test_datasets, get_label_names
    from graph_processor import process_dataset_to_graphs

    # Setup
    setup_logging()
    set_seed()

    # Parse arguments
    parser = argparse.ArgumentParser(description="View sequence of a specific sample")
    parser.add_argument(
        "--sample", type=int, default=10, help="Sample number to view (1-based index)"
    )
    parser.add_argument(
        "--dataset", choices=["train", "test"], default="train", help="Dataset to use"
    )
    parser.add_argument(
        "--traversal", choices=["dfs", "bfs"], default="dfs", help="Traversal method"
    )
    parser.add_argument(
        "--show-full", action="store_true", help="Show full sequence (not truncated)"
    )
    parser.add_argument(
        "--max-chars", type=int, default=500, help="Max characters to show if not full"
    )
    args = parser.parse_args()

    logger.info("=" * 70)
    logger.info(f"Viewing Sequence for Sample #{args.sample} ({args.dataset} set)")
    logger.info("=" * 70)

    # Load data
    train_dataset, test_dataset = load_train_test_datasets(force_reload=False)
    dataset = train_dataset if args.dataset == "train" else test_dataset

    # Validate sample number
    if args.sample < 1 or args.sample > len(dataset):
        logger.error(f"Sample number must be between 1 and {len(dataset)}")
        exit(1)

    sample_idx = args.sample - 1  # Convert to 0-based index

    # Get sample info
    logger.info(f"\n📊 Sample Information:")
    logger.info(f"  Address: {dataset.addresses[sample_idx]}")
    label_names = get_label_names()
    labels = dataset.labels[sample_idx]
    active_labels = [label_names[i] for i, val in enumerate(labels) if val == 1]
    logger.info(
        f"  Labels: {labels} ({', '.join(active_labels) if active_labels else 'None'})"
    )
    logger.info(f"  AST size: {len(dataset.asts[sample_idx])} characters")

    # Process single graph
    logger.info(f"\n🔧 Processing AST to Graph...")
    from graph_processor import CFGGraph, parse_cfg_json
    import networkx as nx

    graph = parse_cfg_json(dataset.asts[sample_idx])
    if graph is None or graph.number_of_nodes() == 0:
        logger.error("Failed to parse AST")
        exit(1)

    cfg_graph = CFGGraph(
        graph=graph,
        address=dataset.addresses[sample_idx],
        labels=labels,
        ast_json=dataset.asts[sample_idx],
    )

    logger.info(f"  Graph nodes: {cfg_graph.graph.number_of_nodes()}")
    logger.info(f"  Graph edges: {cfg_graph.graph.number_of_edges()}")

    # Convert to sequence
    logger.info(f"\n🔄 Converting Graph to Sequence ({args.traversal.upper()})...")
    sequence_str = graph_to_sequence(
        cfg_graph.graph,  # Pass the NetworkX graph, not the CFGGraph wrapper
        traversal_method=args.traversal,
    )

    # Create GraphSequence object
    sequence_obj = GraphSequence(
        sequence=sequence_str,
        address=cfg_graph.address,
        labels=cfg_graph.labels,
        graph_stats=cfg_graph.get_statistics(),
    )

    if sequence_obj is None:
        logger.error("Failed to convert graph to sequence")
        exit(1)

    logger.info(f"  Sequence length: {len(sequence_obj)} tokens")
    logger.info(
        f"  Truncation needed for BERT (512 tokens): {'Yes' if len(sequence_obj) > 512 else 'No'}"
    )

    # Display sequence
    logger.info(f"\n📝 Sequence Content:")
    logger.info("=" * 70)
    if args.show_full:
        print(sequence_obj.sequence)
    else:
        print(sequence_obj.sequence[: args.max_chars])
        if len(sequence_obj.sequence) > args.max_chars:
            logger.info(
                f"\n... (truncated, showing {args.max_chars}/{len(sequence_obj.sequence)} characters)"
            )
            logger.info(f"    Use --show-full to see complete sequence")
    logger.info("=" * 70)

    logger.info(f"\n✅ Done! Use --help to see all options")
