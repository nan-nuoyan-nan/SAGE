import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    print("Loading 200k subset data (city_id=13)...")
    df = pd.read_csv('/workspace/demand_imputation/train_city13_200k.csv')
    
    # Map each row to its class based on stock_hour6_22_cnt
    def get_class(cnt):
        if cnt == 16: return 'A (0h)'
        elif cnt in [14, 15]: return 'B (1-2h)'
        elif cnt in [12, 13]: return 'C (3-4h)'
        elif cnt in [10, 11]: return 'D (5-6h)'
        elif cnt in [8, 9]: return 'E (7-8h)'
        elif cnt in [6, 7]: return 'F (9-10h)'
        elif cnt in [4, 5]: return 'G (11-12h)'
        else: return 'H (>=13h)'
        
    df['stock_class'] = df['stock_hour6_22_cnt'].apply(get_class)
    
    # Group by stock_class and product_id to count rows
    class_product_counts = df.groupby(['stock_class', 'product_id']).size().unstack(fill_value=0)
    
    # Reorder columns (product_id) by total count to make the plot look organized
    product_totals = class_product_counts.sum(axis=0).sort_values(ascending=False)
    class_product_counts = class_product_counts[product_totals.index]
    
    # Reorder rows to match A to H
    class_order = ['A (0h)', 'B (1-2h)', 'C (3-4h)', 'D (5-6h)', 'E (7-8h)', 'F (9-10h)', 'G (11-12h)', 'H (>=13h)']
    class_product_counts = class_product_counts.reindex(class_order)
    
    # Save the cross-tabulation to CSV
    csv_path = '/workspace/demand_imputation/task6_abcde_analysis/class_product_distribution.csv'
    class_product_counts.to_csv(csv_path)
    print(f"\nSaved cross-tabulation of Classes vs Products to {csv_path}")
    
    # We will draw a Stacked Bar Chart where x-axis is Class, and bars are stacked by Product ID.
    # But since there might be many products, a heatmap is usually better for visualizing relationships 
    # between two categorical variables with counts.
    # Let's draw a Heatmap for clear relationships!
    
    plt.figure(figsize=(16, 8))
    # Use log scale for colors if values vary too much, but let's try standard first
    sns.heatmap(class_product_counts, cmap='YlOrRd', annot=False, fmt="d", linewidths=.5)
    
    plt.title('Relationship between Stock Missing Classes (A-H) and Product IDs in City 13', fontsize=14)
    plt.xlabel('Product ID (Sorted by total data count)', fontsize=12)
    plt.ylabel('Missing Hours Class', fontsize=12)
    
    plt.tight_layout()
    
    plot_path = '/workspace/demand_imputation/task6_abcde_analysis/class_product_heatmap.png'
    plt.savefig(plot_path)
    
    print(f"Saved Relationship Heatmap to: {plot_path}")
    
    # Let's also draw a stacked bar chart for a different perspective
    ax = class_product_counts.plot(kind='bar', stacked=True, figsize=(14, 8), colormap='tab20')
    plt.title('Stacked Bar Chart of Product IDs across Classes (A-H)', fontsize=14)
    plt.xlabel('Missing Hours Class', fontsize=12)
    plt.ylabel('Number of Rows', fontsize=12)
    # Move legend outside
    plt.legend(title='Product ID', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small', ncol=2)
    plt.tight_layout()
    
    stacked_path = '/workspace/demand_imputation/task6_abcde_analysis/class_product_stacked_bar.png'
    plt.savefig(stacked_path)
    print(f"Saved Stacked Bar Chart to: {stacked_path}")

if __name__ == '__main__':
    main()
