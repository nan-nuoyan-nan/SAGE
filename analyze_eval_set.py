import pandas as pd
from datasets import load_dataset

print("Loading dataset from Hugging Face...")
dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")

print("\n--- Analyzing Train Set ---")
train_df = dataset['train'].select_columns(['dt', 'store_id', 'product_id', 'management_group_id']).to_pandas()
print(f"Train Rows: {len(train_df)}")
print(f"Train Date Range: {train_df['dt'].min()} to {train_df['dt'].max()}")
print(f"Train Unique Stores: {train_df['store_id'].nunique()}")
print(f"Train Unique Products: {train_df['product_id'].nunique()}")
print(f"Train Unique Management Groups: {train_df['management_group_id'].nunique()}")

print("\n--- Analyzing Eval Set ---")
eval_df = dataset['eval'].select_columns(['dt', 'store_id', 'product_id', 'management_group_id']).to_pandas()
print(f"Eval Rows: {len(eval_df)}")
print(f"Eval Date Range: {eval_df['dt'].min()} to {eval_df['dt'].max()}")
print(f"Eval Unique Stores: {eval_df['store_id'].nunique()}")
print(f"Eval Unique Products: {eval_df['product_id'].nunique()}")
print(f"Eval Unique Management Groups: {eval_df['management_group_id'].nunique()}")

print("\n--- Comparing Sets ---")
train_store_product = set(zip(train_df['store_id'], train_df['product_id']))
eval_store_product = set(zip(eval_df['store_id'], eval_df['product_id']))

new_pairs_in_eval = eval_store_product - train_store_product
print(f"Store-Product Pairs in Eval: {len(eval_store_product)}")
print(f"Store-Product Pairs in Eval but NOT in Train (New combinations): {len(new_pairs_in_eval)}")

