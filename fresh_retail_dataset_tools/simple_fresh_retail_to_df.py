"""
FreshRetailNet数据集转DataFrame工具
简单、直接地将Hugging Face数据集转换为pandas DataFrame
"""

from datasets import load_dataset
import pandas as pd
import os

def load_fresh_retail_as_df(split="train", n_rows=None):
    """
    加载FreshRetailNet数据集为DataFrame
    
    参数:
        split: "train" 或 "eval"
        n_rows: 要加载的行数，None表示全部（谨慎使用，训练集有450万行）
    
    返回:
        pandas DataFrame
    """
    print(f"正在加载FreshRetailNet数据集 ({split})...")
    
    # 加载数据集（会自动使用本地缓存）
    dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")
    
    if split not in dataset:
        raise ValueError(f"数据集没有 {split} 分割，可用的分割: {list(dataset.keys())}")
    
    data_split = dataset[split]
    
    if n_rows is not None:
        print(f"只加载前 {n_rows} 行...")
        data_split = data_split.select(range(min(n_rows, len(data_split))))
    
    # 转换为DataFrame
    print("转换为DataFrame...")
    df = pd.DataFrame(data_split)
    
    print(f"✅ 加载完成! DataFrame形状: {df.shape}")
    print(f"列名: {df.columns.tolist()}")
    
    return df

def save_df_to_csv(df, filename=None):
    """保存DataFrame为CSV文件"""
    if filename is None:
        filename = f"fresh_retail_{len(df)}_rows.csv"
    
    filepath = os.path.join(os.path.dirname(__file__), filename)
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✅ 已保存到: {filepath}")
    return filepath

def show_dataset_info():
    """显示数据集基本信息"""
    print("=" * 60)
    print("FreshRetailNet-50K 数据集信息")
    print("=" * 60)
    
    dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")
    
    print(f"数据集结构: {list(dataset.keys())}")
    
    for split_name, split_data in dataset.items():
        print(f"\n{split_name.upper()} 集:")
        print(f"  行数: {len(split_data):,}")
        print(f"  特征数: {len(split_data.features)}")
        print(f"  特征列表:")
        for i, (feature_name, feature_type) in enumerate(split_data.features.items()):
            print(f"    {i+1:2d}. {feature_name}: {feature_type}")
    
    print(f"\n示例数据列解释:")
    print(f"  city_id, store_id: 城市和店铺ID")
    print(f"  product_id: 商品ID")
    print(f"  dt: 日期 (格式: YYYY-MM-DD)")
    print(f"  sale_amount: 日销售额")
    print(f"  hours_sale: 24小时销售列表")
    print(f"  stock_hour6_22_cnt: 6-22点库存数量")
    print(f"  hours_stock_status: 24小时库存状态列表")
    print(f"  discount: 折扣率")
    print(f"  holiday_flag, activity_flag: 节假日和活动标志")
    print(f"  precpt, avg_temperature, avg_humidity, avg_wind_level: 天气数据")

# 使用示例
if __name__ == "__main__":
    # 示例1: 显示数据集信息
    show_dataset_info()
    
    print("\n" + "=" * 60)
    print("使用示例")
    print("=" * 60)
    
    # 示例2: 加载训练集前1000行
    df_train = load_fresh_retail_as_df("train", n_rows=1000)
    print(f"\n训练集前5行:")
    print(df_train.head())
    
    # 保存为CSV
    csv_path = save_df_to_csv(df_train, "fresh_retail_train_1000.csv")
    
    # 示例3: 加载评估集前500行
    print("\n" + "=" * 60)
    df_eval = load_fresh_retail_as_df("eval", n_rows=500)
    save_df_to_csv(df_eval, "fresh_retail_eval_500.csv")
    
    print("\n✅ 所有操作完成!")
    print("提示: 大数据集建议分批次处理，避免内存溢出")