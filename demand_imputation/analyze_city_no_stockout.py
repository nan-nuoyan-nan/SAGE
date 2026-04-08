import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Load dataset
    df = pd.read_csv('/workspace/group4_dataset/train_group4.csv')
    
    # "没缺货" means stock is available all 16 hours (from hour 6 to hour 22)
    # stock_hour6_22_cnt counts how many hours have stock.
    # So max is 16. We define "a级" (no stockout) as stock_hour6_22_cnt == 16
    df['is_a_class'] = (df['stock_hour6_22_cnt'] == 16)
    
    # Group by city_id
    city_stats = df.groupby('city_id').agg(
        total_rows=('city_id', 'count'),
        no_stockout_rows=('is_a_class', 'sum')
    ).reset_index()
    
    city_stats['no_stockout_ratio'] = city_stats['no_stockout_rows'] / city_stats['total_rows']
    
    # Sort by total_rows descending (as we did in the previous plot)
    city_stats = city_stats.sort_values(by='total_rows', ascending=False)
    
    # Save the results
    output_csv = '/workspace/demand_imputation/city_no_stockout_stats.csv'
    city_stats.to_csv(output_csv, index=False)
    
    print("各城市“没缺货（A类）”数据统计：")
    print(city_stats.to_string(index=False))
    
    # Let's also plot this as a line chart to visualize
    plt.figure(figsize=(12, 6))
    
    # Plot total rows
    plt.plot(range(len(city_stats)), city_stats['total_rows'], label='Total Rows', color='blue', marker='o', markersize=4)
    
    # Plot no stockout rows
    plt.plot(range(len(city_stats)), city_stats['no_stockout_rows'], label='No Stockout (A-class) Rows', color='green', marker='s', markersize=4)
    
    plt.title('City Data Distribution & No-Stockout (A-class) Rows (Sorted by Total Count)')
    plt.xlabel('City Rank (by total rows)')
    plt.ylabel('Number of Rows')
    
    # Use city_id as x-ticks (show top 20 to avoid clutter)
    plt.xticks(range(len(city_stats)), city_stats['city_id'], rotation=90)
    plt.xlim(-1, min(50, len(city_stats))) # Just show first 50 cities on x-axis to keep it readable
    
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    output_png = '/workspace/demand_imputation/city_no_stockout_line_chart.png'
    plt.savefig(output_png)
    print(f"\nSaved CSV to: {output_csv}")
    print(f"Saved Chart to: {output_png}")

if __name__ == '__main__':
    main()
