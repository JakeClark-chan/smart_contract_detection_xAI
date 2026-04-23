import json

filename = "notebook/smart-contract-vulnerability-detection-gpt-2.ipynb"
with open(filename, "r") as f:
    nb = json.load(f)

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        for i, line in enumerate(cell["source"]):
            if "result[num_train_samples]" in line:
                cell["source"][i] = line.replace("result[num_train_samples]", "result['num_train_samples']").replace("result[num_test_samples]", "result['num_test_samples']")
            if "result[train_time]" in line:
                cell["source"][i] = line.replace("result[train_time]", "result['train_time']")
            if "result[test_inference_time]" in line:
                cell["source"][i] = line.replace("result[test_inference_time]", "result['test_inference_time']")
            if "result[precision]" in line:
                cell["source"][i] = line.replace("result[precision]", "result['precision']")
            if "result[recall]" in line:
                cell["source"][i] = line.replace("result[recall]", "result['recall']")
            if "result[f1]" in line:
                cell["source"][i] = line.replace("result[f1]", "result['f1']")
            if "result[hamming_score]" in line:
                cell["source"][i] = line.replace("result[hamming_score]", "result['hamming_score']")
            if "result[hamming_loss]" in line:
                cell["source"][i] = line.replace("result[hamming_loss]", "result['hamming_loss']")

with open(filename, "w") as f:
    json.dump(nb, f, indent=1)
    f.write("\n")

print("Fixed notebook.")
