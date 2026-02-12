"""
Graph Processor for Smart Contract CFG
Handles CFG JSON parsing, NetworkX graph construction, and statistics computation
"""

import json
import networkx as nx
import numpy as np
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

import config
from utils import (
    get_logger,
    save_pickle,
    load_pickle,
    pickle_exists,
    timeit,
    Timer,
    compute_graph_statistics
)
from data_loader import VulnerabilityDataset


logger = get_logger(__name__)


class CFGGraph:
    """
    Wrapper class for Control Flow Graph / AST with metadata
    """
    
    def __init__(self, graph: nx.DiGraph, address: str, labels: np.ndarray, ast_json: str):
        """
        Initialize CFG/AST Graph
        
        Args:
            graph: NetworkX directed graph
            address: Contract address
            labels: Vulnerability labels
            ast_json: Original AST/CFG JSON string
        """
        self.graph = graph
        self.address = address
        self.labels = labels
        self.ast_json = ast_json  # Changed from cfg_json
        
    def get_statistics(self) -> Dict:
        """Get graph statistics"""
        return {
            'num_nodes': self.graph.number_of_nodes(),
            'num_edges': self.graph.number_of_edges(),
            'is_connected': nx.is_weakly_connected(self.graph),
            'num_components': nx.number_weakly_connected_components(self.graph),
        }
    
    def __repr__(self):
        return f"CFGGraph(nodes={self.graph.number_of_nodes()}, edges={self.graph.number_of_edges()}, address={self.address[:10]}...)"


def parse_cfg_json(cfg_string: str, address: str = "unknown") -> Optional[nx.DiGraph]:
    """
    Parse AST/CFG string to NetworkX graph
    Supports both JSON AST format (primary) and GraphViz DOT format (fallback)
    
    Args:
        cfg_string: AST JSON or CFG DOT string
        address: Contract address (for logging)
        
    Returns:
        NetworkX DiGraph or None if parsing fails
    """
    try:
        # First try JSON format (AST)
        if cfg_string.strip().startswith('{') or cfg_string.strip().startswith('['):
            try:
                ast_data = json.loads(cfg_string)
                graph = nx.DiGraph()
                
                # Parse AST recursively
                def parse_ast_node(node, parent_id=None, node_counter=[0]):
                    """Recursively parse AST node and add to graph"""
                    if not isinstance(node, dict):
                        return
                    
                    # Generate unique node ID
                    node_id = node_counter[0]
                    node_counter[0] += 1
                    
                    # Extract node info
                    node_name = node.get('name', 'Node')
                    node_type = node.get('name', node.get('nodeType', node.get('type', 'unknown')))
                    
                    # Add node to graph
                    graph.add_node(node_id, 
                                 label=node_name, 
                                 type=node_type,
                                 node_data=node)
                    
                    # Add edge from parent
                    if parent_id is not None:
                        graph.add_edge(parent_id, node_id)
                    
                    # Process children
                    children = node.get('children', [])
                    if children:
                        for child in children:
                            if isinstance(child, dict):
                                parse_ast_node(child, node_id, node_counter)
                    
                    # Process other list fields that might contain nodes
                    for key in ['body', 'statements', 'nodes', 'declarations']:
                        items = node.get(key, [])
                        if isinstance(items, list):
                            for item in items:
                                if isinstance(item, dict):
                                    parse_ast_node(item, node_id, node_counter)
                    
                    return node_id
                
                # Start parsing from root
                if isinstance(ast_data, dict):
                    parse_ast_node(ast_data)
                elif isinstance(ast_data, list):
                    # Handle list of root nodes
                    for item in ast_data:
                        if isinstance(item, dict):
                            parse_ast_node(item)
                
                if graph.number_of_nodes() > 0:
                    return graph
                else:
                    logger.warning(f"Empty graph from AST for {address}")
                    graph.add_node(0, label="empty")
                    return graph
                    
            except json.JSONDecodeError:
                pass  # Try DOT format next
        
        # Try DOT format (GraphViz) - fallback for CFG
        if cfg_string.strip().startswith('digraph'):
            try:
                # Use networkx to parse DOT format
                from io import StringIO
                graph = nx.DiGraph(nx.nx_pydot.read_dot(StringIO(cfg_string)))
                
                # Convert node IDs to integers if possible
                mapping = {}
                for node in graph.nodes():
                    try:
                        mapping[node] = int(node)
                    except (ValueError, TypeError):
                        mapping[node] = node
                
                graph = nx.relabel_nodes(graph, mapping)
                
                return graph
                
            except Exception as e:
                logger.error(f"Error parsing DOT format for {address}: {e}")
                # Try alternative method with pydot
                try:
                    import pydot
                    pydot_graph = pydot.graph_from_dot_data(cfg_string)[0]
                    graph = nx.DiGraph()
                    
                    # Add nodes
                    for node in pydot_graph.get_nodes():
                        node_name = node.get_name().strip('"')
                        if node_name and node_name not in ['node', 'edge', 'graph']:
                            try:
                                node_id = int(node_name)
                            except (ValueError, TypeError):
                                node_id = node_name
                            
                            # Extract label if exists
                            label = node.get_label()
                            if label:
                                label = label.strip('"')
                            
                            graph.add_node(node_id, label=label)
                    
                    # Add edges
                    for edge in pydot_graph.get_edges():
                        source = edge.get_source().strip('"')
                        target = edge.get_destination().strip('"')
                        
                        try:
                            source = int(source)
                        except (ValueError, TypeError):
                            pass
                        
                        try:
                            target = int(target)
                        except (ValueError, TypeError):
                            pass
                        
                        if source in graph.nodes() and target in graph.nodes():
                            graph.add_edge(source, target)
                    
                    return graph
                    
                except Exception as e2:
                    logger.error(f"Alternative DOT parsing also failed for {address}: {e2}")
                    return None
        
        # If neither JSON nor DOT, create minimal graph
        logger.warning(f"Unknown format for {address}, creating minimal graph")
        graph = nx.DiGraph()
        graph.add_node(0, label="unknown")
        return graph
        
    except Exception as e:
        logger.error(f"Error parsing AST/CFG for {address}: {e}")
        return None


@timeit
def process_dataset_to_graphs(
    dataset: VulnerabilityDataset,
    force_reprocess: bool = False,
    cache_file: str = None
) -> List[CFGGraph]:
    """
    Process dataset ASTs to NetworkX graphs
    
    Args:
        dataset: VulnerabilityDataset object
        force_reprocess: Force reprocessing even if cache exists
        cache_file: Custom cache file path
        
    Returns:
        List of CFGGraph objects
    """
    if cache_file is None:
        cache_file = config.PICKLE_PROCESSED_GRAPHS
    
    # Check cache
    if not force_reprocess and pickle_exists(cache_file):
        logger.info(f"Loading processed graphs from cache: {cache_file.name}")
        graphs = load_pickle(cache_file, logger)
        if graphs is not None:
            logger.info(f"Loaded {len(graphs)} graphs from cache")
            
            # Compute and display statistics
            nx_graphs = [g.graph for g in graphs if g and g.graph]
            stats = compute_graph_statistics(nx_graphs, "Processed AST Graphs")
            
            return graphs
    
    # Process ASTs
    logger.info(f"Processing {len(dataset)} ASTs to graphs...")
    
    graphs = []
    failed_count = 0
    
    with Timer("AST to Graph conversion", logger):
        for i in range(len(dataset)):
            sample = dataset[i]
            
            # Parse AST/CFG
            nx_graph = parse_cfg_json(sample['ast'], sample['address'])
            
            if nx_graph is not None and nx_graph.number_of_nodes() > 0:
                cfg_graph = CFGGraph(
                    graph=nx_graph,
                    address=sample['address'],
                    labels=sample['labels'],
                    ast_json=sample['ast']
                )
                graphs.append(cfg_graph)
            else:
                failed_count += 1
                graphs.append(None)
            
            # Progress logging
            if (i + 1) % 1000 == 0:
                logger.info(f"Processed {i + 1}/{len(dataset)} ASTs ({failed_count} failed)")
    
    logger.info(f"Successfully processed {len(graphs) - failed_count}/{len(dataset)} ASTs")
    logger.info(f"Failed to process: {failed_count}")
    
    # Compute statistics
    nx_graphs = [g.graph for g in graphs if g and g.graph]
    stats = compute_graph_statistics(nx_graphs, "Processed AST Graphs")
    
    # Save to cache
    logger.info(f"Saving processed graphs to cache: {cache_file.name}")
    save_pickle(graphs, cache_file, logger)
    
    # Save statistics
    save_pickle(stats, config.STATS_BEFORE_OPTIMIZATION, logger)
    
    return graphs


def get_entry_nodes(graph: nx.DiGraph) -> List:
    """
    Get entry nodes (nodes with no predecessors) from graph
    
    Args:
        graph: NetworkX graph
        
    Returns:
        List of entry node IDs
    """
    entry_nodes = [node for node in graph.nodes() if graph.in_degree(node) == 0]
    
    # If no entry nodes found, use the first node
    if not entry_nodes and graph.number_of_nodes() > 0:
        entry_nodes = [list(graph.nodes())[0]]
    
    return entry_nodes


def get_function_entry_points(graph: nx.DiGraph) -> List:
    """
    Identify function entry points in CFG
    
    Args:
        graph: NetworkX graph
        
    Returns:
        List of function entry node IDs
    """
    function_entries = []
    
    for node in graph.nodes():
        node_data = graph.nodes[node]
        
        # Check for function-related attributes
        node_type = node_data.get('type', node_data.get('node_type', ''))
        node_label = node_data.get('label', node_data.get('name', ''))
        
        # Identify function entries
        if any(keyword in str(node_type).lower() for keyword in ['function', 'entry', 'start']):
            function_entries.append(node)
        elif any(keyword in str(node_label).lower() for keyword in ['function', 'entry', 'start']):
            function_entries.append(node)
        
        # Also include nodes with no predecessors
        if graph.in_degree(node) == 0:
            if node not in function_entries:
                function_entries.append(node)
    
    # If no function entries found, use entry nodes
    if not function_entries:
        function_entries = get_entry_nodes(graph)
    
    return function_entries


def subgraph_from_nodes(graph: nx.DiGraph, nodes: List) -> nx.DiGraph:
    """
    Create subgraph from selected nodes
    
    Args:
        graph: Original graph
        nodes: List of node IDs to include
        
    Returns:
        Subgraph containing only selected nodes
    """
    return graph.subgraph(nodes).copy()


def compute_graph_complexity_metrics(graph: nx.DiGraph) -> Dict:
    """
    Compute complexity metrics for a graph
    
    Args:
        graph: NetworkX graph
        
    Returns:
        Dictionary of complexity metrics
    """
    metrics = {
        'num_nodes': graph.number_of_nodes(),
        'num_edges': graph.number_of_edges(),
        'density': nx.density(graph) if graph.number_of_nodes() > 0 else 0,
        'avg_degree': sum(dict(graph.degree()).values()) / graph.number_of_nodes() if graph.number_of_nodes() > 0 else 0,
    }
    
    try:
        # Cyclomatic complexity (for weakly connected graphs)
        num_components = nx.number_weakly_connected_components(graph)
        cyclomatic = graph.number_of_edges() - graph.number_of_nodes() + 2 * num_components
        metrics['cyclomatic_complexity'] = cyclomatic
    except:
        metrics['cyclomatic_complexity'] = 0
    
    return metrics


# ============================================================================
# MAIN (for testing)
# ============================================================================
if __name__ == "__main__":
    import argparse
    from utils import setup_logging, set_seed
    from data_loader import load_train_test_datasets, get_label_names
    
    # Setup
    setup_logging()
    set_seed()
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='View AST graph structure of a specific sample')
    parser.add_argument('--sample', type=int, default=1, help='Sample number to view (1-based index)')
    parser.add_argument('--dataset', choices=['train', 'test'], default='train', help='Dataset to use')
    parser.add_argument('--show-nodes', action='store_true', help='Show all nodes with details')
    parser.add_argument('--show-edges', action='store_true', help='Show all edges')
    parser.add_argument('--export-dot', type=str, help='Export graph to DOT file (provide filename)')
    parser.add_argument('--max-nodes', type=int, default=50, help='Max nodes to display if --show-nodes')
    args = parser.parse_args()
    
    logger.info("="*70)
    logger.info(f"Viewing AST Graph for Sample #{args.sample} ({args.dataset} set)")
    logger.info("="*70)
    
    # Load data
    train_dataset, test_dataset = load_train_test_datasets(force_reload=False)
    dataset = train_dataset if args.dataset == 'train' else test_dataset
    
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
    logger.info(f"  Labels: {labels} ({', '.join(active_labels) if active_labels else 'None'})")
    logger.info(f"  AST size: {len(dataset.asts[sample_idx])} characters")
    
    # Parse AST to graph
    logger.info(f"\n🔧 Parsing AST to Graph...")
    graph = parse_cfg_json(dataset.asts[sample_idx])
    
    if graph is None or graph.number_of_nodes() == 0:
        logger.error("Failed to parse AST")
        exit(1)
    
    cfg_graph = CFGGraph(
        graph=graph,
        address=dataset.addresses[sample_idx],
        labels=labels,
        ast_json=dataset.asts[sample_idx]
    )
    
    # Display graph statistics
    stats = cfg_graph.get_statistics()
    logger.info(f"\n📈 Graph Statistics:")
    logger.info(f"  Total nodes: {stats['num_nodes']}")
    logger.info(f"  Total edges: {stats['num_edges']}")
    
    # Compute additional metrics
    if stats['num_nodes'] > 0:
        avg_degree = sum(dict(graph.degree()).values()) / stats['num_nodes']
        density = stats['num_edges'] / (stats['num_nodes'] * (stats['num_nodes'] - 1)) if stats['num_nodes'] > 1 else 0
        logger.info(f"  Average degree: {avg_degree:.2f}")
        logger.info(f"  Graph density: {density:.4f}")
    
    logger.info(f"  Weakly connected: {stats['is_connected']}")
    logger.info(f"  Connected components: {stats['num_components']}")
    
    # Get entry points
    entry_nodes = get_entry_nodes(graph)
    function_entries = get_function_entry_points(graph)
    logger.info(f"\n🚪 Entry Points:")
    logger.info(f"  Entry nodes (in-degree 0): {len(entry_nodes)}")
    logger.info(f"  Function entry points: {len(function_entries)}")
    
    # Node type distribution
    logger.info(f"\n📋 Node Type Distribution:")
    node_types = {}
    for node in graph.nodes():
        node_data = graph.nodes[node]
        node_type = node_data.get('type', 'Unknown')
        node_types[node_type] = node_types.get(node_type, 0) + 1
    
    # Sort by count descending
    sorted_types = sorted(node_types.items(), key=lambda x: x[1], reverse=True)
    for node_type, count in sorted_types[:10]:  # Show top 10
        percentage = (count / stats['num_nodes']) * 100
        logger.info(f"  {node_type}: {count} ({percentage:.1f}%)")
    
    if len(sorted_types) > 10:
        logger.info(f"  ... and {len(sorted_types) - 10} more types")
    
    # Show nodes if requested
    if args.show_nodes:
        logger.info(f"\n🔍 Node Details (showing up to {args.max_nodes}):")
        logger.info("="*70)
        for i, node in enumerate(list(graph.nodes())[:args.max_nodes]):
            node_data = graph.nodes[node]
            node_type = node_data.get('type', 'Unknown')
            in_deg = graph.in_degree(node)
            out_deg = graph.out_degree(node)
            logger.info(f"  [{i+1}] Node {node}:")
            logger.info(f"      Type: {node_type}")
            logger.info(f"      In-degree: {in_deg}, Out-degree: {out_deg}")
            
            # Show some attributes
            attrs = {k: v for k, v in node_data.items() if k != 'type' and not k.startswith('_')}
            if attrs:
                logger.info(f"      Attributes: {list(attrs.keys())[:5]}")
        
        if stats['num_nodes'] > args.max_nodes:
            logger.info(f"\n  ... and {stats['num_nodes'] - args.max_nodes} more nodes")
            logger.info(f"      Use --max-nodes to show more")
    
    # Show edges if requested
    if args.show_edges:
        logger.info(f"\n🔗 Edge Details (showing first 50):")
        logger.info("="*70)
        for i, (src, dst) in enumerate(list(graph.edges())[:50]):
            src_type = graph.nodes[src].get('type', 'Unknown')
            dst_type = graph.nodes[dst].get('type', 'Unknown')
            logger.info(f"  [{i+1}] {src} ({src_type}) -> {dst} ({dst_type})")
        
        if stats['num_edges'] > 50:
            logger.info(f"\n  ... and {stats['num_edges'] - 50} more edges")
    
    # Export to DOT if requested
    if args.export_dot:
        try:
            import pydot
            from networkx.drawing.nx_pydot import write_dot
            
            output_path = config.OUTPUT_DIR / args.export_dot
            if not output_path.suffix:
                output_path = output_path.with_suffix('.dot')
            
            logger.info(f"\n💾 Exporting graph to DOT format...")
            write_dot(graph, str(output_path))
            logger.info(f"  Saved to: {output_path}")
            logger.info(f"  View with: dot -Tpng {output_path} -o graph.png")
        except ImportError:
            logger.error("pydot not installed. Cannot export DOT file.")
        except Exception as e:
            logger.error(f"Failed to export DOT file: {e}")
    
    logger.info(f"\n✅ Done! Use --help to see all options")
