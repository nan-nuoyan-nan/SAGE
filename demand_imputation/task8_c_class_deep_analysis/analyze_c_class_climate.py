import pandas as pd

def main():
    print("【任务1】分析 C 类数据（缺货 3-4 小时）的气候特征 (均值与方差)")
    
    # 1. 加载 10 万行数据集 (删除无用的 city_id 列)
    df = pd.read_csv('/workspace/demand_imputation/train_city4_100k.csv')
    df.drop(columns=['city_id'], inplace=True, errors='ignore')
    
    # 2. 提取 C 类数据 (stock_hour6_22_cnt == 12 或 13)
    df_c = df[df['stock_hour6_22_cnt'].isin([12, 13])].copy()
    print(f"成功提取 C 类数据：{len(df_c)} 行")
    
    # 3. 筛选出气候相关的特征列
    climate_features = ['precpt', 'avg_temperature', 'avg_humidity', 'avg_wind_level']
    
    # 4. 计算均值和方差
    # 注意：如果特征中有分类变量（如 weather_type 可能为数字编码），我们直接按数值计算作为统计参考
    mean_series = df_c[climate_features].mean()
    var_series = df_c[climate_features].var()
    
    # 将结果组合成一个 DataFrame 方便查看
    stats_df = pd.DataFrame({
        '均值 (Mean)': mean_series,
        '方差 (Variance)': var_series
    })
    
    print("\n--- C类数据气候特征统计 ---")
    print(stats_df.round(2).to_string())
    
    # 保存结果
    output_path = '/workspace/demand_imputation/task8_c_class_deep_analysis/c_class_climate_stats.csv'
    stats_df.to_csv(output_path)
    print(f"\n统计结果已保存至：{output_path}")

if __name__ == "__main__":
    main()
