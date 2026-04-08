import pandas as pd
import matplotlib.pyplot as plt

def main():
    print("【任务3】分析 C 类数据的日期 (dt) 特征，并绘制散点图")
    
    # 1. 加载 10 万行数据集
    df = pd.read_csv('/workspace/demand_imputation/train_city4_100k.csv')
    df.drop(columns=['city_id'], inplace=True, errors='ignore')
    
    # 2. 提取 C 类数据 (缺货 3-4 小时)
    df_c = df[df['stock_hour6_22_cnt'].isin([12, 13])].copy()
    
    # 3. 统计每天发生 C 类缺货的次数
    # dt 格式通常为类似 '2023-01-01' 的日期字符串
    daily_c_counts = df_c['dt'].value_counts().sort_index()
    
    # 为了方便绘图，我们将日期转换为数字序列 (第几天)
    x_days = range(len(daily_c_counts))
    y_counts = daily_c_counts.values
    dates = daily_c_counts.index
    
    # 4. 绘制散点图
    plt.figure(figsize=(14, 6))

    # 散点图，观察缺货事件是否呈现聚集性或周期性
    plt.scatter(x_days, y_counts, color='teal', alpha=0.7, s=60, edgecolors='k')

    # 添加一条均值参考线
    mean_count = y_counts.mean()
    plt.axhline(mean_count, color='red', linestyle='--', alpha=0.8, label=f'Mean C-class out-of-stock per day ({mean_count:.1f})')

    plt.title('Daily C-Class Out-of-Stock Events Scatter Plot', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Daily C-Class Out-of-Stock Count', fontsize=12)
    
    # 设置 x 轴刻度，为避免重叠，每隔 5 天显示一次日期
    step = max(1, len(x_days) // 20)
    plt.xticks(x_days[::step], dates[::step], rotation=45, fontsize=9)
    
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    
    # 保存图片
    output_path = '/workspace/demand_imputation/task8_c_class_deep_analysis/c_class_daily_scatter.png'
    plt.savefig(output_path)
    
    print(f"\n【完成】日期分布散点图已保存至：{output_path}")

if __name__ == "__main__":
    main()
