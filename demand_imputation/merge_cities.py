import pandas as pd

def main():
    print("【开始合并城市数据】...")
    
    # 1. 加载包含城市 5, 15, 11 的数据集
    print("正在加载城市 5, 15, 11 的数据...")
    df_5_15_11 = pd.read_csv('/workspace/demand_imputation/train_cities_5_15_11.csv')
    print(f"数据量: {len(df_5_15_11)} 行")
    
    # 2. 加载包含城市 4 的数据集
    print("正在加载城市 4 的数据...")
    df_4 = pd.read_csv('/workspace/demand_imputation/train_city4_100k.csv')
    print(f"数据量: {len(df_4)} 行")
    
    # 3. 纵向合并数据
    print("正在合并数据...")
    df_combined = pd.concat([df_4, df_5_15_11], ignore_index=True)

    
    print("\n--- 合并完成 ---")
    print(f"合并后的总行数: {len(df_combined)}")
    print("\n各城市行数统计:")
    print(df_combined['city_id'].value_counts())
    
    # 4. 保存为新的 CSV
    output_path = '/workspace/demand_imputation/train_cities_4_5_11_15.csv'
    print(f"\n正在保存合并后的 CSV 文件: {output_path} ...")
    df_combined.to_csv(output_path, index=False)
    
    print("完成！数据已保存。")

if __name__ == "__main__":
    main()
