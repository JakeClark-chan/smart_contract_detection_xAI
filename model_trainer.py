"""
Model Trainer for Multi-label Vulnerability Classification
Handles BERT-based model training with TrainingArguments, Trainer, and multi-GPU support
"""

import torch
import torch.nn as nn
import numpy as np
from typing import List, Dict, Tuple, Optional
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from transformers import (
    AutoTokenizer,
    AutoModel,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback
)
from torch.utils.data import Dataset as TorchDataset
import time

import config
from utils import (
    get_logger,
    get_device,
    detect_gpu_configuration,
    Timer,
    timeit,
    set_seed
)
from sequence_converter import GraphSequence, truncate_sequence
from data_loader import get_num_labels


logger = get_logger(__name__)


# ============================================================================
# DATASET CLASS
# ============================================================================
class SequenceDataset(TorchDataset):
    """
    PyTorch Dataset for graph sequences
    """
    
    def __init__(self, sequences: List[GraphSequence], tokenizer, max_length: int = None):
        """
        Initialize dataset
        
        Args:
            sequences: List of GraphSequence objects
            tokenizer: HuggingFace tokenizer
            max_length: Maximum sequence length
        """
        self.sequences = [s for s in sequences if s is not None]
        self.tokenizer = tokenizer
        self.max_length = max_length or config.MAX_SEQUENCE_LENGTH
        
        logger.info(f"Created SequenceDataset with {len(self.sequences)} samples")
    
    def __len__(self):
        return len(self.sequences)
    
    def __getitem__(self, idx):
        graph_seq = self.sequences[idx]
        
        # Truncate sequence if needed
        sequence = truncate_sequence(graph_seq.sequence, self.max_length)
        
        # Tokenize
        encoding = self.tokenizer(
            sequence,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        # Prepare output
        item = {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(graph_seq.labels, dtype=torch.float)
        }
        
        return item


# ============================================================================
# MULTI-LABEL BERT CLASSIFIER
# ============================================================================
class BERTMultiLabelClassifier(nn.Module):
    """
    BERT-based multi-label classifier for vulnerability detection
    """
    
    def __init__(self, model_name: str, num_labels: int, dropout: float = 0.3):
        super(BERTMultiLabelClassifier, self).__init__()
        
        self.bert = AutoModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_labels)
        
        logger.info(f"Initialized BERT classifier: {model_name}, {num_labels} labels")
    
    def forward(self, input_ids, attention_mask, labels=None):
        # Get BERT outputs
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        
        # Use [CLS] token representation
        pooled_output = outputs.last_hidden_state[:, 0, :]
        
        # Apply dropout and classification layer
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        
        # Calculate loss if labels provided
        loss = None
        if labels is not None:
            loss_fct = nn.BCEWithLogitsLoss()
            loss = loss_fct(logits, labels)
        
        return {'loss': loss, 'logits': logits}


# ============================================================================
# METRICS COMPUTATION
# ============================================================================
def compute_metrics(eval_pred):
    """
    Compute metrics for multi-label classification
    
    Args:
        eval_pred: Tuple of (predictions, labels)
        
    Returns:
        Dictionary of metrics
    """
    predictions, labels = eval_pred
    
    # Apply sigmoid to get probabilities
    probs = 1 / (1 + np.exp(-predictions))  # Sigmoid
    
    # Convert to binary predictions (threshold = 0.5)
    preds = (probs > 0.5).astype(int)
    
    # Compute metrics
    accuracy = accuracy_score(labels, preds)
    
    # Compute per-label metrics
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average='macro', zero_division=0
    )
    
    # Compute micro-average metrics
    precision_micro, recall_micro, f1_micro, _ = precision_recall_fscore_support(
        labels, preds, average='micro', zero_division=0
    )
    
    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'precision_micro': precision_micro,
        'recall_micro': recall_micro,
        'f1_micro': f1_micro,
    }
    
    return metrics


# ============================================================================
# TRAINING PIPELINE
# ============================================================================
@timeit
def train_model(
    train_sequences: List[GraphSequence],
    test_sequences: List[GraphSequence],
    model_name: str = None,
    training_args_dict: Dict = None
) -> Tuple[BERTMultiLabelClassifier, Dict]:
    """
    Train BERT-based multi-label classifier
    
    Args:
        train_sequences: Training sequences
        test_sequences: Test sequences
        model_name: HuggingFace model name (default: config.CURRENT_MODEL_NAME)
        training_args_dict: Training arguments (default: config.TRAINING_ARGS)
        
    Returns:
        Tuple of (trained_model, metrics_dict)
    """
    if model_name is None:
        model_name = config.CURRENT_MODEL_NAME
    
    if training_args_dict is None:
        training_args_dict = config.TRAINING_ARGS.copy()
    
    logger.info(f"\n{'='*70}")
    logger.info(f"Training Model: {model_name}")
    logger.info(f"{'='*70}")
    
    # Detect GPU configuration
    gpu_config = detect_gpu_configuration()
    
    # Update training args for multi-GPU
    if gpu_config['use_multi_gpu']:
        logger.info(f"Using {gpu_config['device_count']} GPUs for training")
        # DataParallel will be handled automatically by Trainer
    
    # Load tokenizer
    logger.info("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Create datasets
    logger.info("Creating datasets...")
    train_dataset = SequenceDataset(train_sequences, tokenizer)
    test_dataset = SequenceDataset(test_sequences, tokenizer)
    
    logger.info(f"Train dataset: {len(train_dataset)} samples")
    logger.info(f"Test dataset: {len(test_dataset)} samples")
    
    # Initialize model
    logger.info("Initializing model...")
    num_labels = get_num_labels()
    model = BERTMultiLabelClassifier(model_name, num_labels)
    
    # Move to device(s)
    device = get_device()
    model.to(device)
    
    # Wrap with DataParallel if multiple GPUs
    if gpu_config['use_multi_gpu'] and gpu_config['device_count'] > 1:
        model = nn.DataParallel(model)
        logger.info(f"Model wrapped with DataParallel for {gpu_config['device_count']} GPUs")
    
    # Setup training arguments
    training_args = TrainingArguments(**training_args_dict)
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
    )
    
    # Train
    logger.info("Starting training...")
    train_start_time = time.time()
    
    train_result = trainer.train()
    
    train_time = time.time() - train_start_time
    logger.info(f"Training completed in {train_time:.2f} seconds ({train_time/60:.2f} minutes)")
    
    # Evaluate
    logger.info("Evaluating on test set...")
    eval_start_time = time.time()
    
    eval_results = trainer.evaluate()
    
    eval_time = time.time() - eval_start_time
    logger.info(f"Evaluation completed in {eval_time:.2f} seconds")
    
    # Log results
    logger.info(f"\n{'='*70}")
    logger.info(f"Training Results:")
    logger.info(f"{'='*70}")
    logger.info(f"Train loss: {train_result.training_loss:.4f}")
    logger.info(f"Train time: {train_time:.2f} seconds")
    logger.info(f"\nEvaluation Results:")
    for key, value in eval_results.items():
        logger.info(f"  {key}: {value:.4f}")
    logger.info(f"Inference time: {eval_time:.2f} seconds")
    logger.info(f"{'='*70}\n")
    
    # Prepare metrics dictionary
    metrics = {
        'model_name': model_name,
        'train_loss': train_result.training_loss,
        'train_time': train_time,
        'eval_results': eval_results,
        'inference_time': eval_time,
        'num_train_samples': len(train_dataset),
        'num_test_samples': len(test_dataset),
        'gpu_config': gpu_config
    }
    
    # Save model
    model_save_path = config.get_model_output_dir(config.DEFAULT_MODEL) / "final_model"
    trainer.save_model(str(model_save_path))
    logger.info(f"Model saved to {model_save_path}")
    
    # Get the base model (unwrap DataParallel if used)
    if isinstance(model, nn.DataParallel):
        model = model.module
    
    return model, metrics


@timeit
def evaluate_model(
    model: BERTMultiLabelClassifier,
    test_sequences: List[GraphSequence],
    model_name: str = None
) -> Dict:
    """
    Evaluate model on test set
    
    Args:
        model: Trained model
        test_sequences: Test sequences
        model_name: Model name for logging
        
    Returns:
        Dictionary of evaluation metrics
    """
    if model_name is None:
        model_name = config.CURRENT_MODEL_NAME
    
    logger.info(f"Evaluating model: {model_name}")
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Create dataset
    test_dataset = SequenceDataset(test_sequences, tokenizer)
    
    # Setup trainer for evaluation
    training_args = TrainingArguments(
        output_dir=str(config.get_model_output_dir()),
        per_device_eval_batch_size=config.TRAINING_ARGS['per_device_eval_batch_size'],
        report_to='none'
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics
    )
    
    # Evaluate
    eval_start_time = time.time()
    eval_results = trainer.evaluate()
    eval_time = time.time() - eval_start_time
    
    logger.info(f"Evaluation completed in {eval_time:.2f} seconds")
    logger.info(f"Results: {eval_results}")
    
    eval_results['inference_time'] = eval_time
    
    return eval_results


# ============================================================================
# MODEL COMPARISON
# ============================================================================
def compare_models(
    train_sequences: List[GraphSequence],
    test_sequences: List[GraphSequence],
    model_keys: List[str] = None
) -> Dict:
    """
    Train and compare multiple models
    
    Args:
        train_sequences: Training sequences
        test_sequences: Test sequences
        model_keys: List of model keys to compare (default: ['bert', 'distilbert'])
        
    Returns:
        Dictionary of comparison results
    """
    if model_keys is None:
        model_keys = ['bert', 'distilbert']
    
    logger.info(f"\n{'='*70}")
    logger.info(f"Comparing Models: {', '.join(model_keys)}")
    logger.info(f"{'='*70}\n")
    
    results = {}
    
    for model_key in model_keys:
        logger.info(f"\n{'#'*70}")
        logger.info(f"# Training {model_key.upper()}")
        logger.info(f"{'#'*70}\n")
        
        # Update config for current model
        config.update_model(model_key)
        
        # Train model
        model, metrics = train_model(
            train_sequences,
            test_sequences,
            model_name=config.get_model_name(model_key)
        )
        
        results[model_key] = metrics
    
    # Log comparison
    logger.info(f"\n{'='*70}")
    logger.info(f"Model Comparison Summary:")
    logger.info(f"{'='*70}")
    
    for model_key, metrics in results.items():
        logger.info(f"\n{model_key.upper()}:")
        logger.info(f"  Train time: {metrics['train_time']:.2f}s")
        logger.info(f"  Inference time: {metrics['inference_time']:.2f}s")
        logger.info(f"  F1 Score: {metrics['eval_results'].get('eval_f1', 0):.4f}")
        logger.info(f"  Accuracy: {metrics['eval_results'].get('eval_accuracy', 0):.4f}")
    
    logger.info(f"{'='*70}\n")
    
    return results


# ============================================================================
# MAIN (for testing)
# ============================================================================
if __name__ == "__main__":
    from utils import setup_logging
    from data_loader import load_train_test_datasets
    from graph_processor import process_dataset_to_graphs
    from xai_optimizer import optimize_graphs
    from sequence_converter import convert_graphs_to_sequences
    
    # Setup
    setup_logging()
    set_seed()
    
    logger.info("Testing model_trainer.py")
    
    # Load data (small subset for testing)
    train_dataset, test_dataset = load_train_test_datasets(force_reload=False)
    
    # Process graphs (small subset)
    train_graphs = process_dataset_to_graphs(train_dataset, force_reprocess=False)
    test_graphs = process_dataset_to_graphs(test_dataset, force_reprocess=False)
    
    # Use only first 100 for quick testing
    train_graphs_subset = [g for g in train_graphs[:100] if g is not None]
    test_graphs_subset = [g for g in test_graphs[:50] if g is not None]
    
    # Optimize
    optimized_train = optimize_graphs(train_graphs_subset, use_gnn_explainer=False, force_reoptimize=False)
    optimized_test = optimize_graphs(test_graphs_subset, use_gnn_explainer=False, force_reoptimize=False)
    
    # Convert to sequences (using DFS)
    train_sequences = convert_graphs_to_sequences(optimized_train, traversal_method='dfs', force_reconvert=False)
    test_sequences = convert_graphs_to_sequences(optimized_test, traversal_method='dfs', force_reconvert=False)
    
    # Train model
    model, metrics = train_model(train_sequences, test_sequences)
    
    logger.info(f"\nTraining completed successfully!")
    logger.info(f"Metrics: {metrics}")
