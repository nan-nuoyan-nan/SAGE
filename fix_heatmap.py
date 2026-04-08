import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datasets import load_dataset
import matplotlib

matplotlib.rcParams['axes.unicode_minus'] = False
try:
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
except:
    pass

print("Loading dataset...")
dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")
id_features = ['city_id', 'store_id', 'management_group_id', 
               'first_category_id', 'second_category_id', 
               'third_category_id', 'product_id']

df = dataset['train'].select_columns(id_features).to_pandas().sample(n=50000, random_state=42)
corr = df.corr()

# Fix the layout issue
plt.figure(figsize=(10, 8)) # Make figure wider to accommodate long labels
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.3f', linewidths=0.5)
plt.title('Correlation Heatmap of 7 ID Features', fontsize=14)

# Force matplotlib to fit everything into the figure area
plt.tight_layout()

# Increase left margin manually just in case
plt.subplots_adjust(left=0.25, bottom=0.2)

plt.savefig('/workspace/id_correlation_heatmap_fixed.png', dpi=300, bbox_inches='tight')
print("Fixed heatmap saved to /workspace/id_correlation_heatmap_fixed.png")
