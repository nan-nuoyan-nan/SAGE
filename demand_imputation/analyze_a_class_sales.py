import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("Loading data...")
    df = pd.read_csv('/workspace/group4_dataset/train_group4.csv')
    
    # Extract A-class data (no stockout all 16 hours)
    a_class = df[df['stock_hour6_22_cnt'] == 16].copy()
    print(f"Total A-class rows found: {len(a_class)}")
    
    # Store results
    city_hourly_avg = []
    
    # Iterate over each city in A-class data
    for city_id, group in a_class.groupby('city_id'):
        # We need to accumulate sales for each hour (6:00 to 22:00 -> index 6 to 21)
        # Initialize an array of 16 zeros
        hourly_sales_sum = np.zeros(16)
        
        for _, row in group.iterrows():
            # hours_sale format is a string representation of an array, e.g., "[0. 0. 0. ...]"
            # remove brackets and convert to numpy array
            sales_arr_str = row['hours_sale'].replace('[', '').replace(']', '').strip()
            sales_arr = np.fromstring(sales_arr_str, sep=' ')
            
            # The sales array is 24 hours, we only care about 6:00 to 22:00 (index 6 to 21 inclusive)
            hourly_sales_sum += sales_arr[6:22]
            
        # Calculate average for this city
        hourly_sales_avg = hourly_sales_sum / len(group)
        
        # Append to our results
        for hour_idx in range(16):
            actual_hour = hour_idx + 6  # 0 corresponds to 6:00
            city_hourly_avg.append({
                'city_id': city_id,
                'hour': f"{actual_hour}:00",
                'avg_sale': hourly_sales_avg[hour_idx]
            })
            
    results_df = pd.DataFrame(city_hourly_avg)
    
    # Sort and create rankings for each city
    results_df = results_df.sort_values(by=['city_id', 'avg_sale'], ascending=[True, False])
    results_df['rank'] = results_df.groupby('city_id')['avg_sale'].rank(method='min', ascending=False).astype(int)
    
    # Save results to CSV
    csv_path = '/workspace/demand_imputation/a_class_hourly_avg_sales.csv'
    results_df.to_csv(csv_path, index=False)
    
    print("\nTop 3 hours with highest average sales for each city (A-class only):")
    # Group by city and print the top 3
    for city_id, group in results_df.groupby('city_id'):
        print(f"\n--- City {city_id} ---")
        top_3 = group.head(3)
        for _, row in top_3.iterrows():
            print(f"Rank {row['rank']}: {row['hour']} -> {row['avg_sale']:.4f} average sales")
            
    print(f"\nFull ranking saved to: {csv_path}")

if __name__ == '__main__':
    main()
