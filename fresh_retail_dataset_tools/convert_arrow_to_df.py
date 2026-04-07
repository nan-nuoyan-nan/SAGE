import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import os

# Arrow文件路径
arrow_dir = r"d:\HP\pythonwork\new_live\SAGE\统计建模\FreshRetailNet_cache\Dingdong-Inc___fresh_retail_net-50_k\default\0.0.0\08c1fab7f9257bc73679d415d65d644165d351d4"

print(f"正在检查Arrow文件目录: {arrow_dir}")

# 列出所有文件
files = os.listdir(arrow_dir)
print(f"找到 {len(files)} 个文件:")
for f in files:
    print(f"  - {f}")

# 尝试读取评估集（较小的文件）
eval_file = os.path.join(arrow_dir, "fresh_retail_net-50_k-eval.arrow")
print(f"\n尝试读取评估集文件: {eval_file}")

try:
    # 使用pyarrow读取Arrow文件
    with pa.ipc.open_file(eval_file) as reader:
        table = reader.read_all()
        print(f"成功读取评估集:")
        print(f"  行数: {table.num_rows}")
        print(f"  列数: {table.num_columns}")
        print(f"  列名: {table.column_names}")
        
        # 转换为DataFrame
        df = table.to_pandas()
        print(f"\n转换为DataFrame成功:")
        print(f"  DataFrame形状: {df.shape}")
        print(f"  前几行:")
        print(df.head())
        
        # 保存为CSV（可选）
        csv_path = os.path.join(os.path.dirname(__file__), "fresh_retail_eval_sample.csv")
        df.head(1000).to_csv(csv_path, index=False, encoding='utf-8')
        print(f"\n已保存前1000行到: {csv_path}")
        
except Exception as e:
    print(f"读取评估集时出错: {e}")
    import traceback
    traceback.print_exc()

# 尝试读取一个训练分片
print("\n" + "="*80)
print("尝试读取第一个训练分片...")
train_file_0 = os.path.join(arrow_dir, "fresh_retail_net-50_k-train-00000-of-00005.arrow")

try:
    with pa.ipc.open_file(train_file_0) as reader:
        table = reader.read_all()
        print(f"成功读取训练分片0:")
        print(f"  行数: {table.num_rows}")
        print(f"  列数: {table.num_columns}")
        
        # 转换为DataFrame（只取前1000行避免内存问题）
        df_train = table.slice(0, 1000).to_pandas()
        print(f"\n转换为DataFrame成功（前1000行）:")
        print(f"  DataFrame形状: {df_train.shape}")
        print(f"  数据类型:")
        print(df_train.dtypes)
        
        # 保存为CSV
        csv_train_path = os.path.join(os.path.dirname(__file__), "fresh_retail_train_sample.csv")
        df_train.to_csv(csv_train_path, index=False, encoding='utf-8')
        print(f"\n已保存训练分片前1000行到: {csv_train_path}")
        
except Exception as e:
    print(f"读取训练分片时出错: {e}")
    import traceback
    traceback.print_exc()