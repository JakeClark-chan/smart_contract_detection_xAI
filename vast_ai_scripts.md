Scripts to run Vast.ai instance
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/JakeClark-chan/smart_contract_detection_xAI.git
cd smart_contract_detection_xAI
uv pip install -r requirements.txt

```
Scripts to update all csv dataset:

```bash
mkdir -p /tmp/kaggle_upload && \
cp output/dataset-metadata.json /tmp/kaggle_upload/ && \
ln output/*.csv /tmp/kaggle_upload/ && \
ln soliaudit_*.csv /tmp/kaggle_upload/ && \
kaggle datasets version -m "Added optimized datasets and token counts" -p /tmp/kaggle_upload/
```
