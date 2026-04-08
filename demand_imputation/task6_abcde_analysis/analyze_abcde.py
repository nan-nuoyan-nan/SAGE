import pandas as pd
import matplotlib.pyplot as plt

def main():
    print("Loading 100k subset data (city_id=4)...")
    df = pd.read_csv('/workspace/demand_imputation/train_city4_100k.csv')
    
    print(f"Total rows loaded: {len(df)}")
    
    # We only have one city here (city_id=13), but let's count the classes
    # Total hours in 6:00-22:00 window is 16.
    
    # Class definitions:
    # A-class: Missing 0 hours (stock_hour6_22_cnt == 16)
    # B-class: Missing 1 or 2 hours (stock_hour6_22_cnt is 14 or 15)
    # C-class: Missing 3 or 4 hours (stock_hour6_22_cnt is 12 or 13)
    # D-class: Missing 5 or 6 hours (stock_hour6_22_cnt is 10 or 11)
    # E-class: Missing 7 or 8 hours (stock_hour6_22_cnt is 8 or 9)
    # F-class: Missing 9 or 10 hours (stock_hour6_22_cnt is 6 or 7)
    # G-class: Missing 11 or 12 hours (stock_hour6_22_cnt is 4 or 5)
    # H-class: Missing 13 or more hours (stock_hour6_22_cnt <= 3)
    
    a_count = len(df[df['stock_hour6_22_cnt'] == 16])
    b_count = len(df[df['stock_hour6_22_cnt'].isin([14, 15])])
    c_count = len(df[df['stock_hour6_22_cnt'].isin([12, 13])])
    d_count = len(df[df['stock_hour6_22_cnt'].isin([10, 11])])
    e_count = len(df[df['stock_hour6_22_cnt'].isin([8, 9])])
    f_count = len(df[df['stock_hour6_22_cnt'].isin([6, 7])])
    g_count = len(df[df['stock_hour6_22_cnt'].isin([4, 5])])
    h_count = len(df[df['stock_hour6_22_cnt'] <= 3])
    
    total = len(df)
    
    stats = pd.DataFrame({
        'Class': ['A (0h)', 'B (1-2h)', 'C (3-4h)', 'D (5-6h)', 'E (7-8h)', 'F (9-10h)', 'G (11-12h)', 'H (>=13h)'],
        'Count': [a_count, b_count, c_count, d_count, e_count, f_count, g_count, h_count],
        'Ratio': [a_count/total, b_count/total, c_count/total, d_count/total, e_count/total, f_count/total, g_count/total, h_count/total]
    })
    
    csv_path = '/workspace/demand_imputation/task6_abcde_analysis/a_to_h_stats_city4.csv'
    stats.to_csv(csv_path, index=False)
    
    print("\nStats for A to H Classes in City 4:")
    print(stats.to_string(index=False))
    
    # Plotting
    plt.figure(figsize=(14, 6))
    
    # Bar chart is better here since we are showing categories for a single city
    colors = ['green', 'purple', 'red', 'brown', 'orange', 'cyan', 'magenta', 'gray']
    bars = plt.bar(stats['Class'], stats['Count'], color=colors)
    
    # Add text on top of bars
    for bar, ratio in zip(bars, stats['Ratio']):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f"{int(yval)}\n({ratio*100:.2f}%)", 
                 ha='center', va='bottom', fontweight='bold')
        
    plt.title(f'A to H Class Distribution for City 4 (Total Rows: {total})')
    plt.xlabel('Missing Hours Category')
    plt.ylabel('Number of Rows')
    
    # Add some headroom for the text
    plt.ylim(0, stats['Count'].max() * 1.15)
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plot_path = '/workspace/demand_imputation/task6_abcde_analysis/a_to_h_distribution_city4.png'
    plt.savefig(plot_path)
    
    print(f"\nSaved CSV to: {csv_path}")
    print(f"Saved Chart to: {plot_path}")

if __name__ == '__main__':
    main()
