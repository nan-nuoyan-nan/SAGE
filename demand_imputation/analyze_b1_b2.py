import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
    print("Loading data...")
    df = pd.read_csv('/workspace/group4_dataset/train_group4.csv')
    
    # We need to determine b_1 and b_2 categories based on user's definition.
    # B category: missing 1 to 2 hours (i.e. stock_hour6_22_cnt is 14 or 15).
    # b_1: missing 1-2 hours AND the missing hours include the last 2 hours of A's average sales.
    # To simplify and implement the core idea, we assume the last 2 hours of the 16-hour window 
    # (which are 20:00-21:00 and 21:00-22:00) are the "end of the day".
    # Let's extract the stock array to check exactly which hours are missing.
    
    b_1_counts = []
    b_2_counts = []
    cities = []
    
    # Group by city_id
    city_groups = df.groupby('city_id')
    
    for city_id, group in city_groups:
        cities.append(city_id)
        
        b1 = 0
        b2 = 0
        
        for _, row in group.iterrows():
            cnt = row['stock_hour6_22_cnt']
            if cnt == 14 or cnt == 15:
                # It belongs to B category. Now distinguish b_1 and b_2.
                # Extract the stock array
                arr_str = row['hours_stock_status'][1:-1] # Remove brackets
                arr = np.fromstring(arr_str, sep=' ')
                
                # The 6:00 to 22:00 window is indices 6 to 21 (inclusive).
                # The "last two hours" of this window are indices 20 and 21 (i.e. 20:00 and 21:00).
                # If either of these two hours is out of stock (value == 0), we classify it as b_1.
                # Otherwise, it's b_2.
                if arr[20] == 0 or arr[21] == 0:
                    b1 += 1
                else:
                    b2 += 1
                    
        b_1_counts.append(b1)
        b_2_counts.append(b2)
        
    # Create a summary dataframe
    stats_df = pd.DataFrame({
        'city_id': cities,
        'b_1_count': b_1_counts,
        'b_2_count': b_2_counts
    })
    
    # Sort by the sum of b1 and b2 to make the plot look organized (Pareto style)
    stats_df['total_b'] = stats_df['b_1_count'] + stats_df['b_2_count']
    stats_df = stats_df.sort_values(by='total_b', ascending=False).reset_index(drop=True)
    
    # Save the stats to CSV
    csv_path = '/workspace/demand_imputation/city_b1_b2_stats.csv'
    stats_df.to_csv(csv_path, index=False)
    print("\nStats for b_1 and b_2 categories:")
    print(stats_df.to_string(index=False))
    
    # Plotting
    plt.figure(figsize=(10, 6))
    
    x = range(len(stats_df))
    plt.plot(x, stats_df['b_1_count'], label='b_1 (Missing 1-2h, includes end of day)', color='orange', marker='o', markersize=6, linewidth=2)
    plt.plot(x, stats_df['b_2_count'], label='b_2 (Missing 1-2h, does NOT include end of day)', color='purple', marker='s', markersize=6, linewidth=2)
    
    # Add text annotations for b_1
    y_offset = stats_df['total_b'].max() * 0.03
    for i, count in enumerate(stats_df['b_1_count']):
        plt.text(i, count + y_offset, str(count), ha='center', va='bottom', fontsize=9, color='orange', fontweight='bold')
        
    # Add text annotations for b_2
    for i, count in enumerate(stats_df['b_2_count']):
        plt.text(i, count - y_offset * 1.5, str(count), ha='center', va='top', fontsize=9, color='purple', fontweight='bold')

    plt.title('Comparison of b_1 and b_2 Category Rows by City')
    plt.xlabel('City Rank (by total B category rows)')
    plt.ylabel('Number of Rows')
    
    plt.xticks(x, stats_df['city_id'])
    plt.xlim(-0.5, len(stats_df) - 0.5)
    
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plot_path = '/workspace/demand_imputation/city_b1_b2_comparison.png'
    plt.savefig(plot_path)
    
    print(f"\nSaved CSV to: {csv_path}")
    print(f"Saved Chart to: {plot_path}")

if __name__ == '__main__':
    main()
