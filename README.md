# Smart Contract Vulnerability Detection with XAI

## Overview

This project implements a novel approach for **smart contract vulnerability detection** using:
- **Explainable AI (XAI)**: GNN Explainer to identify sensitive nodes in Control Flow Graphs (CFG)
- **Graph-to-Sequence Optimization**: DFS traversal to convert optimized CFG subgraphs to sequences
- **BERT-based Classification**: Multi-label classification using BERT, DistilBERT, CodeBERT, and other transformer models

### Key Features
✅ **Efficient Pickle Caching**: Minimize preprocessing time with automatic cache management  
✅ **Multi-GPU Support**: Automatic detection and configuration for single/multiple GPU training  
✅ **Modular Design**: Each pipeline step is in a separate module for easy modification  
✅ **XAI Optimization**: Compare results before/after graph optimization  
✅ **Comprehensive Logging**: Detailed logs with timing information for every step  
✅ **Model Comparison**: Easy switching between BERT models and performance comparison  

---

## Project Structure

```
smart_contract_detection_xAI/
├── config.py                 # Central configuration (paths, models, hyperparameters)
├── utils.py                  # Logging, GPU detection, timing, pickle caching
├── data_loader.py           # Dataset loading, train/test split, caching
├── graph_processor.py       # CFG JSON parsing, NetworkX graph creation
├── xai_optimizer.py         # GNN Explainer, node importance, graph optimization
├── sequence_converter.py    # DFS/BFS traversal, graph-to-sequence conversion
├── model_trainer.py         # BERT training, evaluation, metrics computation
├── main.py                  # Main orchestrator script
├── requirements.txt         # Python dependencies
├── soliaudit_dasp_v2.csv   # Dataset (SoliAudit)
├── cache/                   # Pickle cache directory (auto-created)
├── models/                  # Trained models directory (auto-created)
├── output/                  # Results and comparison files (auto-created)
└── logs/                    # Log files (auto-created)
```

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

### Basic Usage (Default: BERT model)

```bash
python main.py
```

### Quick Testing (Use Subset)

```bash
python main.py --subset 1000
```

### Skip XAI Optimization (Baseline Comparison)

```bash
python main.py --skip-optimization
```

### Use Different Model

```bash
python main.py --model distilbert
python main.py --model codebert
```

### Compare Multiple Models

```bash
python main.py --compare-models
```

### Use GNN Explainer (More Accurate but Slower)

```bash
python main.py --use-gnn-explainer
```

### Force Reload All Data (Clear Cache)

```bash
python main.py --force-reload
```

### Custom Training Epochs

```bash
python main.py --epochs 5
```

### Combine Options

```bash
python main.py --model distilbert --subset 5000 --epochs 3 --use-gnn-explainer
```

---

## Command-Line Arguments

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
- Loads `soliaudit_dasp_v2.csv`
- Extracts: `Addr`, `CFG`, and vulnerability labels (4 labels)
- Caches to `cache/raw_dataset.pkl`

### Step 2: Split Dataset
- 80% training, 20% testing
- Stratified split based on vulnerability presence
- Caches to `cache/train_dataset.pkl` and `cache/test_dataset.pkl`

### Step 3: Process CFGs to Graphs
- Parses CFG strings (GraphViz DOT format) to NetworkX DiGraph objects
- Supports both DOT format (primary) and JSON format (fallback)
- Computes statistics (nodes, edges)
- Caches to `cache/processed_graphs.pkl`

### Step 4: Optimize Graphs with XAI (Optional)
- Uses GNN Explainer or heuristics to identify sensitive nodes
- Filters graphs based on SHAP threshold or top N% nodes
- Computes before/after statistics
- Caches to `cache/optimized_graphs.pkl`

### Step 5: Convert Graphs to Sequences
- DFS traversal starting from function entry points
- Converts node paths to token sequences
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
SHAP_THRESHOLD = 0.5           # Node importance threshold
TOP_NODES_PERCENTAGE = 0.2     # Keep top 20% of nodes
GNN_EXPLAINER_EPOCHS = 200     # GNN Explainer training epochs
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

### Dataset Configuration
```python
TRAIN_TEST_SPLIT = 0.8  # 80% train, 20% test
MAX_SEQUENCE_LENGTH = 512  # BERT token limit
```

---

## Vulnerability Labels

The project detects 4 types of vulnerabilities:
1. **Unchecked_Low_Level_Calls** - Unchecked external calls
2. **Arithmetic** - Integer overflow/underflow
3. **Reentrancy** - Reentrancy attacks (e.g., DAO hack)
4. **Time_Manipulation** - Timestamp dependence

---

## Output Files

### `output/experiment_results.json`
Complete experiment configuration and results in JSON format.

### `output/comparison_results.csv`
Model comparison table with metrics:
- Train time, inference time
- Accuracy, Precision, Recall, F1 score

### `logs/experiment.log`
Detailed logs with timing information for debugging.

### `models/<model_name>/`
Trained model checkpoints and tokenizer.

---

## Performance Optimization Tips

### Use Pickle Cache
The pipeline automatically caches processed data. Don't use `--force-reload` unless you've changed the dataset.

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
- Reduce sequence length: `MAX_SEQUENCE_LENGTH = 256`

### Slow Processing
- Ensure pickle cache is being used (check logs)
- Use `--skip-optimization` to skip XAI step
- Use fewer epochs: `--epochs 1`

### Import Errors
- Install PyTorch Geometric properly:
  ```bash
  pip install torch-geometric torch-scatter torch-sparse
  ```

---

## Research Context

This implementation is based on the research proposal:
- **Method**: CFG → GNN Explainer → Optimized Sequence → BERT Classification
- **Dataset**: SoliAudit (17,980 smart contract samples)
- **XAI Technique**: GNN Explainer for sensitive node identification
- **Innovation**: Token-efficient sequence generation for BERT (<=512 tokens)

### Expected Experiments
1. **Baseline**: AST → Sequence (no XAI)
2. **Proposed**: AST → GNN Explainer → Optimized Sequence
3. **Comparison**: Different BERT models (BERT, DistilBERT, CodeBERT)
4. **Metrics**: Training time, inference time, accuracy, F1 score, node/edge reduction

---

## Citation

If you use this code, please cite:
```
Smart Contract Vulnerability Detection using XAI and BERT-based Models
[Your Name], 2024
```

---

## License

[Specify your license]

---

## Contact

For questions or issues, please open an issue on the repository or contact [your email].
