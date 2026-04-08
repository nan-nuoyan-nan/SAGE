import pandas as pd
import matplotlib.pyplot as plt

def main():
    print("【任务2】分析 C 类数据的四级分类 ID 分布，并绘制折线图")
    
    # 1. 加载 10 万行数据集 (删除无用的 city_id)
    df = pd.read_csv('/workspace/demand_imputation/train_city4_100k.csv')
    df.drop(columns=['city_id'], inplace=True, errors='ignore')
    
    # 2. 提取 C 类数据 (缺货 3-4 小时)
    df_c = df[df['stock_hour6_22_cnt'].isin([12, 13])].copy()
    
    # 3. 统计4级分类(product_id)的分布
    counts = df_c['product_id'].value_counts().sort_values(ascending=False).head(50)

    # 4. 绘制折线图
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(counts)), counts.values, marker='o', linestyle='-', markersize=4)
    plt.title('Product ID Distribution in C Class (Top 50)', fontsize=14)
    plt.xlabel('Product ID', fontsize=12)
    plt.ylabel('Out of Stock Count', fontsize=12)
    plt.xticks(range(len(counts)), counts.index, rotation=90, fontsize=8)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    # 保存图片
    output_path = '/workspace/demand_imputation/task8_c_class_deep_analysis/c_class_category_distribution.png'
    plt.savefig(output_path)
    
    print(f"\n【完成】4 级分类 ID 分布折线图已保存至：{output_path}")

if __name__ == "__main__":
    main()
