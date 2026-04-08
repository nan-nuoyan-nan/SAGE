import pandas as pd
import matplotlib.pyplot as plt

# 读取之前的数据
df = pd.read_csv('/workspace/demand_imputation/train_city_distribution.csv')

# 关键修复：按照数据量（count）从大到小排序，而不是按 city_id 排序！
# 这样画出来的折线图才是一条平滑的“长尾分布”曲线（帕累托图），而不是上下乱跳的锯齿。
df = df.sort_values(by='count', ascending=False)

plt.figure(figsize=(14, 6))

# 绘制折线图
plt.plot(df['city_id'].astype(str), df['count'], marker='o', linestyle='-', linewidth=2.5, color='coral')

# 添加数值标注
for i in range(len(df)):
    plt.annotate(f"{df['count'].iloc[i]:,}", 
                 (df['city_id'].astype(str).iloc[i], df['count'].iloc[i]),
                 textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, rotation=0)

plt.title('Train Data Volume by City (Sorted by Data Volume)', fontsize=15, fontweight='bold')
plt.xlabel('City ID (Sorted from Largest to Smallest)', fontsize=12)
plt.ylabel('Number of Records', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)

# 留出顶部空间给标签
plt.ylim(0, df['count'].max() * 1.15)
plt.tight_layout()

# 保存正确的折线图
save_path = '/workspace/demand_imputation/train_city_distribution_line_chart_sorted.png'
plt.savefig(save_path, dpi=300)
print(f"Perfect sorted line chart saved to {save_path}")

