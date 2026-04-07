import pandas as pd
from datasets import load_dataset
import matplotlib.pyplot as plt

print("Loading dataset from Hugging Face...")
dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")

print("Extracting management_group_id...")
train_df = dataset['train'].select_columns(['management_group_id']).to_pandas()
eval_df = dataset['eval'].select_columns(['management_group_id']).to_pandas()

# Combine both sets to get the full picture
df = pd.concat([train_df, eval_df], ignore_index=True)
total_rows = len(df)
print(f"Total rows: {total_rows}")

# Count occurrences of each management_group_id
group_counts = df['management_group_id'].value_counts().reset_index()
group_counts.columns = ['management_group_id', 'count']
group_counts['percentage'] = (group_counts['count'] / total_rows * 100).round(2)

print("\n--- Distribution of Data by Management Group ---")
print(group_counts.to_string(index=False))

# Calculate cumulative percentage
group_counts['cumulative_percentage'] = group_counts['percentage'].cumsum()

# Save summary to a CSV for easy viewing
group_counts.to_csv('/workspace/management_group_stats.csv', index=False)

# Create a bar chart
plt.figure(figsize=(12, 6))
bars = plt.bar(group_counts['management_group_id'].astype(str), group_counts['count'], color='skyblue')

# Add labels on top of the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:,}', 
             ha='center', va='bottom', fontsize=9, rotation=90)

plt.title('Data Volume by Management Group (management_group_id)', fontsize=14)
plt.xlabel('Management Group ID', fontsize=12)
plt.ylabel('Number of Records', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adjust y-axis limit to fit the labels
plt.ylim(0, group_counts['count'].max() * 1.15)

plt.tight_layout()
plt.savefig('/workspace/management_group_distribution.png', dpi=300)
print("\nSaved distribution chart to /workspace/management_group_distribution.png")
print("Saved detailed stats to /workspace/management_group_stats.csv")

