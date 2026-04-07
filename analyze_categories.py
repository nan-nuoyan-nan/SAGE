import pandas as pd
from datasets import load_dataset

print("Loading dataset from Hugging Face...")
dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K", split='train')

print("Analyzing category relationships...")
df = dataset.select_columns(['first_category_id', 'second_category_id']).to_pandas()

# Count unique combinations
unique_combos = df.drop_duplicates().sort_values(by=['first_category_id', 'second_category_id'])
print(f"\nTotal unique first_category_ids: {df['first_category_id'].nunique()}")
print(f"Total unique second_category_ids: {df['second_category_id'].nunique()}")
print(f"Total unique combinations: {len(unique_combos)}")

# Check if one second_category_id can belong to multiple first_category_ids
second_to_first = df.groupby('second_category_id')['first_category_id'].nunique()
multi_parent_seconds = second_to_first[second_to_first > 1]
print(f"\nNumber of second_category_ids belonging to multiple first_category_ids: {len(multi_parent_seconds)}")

if len(multi_parent_seconds) == 0:
    print("Conclusion: Every second_category_id strictly belongs to EXACTLY ONE first_category_id (Strict Hierarchy).")

# Print a few examples
print("\nSample mapping (First -> Second):")
sample_mapping = unique_combos.head(10)
print(sample_mapping.to_string(index=False))
