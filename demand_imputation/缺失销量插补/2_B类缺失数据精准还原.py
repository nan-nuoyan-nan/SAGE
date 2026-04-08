import pandas as pd
import numpy as np

def main():
    print("步骤 2：使用 A 类画像库，对 B 类数据（缺货 1-2 小时）进行需求还原（插补）...")
    
    # 1. 加载原始数据集和刚刚生成的 A 类画像库
    df = pd.read_csv('/workspace/demand_imputation/train_city4_100k.csv')
    profiles_df = pd.read_csv('/workspace/demand_imputation/task7_hierarchical_imputation/a_class_profiles.csv')
    
    # 2. 将画像库转化为字典，提升查询速度。格式：{ 商品ID: [6点比例, 7点比例... 21点比例] }
    profiles_dict = {}
    for _, row in profiles_df.iterrows():
        ratios = [row[f'ratio_hour_{i}'] for i in range(6, 22)]
        profiles_dict[row['product_id']] = np.array(ratios)
        
    # 用于记录每行数据插补后的新销量，以及是否被插补过的标记
    imputed_sale_amounts = []
    is_imputed_flags = []
    
    # 兜底策略：如果某个商品完全没有 A 类数据，则采用均匀分布（每个小时销量均等）
    global_fallback_profile = np.ones(16) / 16.0
    
    count_imputed = 0
    count_fallback = 0
    
    # 3. 遍历每一行数据，寻找需要插补的 B 类数据
    for i, row in df.iterrows():
        # stock_hour6_22_cnt 表示营业期间（16小时）有货的小时数
        cnt = row['stock_hour6_22_cnt']
        
        # 判断是否为 B 类数据（缺货 1 到 2 个小时，即有货时间为 14 或 15 小时）
        if cnt in [14, 15]:
            product_id = row['product_id']
            actual_sales_total = row['sale_amount']  # 当天存活时间内的实际销量（截断销量）
            
            # 获取该商品的标准时段画像
            if product_id in profiles_dict:
                profile = profiles_dict[product_id]
            else:
                profile = global_fallback_profile
                count_fallback += 1
                
            # 解析 24 小时缺货序列，提取 6:00-22:00 的状态（1为有货，0为缺货）
            stock_arr_str = row['hours_stock_status'].replace('[', '').replace(']', '').strip()
            stock_6_22 = np.fromstring(stock_arr_str, sep=' ')[6:22]
            
            # 计算有货时段的标准占比 (Normal_Ratio) 和缺货时段的标准占比 (Missing_Ratio)
            normal_ratio = np.sum(profile[stock_6_22 == 1])
            missing_ratio = np.sum(profile[stock_6_22 == 0])
            
            # 核心插补算法：等比例放大
            # 缺失的销量 = 实际销量 * (缺货时段占比 / 有货时段占比)
            if normal_ratio > 0.0001:
                estimated_missing_sales = actual_sales_total * (missing_ratio / normal_ratio)
            else:
                # 极端异常处理：如果画像显示有货时段原本就不该有销量，则按时间比例粗暴平摊
                missing_hours = 16 - cnt
                estimated_missing_sales = actual_sales_total * (missing_hours / float(cnt))
                
            # 最终回填：原销量 + 估算出的缺失销量
            new_total_sales = actual_sales_total + estimated_missing_sales
            
            imputed_sale_amounts.append(new_total_sales)
            is_imputed_flags.append(1)  # 标记 1，表示该行已完成插补
            count_imputed += 1
            
        else:
            # 对于非 B 类数据（A、C、D、E 等），暂时保持原销量不变
            imputed_sale_amounts.append(row['sale_amount'])
            is_imputed_flags.append(0)
            
    # 4. 将插补结果新增为数据集的两列
    df['imputed_sale_amount'] = imputed_sale_amounts
    df['is_imputed_b_class'] = is_imputed_flags
    
    # 保存插补后的全新数据集
    output_path = '/workspace/demand_imputation/task7_hierarchical_imputation/train_city4_imputed_B.csv'
    df.to_csv(output_path, index=False)
    
    print("\n【插补完成】需求还原（A补B）已结束！")
    print(f"成功插补了 {count_imputed} 条 B 类数据。")
    if count_fallback > 0:
        print(f"其中有 {count_fallback} 条数据因为缺少 A 类画像，触发了均匀分布兜底策略。")
        
    print(f"包含最新插补销量（imputed_sale_amount）的数据集已保存至：{output_path}")

if __name__ == "__main__":
    main()
