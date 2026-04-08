import pandas as pd
import numpy as np

def main():
    print("步骤 1：开始构建 A 类数据（健康不缺货）的商品销售时段画像库...")
    
    # 1. 加载提取出的 10 万行数据集 (城市 ID = 4)
    df = pd.read_csv('/workspace/demand_imputation/train_city4_100k.csv')
    
    # 2. 筛选出 A 类数据（营业时间 6:00-22:00 全天 16 个小时都不缺货）
    df_a = df[df['stock_hour6_22_cnt'] == 16].copy()
    print(f"成功提取出 {len(df_a)} 条 A 类基准数据。")
    
    # 用于存放每个商品的标准画像（各小时销量占比）
    profiles = []
    
    # 3. 按商品 (product_id) 进行分组，计算各商品在健康状态下的销售时间分布规律
    for product_id, group in df_a.groupby('product_id'):
        
        # 初始化一个长度为 16 的数组，用于累加 6:00 到 22:00 每个小时的总销量
        total_sales_arr = np.zeros(16)
        
        for _, row in group.iterrows():
            # 将字符串格式的小时销量数组转换为 Numpy 数组
            arr_str = row['hours_sale'].replace('[', '').replace(']', '').strip()
            sales_arr = np.fromstring(arr_str, sep=' ')
            
            # 截取营业时间 6:00 到 22:00 (数组索引 6 到 21) 并累加
            total_sales_arr += sales_arr[6:22]
            
        # 4. 计算占比：用每个小时的销量 / 全天总销量
        sum_sales = total_sales_arr.sum()
        
        if sum_sales > 0:
            # 正常商品：计算出 16 个小时真实的销售比例分布
            ratio_arr = total_sales_arr / sum_sales
        else:
            # 极端异常情况：A类数据里该商品全天销量为 0，则采用均匀平摊分布作为兜底
            ratio_arr = np.ones(16) / 16.0
            
        # 5. 组装该商品的画像数据并保存
        profile_row = {
            'product_id': product_id, 
            'a_class_sample_count': len(group)  # 记录该画像是由多少条数据计算得出的，方便后续评估置信度
        }
        
        for i in range(16):
            profile_row[f'ratio_hour_{i+6}'] = ratio_arr[i]
            
        profiles.append(profile_row)
        
    # 将所有的画像数据转换为 DataFrame 并保存为 CSV
    profile_df = pd.DataFrame(profiles)
    output_path = '/workspace/demand_imputation/task7_hierarchical_imputation/a_class_profiles.csv'
    profile_df.to_csv(output_path, index=False)
    
    print("\n【构建完成】A类基准画像库（各商品每小时销量标准占比）已生成！")
    print(f"共生成了 {len(profile_df)} 个独立商品的画像。")
    print(f"文件保存至：{output_path}")

if __name__ == "__main__":
    main()
