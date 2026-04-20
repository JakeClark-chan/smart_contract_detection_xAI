"""
Generate Node/Edge Statistics for AST Graphs (Before Optimization)
Downloads dataset from HuggingFace, parses AST JSON to NetworkX graphs,
and computes per-contract node/edge statistics with distribution analysis.

Usage:
    uv run python generate_graph_stats.py
"""

import json
import csv
import statistics
from pathlib import Path

import networkx as nx
from datasets import load_dataset


# ============================================================================
# AST PARSER (standalone, no project imports needed)
# ============================================================================
def parse_ast_to_graph(ast_string: str) -> nx.DiGraph | None:
    """Parse AST JSON string to NetworkX directed graph."""
    try:
        if not ast_string or not ast_string.strip():
            return None

        ast_data = json.loads(ast_string)
        graph = nx.DiGraph()
        counter = [0]

        def _add_node(node, parent_id=None):
            if not isinstance(node, dict):
                return
            node_id = counter[0]
            counter[0] += 1
            node_name = node.get("name", node.get("nodeType", node.get("type", "Node")))
            graph.add_node(node_id, label=node_name, type=node_name)
            if parent_id is not None:
                graph.add_edge(parent_id, node_id)
            for key in ["children", "body", "statements", "nodes", "declarations"]:
                items = node.get(key, [])
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            _add_node(item, node_id)

        if isinstance(ast_data, dict):
            _add_node(ast_data)
        elif isinstance(ast_data, list):
            for item in ast_data:
                if isinstance(item, dict):
                    _add_node(item)

        return graph if graph.number_of_nodes() > 0 else None
    except Exception:
        return None


# ============================================================================
# MAIN
# ============================================================================
def main():
    dataset_name = "JakeClark/soliaudit-dasp-ast-graph"
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    print(f"Loading dataset from HuggingFace: {dataset_name}")
    ds = load_dataset(dataset_name)

    all_stats = []  # (split, address, num_nodes, num_edges)

    for split_name in ["train", "test"]:
        if split_name not in ds:
            print(f"  ⚠ Split '{split_name}' not found, skipping")
            continue

        split = ds[split_name]
        print(f"\n{'='*70}")
        print(f"Processing {split_name} split ({len(split)} samples)")
        print(f"{'='*70}")

        split_stats = []
        failed = 0

        for i, row in enumerate(split):
            address = row.get("address", f"sample_{i}")
            ast_str = row.get("AST", "")
            graph = parse_ast_to_graph(ast_str)

            if graph is not None:
                n_nodes = graph.number_of_nodes()
                n_edges = graph.number_of_edges()
            else:
                n_nodes = 0
                n_edges = 0
                failed += 1

            split_stats.append((split_name, address, n_nodes, n_edges))

            if (i + 1) % 2000 == 0:
                print(f"  Processed {i+1}/{len(split)} ({failed} failed)")

        all_stats.extend(split_stats)
        print(f"  Done: {len(split) - failed} success, {failed} failed")

    # ========================================================================
    # Save per-contract CSV
    # ========================================================================
    csv_path = output_dir / "graph_node_edge_stats.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["split", "address", "num_nodes", "num_edges"])
        writer.writerows(all_stats)
    print(f"\n✅ Per-contract stats saved to: {csv_path}")

    # ========================================================================
    # Compute summary statistics
    # ========================================================================
    node_buckets = [10, 50, 100, 200, 500, 1000, 2000]

    lines = []
    lines.append("# Graph Node/Edge Statistics (Before Optimization)")
    lines.append("")
    lines.append(f"Dataset: `{dataset_name}`")
    lines.append("")

    for split_name in ["train", "test"]:
        rows = [(n, e) for (s, _, n, e) in all_stats if s == split_name and n > 0]
        if not rows:
            continue

        nodes_list = [r[0] for r in rows]
        edges_list = [r[1] for r in rows]
        total = len(rows)

        lines.append(f"## {split_name.capitalize()} Set ({total} valid samples)")
        lines.append("")

        # Summary table
        lines.append("### Summary Statistics")
        lines.append("")
        lines.append("| Metric | Nodes | Edges |")
        lines.append("|--------|-------|-------|")
        lines.append(f"| Mean | {statistics.mean(nodes_list):.1f} | {statistics.mean(edges_list):.1f} |")
        lines.append(f"| Median | {statistics.median(nodes_list):.1f} | {statistics.median(edges_list):.1f} |")
        lines.append(f"| Std Dev | {statistics.stdev(nodes_list):.1f} | {statistics.stdev(edges_list):.1f} |")
        lines.append(f"| Min | {min(nodes_list)} | {min(edges_list)} |")
        lines.append(f"| Max | {max(nodes_list)} | {max(edges_list)} |")

        # Percentiles
        sorted_nodes = sorted(nodes_list)
        sorted_edges = sorted(edges_list)
        for p in [25, 50, 75, 90, 95, 99]:
            idx = int(len(sorted_nodes) * p / 100)
            idx = min(idx, len(sorted_nodes) - 1)
            lines.append(f"| P{p} | {sorted_nodes[idx]} | {sorted_edges[idx]} |")

        lines.append("")

        # Node count distribution (buckets)
        lines.append("### Node Count Distribution")
        lines.append("")
        lines.append("| Node Range | Count | Percentage |")
        lines.append("|-----------|-------|------------|")

        prev = 0
        for bucket in node_buckets:
            count = sum(1 for n in nodes_list if prev < n <= bucket)
            pct = count / total * 100
            lines.append(f"| {prev+1}–{bucket} | {count} | {pct:.1f}% |")
            prev = bucket
        # > last bucket
        count = sum(1 for n in nodes_list if n > node_buckets[-1])
        pct = count / total * 100
        lines.append(f"| >{node_buckets[-1]} | {count} | {pct:.1f}% |")
        lines.append("")

        # Cumulative "samples with nodes > X"
        lines.append("### Samples Exceeding Node Thresholds")
        lines.append("")
        lines.append("| Threshold | Count | Percentage |")
        lines.append("|-----------|-------|------------|")
        for threshold in [10, 50, 100, 200, 500, 1000, 1500, 2000]:
            count = sum(1 for n in nodes_list if n > threshold)
            pct = count / total * 100
            lines.append(f"| > {threshold} nodes | {count} | {pct:.1f}% |")
        lines.append("")

    # ========================================================================
    # Combined table (train + test)
    # ========================================================================
    lines.append("## Combined Summary (Train + Test)")
    lines.append("")
    all_nodes = [n for (s, _, n, e) in all_stats if n > 0]
    all_edges = [e for (s, _, n, e) in all_stats if n > 0]
    total_all = len(all_nodes)
    lines.append(f"Total valid samples: {total_all}")
    lines.append("")
    lines.append("| Metric | Nodes | Edges |")
    lines.append("|--------|-------|-------|")
    lines.append(f"| Mean | {statistics.mean(all_nodes):.1f} | {statistics.mean(all_edges):.1f} |")
    lines.append(f"| Median | {statistics.median(all_nodes):.1f} | {statistics.median(all_edges):.1f} |")
    lines.append(f"| Min | {min(all_nodes)} | {min(all_edges)} |")
    lines.append(f"| Max | {max(all_nodes)} | {max(all_edges)} |")
    lines.append("")

    # Save markdown
    md_path = output_dir / "graph_node_edge_stats.md"
    with open(md_path, "w") as f:
        f.write("\n".join(lines))
    print(f"✅ Summary report saved to: {md_path}")

    # Print summary to console
    print("\n" + "\n".join(lines))


if __name__ == "__main__":
    main()
