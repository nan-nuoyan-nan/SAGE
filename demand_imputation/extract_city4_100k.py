import pandas as pd
from datasets import load_dataset

def main():
    print("Loading full dataset directly from HuggingFace to extract city_id=4 (approx 100k rows)...")
    dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K", split='train')
    
    print("Converting dataset to Pandas DataFrame...")
    df_full = dataset.to_pandas()
    
    print("Filtering rows where city_id == 4...")
    df_target = df_full[df_full['city_id'] == 4].copy()
    
    row_count = len(df_target)
    print(f"\nExtracted {row_count} rows for city_id=4.")
    
    output_path = '/workspace/demand_imputation/train_city4_100k.csv'
    print(f"Saving to {output_path} ...")
    df_target.to_csv(output_path, index=False)
    
    print("Done! CSV file saved successfully.")

if __name__ == "__main__":
    main()
