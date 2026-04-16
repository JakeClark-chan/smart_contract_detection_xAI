Scripts to run Vast.ai instance
```bash
git clone https://github.com/JakeClark-chan/smart_contract_detection_xAI.git
cd smart_contract_detection_xAI
uv pip install -r --no-upgrade requirements.txt
/venv/main/bin/python generate_optimized_exp_set.py --force-reload --use-gnn --upload-to-hf
```
