import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datasets import load_dataset
import matplotlib

# Set Chinese font if available, else default
matplotlib.rcParams['axes.unicode_minus'] = False
try:
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
except:
    pass

print("Loading dataset from Hugging Face...")
dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")

# Select 7 ID features
features = [
    'city_id', 'store_id', 'management_group_id', 
    'first_category_id', 'second_category_id', 
    'third_category_id', 'product_id'
]

print("Combining and sampling data...")
train_df = dataset['train'].select_columns(features).to_pandas()
eval_df = dataset['eval'].select_columns(features).to_pandas()
df = pd.concat([train_df, eval_df], ignore_index=True)

# Randomly sample 150,000 rows
df_sampled = df.sample(n=150000, random_state=42)

# Calculate correlation matrix
corr = df_sampled.corr()
print("\nCorrelation Matrix:")
print(corr)

# Generate pairs (total 21 pairs)
pairs = []
for i in range(len(features)):
    for j in range(i+1, len(features)):
        pairs.append((features[i], features[j]))

# Split pairs into 3 groups of 7
groups = [pairs[0:7], pairs[7:14], pairs[14:21]]

for group_idx, group in enumerate(groups):
    fig, axes = plt.subplots(4, 2, figsize=(15, 20))
    axes = axes.flatten()
    
    for pair_idx, (f1, f2) in enumerate(group):
        ax = axes[pair_idx]
        
        # ID features are categorical/discrete, so we group by f1 and calculate the mean of f2
        # However, plotting raw IDs might be noisy. Let's do a scatter plot with density/alpha 
        # or a boxplot/violin plot if the cardinality is small. 
        # But user requested LINE CHARTS, so we group by f1, sort by f1, and plot the mean of f2.
        
        # To make the line chart readable, we group by f1 and take the mean of f2
        # We also count the frequency to filter out very rare categories if needed, but we'll keep all for now.
        grouped = df_sampled.groupby(f1)[f2].mean().reset_index().sort_values(by=f1)
        
        ax.plot(grouped[f1], grouped[f2], marker='o', linestyle='-', linewidth=2, color='g', markersize=4)
        ax.set_title(f"{f1} vs {f2}\n(Correlation: {corr.loc[f1, f2]:.3f})")
        ax.set_xlabel(f1)
        ax.set_ylabel(f"Mean of {f2}")
        ax.grid(True, linestyle='--', alpha=0.7)
    
    # Hide the empty 8th subplot
    axes[7].set_visible(False)
    
    plt.tight_layout()
    filename = f'/workspace/id_correlation_line_charts_part{group_idx+1}.png'
    plt.savefig(filename, dpi=300)
    print(f"Saved {filename}")

# Also plot the heatmap of correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.3f')
plt.title('Correlation Heatmap of 7 ID Features')
plt.tight_layout()
plt.savefig('/workspace/id_correlation_heatmap.png', dpi=300)
print("Saved /workspace/id_correlation_heatmap.png")

