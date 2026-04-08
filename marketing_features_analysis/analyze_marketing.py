import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datasets import load_dataset
import matplotlib

# Set font for matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False
try:
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
except:
    pass

print("Loading dataset from Hugging Face...")
dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")

features = ['discount', 'holiday_flag', 'activity_flag']

print("Extracting features...")
train_df = dataset['train'].select_columns(features).to_pandas()
eval_df = dataset['eval'].select_columns(features).to_pandas()
df = pd.concat([train_df, eval_df], ignore_index=True)

print("Sampling 100,000 rows as requested...")
df_sampled = df.sample(n=100000, random_state=42)

print("\nCalculating Correlation Matrix (R)...")
corr = df_sampled.corr()
print(corr)

# 1. Plot Correlation Heatmap (R图)
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.3f', linewidths=0.5)
plt.title('Correlation Heatmap of Marketing Features', fontsize=14)
plt.tight_layout()
plt.savefig('/workspace/marketing_correlation_heatmap.png', dpi=300)
print("\nSaved Correlation Heatmap to /workspace/marketing_correlation_heatmap.png")

# 2. Plot Scatter Plots (Pairplot)
# Since holiday_flag and activity_flag are binary (0 or 1), standard scatter plots might look like just 4 dots.
# To make it readable, we will add some jitter (slight random noise) to the binary features for the scatter plot,
# or use Seaborn's pairplot with specific settings.
print("Generating Scatter Plots...")

# Create a copy for plotting to add jitter to binary features
plot_df = df_sampled.copy()
# Add small random noise to binary flags just for visualization purposes
plot_df['holiday_flag_jitter'] = plot_df['holiday_flag'] + np.random.uniform(-0.1, 0.1, size=len(plot_df))
plot_df['activity_flag_jitter'] = plot_df['activity_flag'] + np.random.uniform(-0.1, 0.1, size=len(plot_df))

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot 1: discount vs holiday_flag
sns.scatterplot(data=plot_df, x='holiday_flag_jitter', y='discount', alpha=0.1, ax=axes[0], color='blue')
axes[0].set_title(f'Discount vs Holiday Flag\n(R = {corr.loc["discount", "holiday_flag"]:.3f})')
axes[0].set_xlabel('Holiday Flag (with jitter)')
axes[0].set_ylabel('Discount (0-1)')
axes[0].set_xticks([0, 1])

# Plot 2: discount vs activity_flag
sns.scatterplot(data=plot_df, x='activity_flag_jitter', y='discount', alpha=0.1, ax=axes[1], color='green')
axes[1].set_title(f'Discount vs Activity Flag\n(R = {corr.loc["discount", "activity_flag"]:.3f})')
axes[1].set_xlabel('Activity Flag (with jitter)')
axes[1].set_ylabel('Discount (0-1)')
axes[1].set_xticks([0, 1])

# Plot 3: holiday_flag vs activity_flag (2D histogram/hexbin is better here, but we use scatter with jitter)
sns.scatterplot(data=plot_df, x='holiday_flag_jitter', y='activity_flag_jitter', alpha=0.01, ax=axes[2], color='purple')
axes[2].set_title(f'Activity Flag vs Holiday Flag\n(R = {corr.loc["holiday_flag", "activity_flag"]:.3f})')
axes[2].set_xlabel('Holiday Flag (with jitter)')
axes[2].set_ylabel('Activity Flag (with jitter)')
axes[2].set_xticks([0, 1])
axes[2].set_yticks([0, 1])

plt.tight_layout()
plt.savefig('/workspace/marketing_scatter_plots.png', dpi=300)
print("Saved Scatter Plots to /workspace/marketing_scatter_plots.png")

