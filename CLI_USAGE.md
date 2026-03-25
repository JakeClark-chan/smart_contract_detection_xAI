# CLI Tools Usage Guide

## 1. data_loader.py - Dataset Exploration & Sample Viewing

Explore the dataset with comprehensive statistics or view specific samples:

```bash
# View full dataset overview (default mode)
python data_loader.py
# Shows: dataset sizes, columns, label names, data quality, 
#        AST size statistics, label distributions, multi-label stats

# View specific sample with preview (first 500 chars of AST)
python data_loader.py --sample 10

# View specific sample with FULL AST content
python data_loader.py --sample 10 --show-ast

# View from test set
python data_loader.py --sample 5 --dataset test

# Analyze a range of samples (e.g., samples 1-100)
python data_loader.py --range 1-100
# Shows: label distribution, AST size stats, multi-label stats for subset

# Control AST preview length
python data_loader.py --sample 10 --max-ast-chars 1000
```

**Output Modes:**
1. **Default (no sample specified):**
   - Dataset sizes (train: 8,444, test: 2,111)
   - Column descriptions and label name mappings
   - Data quality check (nulls, duplicates, unique addresses)
   - AST size statistics (min, max, mean, median)
   - Label distributions with percentages
   - Multi-label statistics (samples with 0/1/2+ vulnerabilities, average per sample)

2. **Sample View (--sample N):**
   - Address (contract identifier)
   - All label values with checkmarks (✓/✗)
   - AST statistics (total characters, lines, node count)
   - AST JSON preview (first 500 chars by default, or full with --show-ast)

3. **Range Analysis (--range 1-100):**
   - Label distribution for subset
   - AST size statistics for subset
   - Multi-label statistics for subset

---

## 2. sequence_converter.py - View Graph Sequences

View the converted sequence for any sample:

```bash
# Basic usage - view sample 10 from train set
python sequence_converter.py --sample 10

# View from test set with BFS traversal
python sequence_converter.py --sample 5 --dataset test --traversal bfs

# Show full sequence (not truncated)
python sequence_converter.py --sample 1 --show-full

# Control truncation length
python sequence_converter.py --sample 1 --max-chars 1000
```

**Output:**
- Sample address, labels, AST size
- Graph nodes/edges
- Sequence length, BERT truncation warning
- Sequence content (formatted with node types)

---

## 3. graph_processor.py - View AST Graph Structure

Analyze the graph structure of any sample:

```bash
# Basic usage - view graph stats for sample 10
python graph_processor.py --sample 10

# Show detailed node information (limited to 20 nodes)
python graph_processor.py --sample 10 --show-nodes --max-nodes 20

# Show edge connections
python graph_processor.py --sample 10 --show-edges

# View from test set
python graph_processor.py --sample 5 --dataset test

# Export graph to DOT format for visualization
python graph_processor.py --sample 10 --export-dot sample_10_graph
# Then convert to image: dot -Tpng output/sample_10_graph.dot -o graph.png
```

**Output:**
- Sample address, labels
- Graph statistics (nodes, edges, density, degree)
- Entry points and function entries
- Node type distribution
- Optional: detailed node/edge information

---

## 4. xai_optimizer.py - Compare Graph Optimization

Compare original vs optimized graphs using XAI:

```bash
# Basic usage - optimize sample 10 with heuristic method
python xai_optimizer.py --sample 10

# Show which nodes were kept/removed
python xai_optimizer.py --sample 10 --show-nodes

# Use custom SHAP threshold
python xai_optimizer.py --sample 1 --threshold 0.3 --show-nodes

# Try GNN explainer method (if torch-geometric available)
python xai_optimizer.py --sample 10 --method gnn

# Optimize from test set
python xai_optimizer.py --sample 5 --dataset test --show-nodes
```

**Output:**
- Sample address, labels
- Original vs optimized graph statistics
- Node/edge reduction percentage
- Graph complexity comparison (density, avg degree)
- Optional: removed/kept node type distributions

---

## Common Options

All tools support:
- `--sample N`: Sample number to view (1-based index)
- `--dataset {train,test}`: Choose dataset (default: train)
- `--help`: Show help message

## Example Workflow

```bash
# 1. Explore dataset overview
python data_loader.py
# See: total samples, label distributions, AST size stats, multi-label patterns

# 2. Analyze a range of samples
python data_loader.py --range 1-100
# Get statistics for first 100 samples

# 3. View specific sample details
python data_loader.py --sample 10
# See: address, all labels, AST preview

# 4. View graph structure
python graph_processor.py --sample 10 --show-nodes --max-nodes 15

# 5. See optimization impact
python xai_optimizer.py --sample 10 --show-nodes

# 6. View final sequence
python sequence_converter.py --sample 10 --max-chars 800
```

## Dataset Info
- Train: 8,444 samples
- Test: 2,111 samples
- Labels: Arithmetic, LowLevelCall, DoS, TimeManipulation, Reentrancy
