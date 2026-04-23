# Smart Contract Vulnerability Detection with XAI

## Project Overview

This research project focuses on **smart contract vulnerability detection** using a hybrid approach that combines:
- **Large Language Models (LLMs)**: BERT, CodeBERT, GraphCodeBERT, GPT-2
- **Explainable AI (XAI)**: SHAP (SHapley Additive exPlanations) and GNN Explainer
- **Graph-to-Sequence Optimization**: Converting Abstract Syntax Trees (AST) to semantic sequences

**Primary Goal**: Detect and classify vulnerabilities in Ethereum smart contracts by identifying sensitive nodes in AST graphs, then converting optimized subgraphs to sequences for LLM processing.

**Dataset**: SoliAudit (17,980 samples from Ethereum and CTF challenges)

### Research Architecture

### Pipeline Overview
1. **Smart Contract → AST Graph**: Parse Solidity contracts into Abstract Syntax Trees
2. **XAI Node Identification**: Use **GNN Explainer** to find sensitive/critical nodes
3. **Graph Optimization**: Apply DFS traversal on sensitive subgraphs to preserve execution flow
4. **Sequence Generation**: Convert optimized graphs to tokenizable sequences
5. **LLM Classification**: Fine-tune BERT-family models (start with **BERT and DistilBERT**) for multi-label vulnerability detection

### Key Innovation
- **Token Limit Solution**: Instead of feeding entire contracts (>512 tokens) to LLMs, extract only sensitive node sequences using **SHAP value thresholds**
- **Semantic Preservation**: DFS traversal maintains attack flow logic while reducing sequence length

## Development Guidelines

### Language & Framework Expectations
- **Primary Language**: Python 3.x
- **ML Frameworks**: PyTorch for LLM fine-tuning and GNN operations
- **Code Location**: Python scripts in the **project root directory** (same level as `note_xai.txt`)
- **Expected Libraries**:
  - `transformers` (Hugging Face - prioritize BERT and DistilBERT models)
  - `torch-geometric` (GNN Explainer implementation)
  - `shap` (SHAP value threshold calculation)
  - `networkx` (Graph manipulation and DFS traversal)
  - `pandas` (AST column extraction from soliaudit_dasp_v2)

### Vulnerability Types to Detect
Common smart contract vulnerabilities in scope:
- **Reentrancy** (e.g., DAO attack, KyberSwap 2023)
- **Integer Overflow/Underflow**
- **Access Control Issues**
- **Delegatecall Injection**
- **Unchecked External Calls**

### Data Processing Conventions

#### AST → Sequence Conversion
- Preserve node types, relationships, and control flow
- DFS traversal starting from sensitive nodes identified by XAI
- Example sequence format: `FunctionDef->IfStmt->Call->Transfer->Return`

#### Tokenization Strategy
- Use domain-specific tokenizers (CodeBERT tokenizer for code semantics)
- Handle Solidity-specific keywords and identifiers
- Target sequence length: ≤512 tokens after optimization

### Model Training Patterns

#### Model Selection Priority
1. **Start with BERT** (baseline model, well-documented)
2. **Then DistilBERT** (lighter, faster inference)
3. **Optional**: CodeBERT, GraphCodeBERT, GPT-2 for comparison

#### Comparison Experiments (from `note_xai.txt`)
The project compares:
1. **Baseline**: AST → Sequence (no XAI optimization)
2. **Proposed**: AST → GNN Explainer → Optimized Sequence (using SHAP value threshold)
3. **Alternative**: AST + GNN (graph-based, no sequence conversion)
4. **Comparison**: AST + GCN

**Metrics to Track**:
- Training/inference time
- Node/edge statistics (before/after optimization)
- Detection accuracy per vulnerability type

### LaTeX Documentation Structure

The research proposal in `NCKHSV_Graph_SmartContract_Nov2024/main.tex` follows Vietnamese academic format:
- Uses `biblatex` with BibTeX backend (sources in `ref.bib`)
- Figures stored in `Figures/` directory
- Vietnamese language support via `\usepackage[utf8]{vietnam}`
- Custom blue section headings with `titlesec`

When updating documentation:
- Add new references to `ref.bib` using citation keys like `@article{author2024title}`
- Place diagrams in `Figures/` with descriptive Vietnamese names
- Follow existing structure: Sections A (Info), B (Research Description), B1-B4 (Subsections)

## Common Workflows

### Building LaTeX Document
```bash
cd NCKHSV_Graph_SmartContract_Nov2024
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### Expected Python Script Patterns
When implementing model training:
```python
# Typical structure for AST processing with GNN Explainer
ast_graph = parse_solidity_to_AST(contract_code)  # Focus on AST column
gnn_explainer = GNNExplainer(model, epochs=200)
node_importance = gnn_explainer.explain_node(ast_graph, node_idx)

# Filter sensitive nodes using SHAP value threshold
sensitive_nodes = [n for n, score in node_importance if score > shap_threshold]
optimized_subgraph = dfs_traverse(ast_graph, sensitive_nodes)
sequence = graph_to_sequence(optimized_subgraph)

# Tokenize for BERT/DistilBERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
tokens = tokenizer(sequence, max_length=512, truncation=True, padding=True)
```

### Dataset Expectations
- **Dataset Location**: `soliaudit_dasp_v2` dataset in project root
- **Focus Column**: **AST (Control Flow Graph)** - this is the primary data source (large file, use efficiently)
- **SoliAudit format**: Solidity source code with vulnerability labels
- **Multi-label classification**: One contract may have multiple vulnerabilities
- **Preprocessing**: Extract AST column, remove comments, normalize whitespace

## Research Timeline (6 months)

1. **Months 1-2**: LLM architecture study + vulnerability dataset preparation
2. **Months 2-4**: XAI integration + Graph→Sequence conversion algorithm
3. **Months 3-5**: Tokenizer design + LLM fine-tuning experiments
4. **Months 4-6**: Implementation, benchmarking, and report writing

## Critical Context for AI Agents

### When Writing Code
- **Use GNN Explainer**: Primary XAI method for identifying sensitive nodes
- **SHAP Value Thresholding**: Filter nodes based on SHAP importance scores (define threshold empirically)
- **AST-First Approach**: Always load AST column from `soliaudit_dasp_v2` dataset (memory-efficient chunking recommended)
- **Model Priority**: Start BERT baseline, then DistilBERT for comparison
- **Prioritize interpretability**: This is XAI research—add SHAP value visualization, attention heatmaps
- **Handle Vietnamese text**: Comments and documentation may mix English/Vietnamese
- **Token efficiency**: Always consider BERT's 512 token limit when designing sequences
- **Graph operations**: Expect frequent AST manipulation—use efficient libraries like NetworkX
- **Place scripts in root**: Keep Python files alongside `note_xai.txt`, not in subdirectories

### When Analyzing Vulnerabilities
- Reference real attacks (KyberSwap 2023 reentrancy) when explaining detection logic
- Compare with baseline tools: Slither, Mythril, Oyente
- Emphasize **why XAI helps**: showing which code patterns trigger vulnerability predictions

### When Updating Documentation
- LaTeX files use Vietnamese academic style—maintain formal language
- Research follows 4-phase structure (ND1-ND4 in Gantt chart)
- Expected deliverables: Technical reports (Vietnamese) + Scientific papers (English/Vietnamese)

## Key Files Reference

- `note_xai.txt`: Experiment plan with model comparisons (Vietnamese notes)
- `soliaudit_dasp_v2`: Dataset file - **use AST column only** (large file, handle with care)
- `NCKHSV_Graph_SmartContract_Nov2024/main.tex`: Research proposal (Vietnamese, 30-page target)
- `NCKHSV_Graph_SmartContract_Nov2024/ref.bib`: Academic references (Liu2021, Sendner2023, etc.)
- `NCKHSV_Graph_SmartContract_Nov2024/Figures/Tong_Quan_Mo_Hinh_NCKH.png`: Architecture diagram

## Implementation Decisions (Confirmed)

✅ **XAI Method**: GNN Explainer (not SHAP alone)  
✅ **Node Selection**: SHAP value threshold (define threshold empirically during experiments)  
✅ **Starting Models**: BERT → DistilBERT (baseline before trying CodeBERT/GPT-2)  
✅ **Dataset**: `soliaudit_dasp_v2` dataset in root, **focus on AST column**  
✅ **Code Location**: Python scripts in project root directory  

## Common Implementation Questions

If implementing code, clarify:
1. What SHAP value threshold to use? (suggest: start with top 20% of nodes or score > 0.5)
2. For DFS traversal, start from function entry points or vulnerability patterns?
3. How to handle AST column parsing? (JSON format? Graph representation?)
