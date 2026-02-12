"""
Utility functions for Smart Contract Vulnerability Detection with XAI
Includes logging setup, GPU detection, timing decorators, and helper functions
"""

import logging
import time
import json
import pickle
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
import torch
import numpy as np
from datetime import datetime

import config


# ============================================================================
# LOGGING SETUP
# ============================================================================
def setup_logging(log_file: Path = None, log_level: str = None):
    """
    Setup logging configuration
    
    Args:
        log_file: Path to log file (default: config.LOG_FILE)
        log_level: Logging level (default: config.LOG_LEVEL)
    """
    if log_file is None:
        log_file = config.LOG_FILE
    if log_level is None:
        log_level = config.LOG_LEVEL
    
    # Create formatter
    formatter = logging.Formatter(config.LOG_FORMAT)
    
    # Setup file handler
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str):
    """Get logger for specific module"""
    return logging.getLogger(name)


# ============================================================================
# GPU DETECTION AND CONFIGURATION
# ============================================================================
def detect_gpu_configuration():
    """
    Detect available GPU configuration
    
    Returns:
        dict: GPU configuration including device, count, names, and memory
    """
    logger = get_logger(__name__)
    
    gpu_config = {
        'available': torch.cuda.is_available(),
        'device': 'cpu',
        'device_count': 0,
        'device_names': [],
        'total_memory_gb': [],
        'use_multi_gpu': False
    }
    
    if torch.cuda.is_available():
        gpu_config['device'] = 'cuda'
        gpu_config['device_count'] = torch.cuda.device_count()
        
        for i in range(gpu_config['device_count']):
            device_name = torch.cuda.get_device_name(i)
            total_memory = torch.cuda.get_device_properties(i).total_memory / (1024**3)
            gpu_config['device_names'].append(device_name)
            gpu_config['total_memory_gb'].append(f"{total_memory:.2f}")
            
            logger.info(f"GPU {i}: {device_name} - {total_memory:.2f} GB")
        
        # Enable multi-GPU if more than 1 GPU and config allows
        if gpu_config['device_count'] > 1 and config.USE_MULTI_GPU:
            gpu_config['use_multi_gpu'] = True
            logger.info(f"Multi-GPU enabled: {gpu_config['device_count']} GPUs available")
        else:
            logger.info(f"Single GPU mode: Using GPU 0")
    else:
        logger.warning("No GPU available. Using CPU for training.")
    
    return gpu_config


def get_device():
    """Get PyTorch device (cuda/cpu)"""
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# ============================================================================
# TIMING DECORATORS
# ============================================================================
def timeit(func: Callable) -> Callable:
    """
    Decorator to measure function execution time
    
    Usage:
        @timeit
        def my_function():
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()
        logger.info(f"Starting {func.__name__}...")
        
        result = func(*args, **kwargs)
        
        elapsed_time = time.time() - start_time
        logger.info(f"Completed {func.__name__} in {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
        
        return result
    
    return wrapper


class Timer:
    """Context manager for timing code blocks"""
    
    def __init__(self, name: str = "Operation", logger=None):
        self.name = name
        self.logger = logger or get_logger(__name__)
        self.start_time = None
        self.elapsed = None
    
    def __enter__(self):
        self.start_time = time.time()
        self.logger.info(f"Starting {self.name}...")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start_time
        self.logger.info(f"Completed {self.name} in {self.elapsed:.2f} seconds ({self.elapsed/60:.2f} minutes)")
        return False
    
    def get_elapsed(self):
        """Get elapsed time in seconds"""
        return self.elapsed


# ============================================================================
# PICKLE CACHING
# ============================================================================
def save_pickle(data: Any, filepath: Path, logger=None):
    """
    Save data to pickle file
    
    Args:
        data: Data to save
        filepath: Path to pickle file
        logger: Logger instance
    """
    if logger is None:
        logger = get_logger(__name__)
    
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with Timer(f"Saving pickle to {filepath.name}", logger):
        with open(filepath, 'wb') as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    file_size_mb = filepath.stat().st_size / (1024**2)
    logger.info(f"Saved {filepath.name} ({file_size_mb:.2f} MB)")


def load_pickle(filepath: Path, logger=None):
    """
    Load data from pickle file
    
    Args:
        filepath: Path to pickle file
        logger: Logger instance
        
    Returns:
        Loaded data or None if file doesn't exist
    """
    if logger is None:
        logger = get_logger(__name__)
    
    filepath = Path(filepath)
    
    if not filepath.exists():
        logger.warning(f"Pickle file not found: {filepath.name}")
        return None
    
    file_size_mb = filepath.stat().st_size / (1024**2)
    
    with Timer(f"Loading pickle from {filepath.name} ({file_size_mb:.2f} MB)", logger):
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
    
    logger.info(f"Loaded {filepath.name} successfully")
    return data


def pickle_exists(filepath: Path):
    """Check if pickle file exists"""
    return Path(filepath).exists()


# ============================================================================
# STATISTICS FUNCTIONS
# ============================================================================
def compute_graph_statistics(graphs: List, label: str = "Graph") -> Dict:
    """
    Compute statistics for a list of graphs
    
    Args:
        graphs: List of NetworkX graphs
        label: Label for statistics
        
    Returns:
        dict: Statistics including node/edge counts
    """
    logger = get_logger(__name__)
    
    if not graphs:
        logger.warning(f"No graphs provided for statistics computation")
        return {}
    
    node_counts = [g.number_of_nodes() for g in graphs if g is not None]
    edge_counts = [g.number_of_edges() for g in graphs if g is not None]
    
    stats = {
        'label': label,
        'total_graphs': len(graphs),
        'valid_graphs': len(node_counts),
        'total_nodes': sum(node_counts),
        'total_edges': sum(edge_counts),
        'avg_nodes': np.mean(node_counts) if node_counts else 0,
        'avg_edges': np.mean(edge_counts) if edge_counts else 0,
        'min_nodes': min(node_counts) if node_counts else 0,
        'max_nodes': max(node_counts) if node_counts else 0,
        'min_edges': min(edge_counts) if edge_counts else 0,
        'max_edges': max(edge_counts) if edge_counts else 0,
        'median_nodes': np.median(node_counts) if node_counts else 0,
        'median_edges': np.median(edge_counts) if edge_counts else 0,
    }
    
    logger.info(f"\n{'='*70}")
    logger.info(f"{label} Statistics:")
    logger.info(f"{'='*70}")
    logger.info(f"Total graphs: {stats['total_graphs']}")
    logger.info(f"Valid graphs: {stats['valid_graphs']}")
    logger.info(f"Total nodes: {stats['total_nodes']:,}")
    logger.info(f"Total edges: {stats['total_edges']:,}")
    logger.info(f"Average nodes per graph: {stats['avg_nodes']:.2f}")
    logger.info(f"Average edges per graph: {stats['avg_edges']:.2f}")
    logger.info(f"Node range: [{stats['min_nodes']}, {stats['max_nodes']}]")
    logger.info(f"Edge range: [{stats['min_edges']}, {stats['max_edges']}]")
    logger.info(f"{'='*70}\n")
    
    return stats


def compare_statistics(before_stats: Dict, after_stats: Dict) -> Dict:
    """
    Compare statistics before and after optimization
    
    Args:
        before_stats: Statistics before optimization
        after_stats: Statistics after optimization
        
    Returns:
        dict: Comparison metrics
    """
    logger = get_logger(__name__)
    
    comparison = {
        'node_reduction_ratio': 1 - (after_stats['total_nodes'] / before_stats['total_nodes']),
        'edge_reduction_ratio': 1 - (after_stats['total_edges'] / before_stats['total_edges']),
        'avg_node_reduction': before_stats['avg_nodes'] - after_stats['avg_nodes'],
        'avg_edge_reduction': before_stats['avg_edges'] - after_stats['avg_edges'],
        'node_reduction_percentage': (1 - (after_stats['total_nodes'] / before_stats['total_nodes'])) * 100,
        'edge_reduction_percentage': (1 - (after_stats['total_edges'] / before_stats['total_edges'])) * 100,
    }
    
    logger.info(f"\n{'='*70}")
    logger.info(f"Optimization Impact:")
    logger.info(f"{'='*70}")
    logger.info(f"Node reduction: {comparison['node_reduction_percentage']:.2f}%")
    logger.info(f"Edge reduction: {comparison['edge_reduction_percentage']:.2f}%")
    logger.info(f"Avg nodes reduced: {comparison['avg_node_reduction']:.2f}")
    logger.info(f"Avg edges reduced: {comparison['avg_edge_reduction']:.2f}")
    logger.info(f"{'='*70}\n")
    
    return comparison


# ============================================================================
# EXPERIMENT TRACKING
# ============================================================================
def save_experiment_results(results: Dict, filepath: Path = None):
    """Save experiment results to JSON"""
    if filepath is None:
        filepath = config.EXPERIMENT_RESULTS_FILE
    
    logger = get_logger(__name__)
    filepath = Path(filepath)
    
    # Add timestamp
    results['timestamp'] = datetime.now().isoformat()
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Saved experiment results to {filepath}")


def load_experiment_results(filepath: Path = None) -> Optional[Dict]:
    """Load experiment results from JSON"""
    if filepath is None:
        filepath = config.EXPERIMENT_RESULTS_FILE
    
    logger = get_logger(__name__)
    filepath = Path(filepath)
    
    if not filepath.exists():
        logger.warning(f"Experiment results file not found: {filepath}")
        return None
    
    with open(filepath, 'r') as f:
        results = json.load(f)
    
    logger.info(f"Loaded experiment results from {filepath}")
    return results


# ============================================================================
# SEED SETTING FOR REPRODUCIBILITY
# ============================================================================
def set_seed(seed: int = None):
    """Set random seed for reproducibility"""
    if seed is None:
        seed = config.RANDOM_SEED
    
    logger = get_logger(__name__)
    logger.info(f"Setting random seed: {seed}")
    
    import random
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


# ============================================================================
# MAIN (for testing)
# ============================================================================
if __name__ == "__main__":
    # Test logging
    setup_logging()
    logger = get_logger(__name__)
    
    logger.info("Testing utils.py")
    
    # Test GPU detection
    gpu_config = detect_gpu_configuration()
    print(f"\nGPU Configuration: {gpu_config}")
    
    # Test timer
    with Timer("Test operation", logger):
        time.sleep(1)
    
    # Test pickle
    test_data = {'key': 'value', 'list': [1, 2, 3]}
    save_pickle(test_data, config.CACHE_DIR / "test.pkl", logger)
    loaded_data = load_pickle(config.CACHE_DIR / "test.pkl", logger)
    print(f"\nLoaded data: {loaded_data}")
