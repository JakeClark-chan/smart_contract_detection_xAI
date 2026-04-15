"""
Configuration file for Smart Contract Vulnerability Detection with XAI
Centralized settings for paths, models, hyperparameters, and GPU configuration
"""

import os
from pathlib import Path

# ============================================================================
# PROJECT PATHS
# ============================================================================
PROJECT_ROOT = Path(__file__).parent.absolute()
DATA_DIR = PROJECT_ROOT / "data"
CACHE_DIR = PROJECT_ROOT / "cache"
OUTPUT_DIR = PROJECT_ROOT / "output"
LOGS_DIR = PROJECT_ROOT / "logs"
MODELS_DIR = PROJECT_ROOT / "models"

# Create directories if they don't exist
for directory in [DATA_DIR, CACHE_DIR, OUTPUT_DIR, LOGS_DIR, MODELS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================================
# DATASET CONFIGURATION
# ============================================================================
USE_HUGGINGFACE = True  # Set to True to load datasets from HuggingFace Hub
HUGGINGFACE_DATASET_NAME = "JakeClark/soliaudit-dasp-ast-graph"

TRAIN_DATASET_PATH = PROJECT_ROOT / "soliaudit_graph_train_with_reentrancy.csv"
TEST_DATASET_PATH = PROJECT_ROOT / "soliaudit_graph_test_with_reentrancy.csv"

# Columns to extract from dataset
DATASET_COLUMNS = {
    "address": "address",
    "ast": "AST",  # Use AST column instead of CFG
    "labels": [
        "Arithmetic",
        "Unchecked Return Values For Low Level Calls",  # LowLevelCall
        "Denial of Service",  # DoS
        "Time manipulation",
        "Reentrancy",  # Now directly from the new dataset files
    ],
}

# Label name mapping for cleaner display
LABEL_DISPLAY_NAMES = {
    "Arithmetic": "Arithmetic",
    "Unchecked Return Values For Low Level Calls": "LowLevelCall",
    "Denial of Service": "DoS",
    "Time manipulation": "TimeManipulation",
    "Reentrancy": "Reentrancy",
}

# Train/Test split ratio (not used - we have separate train/test files)
# TRAIN_TEST_SPLIT = 0.8  # Using pre-split files instead

# Pickle cache files
PICKLE_RAW_DATASET = CACHE_DIR / "raw_dataset.pkl"
PICKLE_PROCESSED_GRAPHS = CACHE_DIR / "processed_graphs.pkl"
PICKLE_OPTIMIZED_GRAPHS = CACHE_DIR / "optimized_graphs.pkl"
PICKLE_SEQUENCES = CACHE_DIR / "sequences.pkl"
PICKLE_TRAIN_DATASET = CACHE_DIR / "train_dataset.pkl"
PICKLE_TEST_DATASET = CACHE_DIR / "test_dataset.pkl"

# Statistics cache
STATS_BEFORE_OPTIMIZATION = CACHE_DIR / "stats_before_optimization.pkl"
STATS_AFTER_OPTIMIZATION = CACHE_DIR / "stats_after_optimization.pkl"

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================
# Available models to use (start with BERT and DistilBERT as per instructions)
AVAILABLE_MODELS = {
    "bert": "bert-base-uncased",
    "distilbert": "distilbert-base-uncased",
    "codebert": "microsoft/codebert-base",
    "graphcodebert": "microsoft/graphcodebert-base",
    "gpt2": "gpt2",
}

# Default model to use (can be changed easily)
DEFAULT_MODEL = "bert"  # Change to 'distilbert', 'codebert', etc.

# Get current model name
CURRENT_MODEL_NAME = AVAILABLE_MODELS[DEFAULT_MODEL]

# ============================================================================
# XAI & GRAPH OPTIMIZATION CONFIGURATION
# ============================================================================
# GNN Explainer settings
GNN_EXPLAINER_EPOCHS = 200
SHAP_THRESHOLD = 0.5  # Node importance threshold (top nodes to keep)
TOP_NODES_PERCENTAGE = 0.2  # Alternative: keep top 20% of nodes

# Graph processing
MAX_SEQUENCE_LENGTH = 512  # BERT token limit
USE_DFS_TRAVERSAL = True  # Use DFS for graph-to-sequence conversion
DFS_START_FROM_ENTRY = True  # Start DFS from function entry points

# ============================================================================
# TRAINING CONFIGURATION
# ============================================================================
TRAINING_ARGS = {
    "output_dir": str(MODELS_DIR / DEFAULT_MODEL),
    "eval_strategy": "epoch",  # Changed from evaluation_strategy in newer transformers
    "save_strategy": "epoch",
    "learning_rate": 2e-5,
    "per_device_train_batch_size": 8,
    "per_device_eval_batch_size": 16,
    "num_train_epochs": 3,
    "weight_decay": 0.01,
    "logging_dir": str(LOGS_DIR),
    "logging_steps": 10,
    "load_best_model_at_end": True,
    "metric_for_best_model": "f1",
    "save_total_limit": 2,
    "fp16": True,  # Use mixed precision if GPU supports it
    "dataloader_num_workers": 4,
    "report_to": "none",  # Disable wandb/tensorboard by default
}

# Multi-GPU settings (auto-detected)
USE_MULTI_GPU = True  # Enable if multiple GPUs are available

# ============================================================================
# EVALUATION METRICS
# ============================================================================
METRICS_TO_COMPUTE = ["accuracy", "precision", "recall", "f1"]

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "experiment.log"

# ============================================================================
# EXPERIMENT TRACKING
# ============================================================================
EXPERIMENT_RESULTS_FILE = OUTPUT_DIR / "experiment_results.json"
COMPARISON_RESULTS_FILE = OUTPUT_DIR / "comparison_results.csv"

# ============================================================================
# REPRODUCIBILITY
# ============================================================================
RANDOM_SEED = 42


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def get_model_output_dir(model_name: str = None):
    """Get output directory for specific model"""
    if model_name is None:
        model_name = DEFAULT_MODEL
    return MODELS_DIR / model_name


def get_model_name(model_key: str = None):
    """Get HuggingFace model name from key"""
    if model_key is None:
        model_key = DEFAULT_MODEL
    return AVAILABLE_MODELS.get(model_key, AVAILABLE_MODELS["bert"])


def update_model(model_key: str):
    """Update current model configuration"""
    global DEFAULT_MODEL, CURRENT_MODEL_NAME
    if model_key in AVAILABLE_MODELS:
        DEFAULT_MODEL = model_key
        CURRENT_MODEL_NAME = AVAILABLE_MODELS[model_key]
        TRAINING_ARGS["output_dir"] = str(get_model_output_dir(model_key))
        return True
    return False


# ============================================================================
# DISPLAY CONFIGURATION (for logging)
# ============================================================================
def print_config():
    """Print current configuration"""
    config_str = f"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║  Smart Contract Vulnerability Detection with XAI Configuration  ║
    ╚══════════════════════════════════════════════════════════════════╝

    📁 Project Root: {PROJECT_ROOT}
    📊 Train Dataset: {TRAIN_DATASET_PATH.name}
    📊 Test Dataset: {TEST_DATASET_PATH.name}

    🤖 Current Model: {DEFAULT_MODEL} ({CURRENT_MODEL_NAME})

    🔬 XAI Configuration:
       - GNN Explainer Epochs: {GNN_EXPLAINER_EPOCHS}
       - SHAP Threshold: {SHAP_THRESHOLD}
       - Top Nodes %: {TOP_NODES_PERCENTAGE * 100}%

    🎯 Training Configuration:
       - Batch Size: {TRAINING_ARGS["per_device_train_batch_size"]}
       - Epochs: {TRAINING_ARGS["num_train_epochs"]}
       - Learning Rate: {TRAINING_ARGS["learning_rate"]}
       - Using Pre-split Train/Test Files

    💾 Cache Files:
       - Raw Dataset: {PICKLE_RAW_DATASET.exists()}
       - Processed Graphs: {PICKLE_PROCESSED_GRAPHS.exists()}
       - Optimized Graphs: {PICKLE_OPTIMIZED_GRAPHS.exists()}
       - Sequences: {PICKLE_SEQUENCES.exists()}

    📝 Labels: {", ".join([LABEL_DISPLAY_NAMES.get(l, l) for l in DATASET_COLUMNS["labels"]])}
    """
    return config_str


if __name__ == "__main__":
    print(print_config())
