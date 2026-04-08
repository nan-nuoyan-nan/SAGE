import pandas as pd
from datasets import load_dataset

def main():
    print("【开始提取最后四个城市（数据量最少的四个城市）的数据】...")
    
    # 1. 目标城市列表（根据刚才的统计结果）
    # 城市 ID 分别为：10 (32,850行), 17 (23,670行), 9 (17,730行), 8 (5,850行)
    target_cities = [10, 17, 9, 8]
    
    print(f"目标城市 IDs: {target_cities}")
    
    # 2. 从 HuggingFace 加载完整训练集
    print("正在从 HuggingFace 下载/加载原始数据集 (可能需要几秒钟)...")
    dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K", split='train')
    
    # 3. 转换为 pandas DataFrame
    print("正在转换为 Pandas DataFrame...")
    df_full = dataset.to_pandas()
    
    # 4. 过滤并提取目标城市的数据
    print("正在过滤数据...")
    df_target = df_full[df_full['city_id'].isin(target_cities)].copy()
    
    # 验证提取的数据量
    print("\n--- 提取成功 ---")
    print(f"提取到的总行数: {len(df_target)}")
    print("\n各城市行数统计:")
    print(df_target['city_id'].value_counts())
    
    # 5. 保存为 CSV
    output_path = '/workspace/demand_imputation/train_cities_10_17_9_8.csv'
    print(f"\n正在保存为 CSV 文件: {output_path} ...")
    df_target.to_csv(output_path, index=False)
    
    print("完成！数据已保存。")

if __name__ == "__main__":
    main()
