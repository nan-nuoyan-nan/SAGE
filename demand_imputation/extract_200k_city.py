import pandas as pd
from datasets import load_dataset

def main():
    print("Loading full dataset directly from HuggingFace to find cities ~200k rows...")
    # Load just the city_id column to save memory
    dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K", split='train')
    df_city = dataset.select_columns(['city_id']).to_pandas()
    
    city_counts = df_city['city_id'].value_counts()
    print('\nTop cities by total rows:')
    print(city_counts.head(10))
    
    # Target: ~200k rows (between 150k and 250k)
    target_cities = city_counts[(city_counts >= 150000) & (city_counts <= 250000)]
    print('\nCities with row count around 200,000 (between 150k and 250k):')
    print(target_cities)
    
    if not target_cities.empty:
        # Pick the one closest to 200,000
        best_city = (target_cities - 200000).abs().idxmin()
        best_count = target_cities[best_city]
        print(f"\nBest city selected: city_id={best_city} with {best_count} rows.")
        
        # Now extract full data for this city
        print(f"Extracting full data for city {best_city}...")
        df_full = dataset.to_pandas()
        df_target = df_full[df_full['city_id'] == best_city].copy()
        
        output_path = f'/workspace/demand_imputation/train_city{best_city}_200k.csv'
        df_target.to_csv(output_path, index=False)
        print(f"Saved target dataset to {output_path}")
    else:
        print("\nNo city found in the 150k-250k range. Let's find the closest one to 200k globally.")
        best_city = (city_counts - 200000).abs().idxmin()
        best_count = city_counts[best_city]
        print(f"Closest city is city_id={best_city} with {best_count} rows.")
        
        print(f"Extracting full data for city {best_city}...")
        df_full = dataset.to_pandas()
        df_target = df_full[df_full['city_id'] == best_city].copy()
        
        output_path = f'/workspace/demand_imputation/train_city{best_city}_{best_count//1000}k.csv'
        df_target.to_csv(output_path, index=False)
        print(f"Saved target dataset to {output_path}")

if __name__ == "__main__":
    main()
