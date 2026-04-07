"""
安全大数据处理方案 - 不一次性加载所有数据，避免内存爆炸
使用流式处理或分批次处理大型数据集
"""

import pandas as pd
import pyarrow as pa
import os
from datasets import load_dataset

def process_in_chunks(split="train", chunk_size=100000, output_prefix="chunk"):
    """
    分批次处理大数据集，避免内存溢出
    
    参数:
        split: 数据集分割 ("train" 或 "eval")
        chunk_size: 每个批次处理的行数
        output_prefix: 输出文件前缀
    """
    print(f"开始分批次处理 {split} 数据集，每批次 {chunk_size:,} 行")
    
    # 加载数据集（使用datasets库的流式功能）
    dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K", split=split)
    
    total_rows = len(dataset)
    print(f"数据集总行数: {total_rows:,}")
    
    # 计算需要多少批次
    num_chunks = (total_rows + chunk_size - 1) // chunk_size
    print(f"需要 {num_chunks} 个批次")
    
    chunk_files = []
    
    for chunk_idx in range(num_chunks):
        print(f"\n处理批次 {chunk_idx+1}/{num_chunks}...")
        
        # 计算当前批次的起始和结束索引
        start_idx = chunk_idx * chunk_size
        end_idx = min((chunk_idx + 1) * chunk_size, total_rows)
        
        # 加载当前批次的数据
        print(f"  加载行 {start_idx:,} 到 {end_idx:,}...")
        chunk_data = dataset.select(range(start_idx, end_idx))
        
        # 转换为DataFrame
        print(f"  转换为DataFrame...")
        df_chunk = pd.DataFrame(chunk_data)
        
        # 保存当前批次
        chunk_filename = f"{output_prefix}_{split}_{chunk_idx+1:03d}.csv"
        chunk_path = os.path.join(os.path.dirname(__file__), chunk_filename)
        df_chunk.to_csv(chunk_path, index=False, encoding='utf-8')
        
        print(f"  ✅ 已保存: {chunk_filename} ({df_chunk.shape[0]:,}行)")
        chunk_files.append(chunk_path)
        
        # 显示内存使用情况（可选）
        import psutil
        process = psutil.Process()
        mem_info = process.memory_info()
        print(f"  当前内存使用: {mem_info.rss / 1024 / 1024:.1f} MB")
    
    print(f"\n✅ 所有批次处理完成!")
    print(f"共生成 {len(chunk_files)} 个文件")
    
    return chunk_files

def stream_process_with_iterator(split="train", max_samples=10000):
    """
    使用迭代器流式处理数据，只保持少量数据在内存中
    
    参数:
        split: 数据集分割
        max_samples: 最大处理样本数（用于演示）
    """
    print(f"使用迭代器流式处理 {split} 数据集 (最多 {max_samples:,} 行)")
    
    # 使用datasets的迭代器功能
    dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K", split=split)
    
    # 创建结果列表（可以改为直接写入文件或数据库）
    results = []
    processed_count = 0
    
    for i, example in enumerate(dataset):
        if i >= max_samples:
            break
            
        # 处理单个样本
        # 这里可以做任何分析或转换
        results.append({
            'index': i,
            'city_id': example['city_id'],
            'store_id': example['store_id'],
            'product_id': example['product_id'],
            'sale_amount': example['sale_amount'],
            'date': example['dt']
        })
        
        processed_count += 1
        
        # 每1000行显示进度
        if processed_count % 1000 == 0:
            print(f"  已处理 {processed_count:,} 行")
            
        # 控制内存：每处理5000行保存一次并清空列表
        if len(results) >= 5000:
            # 保存当前批次
            df_batch = pd.DataFrame(results)
            batch_file = os.path.join(os.path.dirname(__file__), f"stream_batch_{processed_count//5000:03d}.csv")
            df_batch.to_csv(batch_file, index=False, encoding='utf-8')
            print(f"  ✅ 保存批次到: {batch_file}")
            results.clear()  # 清空列表释放内存
    
    print(f"\n✅ 流式处理完成! 共处理 {processed_count:,} 行")

def analyze_with_sampling(split="train", sample_size=10000, random_seed=42):
    """
    使用采样方法分析大数据集
    
    参数:
        split: 数据集分割
        sample_size: 采样大小
        random_seed: 随机种子
    """
    print(f"使用采样方法分析 {split} 数据集 (采样 {sample_size:,} 行)")
    
    dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K", split=split)
    
    # 生成随机索引进行采样
    import random
    random.seed(random_seed)
    
    total_rows = len(dataset)
    if sample_size > total_rows:
        sample_size = total_rows
    
    # 生成随机索引
    sample_indices = random.sample(range(total_rows), sample_size)
    print(f"随机采样 {len(sample_indices):,} 行...")
    
    # 加载采样数据
    sample_data = dataset.select(sample_indices)
    
    # 转换为DataFrame
    df_sample = pd.DataFrame(sample_data)
    print(f"采样DataFrame形状: {df_sample.shape}")
    
    # 保存采样数据
    sample_file = os.path.join(os.path.dirname(__file__), f"{split}_sample_{sample_size}.csv")
    df_sample.to_csv(sample_file, index=False, encoding='utf-8')
    print(f"✅ 采样数据已保存: {sample_file}")
    
    # 显示基本统计信息
    print(f"\n采样数据统计:")
    print(f"  城市数量: {df_sample['city_id'].nunique()}")
    print(f"  店铺数量: {df_sample['store_id'].nunique()}")
    print(f"  商品数量: {df_sample['product_id'].nunique()}")
    print(f"  日期范围: {df_sample['dt'].min()} 到 {df_sample['dt'].max()}")
    print(f"  平均销售额: {df_sample['sale_amount'].mean():.4f}")
    
    return df_sample

def merge_chunks_after_processing(chunk_files, output_file="merged_result.csv"):
    """
    处理完所有分块后，如果需要合并结果
    
    参数:
        chunk_files: 分块文件列表
        output_file: 合并后的输出文件
    """
    print(f"合并 {len(chunk_files)} 个分块文件...")
    
    # 使用pandas的concat方法（如果文件不大）
    # 如果文件很大，建议使用其他方法（如Dask或直接数据库操作）
    
    dfs = []
    for i, chunk_file in enumerate(chunk_files):
        print(f"  读取分块 {i+1}/{len(chunk_files)}: {os.path.basename(chunk_file)}")
        df_chunk = pd.read_csv(chunk_file)
        dfs.append(df_chunk)
    
    # 合并所有DataFrame
    print("合并所有分块...")
    merged_df = pd.concat(dfs, ignore_index=True)
    
    # 保存合并结果
    output_path = os.path.join(os.path.dirname(__file__), output_file)
    merged_df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"✅ 合并完成! 总行数: {merged_df.shape[0]:,}")
    print(f"合并文件: {output_path}")
    
    return merged_df

# 使用示例
if __name__ == "__main__":
    print("=" * 70)
    print("安全大数据处理方案")
    print("避免内存爆炸，保护你的笔记本")
    print("=" * 70)
    
    print("\n请选择处理方案:")
    print("1. 分批次处理 (推荐，最安全)")
    print("2. 流式迭代处理 (适合逐行分析)")
    print("3. 随机采样分析 (适合探索性分析)")
    print("4. 合并已处理的分块")
    
    choice = input("\n请输入选项 (1-4): ").strip()
    
    if choice == "1":
        print("\n" + "="*70)
        print("方案1: 分批次处理")
        print("将大数据集分成小块处理，避免内存溢出")
        print("="*70)
        
        split = input("处理哪个数据集分割? (train/eval, 默认train): ").strip() or "train"
        chunk_size = input("每个批次大小? (默认100000): ").strip()
        chunk_size = int(chunk_size) if chunk_size else 100000
        
        # 分批次处理
        chunk_files = process_in_chunks(split=split, chunk_size=chunk_size)
        
        print(f"\n⚠️ 提示: 所有数据已分块保存，可以根据需要合并或分别分析")
        
    elif choice == "2":
        print("\n" + "="*70)
        print("方案2: 流式迭代处理")
        print("使用迭代器逐行处理，内存占用最小")
        print("="*70)
        
        split = input("处理哪个数据集分割? (train/eval, 默认train): ").strip() or "train"
        max_samples = input("最大处理行数? (默认10000): ").strip()
        max_samples = int(max_samples) if max_samples else 10000
        
        stream_process_with_iterator(split=split, max_samples=max_samples)
        
    elif choice == "3":
        print("\n" + "="*70)
        print("方案3: 随机采样分析")
        print("从大数据集中随机采样进行分析")
        print("="*70)
        
        split = input("处理哪个数据集分割? (train/eval, 默认train): ").strip() or "train"
        sample_size = input("采样大小? (默认10000): ").strip()
        sample_size = int(sample_size) if sample_size else 10000
        
        analyze_with_sampling(split=split, sample_size=sample_size)
        
    elif choice == "4":
        print("\n" + "="*70)
        print("方案4: 合并已处理的分块")
        print("将分块处理的结果合并成一个文件")
        print("="*70)
        
        # 查找现有的分块文件
        import glob
        chunk_pattern = os.path.join(os.path.dirname(__file__), "chunk_*.csv")
        chunk_files = glob.glob(chunk_pattern)
        
        if not chunk_files:
            print("❌ 没有找到分块文件!")
            print("请先运行方案1进行分块处理")
        else:
            print(f"找到 {len(chunk_files)} 个分块文件:")
            for f in sorted(chunk_files):
                print(f"  - {os.path.basename(f)}")
            
            confirm = input("\n确认合并这些文件? (y/n): ").strip().lower()
            if confirm == 'y':
                output_name = input("输出文件名? (默认merged_result.csv): ").strip() or "merged_result.csv"
                merge_chunks_after_processing(chunk_files, output_name)
    
    else:
        print("❌ 无效选项!")
    
    print("\n" + "="*70)
    print("处理完成!")
    print("="*70)
    print("提示: 大数据集处理的关键是避免一次性加载所有数据到内存")
    print("可以根据需要选择不同的处理策略")