import pandas as pd
import matplotlib.pyplot as plt

# 读取刚才已经生成的 CSV 文件
df = pd.read_csv('/workspace/fresh_retail_dataset_tools/fresh_retail_train_df.csv')

# 确保按数据量从大到小排序，或者按城市ID排序。为了折线图的连贯性，我们按城市ID排序
df = df.sort_values(by='city_id')

plt.figure(figsize=(12, 6))

# 绘制折线图
plt.plot(df['city_id'].astype(str), df['count'], marker='o', linestyle='-', linewidth=2, color='coral')

# 在点上标注具体的数值
for i, txt in enumerate(df['count']):
    plt.annotate(f'{txt:,}', (df['city_id'].astype(str).iloc[i], df['count'].iloc[i]),
                 textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

plt.title('Train Data Volume by City (Line Chart)', fontsize=14)
plt.xlabel('City ID', fontsize=12)
plt.ylabel('Number of Records', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# 保存折线图
plt.savefig('/workspace/demand_imputation/train_city_distribution_line_chart.png', dpi=300)
print("Saved Line Chart to /workspace/demand_imputation/train_city_distribution_line_chart.png")
