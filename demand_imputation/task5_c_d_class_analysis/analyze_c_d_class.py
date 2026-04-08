import pandas as pd
import matplotlib.pyplot as plt

def main():
    print("Loading data...")
    df = pd.read_csv('/workspace/group4_dataset/train_group4.csv')
    
    # Definitions:
    # Total hours in 6:00-22:00 window is 16.
    # C-class: Missing 3 or 4 hours (stock_hour6_22_cnt is 12 or 13)
    # D-class: Missing 5 or 6 hours (stock_hour6_22_cnt is 10 or 11)
    
    df['is_c_class'] = df['stock_hour6_22_cnt'].isin([12, 13])
    df['is_d_class'] = df['stock_hour6_22_cnt'].isin([10, 11])
    
    # Group by city_id to get total rows and class rows
    city_stats = df.groupby('city_id').agg(
        total_rows=('city_id', 'count'),
        c_class_rows=('is_c_class', 'sum'),
        d_class_rows=('is_d_class', 'sum')
    ).reset_index()
    
    # Calculate ratios
    city_stats['c_class_ratio'] = city_stats['c_class_rows'] / city_stats['total_rows']
    city_stats['d_class_ratio'] = city_stats['d_class_rows'] / city_stats['total_rows']
    
    # Sort by total c_class_rows descending
    city_stats = city_stats.sort_values(by='c_class_rows', ascending=False).reset_index(drop=True)
    
    # Save to CSV
    csv_path = '/workspace/demand_imputation/task5_c_d_class_analysis/c_d_class_stats.csv'
    city_stats.to_csv(csv_path, index=False)
    
    print("\nStats for C-class (Missing 3-4h) and D-class (Missing 5-6h) by City:")
    print(city_stats.to_string(index=False))
    
    # Plotting C and D class counts on the same chart
    plt.figure(figsize=(10, 6))
    
    x = range(len(city_stats))
    
    # Plot C-class
    plt.plot(x, city_stats['c_class_rows'], label='C-class Rows (Missing 3-4h)', color='red', marker='o', markersize=6, linewidth=2)
    
    # Plot D-class
    plt.plot(x, city_stats['d_class_rows'], label='D-class Rows (Missing 5-6h)', color='brown', marker='s', markersize=6, linewidth=2)
    
    # Add text annotations for C-class data
    y_offset_c = city_stats['c_class_rows'].max() * 0.03
    for i, count in enumerate(city_stats['c_class_rows']):
        count = int(count)
        plt.text(i, count + y_offset_c, str(count), ha='center', va='bottom', fontsize=9, color='red', fontweight='bold')

    # Add text annotations for D-class data
    y_offset_d = city_stats['d_class_rows'].max() * 0.03
    for i, count in enumerate(city_stats['d_class_rows']):
        count = int(count)
        plt.text(i, count - y_offset_d * 1.5, str(count), ha='center', va='top', fontsize=9, color='brown', fontweight='bold')

    plt.title('C-class and D-class Rows Distribution by City')
    plt.xlabel('City Rank (by C-class rows count)')
    plt.ylabel('Number of Rows')
    
    plt.xticks(x, city_stats['city_id'])
    
    # Adjust y-limit to make room for text at the top and bottom
    plt.ylim(-city_stats['d_class_rows'].max() * 0.1, city_stats['c_class_rows'].max() * 1.15)
    
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plot_path = '/workspace/demand_imputation/task5_c_d_class_analysis/c_d_class_distribution.png'
    plt.savefig(plot_path)
    
    print(f"\nSaved CSV to: {csv_path}")
    print(f"Saved Chart to: {plot_path}")

if __name__ == '__main__':
    main()
