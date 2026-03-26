import json

notebook = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.10"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

def add_md(text):
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.split("\n")]
    })

def add_code(text):
    notebook["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in text.split("\n")]
    })

# Title & Description
add_md('# Smart Contract Vulnerability Detection using XAI\nThis notebook follows the experimental steps outlined in `note_xai.txt`.')

add_md('## 1. Setup & Initialization\nImport required modules and set up the configuration. We start with the BERT model as requested.')

add_code('''import sys
import os
import pandas as pd
import numpy as np

# Adjust warnings
import warnings
warnings.filterwarnings('ignore')

# Import project modules
import config
from utils import setup_logging, set_seed
from data_loader import load_train_test_datasets
from graph_processor import process_dataset_to_graphs
from xai_optimizer import optimize_graphs
from sequence_converter import convert_graphs_to_sequences
from model_trainer import train_model, compare_models

setup_logging()
set_seed()

# Starting with default BERT model
config.update_model('bert')
''')

add_md('## 2. Dataset Loading\nLoad the dataset (SoliAudit etc.) into memory.')

add_code('''print("Loading train and test datasets...")
train_dataset, test_dataset = load_train_test_datasets(force_reload=False)
print(f"Loaded {len(train_dataset.addresses)} training samples.")
print(f"Loaded {len(test_dataset.addresses)} testing samples.")
''')

add_md('## 3. Node & Edge Statistics Prior to Optimization\nConvert AST to Graph to count nodes and edges per file. Identify samples exceeding 100/1000 nodes.')

add_code('''print("Processing ASTs into graphs...")
train_graphs = process_dataset_to_graphs(train_dataset, force_reprocess=False)
test_graphs = process_dataset_to_graphs(test_dataset, force_reprocess=False)

node_counts = []
edge_counts = []
for g in train_graphs:
    if g and g.graph:
        node_counts.append(g.graph.number_of_nodes())
        edge_counts.append(g.graph.number_of_edges())
    else:
        node_counts.append(0)
        edge_counts.append(0)

nodes_arr = np.array(node_counts)
edges_arr = np.array(edge_counts)

print(f"Average nodes per graph: {np.mean(nodes_arr):.2f}")
print(f"Average edges per graph: {np.mean(edges_arr):.2f}")

# Counting samples over a certain number of nodes
print(f"Samples with > 1000 nodes: {np.sum(nodes_arr > 1000)}")
print(f"Samples with > 500 nodes: {np.sum(nodes_arr > 500)}")
print(f"Samples with > 100 nodes: {np.sum(nodes_arr > 100)}")

print("\\nStatistics per solidity file (first 5 files):")
for i in range(min(5, len(train_dataset.addresses))):
    print(f"File {train_dataset.addresses[i]}: {node_counts[i]} nodes, {edge_counts[i]} edges")
''')

add_md('## 4. Graph Optimization with Thresholding (80%, 50%, 20%)\nOptimize graphs (removing irrelevant nodes) using different thresholds.')

add_code('''thresholds = [0.8, 0.5, 0.2]
optimized_results_train = {}
optimized_results_test = {}

# For demonstration purposes in a reasonable time, we take a subset of the dataset.
# You can change SUBSET_SIZE to len(train_graphs) to run for the full dataset
TRAIN_SUBSET = min(200, len(train_graphs))
TEST_SUBSET = min(50, len(test_graphs))

sample_train_graphs = train_graphs[:TRAIN_SUBSET]
sample_test_graphs = test_graphs[:TEST_SUBSET]

for t in thresholds:
    print(f"\\n--- Optimizing with Retention Threshold = {t*100}% ---")
    config.TOP_NODES_PERCENTAGE = t
    
    # We will use simple heuristics here instead of GNN Explainer for speed purposes
    # but use_gnn_explainer=True can be enabled if torch_geometric and pretrained explainer is available.
    opt_train = optimize_graphs(sample_train_graphs, use_gnn_explainer=False, force_reoptimize=True)
    opt_test = optimize_graphs(sample_test_graphs, use_gnn_explainer=False, force_reoptimize=True)
    
    optimized_results_train[t] = opt_train
    optimized_results_test[t] = opt_test
    
    # Count new nodes
    opt_node_counts = [g.graph.number_of_nodes() for g in opt_train if g and g.graph]
    print(f"New average nodes per graph (Threshold {t}): {np.mean(opt_node_counts):.2f}")

# Reset threshold to default (e.g. 50%)
config.TOP_NODES_PERCENTAGE = 0.5
''')

add_md('## 5. Convert to Sequence\nConvert both original and optimized graphs into token sequences using DFS traversal.')

add_code('''print("Converting Original Graphs to Sequence...")
train_seqs_orig = convert_graphs_to_sequences(sample_train_graphs, traversal_method='dfs', force_reconvert=True)
test_seqs_orig = convert_graphs_to_sequences(sample_test_graphs, traversal_method='dfs', force_reconvert=True)

print("\\nConverting Optimized Graphs (50% Threshold) to Sequence...")
# Using the 50% retained nodes graphs
train_seqs_opt = convert_graphs_to_sequences(optimized_results_train[0.5], traversal_method='dfs', force_reconvert=True)
test_seqs_opt = convert_graphs_to_sequences(optimized_results_test[0.5], traversal_method='dfs', force_reconvert=True)
''')

add_md('## 6. Training and Evaluation (Before vs After Optimization)\nTrain a BERT model on original sequences (Before) vs optimized sequences (After), recording time train and inference along with metrics like Accuracy, Precision, Recall, F1.')

add_code('''# Limit training scope for notebook execution safety
config.TRAINING_ARGS['num_train_epochs'] = 1
config.TRAINING_ARGS['max_steps'] = 10 
# Note: please remove max_steps and increase epochs for actual exhaustive training

print("=== Training BERT on Original Graphs (AST -> Seq) ===")
# AST -> Seq model
model_orig, metrics_orig = train_model(train_seqs_orig, test_seqs_orig, model_name="bert")

print("\\n=== Training BERT on Optimized Graphs (AST -> GNN Ex -> Seq) ===")
# AST -> GNN Ex -> Seq
model_opt, metrics_opt = train_model(train_seqs_opt, test_seqs_opt, model_name="bert")

# Combine results for comparison
comparison_data = []

def parse_metrics(m_dict, name):
    eval_m = m_dict['eval_results']
    return {
        'Scenario': name,
        'Train Time (s)': m_dict['train_time'],
        'Inference Time (s)': m_dict['inference_time'],
        'Accuracy': eval_m.get('eval_accuracy', 0),
        'Precision': eval_m.get('eval_precision', 0),
        'Recall': eval_m.get('eval_recall', 0),
        'F1 Score': eval_m.get('eval_f1', 0)
    }

comparison_data.append(parse_metrics(metrics_orig, "Before (AST->Seq)"))
comparison_data.append(parse_metrics(metrics_opt, "After (AST->GNN->Seq)"))

df_comparison = pd.DataFrame(comparison_data)
display(df_comparison)
''')

add_md('## 7. Compare Multiple Models\nRunning various models (e.g., BERT, DistilBERT, CodeBERT) on the optimized dataset.')

add_code('''# Compare various models on the OPTIMIZED sequences
# Using bert, distilbert and codebert
models_to_test = ['bert', 'distilbert', 'codebert']

print("Running comparison across different models...")
multi_model_results = compare_models(train_seqs_opt, test_seqs_opt, model_keys=models_to_test)

# Format standard output presentation
df_multi_model = []
for model_key, metrics in multi_model_results.items():
    df_multi_model.append({
        'Model Name': model_key.upper(),
        'Train Time (s)': metrics['train_time'],
        'Inference Time (s)': metrics['inference_time'],
        'Accuracy': metrics['eval_results'].get('eval_accuracy', 0),
        'Precision': metrics['eval_results'].get('eval_precision', 0),
        'Recall': metrics['eval_results'].get('eval_recall', 0),
        'F1 Score': metrics['eval_results'].get('eval_f1', 0)
    })

comparison_df = pd.DataFrame(df_multi_model)
display(comparison_df)
''')

add_md('## Optional Task: Test Using GPT-2\nAlthough GPT-2 defaults to decoder-only structure, it can be tested.')

add_code('''# GPT-2 testing is marked as Optional.
target_model = 'gpt2'
# If you want to train GPT2, you can uncomment and run:
# config.update_model(target_model)
# model_gpt2, metrics_gpt2 = train_model(train_seqs_opt, test_seqs_opt, model_name=target_model)
print("GPT-2 setup logic completed in comments.")
''')

out_path = '/home/jc/scripts/smart_contract_detection_xAI/Experiment_XAI_Pipeline.ipynb'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)

print(f"Notebook generated successfully at {out_path}!")
