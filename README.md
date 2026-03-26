# Smart Contract Vulnerability Detection with XAI

## Overview

This project implements a novel approach for **smart contract vulnerability detection** using:
- **Explainable AI (XAI)**: GNN Explainer to identify sensitive nodes in Control Flow Graphs (CFG)
- **Graph-to-Sequence Optimization**: DFS traversal with smart truncation to convert optimized CFG subgraphs to BERT-compatible sequences
- **BERT-based Classification**: Multi-label classification using BERT, DistilBERT, CodeBERT, and other transformer models

### Key Features
✅ **Efficient Pickle Caching**: Minimize preprocessing time with automatic cache management  
✅ **Multi-GPU Support**: Automatic detection and configuration for single/multiple GPU training  
✅ **Modular Design**: Each pipeline step is in a separate module for easy modification  
✅ **XAI Optimization**: Compare results before/after graph optimization  
✅ **Smart Truncation**: BERT 512-token limit respected with importance-weighted sampling
✅ **Compact Token Format**: Optimized tokens (50% shorter) for better model efficiency
✅ **Comprehensive Logging**: Detailed logs with timing information for every step  
✅ **Model Comparison**: Easy switching between BERT models and performance comparison  

---

## Graph Sequence Optimization

### Problem
Raw AST graphs produce verbose tokens that exceed BERT's 512 token limit:
```
# Before (verbose format)
SourceUnit:SourceUnit PragmaDirective:PragmaDirective ContractDefinition:ContractDefinition...
# Mean: 838 tokens, 55.5% exceed BERT limit
```

### Solution: Three-Level Optimization

1. **Compact Token Format**
   ```
   # After (compact format)
   SourceUnit PragmaDirective ContractDefinition...
   # 50% shorter tokens
   ```

2. **Smart Truncation** (importance-weighted + position sampling)
   - 60% from high-importance nodes (entry points, high-degree)
   - 30% from medium importance nodes
   - 10% from tail (captures function endings)

3. **Top-N Node Filtering**
   - `optimized_80p`: Keep top 80% most important nodes
   - `optimized_50p`: Keep top 50% most important nodes
   - `optimized_20p`: Keep top 20% most important nodes

### Node Importance Scoring
```
Score = base_score + role_bonus + position_score

Where:
- base_score: (in_degree + out_degree) / (2 * num_nodes - 2)
- role_bonus: +0.3 (entry), +0.2 (exit), +0.1 (branch)
- position_score: 1.0 - (node_index / num_nodes) * 0.3
```

### Results
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| File Size | 292 MB | 77 MB | **74% smaller** |
| Max tokens | 12,455 | 512 | **BERT limit respected** |
| >512 tokens | 55.5% | 0% | **All fit in BERT** |
| Token format | `Type:Type` | `Type` | **50% shorter** |

---

## Project Structure

```
smart_contract_detection_xAI/
├── config.py                 # Central configuration (paths, models, hyperparameters)
├── utils.py                  # Logging, GPU detection, timing, pickle caching
├── data_loader.py           # Dataset loading, train/test split, caching
├── graph_processor.py       # CFG JSON parsing, NetworkX graph creation
├── xai_optimizer.py         # GNN Explainer, node importance, graph optimization
├── sequence_converter.py    # DFS/BFS traversal, smart truncation, graph-to-sequence
├── model_trainer.py         # BERT training, evaluation, metrics computation
├── main.py                  # Main orchestrator script
├── generate_optimized_dataset.py  # Dataset generation with XAI optimizations
├── requirements.txt         # Python dependencies
├── soliaudit_dasp_v2.csv   # Dataset (SoliAudit) for Reentrancy labels
├── soliaudit_graph_train.csv  # Training data (8,444 samples)
├── soliaudit_graph_test.csv   # Test data (2,111 samples)
├── cache/                   # Pickle cache directory (auto-created)
├── models/                  # Trained models directory (auto-created)
├── output/                  # Results and comparison files (auto-created)
│   ├── train_optimized_dataset.csv  # Optimized train sequences
│   └── test_optimized_dataset.csv   # Optimized test sequences
└── logs/                    # Log files (auto-created)
```

---

## Dataset Output Format

Generated datasets include 5 sequence columns with different optimization levels:

| Column | Description | Typical Tokens |
|--------|-------------|----------------|
| `address` | Contract address | - |
| `before_optimized` | Full graph, truncated to 512 | 29-156 |
| `optimized_80p` | Top 80% important nodes | 156-186 |
| `optimized_50p` | Top 50% important nodes | 133-187 |
| `optimized_20p` | Top 20% important nodes | 106-133 |
| `Arithmetic` | Vulnerability label (0/1) | - |
| `Unchecked Return Values For Low Level Calls` | Vulnerability label | - |
| `Denial of Service` | Vulnerability label | - |
| `Time manipulation` | Vulnerability label | - |
| `Reentrancy` | Vulnerability label | - |

---

## Installation

### 1. Install Dependencies

```bash
# Install PyTorch (with CUDA support if available)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Install PyTorch Geometric
pip install torch-geometric torch-scatter torch-sparse

# Install other requirements
pip install -r requirements.txt
```

### 2. Verify GPU Setup (Optional but Recommended)

```python
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}, GPU count: {torch.cuda.device_count()}')"
```

---

## Usage

### Generate Optimized Dataset

```bash
# Generate full optimized dataset (train + test)
python generate_optimized_dataset.py --force-reload --workers 12

# Quick test with subset
python generate_optimized_dataset.py --subset 100

# Custom workers
python generate_optimized_dataset.py --workers 8 --batch-size 50
```

### Train Model

```bash
# Basic usage (default: BERT model)
python main.py

# Quick testing (use subset)
python main.py --subset 1000

# Skip XAI optimization (baseline comparison)
python main.py --skip-optimization

# Use different model
python main.py --model distilbert
python main.py --model codebert

# Compare multiple models
python main.py --compare-models

# Use GNN Explainer (more accurate but slower)
python main.py --use-gnn-explainer

# Force reload all data (clear cache)
python main.py --force-reload

# Custom training epochs
python main.py --epochs 5

# Combine options
python main.py --model distilbert --subset 5000 --epochs 3 --use-gnn-explainer
```

---

## Command-Line Arguments

### Dataset Generation (`generate_optimized_dataset.py`)

| Argument | Description | Default |
|----------|-------------|---------|
| `--force-reload` | Force regeneration | False |
| `--workers` | Number of parallel workers | All CPU cores |
| `--batch-size` | Samples per batch | 100 |
| `--subset` | Use subset of data | None (all) |

### Training (`main.py`)

| Argument | Description | Default |
|----------|-------------|---------|
| `--force-reload` | Force reload all data (ignore cache) | False |
| `--skip-optimization` | Skip XAI optimization (use original graphs) | False |
| `--model` | Model to train (bert/distilbert/codebert/graphcodebert/gpt2) | bert |
| `--compare-models` | Compare multiple models (bert and distilbert) | False |
| `--use-gnn-explainer` | Use GNN Explainer for optimization | False (uses heuristics) |
| `--subset` | Use only a subset of data (for testing) | None (use all) |
| `--epochs` | Number of training epochs | 3 (from config) |

---

## Pipeline Steps

### Step 1: Load Dataset
- Loads `soliaudit_graph_train.csv` and `soliaudit_graph_test.csv`
- Maps Reentrancy labels from `soliaudit_dasp_v2.csv`
- Extracts: `address`, `AST`, and 5 vulnerability labels
- Caches to `cache/train_dataset.pkl` and `cache/test_dataset.pkl`

### Step 2: Process ASTs to Graphs
- Parses AST JSON to NetworkX DiGraph objects
- Extracts node types and relationships
- Computes statistics (nodes, edges)
- Caches to `cache/processed_graphs.pkl`

### Step 3: Compute Node Importance
- Fast heuristics: degree + structural role + position
- Combines: entry/exit nodes, branching, graph position
- Produces normalized importance scores (0-1)

### Step 4: Graph Optimization (XAI)
- Top-N filtering: Keep 80%, 50%, or 20% most important nodes
- GNN Explainer alternative (slower but more accurate)
- Computes before/after statistics
- Caches to `cache/optimized_graphs.pkl`

### Step 5: Convert Graphs to Sequences
- DFS traversal starting from entry nodes
- **Compact token format**: `Type` instead of `Type:Type`
- **Smart truncation**: Importance-weighted sampling (60/30/10)
- Respects BERT's 512 token limit
- Caches to `cache/sequences.pkl`

### Step 6: Train Model(s)
- Tokenizes sequences with HuggingFace tokenizer
- Fine-tunes BERT-based models for multi-label classification
- Auto-detects and uses multiple GPUs if available
- Computes metrics: accuracy, precision, recall, F1
- Saves models to `models/<model_name>/`

### Step 7: Save Results
- Saves experiment results to `output/experiment_results.json`
- Saves comparison CSV to `output/comparison_results.csv`
- Logs all steps to `logs/experiment.log`

---

## Configuration

Edit `config.py` to customize:

### Model Selection
```python
DEFAULT_MODEL = 'bert'  # Change to 'distilbert', 'codebert', etc.
```

### XAI Parameters
```python
GNN_EXPLAINER_EPOCHS = 200     # GNN Explainer training epochs
SHAP_THRESHOLD = 0.5           # Node importance threshold
TOP_NODES_PERCENTAGE = 0.2     # Keep top 20% of nodes
```

### Sequence Processing
```python
MAX_SEQUENCE_LENGTH = 512      # BERT token limit (strict)
```

### Training Parameters
```python
TRAINING_ARGS = {
    'num_train_epochs': 3,
    'per_device_train_batch_size': 8,
    'learning_rate': 2e-5,
    # ... more parameters
}
```

---

## Vulnerability Labels

The project detects 5 types of vulnerabilities:

| Label | Description | Train Distribution |
|-------|-------------|-------------------|
| `Arithmetic` | Integer overflow/underflow | 92.5% |
| `Unchecked Return Values For Low Level Calls` | Unchecked external calls | 55.9% |
| `Denial of Service` | DoS attacks | 46.6% |
| `Time manipulation` | Timestamp dependence | 31.6% |
| `Reentrancy` | Reentrancy attacks | 39.1% |

---

## Output Files

### `output/experiment_results.json`
Complete experiment configuration and results in JSON format.

### `output/comparison_results.csv`
Model comparison table with metrics:
- Train time, inference time
- Accuracy, Precision, Recall, F1 score

### `output/train_optimized_dataset.csv`
Generated training dataset with optimized sequences.

### `output/test_optimized_dataset.csv`
Generated test dataset with optimized sequences.

### `logs/experiment.log`
Detailed logs with timing information for debugging.

### `models/<model_name>/`
Trained model checkpoints and tokenizer.

---

## Performance Optimization Tips

### Use Pickle Cache
The pipeline automatically caches processed data. Don't use `--force-reload` unless you've changed the dataset.

### Use Multiple Workers for Dataset Generation
```bash
python generate_optimized_dataset.py --workers 12 --batch-size 100
```

### Use Multiple GPUs
If you have multiple GPUs, they will be automatically detected and used via DataParallel.

### Start with Subset
Test your changes with `--subset 1000` before running on the full dataset.

### Use DistilBERT for Speed
DistilBERT is 40% faster than BERT with minimal accuracy loss:
```bash
python main.py --model distilbert
```

### Skip GNN Explainer for Testing
Use simple heuristics (default) for faster optimization during development:
```bash
python main.py  # Uses heuristics by default
```

---

## Troubleshooting

### Out of Memory (OOM)
- Reduce batch size in `config.py`: `per_device_train_batch_size = 4`
- Use subset: `--subset 5000`
- Use DistilBERT instead of BERT

### CUDA Out of Memory
- Disable multi-GPU: Set `USE_MULTI_GPU = False` in `config.py`
- Reduce sequence length: Not recommended (already optimized)

### Slow Dataset Generation
- Increase workers: `--workers 12`
- Increase batch size: `--batch-size 100`
- Use subset for testing: `--subset 100`

### Import Errors
- Install PyTorch Geometric properly:
  ```bash
  pip install torch-geometric torch-scatter torch-sparse
  ```

---

## Research Context

This implementation is based on the research proposal:
- **Method**: AST → Node Importance → Optimized Sequence → BERT Classification
- **Dataset**: SoliAudit (17,980 smart contract samples)
- **XAI Technique**: Graph-based heuristics for node importance
- **Innovation**: Token-efficient sequence generation for BERT (<=512 tokens)

### Expected Experiments
1. **Baseline**: AST → Sequence (no optimization)
2. **Proposed**: AST → Node Importance → Optimized Sequence
3. **Comparison**: Different optimization thresholds (80%, 50%, 20%)
4. **Model Comparison**: Different BERT models (BERT, DistilBERT, CodeBERT)
5. **Metrics**: Training time, inference time, accuracy, F1 score, node reduction

---

## Citation

If you use this code, please cite:
```
Smart Contract Vulnerability Detection using XAI and BERT-based Models
Bruh, 2024
```

---

## License

Bruh

---

## Contact

For questions or issues, please open an issue on the repository or contact nope@nope.com.
