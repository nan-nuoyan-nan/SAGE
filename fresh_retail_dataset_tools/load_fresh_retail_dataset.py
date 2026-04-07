from datasets import load_dataset
import pandas as pd
import os

print("尝试从Hugging Face加载FreshRetailNet数据集...")

try:
    # 方法1: 直接从Hugging Face加载（如果网络允许）
    print("方法1: 从Hugging Face加载...")
    dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")
    
    print(f"数据集加载成功!")
    print(f"数据集结构: {dataset}")
    
    # 查看训练集
    train_dataset = dataset["train"]
    print(f"\n训练集信息:")
    print(f"  行数: {len(train_dataset)}")
    print(f"  特征: {train_dataset.features}")
    
    # 转换为DataFrame（取前1000行）
    print(f"\n转换为DataFrame...")
    df_train = pd.DataFrame(train_dataset.select(range(min(1000, len(train_dataset)))))
    print(f"  DataFrame形状: {df_train.shape}")
    print(f"  列名: {df_train.columns.tolist()}")
    
    # 保存为CSV
    csv_path = os.path.join(os.path.dirname(__file__), "fresh_retail_train_df.csv")
    df_train.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"\n已保存到: {csv_path}")
    
    # 查看评估集
    if "eval" in dataset:
        eval_dataset = dataset["eval"]
        print(f"\n评估集信息:")
        print(f"  行数: {len(eval_dataset)}")
        
        # 转换为DataFrame（取前500行）
        df_eval = pd.DataFrame(eval_dataset.select(range(min(500, len(eval_dataset)))))
        csv_eval_path = os.path.join(os.path.dirname(__file__), "fresh_retail_eval_df.csv")
        df_eval.to_csv(csv_eval_path, index=False, encoding='utf-8')
        print(f"  已保存评估集到: {csv_eval_path}")
    
    # 显示数据示例
    print(f"\n数据示例（前5行）:")
    print(df_train.head())
    print(f"\n数据类型:")
    print(df_train.dtypes)
    
except Exception as e:
    print(f"方法1失败: {e}")
    print("\n尝试方法2: 从本地缓存加载...")
    
    try:
        # 方法2: 从本地缓存加载
        cache_dir = r"d:\HP\pythonwork\new_live\SAGE\统计建模\FreshRetailNet_cache"
        print(f"缓存目录: {cache_dir}")
        
        # 使用本地缓存路径
        dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K", cache_dir=cache_dir)
        
        print(f"从缓存加载成功!")
        print(f"数据集结构: {dataset}")
        
        # 转换为DataFrame（取前1000行）
        train_dataset = dataset["train"]
        df_train = pd.DataFrame(train_dataset.select(range(min(1000, len(train_dataset)))))
        print(f"\nDataFrame形状: {df_train.shape}")
        
        # 保存为CSV
        csv_path = os.path.join(os.path.dirname(__file__), "fresh_retail_train_df.csv")
        df_train.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"已保存到: {csv_path}")
        
        print(f"\n前5行:")
        print(df_train.head())
        
    except Exception as e2:
        print(f"方法2也失败: {e2}")
        print("\n尝试方法3: 直接读取Arrow文件...")
        
        try:
            # 方法3: 尝试用其他方式读取Arrow文件
            import pyarrow as pa
            import pyarrow.dataset as ds
            
            arrow_dir = r"d:\HP\pythonwork\new_live\SAGE\统计建模\FreshRetailNet_cache\Dingdong-Inc___fresh_retail_net-50_k\default\0.0.0\08c1fab7f9257bc73679d415d65d644165d351d4"
            
            # 尝试读取一个文件
            eval_file = os.path.join(arrow_dir, "fresh_retail_net-50_k-eval.arrow")
            print(f"尝试读取文件: {eval_file}")
            
            # 尝试使用pyarrow.dataset
            dataset = ds.dataset(eval_file, format="arrow")
            table = dataset.to_table()
            print(f"读取成功! 行数: {table.num_rows}, 列数: {table.num_columns}")
            
            # 转换为DataFrame
            df = table.to_pandas()
            print(f"DataFrame形状: {df.shape}")
            
            # 保存
            csv_path = os.path.join(os.path.dirname(__file__), "fresh_retail_direct.csv")
            df.head(1000).to_csv(csv_path, index=False, encoding='utf-8')
            print(f"已保存到: {csv_path}")
            
        except Exception as e3:
            print(f"所有方法都失败: {e3}")
            import traceback
            traceback.print_exc()