import pandas as pd
import matplotlib.pyplot as plt

def main():
    print("Loading data...")
    df = pd.read_csv('/workspace/group4_dataset/train_group4.csv')
    
    # B-class definition: Missing 1 or 2 hours in the 6:00-22:00 window.
    # The total hours in this window is 16. 
    # So missing 1 or 2 hours means stock_hour6_22_cnt is 14 or 15.
    df['is_b_class'] = df['stock_hour6_22_cnt'].isin([14, 15])
    
    # Group by city_id to get total rows and B-class rows
    city_stats = df.groupby('city_id').agg(
        total_rows=('city_id', 'count'),
        b_class_rows=('is_b_class', 'sum')
    ).reset_index()
    
    # Calculate ratio of B-class data
    city_stats['b_class_ratio'] = city_stats['b_class_rows'] / city_stats['total_rows']
    
    # Sort by b_class_rows descending
    city_stats = city_stats.sort_values(by='b_class_rows', ascending=False).reset_index(drop=True)
    
    # Save to CSV
    csv_path = '/workspace/demand_imputation/task4_b_class_analysis/b_class_stats.csv'
    city_stats.to_csv(csv_path, index=False)
    
    print("\nStats for B-class (Missing 1-2 hours) by City:")
    print(city_stats.to_string(index=False))
    
    # Plotting the B-class counts
    plt.figure(figsize=(10, 6))
    
    x = range(len(city_stats))
    plt.plot(x, city_stats['b_class_rows'], label='B-class Rows (Missing 1-2 hours)', color='purple', marker='o', markersize=6, linewidth=2)
    
    # Add text annotations for B-class data
    y_offset = city_stats['b_class_rows'].max() * 0.03
    for i, (idx, row) in enumerate(city_stats.iterrows()):
        count = int(row['b_class_rows'])
        ratio = row['b_class_ratio'] * 100
        text_str = f"{count}\n({ratio:.2f}%)"
        plt.text(i, count + y_offset, text_str, ha='center', va='bottom', fontsize=9, color='purple', fontweight='bold')

    plt.title('B-class Rows (Missing 1-2 hours) Distribution by City')
    plt.xlabel('City Rank (by B-class rows count)')
    plt.ylabel('Number of B-class Rows')
    
    plt.xticks(x, city_stats['city_id'])
    
    # Adjust y-limit to make room for text at the top
    plt.ylim(0, city_stats['b_class_rows'].max() * 1.15)
    
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plot_path = '/workspace/demand_imputation/task4_b_class_analysis/b_class_distribution.png'
    plt.savefig(plot_path)
    
    print(f"\nSaved CSV to: {csv_path}")
    print(f"Saved Chart to: {plot_path}")

if __name__ == '__main__':
    main()
