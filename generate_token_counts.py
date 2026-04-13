import os

import pandas as pd
from transformers import BertTokenizer


def generate_token_counts(input_csv, output_csv, tokenizer):
    print(f"Processing {input_csv} -> {output_csv}")
    df = pd.read_csv(input_csv)

    column_mapping = {
        "before_optimized": "before_optimized_token",
        "optimized_80p": "optimized_80p_token",
        "optimized_50p": "optimized_50_token",
        "optimized_20p": "optimize_20p_token",
    }

    result_data = {"address": df["address"]}

    for in_col, out_col in column_mapping.items():
        if in_col in df.columns:
            # Tokenize and count. Handle NaN by returning 0.
            result_data[out_col] = df[in_col].apply(
                lambda x: (
                    len(tokenizer.encode(str(x), add_special_tokens=True))
                    if pd.notnull(x)
                    else 0
                )
            )
        else:
            result_data[out_col] = 0

    output_df = pd.DataFrame(result_data)
    output_df.to_csv(output_csv, index=False)
    print(f"Saved: {output_csv}")


if __name__ == "__main__":
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    os.makedirs("output", exist_ok=True)

    datasets = [
        ("output/test_optimized_dataset.csv", "output/test_optimized_token_count.csv"),
        (
            "output/train_optimized_dataset.csv",
            "output/train_optimized_token_count.csv",
        ),
    ]

    for input_file, output_file in datasets:
        if os.path.exists(input_file):
            generate_token_counts(input_file, output_file, tokenizer)
