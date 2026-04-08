import pandas as pd
import numpy as np

def main():
    print("Step 1: Building A-class standard profiles (Sales Ratio Distribution)...")
    
    # 1. Load the 100k subset data (city_id=4)
    df = pd.read_csv('/workspace/demand_imputation/train_city4_100k.csv')
    
    # 2. Extract A-class data (0 hours missing in 6:00-22:00)
    # This means stock_hour6_22_cnt == 16
    df_a = df[df['stock_hour6_22_cnt'] == 16].copy()
    print(f"Extracted {len(df_a)} A-class rows.")
    
    # We will build profiles based on product_id
    # (Since we are already filtering by city_id=4, no need to group by city_id)
    
    profiles = []
    
    # Group by product_id
    for product_id, group in df_a.groupby('product_id'):
        
        # Accumulate sales for each of the 16 hours (index 6 to 21)
        total_sales_arr = np.zeros(16)
        
        for _, row in group.iterrows():
            # Convert string array to numpy array
            arr_str = row['hours_sale'].replace('[', '').replace(']', '').strip()
            arr = np.fromstring(arr_str, sep=' ')
            
            # Extract 6:00 to 22:00 (16 hours)
            sales_6_to_22 = arr[6:22]
            total_sales_arr += sales_6_to_22
            
        # Calculate the ratio for each hour
        sum_sales = total_sales_arr.sum()
        
        if sum_sales > 0:
            ratio_arr = total_sales_arr / sum_sales
        else:
            # If a product in A-class somehow has 0 total sales all day, we give it a uniform distribution
            ratio_arr = np.ones(16) / 16.0
            
        # Store the profile
        profile_row = {'product_id': product_id, 'a_class_sample_count': len(group)}
        
        for i in range(16):
            hour_label = f'ratio_hour_{i+6}'
            profile_row[hour_label] = ratio_arr[i]
            
        profiles.append(profile_row)
        
    profile_df = pd.DataFrame(profiles)
    
    output_path = '/workspace/demand_imputation/task7_hierarchical_imputation/a_class_profiles.csv'
    profile_df.to_csv(output_path, index=False)
    
    print("\nA-class Profiles (Sales Ratio per hour) successfully built!")
    print(f"Total unique products profiled: {len(profile_df)}")
    print(f"Saved to: {output_path}")
    
    print("\nSample profile (first 2 products):")
    print(profile_df.head(2).to_string())

if __name__ == "__main__":
    main()
