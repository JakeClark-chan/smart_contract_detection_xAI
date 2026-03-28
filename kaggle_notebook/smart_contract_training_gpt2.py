"""
# Smart Contract Vulnerability Detection - GPT-2 Fine-tuning
Training with all optimization thresholds: before_optimized, optimized_80p, optimized_50p, optimized_20p

Uses GPT-2 with prompting to generate structured Markdown vulnerability reports.
Example output format:
Vulnerabilities:
* Arithmetic
* Denial of Service
"""

import os
import subprocess
import sys
import time
import re

import torch

print("=" * 60)
print("ENVIRONMENT CHECK")
print("=" * 60)
print(f"Python: {sys.version}")
print(f"PyTorch: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
print()

print("=" * 60)
print("STEP 1: Install Dependencies")
print("=" * 60)

result = subprocess.run(
    [sys.executable, "-m", "pip", "install", "uv", "-q"],
    capture_output=True,
    text=True,
    timeout=60,
)
print(f"uv install: OK" if result.returncode == 0 else "FAILED")

missing_packages = ["transformers", "accelerate", "datasets", "scikit-learn"]
result = subprocess.run(
    ["uv", "pip", "install", "--system"] + missing_packages,
    capture_output=True,
    text=True,
    timeout=600,
)
print(f"Packages install: OK" if result.returncode == 0 else "FAILED")

for pkg in ["transformers", "pandas", "scikit-learn"]:
    try:
        mod = __import__(pkg)
        print(f"  [OK] {pkg}")
    except ImportError:
        print(f"  [MISSING] {pkg}")
print()

print("=" * 60)
print("STEP 2: Load Optimized Dataset (FULL)")
print("=" * 60)

import pandas as pd

dataset_dir = "/kaggle/input/smart-contract-vulnerability-detection"

train_df = pd.read_csv(os.path.join(dataset_dir, "train_optimized_dataset.csv"))
test_df = pd.read_csv(os.path.join(dataset_dir, "test_optimized_dataset.csv"))

print(f"Train samples: {len(train_df)}")
print(f"Test samples: {len(test_df)}")
print(f"Columns: {train_df.columns.tolist()}")

label_columns = [
    "Arithmetic",
    "Unchecked Return Values For Low Level Calls",
    "Denial of Service",
    "Time manipulation",
    "Reentrancy",
]
print(f"Labels: {label_columns}")
print()

print("=" * 60)
print("STEP 3: Define Helper Functions")
print("=" * 60)

import gc
import numpy as np
from sklearn.metrics import (
    classification_report,
    hamming_loss,
    precision_recall_fscore_support,
)
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from torch.utils.data import Dataset as TorchDataset


def format_vulnerabilities(labels, label_columns):
    """Format multi-label as Markdown vulnerability list"""
    vulns = []
    for i, label in enumerate(label_columns):
        if labels[i] == 1:
            vulns.append(label)
    if not vulns:
        vulns.append("None")
    return "Vulnerabilities:\n" + "\n".join(f"* {v}" for v in vulns)


def create_prompt(text, label_columns):
    """Create prompt with smart contract code"""
    vuln_list = format_vulnerabilities([0] * len(label_columns), label_columns)
    prompt = f"""Analyze the following smart contract for security vulnerabilities:

Smart Contract:
{text[:1500]}

{vuln_list}"""
    return prompt


def parse_vulnerabilities(output_text, label_columns):
    """Parse model output to extract vulnerabilities"""
    output_lower = output_text.lower()

    detected = []
    for label in label_columns:
        label_lower = label.lower()
        if label_lower in output_lower:
            detected.append(1)
        else:
            detected.append(0)

    if sum(detected) == 0:
        detected = [0] * len(label_columns)

    return detected


class VulnerabilityDataset(TorchDataset):
    def __init__(self, texts, labels, tokenizer, label_columns, max_length=1000):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.label_columns = label_columns
        self.max_length = max_length

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]

        prompt = create_prompt(text, self.label_columns)

        encoding = self.tokenizer(
            prompt,
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt",
        )

        item = {key: val.squeeze(0) for key, val in encoding.items()}
        item["labels"] = item["input_ids"].clone()

        return item

    def __len__(self):
        return len(self.texts)


def hamming_score(y_true, y_pred, normalize=True, sample_weight=None):
    acc_list = []
    for i in range(y_true.shape[0]):
        set_true = set(np.where(y_true[i])[0])
        set_pred = set(np.where(y_pred[i])[0])
        tmp_a = None
        if len(set_true) == 0 and len(set_pred) == 0:
            tmp_a = 1
        else:
            tmp_a = len(set_true.intersection(set_pred)) / float(
                len(set_true.union(set_pred))
            )
        acc_list.append(tmp_a)
    return np.mean(acc_list)


def compute_metrics_gpt2(eval_pred, tokenizer, label_columns):
    """Compute metrics for GPT-2 generation"""
    logits, labels = eval_pred

    pred_labels = []
    true_labels = []

    for i in range(len(logits)):
        decoded = tokenizer.decode(logits[i], skip_special_tokens=True)
        pred = parse_vulnerabilities(decoded, label_columns)
        pred_labels.append(pred)
        true_labels.append(labels[i])

    pred_labels = np.array(pred_labels)
    true_labels = np.array(true_labels)

    predictions = pred_labels

    precision, recall, f1, _ = precision_recall_fscore_support(
        true_labels, predictions, average="weighted", zero_division=0
    )

    hamming = hamming_score(true_labels, predictions)
    h_loss = hamming_loss(true_labels, predictions)

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "hamming_score": hamming,
        "hamming_loss": h_loss,
    }


def train_and_evaluate(column_name, train_df, test_df, label_columns, output_dir):
    print(f"\n" + "=" * 60)
    print(f"Training with column: {column_name}")
    print("=" * 60)

    train_texts = train_df[column_name].fillna("").astype(str).tolist()
    test_texts = test_df[column_name].fillna("").astype(str).tolist()
    train_labels = train_df[label_columns].values
    test_labels = test_df[label_columns].values

    print(f"Train: {len(train_texts)}, Test: {len(test_texts)}")

    MODEL_NAME = "gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    train_dataset = VulnerabilityDataset(
        train_texts, train_labels, tokenizer, label_columns
    )
    test_dataset = VulnerabilityDataset(
        test_texts, test_labels, tokenizer, label_columns
    )

    model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)
    model.config.pad_token_id = tokenizer.eos_token_id

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    train_size = int(0.8 * len(train_dataset))
    eval_size = len(train_dataset) - train_size
    train_dataset_split, eval_dataset = torch.utils.data.random_split(
        train_dataset, [train_size, eval_size]
    )

    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=10,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        learning_rate=2e-5,
        weight_decay=0.01,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=False,
        save_total_limit=1,
        fp16=torch.cuda.is_available(),
        logging_steps=100,
        report_to="none",
        gradient_accumulation_steps=2,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset_split,
        eval_dataset=eval_dataset,
    )

    train_start = time.time()
    print("Training...")
    trainer.train()
    train_time = time.time() - train_start

    print("Generating predictions...")
    test_start = time.time()
    preds = trainer.predict(test_dataset)
    test_inference_time = time.time() - test_start

    pred_labels = []
    for i in range(len(preds.predictions)):
        decoded = tokenizer.decode(preds.predictions[i], skip_special_tokens=True)
        pred = parse_vulnerabilities(decoded, label_columns)
        pred_labels.append(pred)

    pred_labels = np.array(pred_labels)

    print("\nClassification Report by Label:")
    print(
        classification_report(
            test_labels, pred_labels, target_names=label_columns, zero_division=0
        )
    )

    precision, recall, f1, _ = precision_recall_fscore_support(
        test_labels, pred_labels, average="weighted", zero_division=0
    )
    hamming = hamming_score(test_labels, pred_labels)
    h_loss = hamming_loss(test_labels, pred_labels)

    model_save_dir = os.path.join(output_dir, column_name)
    os.makedirs(model_save_dir, exist_ok=True)
    model.save_pretrained(model_save_dir)
    tokenizer.save_pretrained(model_save_dir)

    del model, trainer, train_dataset, test_dataset
    gc.collect()
    torch.cuda.empty_cache()

    return {
        "column": column_name,
        "train_time": train_time,
        "train_inference_time": 0,
        "test_inference_time": test_inference_time,
        "num_train_samples": len(train_texts),
        "num_test_samples": len(test_texts),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "hamming_score": hamming,
        "hamming_loss": h_loss,
    }


print("Helper functions defined")
print()

print("=" * 60)
print("STEP 4: Run All Experiments")
print("=" * 60)

import json
from pathlib import Path

output_base = "/kaggle/working/output"
Path(output_base).mkdir(parents=True, exist_ok=True)

columns = ["before_optimized", "optimized_80p", "optimized_50p", "optimized_20p"]

all_results = []
total_start = time.time()

for col in columns:
    result = train_and_evaluate(
        column_name=col,
        train_df=train_df,
        test_df=test_df,
        label_columns=label_columns,
        output_dir=output_base,
    )
    all_results.append(result)

    print(f"\nResults for {col}:")
    print(
        f"  Train Samples: {result['num_train_samples']}, Test Samples: {result['num_test_samples']}"
    )
    print(f"  Train Time: {result['train_time'] / 60:.1f} min")
    print(f"  Train Inference Time: {result['train_inference_time']:.2f}s")
    print(f"  Test Inference Time: {result['test_inference_time']:.2f}s")
    print(f"  Precision: {result['precision']:.4f}")
    print(f"  Recall: {result['recall']:.4f}")
    print(f"  F1: {result['f1']:.4f}")
    print(f"  Hamming Score: {result['hamming_score']:.4f}")
    print(f"  Hamming Loss: {result['hamming_loss']:.4f}")

    gc.collect()
    torch.cuda.empty_cache()

total_time = time.time() - total_start
print(f"\nTotal training time: {total_time / 60:.1f} minutes")
print()

print("=" * 60)
print("STEP 5: Summary Comparison")
print("=" * 60)

comparison_df = pd.DataFrame(all_results)
comparison_df = comparison_df[
    [
        "column",
        "num_train_samples",
        "num_test_samples",
        "train_time",
        "train_inference_time",
        "test_inference_time",
        "precision",
        "recall",
        "f1",
        "hamming_score",
        "hamming_loss",
    ]
]
comparison_df.columns = [
    "Dataset",
    "Train Samples",
    "Test Samples",
    "Train Time (s)",
    "Train Inference (s)",
    "Test Inference (s)",
    "Precision",
    "Recall",
    "F1",
    "Hamming Score",
    "Hamming Loss",
]

print("\n" + "=" * 100)
print("FINAL RESULTS COMPARISON")
print("=" * 100)
print(comparison_df.to_string(index=False))
print("=" * 100)

comparison_csv = os.path.join(output_base, "comparison_results.csv")
comparison_df.to_csv(comparison_csv, index=False)
print(f"\nResults saved to: {comparison_csv}")

results_json = {
    "configuration": {"model": "gpt2", "labels": label_columns},
    "results": all_results,
    "total_time": total_time,
}

results_json_path = os.path.join(output_base, "experiment_results.json")
with open(results_json_path, "w") as f:
    json.dump(results_json, f, indent=2)
print(f"Results saved to: {results_json_path}")

print("\nAll experiments completed!")
print()
