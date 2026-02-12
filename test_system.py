#!/usr/bin/env python3
"""
Quick test script to verify all modules can be imported and basic functionality works
Run this before running the full pipeline to catch any issues early
"""

import sys
from pathlib import Path

def test_imports():
    """Test all module imports"""
    print("🔍 Testing module imports...")
    
    try:
        import config
        print("  ✅ config")
    except Exception as e:
        print(f"  ❌ config: {e}")
        return False
    
    try:
        import utils
        print("  ✅ utils")
    except Exception as e:
        print(f"  ❌ utils: {e}")
        return False
    
    try:
        import data_loader
        print("  ✅ data_loader")
    except Exception as e:
        print(f"  ❌ data_loader: {e}")
        return False
    
    try:
        import graph_processor
        print("  ✅ graph_processor")
    except Exception as e:
        print(f"  ❌ graph_processor: {e}")
        return False
    
    try:
        import xai_optimizer
        print("  ✅ xai_optimizer")
    except Exception as e:
        print(f"  ❌ xai_optimizer: {e}")
        return False
    
    try:
        import sequence_converter
        print("  ✅ sequence_converter")
    except Exception as e:
        print(f"  ❌ sequence_converter: {e}")
        return False
    
    try:
        import model_trainer
        print("  ✅ model_trainer")
    except Exception as e:
        print(f"  ❌ model_trainer: {e}")
        return False
    
    return True


def test_dependencies():
    """Test core dependencies"""
    print("\n🔍 Testing core dependencies...")
    
    try:
        import torch
        print(f"  ✅ torch {torch.__version__}")
        print(f"     CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"     GPU count: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"     GPU {i}: {torch.cuda.get_device_name(i)}")
    except Exception as e:
        print(f"  ❌ torch: {e}")
        return False
    
    try:
        import transformers
        print(f"  ✅ transformers {transformers.__version__}")
    except Exception as e:
        print(f"  ❌ transformers: {e}")
        return False
    
    try:
        import networkx as nx
        print(f"  ✅ networkx {nx.__version__}")
    except Exception as e:
        print(f"  ❌ networkx: {e}")
        return False
    
    try:
        import pandas as pd
        print(f"  ✅ pandas {pd.__version__}")
    except Exception as e:
        print(f"  ❌ pandas: {e}")
        return False
    
    try:
        import numpy as np
        print(f"  ✅ numpy {np.__version__}")
    except Exception as e:
        print(f"  ❌ numpy: {e}")
        return False
    
    try:
        import sklearn
        print(f"  ✅ scikit-learn {sklearn.__version__}")
    except Exception as e:
        print(f"  ❌ scikit-learn: {e}")
        return False
    
    try:
        import torch_geometric
        print(f"  ✅ torch_geometric {torch_geometric.__version__}")
    except Exception as e:
        print(f"  ❌ torch_geometric: {e}")
        return False
    
    return True


def test_dataset():
    """Test dataset file exists"""
    print("\n🔍 Testing dataset...")
    
    import config
    
    train_exists = config.TRAIN_DATASET_PATH.exists()
    test_exists = config.TEST_DATASET_PATH.exists()
    
    if train_exists and test_exists:
        train_size_mb = config.TRAIN_DATASET_PATH.stat().st_size / (1024**2)
        test_size_mb = config.TEST_DATASET_PATH.stat().st_size / (1024**2)
        print(f"  ✅ Train dataset found: {config.TRAIN_DATASET_PATH.name} ({train_size_mb:.2f} MB)")
        print(f"  ✅ Test dataset found: {config.TEST_DATASET_PATH.name} ({test_size_mb:.2f} MB)")
        
        # Check for reentrancy mapping file
        if config.REENTRANCY_MAPPING_PATH.exists():
            mapping_size_mb = config.REENTRANCY_MAPPING_PATH.stat().st_size / (1024**2)
            print(f"  ✅ Reentrancy mapping found: {config.REENTRANCY_MAPPING_PATH.name} ({mapping_size_mb:.2f} MB)")
        else:
            print(f"  ⚠️  Reentrancy mapping not found: {config.REENTRANCY_MAPPING_PATH.name}")
        
        return True
    else:
        if not train_exists:
            print(f"  ❌ Train dataset not found: {config.TRAIN_DATASET_PATH}")
        if not test_exists:
            print(f"  ❌ Test dataset not found: {config.TEST_DATASET_PATH}")
        print(f"     Please ensure soliaudit_graph_train.csv and soliaudit_graph_test.csv are in the project directory")
        return False


def test_config():
    """Test configuration"""
    print("\n🔍 Testing configuration...")
    
    import config
    
    print(f"  Default model: {config.DEFAULT_MODEL}")
    print(f"  Model name: {config.CURRENT_MODEL_NAME}")
    print(f"  Max sequence length: {config.MAX_SEQUENCE_LENGTH}")
    print(f"  SHAP threshold: {config.SHAP_THRESHOLD}")
    print(f"  Training epochs: {config.TRAINING_ARGS['num_train_epochs']}")
    print(f"  Batch size: {config.TRAINING_ARGS['per_device_train_batch_size']}")
    
    print("\n  Dataset files:")
    print(f"    Train: {config.TRAIN_DATASET_PATH.name}")
    print(f"    Test: {config.TEST_DATASET_PATH.name}")
    print(f"    Reentrancy mapping: {config.REENTRANCY_MAPPING_PATH.name}")
    
    print("\n  Cache directories:")
    print(f"    Data: {config.DATA_DIR}")
    print(f"    Cache: {config.CACHE_DIR}")
    print(f"    Output: {config.OUTPUT_DIR}")
    print(f"    Logs: {config.LOGS_DIR}")
    print(f"    Models: {config.MODELS_DIR}")
    
    return True


def test_utils():
    """Test utility functions"""
    print("\n🔍 Testing utility functions...")
    
    try:
        from utils import setup_logging, detect_gpu_configuration, set_seed
        
        # Test logging
        setup_logging()
        print("  ✅ Logging setup successful")
        
        # Test GPU detection
        gpu_config = detect_gpu_configuration()
        print(f"  ✅ GPU detection successful")
        
        # Test seed setting
        set_seed()
        print("  ✅ Random seed set")
        
        return True
    except Exception as e:
        print(f"  ❌ Utils test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║  Smart Contract Vulnerability Detection - System Test                   ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝")
    print()
    
    results = []
    
    # Test imports
    results.append(test_imports())
    
    # Test dependencies
    results.append(test_dependencies())
    
    # Test dataset
    results.append(test_dataset())
    
    # Test configuration
    results.append(test_config())
    
    # Test utils
    results.append(test_utils())
    
    # Summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    
    if all(results):
        print("✅ All tests passed!")
        print("\n🚀 System is ready to run the pipeline")
        print("\nQuick start commands:")
        print("  python main.py --subset 100    # Quick test with 100 samples")
        print("  python main.py --help          # View all options")
        print("  python main.py                 # Run full pipeline")
        return 0
    else:
        print("❌ Some tests failed")
        print("\n⚠️  Please fix the issues above before running the pipeline")
        print("\nCommon fixes:")
        print("  - Install missing dependencies: pip install -r requirements.txt")
        print("  - Ensure dataset file is in the project directory")
        print("  - Check Python version (requires Python 3.8+)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
