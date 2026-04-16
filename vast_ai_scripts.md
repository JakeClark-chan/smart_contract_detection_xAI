Scripts to run Vast.ai instance
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/JakeClark-chan/smart_contract_detection_xAI.git
cd smart_contract_detection_xAI
uv pip install -r requirements.txt
uv run generate_optimized_exp_set.py --force-reload --use-gnn --upload-to-hf
```
