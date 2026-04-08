import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def main():
    print("Loading data...")
    # Read the full dataframe (we will sample 100k rows if needed, or use the 50k dataset)
    df = pd.read_csv('/workspace/group4_dataset/train_group4.csv')
    
    # 7 ID features
    id_features = [
        'city_id',
        'store_id',
        'management_group_id',
        'first_category_id',
        'second_category_id',
        'third_category_id',
        'product_id'
    ]
    
    print("Computing correlation matrix...")
    corr_matrix = df[id_features].corr()
    
    # Extract pairs
    pairs = []
    for i in range(len(id_features)):
        for j in range(i + 1, len(id_features)):
            pairs.append({
                'Feature 1': id_features[i],
                'Feature 2': id_features[j],
                'Correlation': corr_matrix.iloc[i, j]
            })
            
    corr_df = pd.DataFrame(pairs)
    # Sort by absolute correlation
    corr_df['Abs_Corr'] = corr_df['Correlation'].abs()
    corr_df = corr_df.sort_values(by='Abs_Corr', ascending=False).reset_index(drop=True)
    
    print("Plotting line chart...")
    # Draw line chart instead of heatmap
    plt.figure(figsize=(12, 6))
    
    x_labels = [f"{row['Feature 1']}\n&\n{row['Feature 2']}" for _, row in corr_df.iterrows()]
    
    # We will plot the actual correlation (not absolute)
    plt.plot(range(len(corr_df)), corr_df['Correlation'], marker='o', linestyle='-', color='b')
    
    plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
    
    plt.title('Pearson Correlation Coefficient between 7 ID Features')
    plt.xlabel('Feature Pairs')
    plt.ylabel('Correlation Coefficient')
    
    plt.xticks(range(len(corr_df)), x_labels, rotation=90)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    
    output_path = '/workspace/id_correlation_line_chart_sorted.png'
    plt.savefig(output_path)
    print(f"Chart saved to {output_path}")

if __name__ == '__main__':
    main()
