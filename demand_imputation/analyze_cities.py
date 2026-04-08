import pandas as pd
import matplotlib.pyplot as plt
from datasets import load_dataset
import matplotlib

# Set font
matplotlib.rcParams['axes.unicode_minus'] = False
try:
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
except:
    pass

print("Loading train dataset from Hugging Face...")
# We only load the 'train' split as requested
dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K", split='train')

print("Extracting city_id...")
df = dataset.select_columns(['city_id']).to_pandas()

total_train_rows = len(df)
print(f"Total train rows: {total_train_rows}")

# Count occurrences of each city_id
city_counts = df['city_id'].value_counts().reset_index()
city_counts.columns = ['city_id', 'count']
city_counts['percentage'] = (city_counts['count'] / total_train_rows * 100).round(2)

print("\n--- Distribution of Train Data by City ---")
print(city_counts.to_string(index=False))

# Save to CSV
csv_path = '/workspace/demand_imputation/train_city_distribution.csv'
city_counts.to_csv(csv_path, index=False)

# Plot Bar Chart
plt.figure(figsize=(16, 6))
bars = plt.bar(city_counts['city_id'].astype(str), city_counts['count'], color='coral')

# Add labels on top of the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + (yval * 0.01), f'{yval:,}', 
             ha='center', va='bottom', fontsize=8, rotation=45)

plt.title('Train Data Volume by City (city_id)', fontsize=14)
plt.xlabel('City ID', fontsize=12)
plt.ylabel('Number of Records (Train Dataset)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adjust y-axis limit to fit the labels
plt.ylim(0, city_counts['count'].max() * 1.15)
plt.tight_layout()

img_path = '/workspace/demand_imputation/train_city_distribution.png'
plt.savefig(img_path, dpi=300)

print(f"\nSaved distribution chart to {img_path}")
print(f"Saved detailed stats to {csv_path}")

