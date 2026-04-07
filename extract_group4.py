import pandas as pd
from datasets import load_dataset
import os

print("Loading dataset from Hugging Face...")
dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")

print("\n--- Extracting Management Group 4 ---")
# Convert to pandas for easier filtering
train_df = dataset['train'].to_pandas()
eval_df = dataset['eval'].to_pandas()

# Filter for management_group_id == 4
train_group4 = train_df[train_df['management_group_id'] == 4]
eval_group4 = eval_df[eval_df['management_group_id'] == 4]

print(f"Original Train Rows: {len(train_df)} -> Group 4 Train Rows: {len(train_group4)}")
print(f"Original Eval Rows: {len(eval_df)} -> Group 4 Eval Rows: {len(eval_group4)}")

# Verify the target column is present
print("\nChecking for 'sale_amount' target column:")
print(f"'sale_amount' in Train: {'sale_amount' in train_group4.columns}")
print(f"'sale_amount' in Eval: {'sale_amount' in eval_group4.columns}")

# Save to CSV
output_dir = "/workspace/group4_dataset"
os.makedirs(output_dir, exist_ok=True)

train_path = os.path.join(output_dir, "train_group4.csv")
eval_path = os.path.join(output_dir, "eval_group4.csv")

print(f"\nSaving to CSV...")
train_group4.to_csv(train_path, index=False)
eval_group4.to_csv(eval_path, index=False)

print(f"Successfully saved:")
print(f"  - Train: {train_path} ({len(train_group4)} rows)")
print(f"  - Eval: {eval_path} ({len(eval_group4)} rows)")

