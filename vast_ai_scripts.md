Scripts to run Vast.ai instance
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/JakeClark-chan/smart_contract_detection_xAI.git
cd smart_contract_detection_xAI
uv pip install -r requirements.txt
uv pip install kaggle
export KAGGLE_API_TOKEN=KGAT_57afc4e7bca72ee06ff06959f2bbdeb6
kaggle datasets download -d jakeclark38a/smart-contract-vulnerability-detection --version 1
```
Scripts to update all csv dataset:

```bash
mkdir -p /tmp/kaggle_upload && \
cp output/dataset-metadata.json /tmp/kaggle_upload/ && \
ln output/*.csv /tmp/kaggle_upload/ && \
ln soliaudit_*.csv /tmp/kaggle_upload/ && \
kaggle datasets version -m "Added optimized datasets and token counts" -p /tmp/kaggle_upload/
```
