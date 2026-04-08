import pandas as pd

def main():
    print("步骤 4：清理无用特征，准备最终用于模型训练的数据集...")

    # 1. 加载已经完成销量插补（A、B、C 及以下全部完成）的最终数据集
    input_path = '/workspace/demand_imputation/缺失销量插补/10万行_插补完成最终数据集.csv'
    df = pd.read_csv(input_path)
    print(f"成功加载插补数据集，初始形状: {df.shape}")

    # 2. 定义需要删除的特征列表
    columns_to_drop = [
        'city_id',             # 之前分析 C 类数据时我们就明确了，由于全是 city_id=4，所以该特征冗余，直接删除
        'hours_sale',          # 这是原始数据中每小时销量的数组，现在我们已经还原了全天总销量，这个冗余且模型无法直接使用
        'hours_stock_status'   # 这是原始数据中每小时是否有货的数组，同样模型无法直接使用，我们已经利用它算出了插补销量
    ]

    # 3. 找出数据集中实际存在的、需要删除的列，并进行删除
    cols_to_drop_actual = [col for col in columns_to_drop if col in df.columns]
    
    if cols_to_drop_actual:
        df.drop(columns=cols_to_drop_actual, inplace=True)
        print(f"\n已成功删除以下冗余特征列：\n{cols_to_drop_actual}")
    else:
        print("\n未找到需要删除的冗余特征列。")

    # 4. 保存清理后的最终训练数据集
    output_path = '/workspace/demand_imputation/缺失销量插补/4_清理冗余特征_生成模型输入.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n清理完成！最终可用于机器学习模型训练的数据集已保存至：")
    print(f"-> {output_path}")
    print(f"清理后的数据集形状: {df.shape}")
    
    # 打印前几行供检查
    print("\n最终数据集样例（前 2 行）：")
    print(df.head(2).to_string())

if __name__ == "__main__":
    main()
