import pandas as pd
import numpy as np

def main():
    print("Step 2: Imputing B-class data using A-class profiles...")
    
    # Load original data and profiles
    df = pd.read_csv('/workspace/demand_imputation/train_city4_100k.csv')
    profiles_df = pd.read_csv('/workspace/demand_imputation/task7_hierarchical_imputation/a_class_profiles.csv')
    
    # Convert profiles to a dictionary for fast O(1) lookup
    # dict format: { product_id: [ratio_6, ratio_7, ..., ratio_21] }
    profiles_dict = {}
    for _, row in profiles_df.iterrows():
        ratios = [row[f'ratio_hour_{i}'] for i in range(6, 22)]
        profiles_dict[row['product_id']] = np.array(ratios)
        
    # We will create new columns for the imputed results
    # To keep track of what was imputed:
    imputed_sale_amounts = []
    is_imputed_flags = []
    
    # Global fallback profile (average of all A-class) just in case a product has NO A-class data
    global_fallback_profile = np.ones(16) / 16.0
    
    count_imputed = 0
    count_fallback = 0
    
    for i, row in df.iterrows():
        # Identify if it's B-class (missing 1-2 hours -> stock_hour6_22_cnt is 14 or 15)
        cnt = row['stock_hour6_22_cnt']
        
        if cnt in [14, 15]:
            # It's B-class, we need to impute!
            product_id = row['product_id']
            actual_sales_total = row['sale_amount']
            
            # Get the standard profile for this product
            if product_id in profiles_dict:
                profile = profiles_dict[product_id]
            else:
                profile = global_fallback_profile
                count_fallback += 1
                
            # Parse the stock array to find WHICH hours are missing
            stock_arr_str = row['hours_stock_status'].replace('[', '').replace(']', '').strip()
            stock_arr = np.fromstring(stock_arr_str, sep=' ')
            stock_6_22 = stock_arr[6:22] # 1 means in-stock, 0 means out-of-stock
            
            # Calculate Missing_Ratio and Normal_Ratio based on the profile
            # Normal_Ratio is the sum of profile ratios where stock is 1
            # Missing_Ratio is the sum of profile ratios where stock is 0
            normal_ratio = np.sum(profile[stock_6_22 == 1])
            missing_ratio = np.sum(profile[stock_6_22 == 0])
            
            # If normal_ratio is 0 (extremely rare edge case where standard profile says 
            # this product ONLY sells in the missing hours), we can't divide by zero.
            if normal_ratio <= 0.0001:
                # Fallback: Just scale proportionally by time
                missing_hours = 16 - cnt
                estimated_missing_sales = actual_sales_total * (missing_hours / float(cnt))
            else:
                # The core formula: Actual_Sales * (Missing_Ratio / Normal_Ratio)
                estimated_missing_sales = actual_sales_total * (missing_ratio / normal_ratio)
                
            new_total_sales = actual_sales_total + estimated_missing_sales
            
            imputed_sale_amounts.append(new_total_sales)
            is_imputed_flags.append(1) # 1 means it was imputed
            count_imputed += 1
            
        else:
            # Not B-class (could be A, C, D, etc.), leave it untouched for now
            imputed_sale_amounts.append(row['sale_amount'])
            is_imputed_flags.append(0)
            
    # Add the new columns to the dataframe
    df['imputed_sale_amount'] = imputed_sale_amounts
    df['is_imputed_b_class'] = is_imputed_flags
    
    # Save the new dataframe
    output_path = '/workspace/demand_imputation/task7_hierarchical_imputation/train_city4_imputed_B.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\nImputation Complete!")
    print(f"Successfully imputed {count_imputed} B-class rows.")
    if count_fallback > 0:
        print(f"Used global fallback profile for {count_fallback} rows (product had no A-class data).")
        
    print(f"Saved new dataset to: {output_path}")
    
    # Display a small comparison
    print("\nSample of Imputed B-class rows (Original vs Imputed Sales):")
    b_imputed_df = df[df['is_imputed_b_class'] == 1][['product_id', 'stock_hour6_22_cnt', 'sale_amount', 'imputed_sale_amount']]
    print(b_imputed_df.head(10).to_string(index=False))

if __name__ == "__main__":
    main()
