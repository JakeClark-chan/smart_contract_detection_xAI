import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Try to read the dataset
try:
    df_train = pd.read_csv('/home/jc/code_projects/smart_contract_detection_xAI/JakeClark/soliaudit-dasp-sequence-gnn-no-explainer/train_optimized_gnn_ne.csv')
    df_test = pd.read_csv('/home/jc/code_projects/smart_contract_detection_xAI/JakeClark/soliaudit-dasp-sequence-gnn-no-explainer/test_optimized_gnn_ne.csv')
    df = pd.concat([df_train, df_test], ignore_index=True)
    
    labels = ['Arithmetic', 'Unchecked Return Values For Low Level Calls', 'Denial of Service', 'Time manipulation', 'Reentrancy']
    counts_1 = []
    counts_0 = []
    total = len(df)
    for label in labels:
        count_1 = df[label].sum()
        counts_1.append(count_1)
        counts_0.append(total - count_1)

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))

    y = np.arange(len(labels))
    height = 0.6

    # Lật ngược mảng để vẽ Arithmetic ở trên cùng
    labels.reverse()
    counts_1.reverse()
    counts_0.reverse()

    p1 = ax.barh(y, counts_0, height, color='#2ecc71', label='Không có (0)')
    p2 = ax.barh(y, counts_1, height, left=counts_0, color='#e74c3c', label='Có lỗ hổng (1)')

    ax.set_yticks(y)
    # Shorten labels for display
    display_labels = [l.replace('Unchecked Return Values For Low Level Calls', 'Unchecked Low Level Calls') for l in labels]
    ax.set_yticklabels(display_labels, fontsize=11)
    ax.set_xlabel('Số lượng mẫu (Smart Contracts)', fontsize=12)
    ax.set_title('Phân phối Lỗ hổng trong Tập dữ liệu (Train + Test)', fontsize=14, pad=15)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=12)

    # Thêm text số liệu
    for i, (c0, c1) in enumerate(zip(counts_0, counts_1)):
        ax.text(c0 / 2, i, str(c0), ha='center', va='center', color='black', fontweight='bold', fontsize=10)
        ax.text(c0 + c1 / 2, i, str(c1), ha='center', va='center', color='white', fontweight='bold', fontsize=10)

    plt.tight_layout()
    plt.savefig('/home/jc/code_projects/smart_contract_detection_xAI/results/images/label_distribution.png', dpi=300, bbox_inches='tight')
    print("Saved to results/images/label_distribution.png")

except Exception as e:
    print(f"Error reading CSVs: {e}")

