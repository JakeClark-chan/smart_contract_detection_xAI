import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import re

# Use a clean, professional style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.3)

out_dir = "../results/images"
os.makedirs(out_dir, exist_ok=True)

# 1. Best F1 Comparison
def plot_f1_best():
    models = ['BERT', 'DistilBERT', 'CodeBERT', 'GPT-2']
    gnn_no = [0.9074, 0.9024, 0.9244, 0.9136]
    gnn_ex = [0.8578, 0.8581, 0.8831, 0.8963]
    gcn_ex = [0.8993, 0.8997, 0.9140, 0.9073]

    x = np.arange(len(models))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width, gnn_no, width, label='GNN (No Explainer)', color='#2ca02c')
    rects2 = ax.bar(x, gnn_ex, width, label='GNN Explainer', color='#d62728')
    rects3 = ax.bar(x + width, gcn_ex, width, label='GCN Explainer', color='#1f77b4')

    ax.set_ylabel('Best F1-Score')
    ax.set_title('So sánh F1-Score tốt nhất theo mô hình và kịch bản')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.set_ylim(0.8, 0.95)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add values
    for rects in [rects1, rects2, rects3]:
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.4f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig(f"{out_dir}/f1_best_comparison.png", dpi=300)
    plt.close()

# 2. F1 vs Threshold
def plot_f1_vs_threshold():
    thresholds = ['Before', '80%', '50%', '20%']
    
    data = {
        'GNN (No Explainer)': {
            'BERT': [0.8730, 0.8871, 0.9021, 0.9074],
            'DistilBERT': [0.8755, 0.8868, 0.9018, 0.9024],
            'CodeBERT': [0.8943, 0.9046, 0.9244, 0.9127],
            'GPT-2': [0.9136, 0.9115, 0.9120, 0.8948]
        },
        'GNN Explainer': {
            'BERT': [0.8578, 0.8521, 0.8565, 0.8489],
            'DistilBERT': [0.8516, 0.8577, 0.8581, 0.8456],
            'CodeBERT': [0.8765, 0.8757, 0.8831, 0.8553],
            'GPT-2': [0.8963, 0.8945, 0.8800, 0.8528]
        },
        'GCN Explainer': {
            'BERT': [0.8918, 0.8944, 0.8993, 0.8989],
            'DistilBERT': [0.8769, 0.8851, 0.8997, 0.8996],
            'CodeBERT': [0.9007, 0.9085, 0.9140, 0.9004],
            'GPT-2': [0.9073, 0.9067, 0.9032, 0.8839]
        }
    }

    fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)
    colors = {'BERT': '#1f77b4', 'DistilBERT': '#ff7f0e', 'CodeBERT': '#2ca02c', 'GPT-2': '#d62728'}
    markers = {'BERT': 'o', 'DistilBERT': 's', 'CodeBERT': '^', 'GPT-2': 'D'}
    
    for i, (scenario, models_data) in enumerate(data.items()):
        ax = axes[i]
        for model, scores in models_data.items():
            ax.plot(thresholds, scores, marker=markers[model], color=colors[model], label=model, linewidth=2, markersize=8)
        ax.set_title(scenario)
        ax.set_xlabel('Mức tối ưu (Pruning Threshold)')
        ax.grid(True, linestyle='--', alpha=0.7)
        if i == 0:
            ax.set_ylabel('F1-Score (Macro Avg)')
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig(f"{out_dir}/f1_vs_threshold.png", dpi=300)
    plt.close()

# 3. Token Count Mean
def plot_token_count_mean():
    thresholds = ['Before', '80%', '50%', '20%']
    gnn_no = [1294.2, 1041.8, 638.1, 255.4]
    gnn_ex = [1295.5, 1039.3, 653.5, 266.9]
    gcn_ex = [1270.1, 1003.2, 626.3, 270.5]

    x = np.arange(len(thresholds))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width, gnn_no, width, label='GNN (No Explainer)', color='#2ca02c')
    rects2 = ax.bar(x, gnn_ex, width, label='GNN Explainer', color='#d62728')
    rects3 = ax.bar(x + width, gcn_ex, width, label='GCN Explainer', color='#1f77b4')

    # Add limit lines
    ax.axhline(y=512, color='orange', linestyle='--', linewidth=2, label='BERT Limit (512)')
    ax.axhline(y=1024, color='purple', linestyle='--', linewidth=2, label='GPT-2 Limit (1024)')

    ax.set_ylabel('Trung bình Token Count')
    ax.set_title('So sánh Token Count theo mức độ tối ưu')
    ax.set_xticks(x)
    ax.set_xticklabels(thresholds)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.savefig(f"{out_dir}/token_count_mean.png", dpi=300)
    plt.close()

# 4. Token Distribution
def plot_token_dist():
    scenarios = [
        ('GNN (No Expl)', 'Before', 84.3, 9.8, 5.9),
        ('GNN (No Expl)', '80%', 64.2, 28.3, 7.5),
        ('GNN (No Expl)', '50%', 0.0, 84.9, 15.1),
        ('GNN (No Expl)', '20%', 0.0, 0.0, 100.0),
        
        ('GCN Expl', 'Before', 84.3, 9.8, 5.9),
        ('GCN Expl', '80%', 62.7, 29.4, 7.9),
        ('GCN Expl', '50%', 0.3, 70.0, 29.7),
        ('GCN Expl', '20%', 0.0, 0.0, 100.0),
    ]

    labels = [f"{s[0]}\n{s[1]}" for s in scenarios]
    over1024 = [s[2] for s in scenarios]
    mid = [s[3] for s in scenarios]
    under512 = [s[4] for s in scenarios]

    x = np.arange(len(labels))
    width = 0.6

    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.bar(x, under512, width, label='< 512 tokens', color='#2ca02c')
    ax.bar(x, mid, width, bottom=under512, label='512 - 1024 tokens', color='#ff7f0e')
    ax.bar(x, over1024, width, bottom=np.array(under512)+np.array(mid), label='> 1024 tokens', color='#d62728')

    ax.set_ylabel('Tỷ lệ mẫu (%)')
    ax.set_title('Phân phối Token Count theo các mức độ tối ưu (GNN vs GCN)')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.savefig(f"{out_dir}/token_distribution.png", dpi=300)
    plt.close()

# 5. Training time CodeBERT
def plot_training_time():
    scenarios = ['GNN (No Expl)', 'GNN Explainer', 'GCN Explainer']
    before = [59.7, 59.7, 59.9]
    opt_20p = [26.5, 29.6, 33.4]

    x = np.arange(len(scenarios))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, before, width, label='Before Optimization', color='#7f7f7f')
    rects2 = ax.bar(x + width/2, opt_20p, width, label='Optimized (20%)', color='#2ca02c')

    ax.set_ylabel('Thời gian Huấn luyện (phút)')
    ax.set_title('Thời gian Huấn luyện CodeBERT (Before vs 20%)')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    for rects in [rects1, rects2]:
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}m',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  
                        textcoords="offset points",
                        ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(f"{out_dir}/training_time_codebert.png", dpi=300)
    plt.close()

# 6 & 7. Radar Chart CodeBERT (GNN@50% vs GCN@50%)
def plot_radar_chart():
    categories = ['Arithmetic', 'Low Level Calls', 'Denial of Service', 'Time manipulation', 'Reentrancy']
    N = len(categories)
    
    # Values
    gnn_50p = [0.98, 0.93, 0.89, 0.82, 0.90] # Macro = 0.90, micro=0.92
    gcn_50p = [0.97, 0.90, 0.87, 0.84, 0.89] # Values from CodeBERT GCN@50p result

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    gnn_50p += gnn_50p[:1]
    gcn_50p += gcn_50p[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    plt.xticks(angles[:-1], categories, size=11)
    ax.set_rlabel_position(0)
    plt.yticks([0.80, 0.85, 0.90, 0.95, 1.0], ["0.80", "0.85", "0.90", "0.95", "1.00"], color="grey", size=10)
    plt.ylim(0.75, 1.0)
    
    ax.plot(angles, gnn_50p, linewidth=2, linestyle='solid', label='GNN (No Explainer) @ 50%', color='#2ca02c')
    ax.fill(angles, gnn_50p, alpha=0.1, color='#2ca02c')
    
    ax.plot(angles, gcn_50p, linewidth=2, linestyle='solid', label='GCN Explainer @ 50%', color='#1f77b4')
    ax.fill(angles, gcn_50p, alpha=0.1, color='#1f77b4')
    
    plt.title('So sánh F1-Score từng loại lỗ hổng (CodeBERT)', size=15, y=1.1)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    plt.tight_layout()
    plt.savefig(f"{out_dir}/f1_radar.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    print("Generating charts...")
    plot_f1_best()
    plot_f1_vs_threshold()
    plot_token_count_mean()
    plot_token_dist()
    plot_training_time()
    plot_radar_chart()
    print("Done! Charts saved to results/images/")
