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
print("Dataset loaded.")

# Combine train and eval
train_df = dataset['train'].select_columns(['precpt', 'avg_temperature', 'avg_humidity', 'avg_wind_level']).to_pandas()
eval_df = dataset['eval'].select_columns(['precpt', 'avg_temperature', 'avg_humidity', 'avg_wind_level']).to_pandas()
df = pd.concat([train_df, eval_df], ignore_index=True)
print(f"Total rows: {len(df)}")

# Randomly sample 150,000 rows
print("Sampling 150,000 rows...")
df_sampled = df.sample(n=150000, random_state=42)

# Calculate correlation matrix
corr = df_sampled.corr()
print("\nCorrelation Matrix:")
print(corr)

# Features to analyze
features = ['precpt', 'avg_temperature', 'avg_humidity', 'avg_wind_level']
feature_names = {
    'precpt': 'Precipitation (mm)',
    'avg_temperature': 'Avg Temperature (C)',
    'avg_humidity': 'Avg Humidity (%)',
    'avg_wind_level': 'Avg Wind Level'
}

# Create subplots for pairwise line charts
fig, axes = plt.subplots(3, 2, figsize=(15, 18))
axes = axes.flatten()

pair_idx = 0
for i in range(len(features)):
    for j in range(i+1, len(features)):
        f1, f2 = features[i], features[j]
        ax = axes[pair_idx]
        
        # To draw a meaningful line chart for 150k points, we bin f1 and plot the mean of f2
        # Create 50 bins for f1
        bins = np.linspace(df_sampled[f1].min(), df_sampled[f1].max(), 50)
        df_sampled['f1_bin'] = pd.cut(df_sampled[f1], bins=bins, labels=False)
        
        # Calculate mean of f1 and f2 for each bin
        bin_means = df_sampled.groupby('f1_bin')[[f1, f2]].mean().dropna()
        
        # Plot line chart
        ax.plot(bin_means[f1], bin_means[f2], marker='o', linestyle='-', linewidth=2, color='b')
        ax.set_title(f"{feature_names[f1]} vs {feature_names[f2]}\n(Correlation: {corr.loc[f1, f2]:.3f})")
        ax.set_xlabel(feature_names[f1])
        ax.set_ylabel(feature_names[f2])
        ax.grid(True, linestyle='--', alpha=0.7)
        
        pair_idx += 1

plt.tight_layout()
plt.savefig('/workspace/climate_correlation_line_charts.png', dpi=300)
print("\nPlot saved to /workspace/climate_correlation_line_charts.png")
