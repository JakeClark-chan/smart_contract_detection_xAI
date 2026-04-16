"""
XAI Optimizer using GNN Explainer
Identifies sensitive nodes and optimizes graphs for vulnerability detection
"""

from typing import Any, Dict, List, Optional

import networkx as nx
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

# Optional torch-geometric imports (for GNN Explainer)
try:
    from torch_geometric.data import Data
    from torch_geometric.explain import Explainer
    from torch_geometric.explain import GNNExplainer as PyGGNNExplainer
    from torch_geometric.nn import GCNConv, global_mean_pool

    HAS_TORCH_GEOMETRIC = True
except ImportError:
    HAS_TORCH_GEOMETRIC = False
    Data = None
    GCNConv = None
    global_mean_pool = None

import config
from graph_processor import CFGGraph, subgraph_from_nodes
from utils import (
    Timer,
    compare_statistics,
    compute_graph_statistics,
    get_device,
    get_logger,
    load_pickle,
    pickle_exists,
    save_pickle,
    timeit,
)

logger = get_logger(__name__)


# ============================================================================
# GNN MODEL FOR GRAPH CLASSIFICATION
# ============================================================================
class GNNClassifier(nn.Module):
    """
    Simple GNN classifier for graph-level prediction
    Used by GNN Explainer to identify important nodes
    """

    def __init__(
        self, num_node_features: int, hidden_channels: int = 64, num_classes: int = 5
    ):
        super(GNNClassifier, self).__init__()

        self.conv1 = GCNConv(num_node_features, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.conv3 = GCNConv(hidden_channels, hidden_channels)

        self.lin = nn.Linear(hidden_channels, num_classes)

    def forward(self, x, edge_index, batch=None):
        # Node embeddings
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.2, training=self.training)

        x = self.conv2(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.2, training=self.training)

        x = self.conv3(x, edge_index)

        # Graph-level pooling
        if batch is None:
            batch = torch.zeros(x.size(0), dtype=torch.long, device=x.device)

        x = global_mean_pool(x, batch)

        # Classification
        x = self.lin(x)

        return x


def train_gnn_model(
    graphs: List[CFGGraph], epochs: int = 50, lr: float = 0.01
) -> GNNClassifier:
    """Train the GNN model on the dataset for better node importance scores."""
    from torch_geometric.loader import DataLoader

    device = get_device()
    num_labels = len(config.DATASET_COLUMNS["labels"])
    model = GNNClassifier(num_node_features=4, num_classes=num_labels).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = torch.nn.BCEWithLogitsLoss()

    # Convert graphs to PyG Data
    pyg_data_list = []
    for g in graphs:
        if g and g.graph.number_of_nodes() > 0:
            pyg_data_list.append(networkx_to_pyg(g.graph, g.labels))

    if not pyg_data_list:
        logger.warning("No valid graphs for GNN training")
        return model

    loader = DataLoader(pyg_data_list, batch_size=32, shuffle=True)

    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for data in loader:
            data = data.to(device)
            optimizer.zero_grad()
            out = model(data.x, data.edge_index, data.batch)
            loss = criterion(out, data.y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * data.num_graphs

        if (epoch + 1) % 10 == 0:
            logger.info(
                f"GNN Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(pyg_data_list):.4f}"
            )

    return model


# ============================================================================
# GRAPH CONVERSION UTILITIES
# ============================================================================
def networkx_to_pyg(nx_graph: nx.DiGraph, labels: np.ndarray = None) -> Data:
    """
    Convert NetworkX graph to PyTorch Geometric Data

    Args:
        nx_graph: NetworkX directed graph
        labels: Graph-level labels (multi-label)

    Returns:
        PyTorch Geometric Data object
    """
    # Get node mapping
    node_list = list(nx_graph.nodes())
    node_to_idx = {node: idx for idx, node in enumerate(node_list)}

    # Create edge index
    edges = []
    for u, v in nx_graph.edges():
        edges.append([node_to_idx[u], node_to_idx[v]])

    if edges:
        edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    else:
        edge_index = torch.empty((2, 0), dtype=torch.long)

    # Create node features (simple one-hot or default features)
    num_nodes = len(node_list)

    # Try to extract node features from graph
    node_features = []
    for node in node_list:
        node_data = nx_graph.nodes[node]

        # Create simple feature vector based on node properties
        feature = [
            nx_graph.out_degree(node),  # Out degree
            nx_graph.in_degree(node),  # In degree
            1.0 if nx_graph.in_degree(node) == 0 else 0.0,  # Is entry node
            1.0 if nx_graph.out_degree(node) == 0 else 0.0,  # Is exit node
        ]

        node_features.append(feature)

    x = torch.tensor(node_features, dtype=torch.float)

    # Create labels
    y = None
    if labels is not None:
        y = torch.tensor(labels, dtype=torch.float).unsqueeze(0)

    return Data(x=x, edge_index=edge_index, y=y)


# ============================================================================
# NODE IMPORTANCE COMPUTATION
# ============================================================================
def compute_node_importance_simple(nx_graph: nx.DiGraph) -> Dict[Any, float]:
    """
    Compute node importance using fast graph-based heuristics.
    Uses in-degree and out-degree for fast computation.

    Args:
        nx_graph: NetworkX graph

    Returns:
        Dictionary mapping node -> importance score
    """
    importance_scores = {}

    num_nodes = nx_graph.number_of_nodes()
    if num_nodes == 0:
        return importance_scores

    for node in nx_graph.nodes():
        in_deg = nx_graph.in_degree(node)
        out_deg = nx_graph.out_degree(node)

        total_deg = in_deg + out_deg

        is_entry = 1.0 if in_deg == 0 else 0.0
        is_exit = 1.0 if out_deg == 0 else 0.0

        score = total_deg / max(1, 2 * num_nodes - 2) + 0.2 * is_entry + 0.1 * is_exit

        importance_scores[node] = score

    return importance_scores


def compute_node_importance_gnn(
    pyg_data: Data, gnn_model: GNNClassifier, target_label_idx: int = 0
) -> np.ndarray:
    """
    Compute node importance using GNN Explainer

    Args:
        pyg_data: PyTorch Geometric graph data
        gnn_model: Trained GNN model
        target_label_idx: Target label index for explanation

    Returns:
        Node importance scores (numpy array)
    """
    device = get_device()
    gnn_model.eval()
    gnn_model.to(device)
    pyg_data = pyg_data.to(device)

    try:
        # Create explainer
        explainer = Explainer(
            model=gnn_model,
            algorithm=PyGGNNExplainer(epochs=config.GNN_EXPLAINER_EPOCHS),
            explanation_type="model",
            node_mask_type="object",
            edge_mask_type="object",
            model_config=dict(
                mode="multiclass_classification",
                task_level="graph",
                return_type="raw",
            ),
        )

        # Generate explanation for the graph
        # Note: For explanation_type="model", target should not be provided
        logger.info(
            f"Running GNN Explainer for graph with {pyg_data.x.size(0)} nodes using {config.GNN_EXPLAINER_EPOCHS} epochs..."
        )
        explanation = explainer(
            pyg_data.x,
            pyg_data.edge_index,
        )

        # Get node importance scores
        if hasattr(explanation, "node_mask"):
            node_importance = explanation.node_mask.detach().cpu().numpy()
            # Handle case where node_mask might be 2D (node x 1) instead of 1D
            if node_importance.ndim > 1:
                # Take the first column if it's 2D, or flatten if needed
                node_importance = node_importance.flatten()
            # Ensure we have a 1D array
            node_importance = node_importance.squeeze()
        else:
            # Fallback: use uniform importance
            node_importance = np.ones(pyg_data.x.size(0))

        logger.info(
            f"GNN Explainer completed for graph with {pyg_data.x.size(0)} nodes"
        )
        return node_importance

    except Exception as e:
        logger.warning(f"GNN Explainer failed: {e}. Using fallback method.")
        # Fallback: uniform importance
        return np.ones(pyg_data.x.size(0))


# ============================================================================
# GRAPH OPTIMIZATION
# ============================================================================
@timeit
def optimize_single_graph(
    cfg_graph: CFGGraph,
    gnn_model: Optional[GNNClassifier] = None,
    use_gnn_explainer: bool = False,
) -> CFGGraph:
    """
    Optimize a single graph by removing low-importance nodes

    Args:
        cfg_graph: CFGGraph object
        gnn_model: Pre-trained GNN model (for GNN Explainer)
        use_gnn_explainer: Whether to use GNN Explainer or simple heuristics

    Returns:
        Optimized CFGGraph
    """
    nx_graph = cfg_graph.graph

    # Compute node importance
    if use_gnn_explainer and gnn_model is not None:
        # Use GNN Explainer
        pyg_data = networkx_to_pyg(nx_graph, cfg_graph.labels)
        node_importance_array = compute_node_importance_gnn(pyg_data, gnn_model)

        # Map to node IDs
        node_list = list(nx_graph.nodes())
        node_importance = {
            node: float(node_importance_array[i]) for i, node in enumerate(node_list)
        }
    else:
        # Use simple heuristics
        node_importance = compute_node_importance_simple(nx_graph)

    # Normalize importance scores
    if node_importance:
        max_score = max(node_importance.values())
        if max_score > 0:
            node_importance = {k: v / max_score for k, v in node_importance.items()}

    # Filter nodes based on threshold
    threshold = config.SHAP_THRESHOLD
    important_nodes = [
        node for node, score in node_importance.items() if score >= threshold
    ]

    # Ensure we keep at least top N% of nodes
    if len(important_nodes) < len(nx_graph.nodes()) * config.TOP_NODES_PERCENTAGE:
        # Sort by importance and keep top N%
        sorted_nodes = sorted(node_importance.items(), key=lambda x: x[1], reverse=True)
        num_keep = max(1, int(len(nx_graph.nodes()) * config.TOP_NODES_PERCENTAGE))
        important_nodes = [node for node, _ in sorted_nodes[:num_keep]]

    # Create optimized subgraph
    if important_nodes:
        optimized_graph = subgraph_from_nodes(nx_graph, important_nodes)
    else:
        # Keep at least one node
        optimized_graph = nx.DiGraph()
        optimized_graph.add_node(list(nx_graph.nodes())[0])

    # Create optimized CFGGraph
    optimized_cfg = CFGGraph(
        graph=optimized_graph,
        address=cfg_graph.address,
        labels=cfg_graph.labels,
        ast_json=cfg_graph.ast_json,
    )

    return optimized_cfg


@timeit
def optimize_graphs(
    cfg_graphs: List[CFGGraph],
    use_gnn_explainer: bool = True,
    force_reoptimize: bool = False,
) -> List[CFGGraph]:
    """
    Optimize multiple graphs using XAI techniques

    Args:
        cfg_graphs: List of CFGGraph objects
        use_gnn_explainer: Whether to use GNN Explainer (vs simple heuristics)
        force_reoptimize: Force re-optimization even if cache exists

    Returns:
        List of optimized CFGGraph objects
    """
    # Check if torch-geometric is available
    if use_gnn_explainer and not HAS_TORCH_GEOMETRIC:
        logger.warning("torch-geometric not available, using simple heuristics instead")
        use_gnn_explainer = False

    # Check cache
    if not force_reoptimize and pickle_exists(config.PICKLE_OPTIMIZED_GRAPHS):
        logger.info(
            f"Loading optimized graphs from cache: {config.PICKLE_OPTIMIZED_GRAPHS.name}"
        )
        optimized_graphs = load_pickle(config.PICKLE_OPTIMIZED_GRAPHS, logger)
        if optimized_graphs is not None:
            logger.info(f"Loaded {len(optimized_graphs)} optimized graphs from cache")

            # Compute and display statistics
            nx_graphs = [g.graph for g in optimized_graphs if g and g.graph]
            stats_after = compute_graph_statistics(nx_graphs, "Optimized CFG Graphs")

            # Load before stats and compare
            stats_before = load_pickle(config.STATS_BEFORE_OPTIMIZATION, logger)
            if stats_before:
                compare_statistics(stats_before, stats_after)

            return optimized_graphs

    logger.info(
        f"Optimizing {len(cfg_graphs)} graphs using {'GNN Explainer' if use_gnn_explainer else 'simple heuristics'}..."
    )

    # Initialize GNN model if using GNN Explainer
    gnn_model = None
    if use_gnn_explainer and HAS_TORCH_GEOMETRIC:
        logger.info("Initializing GNN model for explainer...")
        # Note: In practice, this model should be pre-trained on the dataset
        # For now, we'll use a simple initialized model
        gnn_model = GNNClassifier(
            num_node_features=4, num_classes=len(config.DATASET_COLUMNS["labels"])
        )
        gnn_model.eval()
    elif use_gnn_explainer and not HAS_TORCH_GEOMETRIC:
        logger.warning(
            "GNN Explainer requested but torch-geometric not available, using heuristics"
        )
        use_gnn_explainer = False

    optimized_graphs = []

    with Timer("Graph optimization", logger):
        for i, cfg_graph in enumerate(cfg_graphs):
            if cfg_graph is None or cfg_graph.graph.number_of_nodes() == 0:
                optimized_graphs.append(cfg_graph)
                continue

            try:
                optimized = optimize_single_graph(
                    cfg_graph, gnn_model, use_gnn_explainer
                )
                optimized_graphs.append(optimized)
            except Exception as e:
                logger.error(f"Error optimizing graph {i}: {e}")
                optimized_graphs.append(cfg_graph)  # Keep original on error

            # Progress logging
            if (i + 1) % 1000 == 0:
                logger.info(f"Optimized {i + 1}/{len(cfg_graphs)} graphs")

    # Compute statistics
    nx_graphs_before = [g.graph for g in cfg_graphs if g and g.graph]
    nx_graphs_after = [g.graph for g in optimized_graphs if g and g.graph]

    stats_before = compute_graph_statistics(nx_graphs_before, "Before Optimization")
    stats_after = compute_graph_statistics(nx_graphs_after, "After Optimization")

    # Compare statistics
    comparison = compare_statistics(stats_before, stats_after)

    # Save statistics
    save_pickle(stats_after, config.STATS_AFTER_OPTIMIZATION, logger)

    # Save optimized graphs
    logger.info(
        f"Saving optimized graphs to cache: {config.PICKLE_OPTIMIZED_GRAPHS.name}"
    )
    save_pickle(optimized_graphs, config.PICKLE_OPTIMIZED_GRAPHS, logger)

    return optimized_graphs


# ============================================================================
# MAIN (for testing)
# ============================================================================
if __name__ == "__main__":
    import argparse

    from data_loader import get_label_names, load_train_test_datasets
    from graph_processor import process_dataset_to_graphs
    from utils import set_seed, setup_logging

    # Setup
    setup_logging()
    set_seed()

    # Parse arguments
    parser = argparse.ArgumentParser(description="Compare graph optimization with XAI")
    parser.add_argument(
        "--sample",
        type=int,
        default=1,
        help="Sample number to optimize (1-based index)",
    )
    parser.add_argument(
        "--dataset", choices=["train", "test"], default="train", help="Dataset to use"
    )
    parser.add_argument(
        "--method",
        choices=["gnn", "heuristic"],
        default="heuristic",
        help="Optimization method (GNN Explainer or heuristic)",
    )
    parser.add_argument(
        "--show-nodes", action="store_true", help="Show which nodes were kept/removed"
    )
    parser.add_argument(
        "--threshold", type=float, help="Custom SHAP threshold (default from config)"
    )
    args = parser.parse_args()

    logger.info("=" * 70)
    logger.info(f"Graph Optimization for Sample #{args.sample} ({args.dataset} set)")
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

    # Process single graph
    logger.info(f"\n🔧 Processing AST to Graph...")
    from graph_processor import CFGGraph, parse_cfg_json

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

    logger.info(f"  Original nodes: {cfg_graph.graph.number_of_nodes()}")
    logger.info(f"  Original edges: {cfg_graph.graph.number_of_edges()}")

    # Optimize graph
    use_gnn = args.method == "gnn"
    if use_gnn and not HAS_TORCH_GEOMETRIC:
        logger.warning("GNN Explainer not available, falling back to heuristic")
        use_gnn = False

    logger.info(f"\n🔬 Optimizing with {args.method.upper()} method...")

    # Override threshold if specified
    if args.threshold:
        original_threshold = config.SHAP_THRESHOLD
        config.SHAP_THRESHOLD = args.threshold
        logger.info(f"  Using custom SHAP threshold: {args.threshold}")

    # Initialize GNN model if needed
    gnn_model = None
    if use_gnn:
        logger.info("  Initializing GNN model...")
        gnn_model = GNNClassifier(
            num_node_features=4, num_classes=len(config.DATASET_COLUMNS["labels"])
        )
        gnn_model.eval()

    # Optimize single graph
    try:
        optimized_graph = optimize_single_graph(cfg_graph, gnn_model, use_gnn)
    except Exception as e:
        logger.error(f"Optimization failed: {e}")
        exit(1)

    # Restore threshold if changed
    if args.threshold:
        config.SHAP_THRESHOLD = original_threshold

    # Display results
    logger.info(f"\n📈 Optimization Results:")
    logger.info(f"  Original nodes: {cfg_graph.graph.number_of_nodes()}")
    logger.info(f"  Optimized nodes: {optimized_graph.graph.number_of_nodes()}")
    logger.info(
        f"  Nodes removed: {cfg_graph.graph.number_of_nodes() - optimized_graph.graph.number_of_nodes()}"
    )

    reduction_pct = (
        100
        * (
            1
            - optimized_graph.graph.number_of_nodes()
            / cfg_graph.graph.number_of_nodes()
        )
        if cfg_graph.graph.number_of_nodes() > 0
        else 0
    )
    logger.info(f"  Reduction: {reduction_pct:.1f}%")

    logger.info(f"\n  Original edges: {cfg_graph.graph.number_of_edges()}")
    logger.info(f"  Optimized edges: {optimized_graph.graph.number_of_edges()}")
    logger.info(
        f"  Edges removed: {cfg_graph.graph.number_of_edges() - optimized_graph.graph.number_of_edges()}"
    )

    # Node comparison
    if args.show_nodes:
        original_nodes = set(cfg_graph.graph.nodes())
        optimized_nodes = set(optimized_graph.graph.nodes())
        removed_nodes = original_nodes - optimized_nodes

        logger.info(f"\n🔍 Node Analysis:")
        logger.info(f"  Kept nodes: {len(optimized_nodes)}")
        logger.info(f"  Removed nodes: {len(removed_nodes)}")

        # Show node type distribution of removed nodes
        if removed_nodes:
            logger.info(f"\n📋 Removed Node Types:")
            removed_types = {}
            for node in removed_nodes:
                node_type = cfg_graph.graph.nodes[node].get("type", "Unknown")
                removed_types[node_type] = removed_types.get(node_type, 0) + 1

            sorted_types = sorted(
                removed_types.items(), key=lambda x: x[1], reverse=True
            )
            for node_type, count in sorted_types[:10]:
                logger.info(f"    {node_type}: {count}")

            if len(sorted_types) > 10:
                logger.info(f"    ... and {len(sorted_types) - 10} more types")

        # Show kept node type distribution
        logger.info(f"\n📋 Kept Node Types:")
        kept_types = {}
        for node in optimized_nodes:
            node_type = optimized_graph.graph.nodes[node].get("type", "Unknown")
            kept_types[node_type] = kept_types.get(node_type, 0) + 1

        sorted_types = sorted(kept_types.items(), key=lambda x: x[1], reverse=True)
        for node_type, count in sorted_types[:10]:
            logger.info(f"    {node_type}: {count}")

        if len(sorted_types) > 10:
            logger.info(f"    ... and {len(sorted_types) - 10} more types")

    # Compare graph complexity
    logger.info(f"\n📊 Graph Complexity:")

    # Calculate densities
    orig_density = (
        cfg_graph.graph.number_of_edges()
        / (cfg_graph.graph.number_of_nodes() * (cfg_graph.graph.number_of_nodes() - 1))
        if cfg_graph.graph.number_of_nodes() > 1
        else 0
    )
    opt_density = (
        optimized_graph.graph.number_of_edges()
        / (
            optimized_graph.graph.number_of_nodes()
            * (optimized_graph.graph.number_of_nodes() - 1)
        )
        if optimized_graph.graph.number_of_nodes() > 1
        else 0
    )

    logger.info(f"  Original density: {orig_density:.4f}")
    logger.info(f"  Optimized density: {opt_density:.4f}")

    # Average degrees
    orig_avg_deg = (
        sum(dict(cfg_graph.graph.degree()).values()) / cfg_graph.graph.number_of_nodes()
        if cfg_graph.graph.number_of_nodes() > 0
        else 0
    )
    opt_avg_deg = (
        sum(dict(optimized_graph.graph.degree()).values())
        / optimized_graph.graph.number_of_nodes()
        if optimized_graph.graph.number_of_nodes() > 0
        else 0
    )

    logger.info(f"  Original avg degree: {orig_avg_deg:.2f}")
    logger.info(f"  Optimized avg degree: {opt_avg_deg:.2f}")

    logger.info(f"\n✅ Done! Use --help to see all options")
