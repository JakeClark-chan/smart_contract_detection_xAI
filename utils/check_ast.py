import json
from datasets import load_dataset

ds = load_dataset("JakeClark/soliaudit-dasp-ast-graph", split="train")
target_address = "0xa82749c94ab7f921725624fb90e7600216169597"

for item in ds:
    if target_address in item.get('address', ''):
        ast_str = item.get('AST', '')
        print("AST string snippet:", ast_str[:500])
        break
