#!/usr/bin/env python3
"""
Main Orchestrator for Smart Contract Vulnerability Detection with XAI

This script runs the complete pipeline:
1. Load dataset (with pickle caching)
2. Process CFGs to graphs
3. Optimize graphs using XAI (GNN Explainer)
4. Convert graphs to sequences
5. Train BERT-based models
6. Evaluate and compare results

Usage:
    python main.py [--force-reload] [--skip-optimization] [--model bert|distilbert|codebert]
"""

import argparse
import json
import pandas as pd
from pathlib import Path
import sys

import config
from utils import (
    setup_logging,
    get_logger,
    set_seed,
    detect_gpu_configuration,
    Timer,
    save_experiment_results,
    compare_statistics,
    load_pickle
)
from data_loader import (
    load_train_test_datasets,
    get_label_names
)
from graph_processor import process_dataset_to_graphs
from xai_optimizer import optimize_graphs
from sequence_converter import convert_graphs_to_sequences
from model_trainer import (
    train_model,
    compare_models
)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Smart Contract Vulnerability Detection with XAI"
    )
    
    parser.add_argument(
        '--force-reload',
        action='store_true',
        help='Force reload all data (ignore cache)'
    )
    
    parser.add_argument(
        '--skip-optimization',
        action='store_true',
        help='Skip XAI optimization (use original graphs)'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='bert',
        choices=['bert', 'distilbert', 'codebert', 'graphcodebert', 'gpt2'],
        help='Model to train (default: bert)'
    )
    
    parser.add_argument(
        '--compare-models',
        action='store_true',
        help='Compare multiple models (bert and distilbert)'
    )
    
    parser.add_argument(
        '--use-gnn-explainer',
        action='store_true',
        help='Use GNN Explainer for optimization (slower but more accurate)'
    )
    
    parser.add_argument(
        '--subset',
        type=int,
        default=None,
        help='Use only a subset of data (for quick testing)'
    )
    
    parser.add_argument(
        '--epochs',
        type=int,
        default=None,
        help='Number of training epochs (overrides config)'
    )
    
    return parser.parse_args()


def print_banner():
    """Print project banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║       Smart Contract Vulnerability Detection with XAI                   ║
    ║                                                                          ║
    ║       Using GNN Explainer + BERT for Multi-label Classification         ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_pipeline(args):
    """
    Run the complete pipeline
    
    Args:
        args: Command line arguments
    """
    logger = get_logger(__name__)
    
    print_banner()
    logger.info("Starting Smart Contract Vulnerability Detection Pipeline")
    logger.info(f"Configuration: {args}")
    
    # Display configuration
    logger.info(config.print_config())
    
    # Detect GPU
    gpu_config = detect_gpu_configuration()
    
    # Update model if specified
    if args.model:
        config.update_model(args.model)
        logger.info(f"Using model: {config.DEFAULT_MODEL} ({config.CURRENT_MODEL_NAME})")
    
    # Update epochs if specified
    if args.epochs:
        config.TRAINING_ARGS['num_train_epochs'] = args.epochs
        logger.info(f"Training epochs set to: {args.epochs}")
    
    with Timer("Complete Pipeline", logger):
        
        # ====================================================================
        # STEP 1: Load Dataset
        # ====================================================================
        logger.info("\n" + "="*70)
        logger.info("STEP 1: Loading Train/Test Datasets")
        logger.info("="*70)
        
        train_dataset, test_dataset = load_train_test_datasets(force_reload=args.force_reload)
        
        # Apply subset if specified
        if args.subset and args.subset < len(train_dataset):
            logger.info(f"Using subset of {args.subset} samples for testing")
            train_dataset.addresses = train_dataset.addresses[:args.subset]
            train_dataset.asts = train_dataset.asts[:args.subset]
            train_dataset.labels = train_dataset.labels[:args.subset]
            
            # Also reduce test set proportionally
            test_subset = max(int(args.subset * 0.25), 50)
            test_dataset.addresses = test_dataset.addresses[:test_subset]
            test_dataset.asts = test_dataset.asts[:test_subset]
            test_dataset.labels = test_dataset.labels[:test_subset]
        
        # ====================================================================
        # STEP 2: Process ASTs to Graphs
        # ====================================================================
        logger.info("\n" + "="*70)
        logger.info("STEP 2: Processing ASTs to Graphs")
        logger.info("="*70)
        
        train_graphs = process_dataset_to_graphs(
            train_dataset,
            force_reprocess=args.force_reload
        )
        
        test_graphs = process_dataset_to_graphs(
            test_dataset,
            force_reprocess=args.force_reload,
            cache_file=config.CACHE_DIR / "test_graphs.pkl"
        )
        
        # ====================================================================
        # STEP 3: Optimize Graphs with XAI (Optional)
        # ====================================================================
        if not args.skip_optimization:
            logger.info("\n" + "="*70)
            logger.info("STEP 3: Optimizing Graphs with XAI")
            logger.info("="*70)
            
            optimized_train_graphs = optimize_graphs(
                train_graphs,
                use_gnn_explainer=args.use_gnn_explainer,
                force_reoptimize=args.force_reload
            )
            
            optimized_test_graphs = optimize_graphs(
                test_graphs,
                use_gnn_explainer=args.use_gnn_explainer,
                force_reoptimize=args.force_reload
            )
            
            # Load and compare statistics
            stats_before = load_pickle(config.STATS_BEFORE_OPTIMIZATION, logger)
            stats_after = load_pickle(config.STATS_AFTER_OPTIMIZATION, logger)
            
            if stats_before and stats_after:
                comparison = compare_statistics(stats_before, stats_after)
        else:
            logger.info("\n" + "="*70)
            logger.info("STEP 3: Skipping XAI Optimization (using original graphs)")
            logger.info("="*70)
            
            optimized_train_graphs = train_graphs
            optimized_test_graphs = test_graphs
        
        # ====================================================================
        # STEP 4: Convert Graphs to Sequences (using DFS)
        # ====================================================================
        logger.info("\n" + "="*70)
        logger.info("STEP 4: Converting Graphs to Sequences (DFS Traversal)")
        logger.info("="*70)
        
        train_sequences = convert_graphs_to_sequences(
            optimized_train_graphs,
            traversal_method='dfs',  # Explicitly use DFS as specified
            force_reconvert=args.force_reload
        )
        
        test_sequences = convert_graphs_to_sequences(
            optimized_test_graphs,
            traversal_method='dfs',  # Explicitly use DFS as specified
            force_reconvert=args.force_reload
        )
        
        # ====================================================================
        # STEP 5: Train Model(s)
        # ====================================================================
        logger.info("\n" + "="*70)
        logger.info("STEP 5: Training Model(s)")
        logger.info("="*70)
        
        if args.compare_models:
            # Compare multiple models
            results = compare_models(
                train_sequences,
                test_sequences,
                model_keys=['bert', 'distilbert']
            )
        else:
            # Train single model
            model, metrics = train_model(
                train_sequences,
                test_sequences,
                model_name=config.CURRENT_MODEL_NAME
            )
            
            results = {
                config.DEFAULT_MODEL: metrics
            }
        
        # ====================================================================
        # STEP 6: Save Results
        # ====================================================================
        logger.info("\n" + "="*70)
        logger.info("STEP 6: Saving Results")
        logger.info("="*70)
        
        # Prepare experiment results
        experiment_results = {
            'configuration': {
                'model': config.DEFAULT_MODEL,
                'use_optimization': not args.skip_optimization,
                'use_gnn_explainer': args.use_gnn_explainer,
                'train_samples': len(train_sequences),
                'test_samples': len(test_sequences),
                'labels': get_label_names(),
                'gpu_config': gpu_config
            },
            'results': results
        }
        
        # Save to JSON
        save_experiment_results(experiment_results)
        
        # Save comparison CSV
        comparison_data = []
        for model_key, metrics in results.items():
            row = {
                'model': model_key,
                'train_time': metrics['train_time'],
                'inference_time': metrics['inference_time'],
                'f1_score': metrics['eval_results'].get('eval_f1', 0),
                'accuracy': metrics['eval_results'].get('eval_accuracy', 0),
                'precision': metrics['eval_results'].get('eval_precision', 0),
                'recall': metrics['eval_results'].get('eval_recall', 0),
            }
            comparison_data.append(row)
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_df.to_csv(config.COMPARISON_RESULTS_FILE, index=False)
        logger.info(f"Saved comparison results to {config.COMPARISON_RESULTS_FILE}")
        
        # ====================================================================
        # STEP 7: Display Final Summary
        # ====================================================================
        logger.info("\n" + "="*70)
        logger.info("FINAL SUMMARY")
        logger.info("="*70)
        
        logger.info(f"\n📊 Dataset:")
        logger.info(f"  - Train samples: {len(train_dataset)}")
        logger.info(f"  - Test samples: {len(test_dataset)}")
        
        logger.info(f"\n🔬 Processing:")
        logger.info(f"  - XAI Optimization: {'Yes' if not args.skip_optimization else 'No'}")
        logger.info(f"  - GNN Explainer: {'Yes' if args.use_gnn_explainer else 'No (heuristics)'}")
        
        logger.info(f"\n🤖 Model(s) Trained:")
        for model_key in results.keys():
            logger.info(f"  - {model_key.upper()}")
        
        logger.info(f"\n📈 Best Model Performance:")
        best_model = max(results.items(), key=lambda x: x[1]['eval_results'].get('eval_f1', 0))
        logger.info(f"  - Model: {best_model[0].upper()}")
        logger.info(f"  - F1 Score: {best_model[1]['eval_results'].get('eval_f1', 0):.4f}")
        logger.info(f"  - Accuracy: {best_model[1]['eval_results'].get('eval_accuracy', 0):.4f}")
        logger.info(f"  - Train Time: {best_model[1]['train_time']:.2f}s")
        logger.info(f"  - Inference Time: {best_model[1]['inference_time']:.2f}s")
        
        logger.info(f"\n💾 Output Files:")
        logger.info(f"  - Experiment Results: {config.EXPERIMENT_RESULTS_FILE}")
        logger.info(f"  - Comparison CSV: {config.COMPARISON_RESULTS_FILE}")
        logger.info(f"  - Model Directory: {config.MODELS_DIR}")
        logger.info(f"  - Log File: {config.LOG_FILE}")
        
        logger.info("\n" + "="*70)
        logger.info("✅ Pipeline Completed Successfully!")
        logger.info("="*70 + "\n")
    
    return results


def main():
    """Main entry point"""
    # Parse arguments
    args = parse_arguments()
    
    # Setup logging
    setup_logging()
    logger = get_logger(__name__)
    
    # Set random seed for reproducibility
    set_seed()
    
    try:
        # Run pipeline
        results = run_pipeline(args)
        
        logger.info("Program finished successfully!")
        return 0
        
    except KeyboardInterrupt:
        logger.warning("\nProgram interrupted by user")
        return 130
        
    except Exception as e:
        logger.error(f"Program failed with error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
