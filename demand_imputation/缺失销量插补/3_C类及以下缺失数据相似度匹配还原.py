import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def main():
    print("步骤 3：使用相似度匹配，对 C, D, E 等剩余类数据（缺货 >= 3 小时）进行需求还原...")

    # 设置中文字体 (解决图表乱码问题)
    try:
        font_prop = fm.FontProperties(fname='/workspace/SimHei.ttf')
    except Exception as e:
        print("警告：无法加载中文字体，可能出现乱码", e)


    # 1. 加载包含已插补 B 类数据的数据集，和 A 类画像库
    df = pd.read_csv('/workspace/demand_imputation/task7_hierarchical_imputation/train_city4_imputed_B.csv')
    profiles_df = pd.read_csv('/workspace/demand_imputation/task7_hierarchical_imputation/a_class_profiles.csv')

    # 将画像库转化为字典：{ product_id: np.array([16个比例]) }
    profiles_dict = {row['product_id']: np.array([row[f'ratio_hour_{i}'] for i in range(6, 22)]) 
                     for _, row in profiles_df.iterrows()}
    global_fallback_profile = np.ones(16) / 16.0

    # 2. 提取气候特征并计算全量数据（10万行）的均值和标准差
    climate_cols = ['precpt', 'avg_temperature', 'avg_humidity', 'avg_wind_level']
    means = df[climate_cols].mean()
    stds = df[climate_cols].std()

    # 替换标准差为 0 的情况（防止除零错误）
    stds = stds.replace(0, 1)

    # 预先将气候特征标准化（减均值，除以标准差）
    for col in climate_cols:
        df[f'{col}_std'] = (df[col] - means[col]) / stds[col]
    std_cols = [f'{col}_std' for col in climate_cols]

    # 3. 划分 AB 类数据（有货 >= 14）和需要插补的目标数据（有货 < 14）
    ab_df = df[df['stock_hour6_22_cnt'] >= 14].copy()
    target_idx = df['stock_hour6_22_cnt'] < 14

    # 计算每个 product_id 在 AB 类中的平均销量（注意使用的是已还原的 imputed_sale_amount）
    ab_mean_sales = ab_df.groupby('product_id')['imputed_sale_amount'].mean().to_dict()

    # 构建 AB 类数据的快速查询字典
    # 键为 (product_id, holiday_flag, activity_flag)
    # 值为一个二维 numpy 数组，包含所有符合条件的 AB 行的标准化气候特征
    ab_lookup = {}
    for (pid, h_flag, a_flag), group in ab_df.groupby(['product_id', 'holiday_flag', 'activity_flag']):
        ab_lookup[(pid, h_flag, a_flag)] = group[std_cols].values

    # 准备新列，用于记录插补后的销量和使用的方法
    # 注意：B 类在之前已经有了 imputed_sale_amount，A 类就是原销量
    if 'imputed_sale_amount' not in df.columns:
        df['imputed_sale_amount'] = df['sale_amount'].copy()
        
    imputed_sales = df['imputed_sale_amount'].copy() 
    impute_methods = pd.Series(['None'] * len(df), index=df.index)

    # 更新之前 A/B 类的插补方法标签
    impute_methods[df['stock_hour6_22_cnt'] == 16] = 'A类_无需插补'
    impute_methods[df['stock_hour6_22_cnt'].isin([14, 15])] = 'B类_比例缩放法'

    # 计数器
    count_profile_scaled = 0
    count_ab_mean = 0

    # 4. 遍历目标数据（C, D, E 等）
    # 为提高效率，只遍历目标数据的索引
    for idx in df[target_idx].index:
        row = df.loc[idx]
        pid = row['product_id']
        h_flag = row['holiday_flag']
        a_flag = row['activity_flag']
        cnt = row['stock_hour6_22_cnt']
        actual_sales = row['sale_amount']

        key = (pid, h_flag, a_flag)
        used_profile = False

        if key in ab_lookup:
            # 存在促销和节假日均匹配的 AB 类数据
            candidates_std = ab_lookup[key]
            target_std = row[std_cols].values.astype(float)
            
            # 计算欧氏距离
            distances = np.sqrt(np.sum((candidates_std - target_std)**2, axis=1))
            min_dist = np.min(distances)

            # 如果最小距离 < 1.5，使用画像缩放法（之前的插补法）
            if min_dist < 1.5:
                profile = profiles_dict.get(pid, global_fallback_profile)
                stock_arr_str = row['hours_stock_status'].replace('[', '').replace(']', '').strip()
                stock_6_22 = np.fromstring(stock_arr_str, sep=' ')[6:22]
                
                normal_ratio = np.sum(profile[stock_6_22 == 1])
                missing_ratio = np.sum(profile[stock_6_22 == 0])

                if normal_ratio > 0.0001:
                    imputed = actual_sales + actual_sales * (missing_ratio / normal_ratio)
                else:
                    # 兜底：按时间比例粗暴平摊
                    missing_hours = 16 - cnt
                    imputed = actual_sales + actual_sales * (missing_hours / max(float(cnt), 1))
                
                imputed_sales[idx] = imputed
                impute_methods[idx] = 'C类及以下_画像缩放(距离<1.5)'
                count_profile_scaled += 1
                used_profile = True

        if not used_profile:
            # 如果没有匹配的 AB 行，或最小距离 >= 1.5，则使用该商品在 AB 类的平均销量进行插补
            if pid in ab_mean_sales:
                imputed = ab_mean_sales[pid]
            else:
                # 极端情况：连 AB 类中都没有这个商品的记录，只能使用自己当前的销量
                imputed = actual_sales
                
            imputed_sales[idx] = imputed
            impute_methods[idx] = 'C类及以下_AB均值兜底'
            count_ab_mean += 1

    # 5. 更新 DataFrame
    df['imputed_sale_amount'] = imputed_sales
    df['imputed_method'] = impute_methods

    # 保存插补后的全新数据集
    output_csv = '/workspace/demand_imputation/task9_impute_c_to_h_class/train_city4_imputed_FINAL.csv'
    # 丢弃标准化时的临时列
    df.drop(columns=std_cols, inplace=True)
    df.to_csv(output_csv, index=False)

    print(f"\n【插补完成】C类及以后数据（缺货>=3小时）已全部处理！")
    print(f"- 匹配条件且距离 < 1.5 使用画像缩放法：{count_profile_scaled} 条")
    print(f"- 匹配失败或距离 >= 1.5 使用 AB均值兜底法：{count_ab_mean} 条")
    print(f"包含最新插补销量的数据集已保存至：{output_csv}")

    # 6. 绘图：展示各类插补方法的使用数量分布
    plt.figure(figsize=(12, 7))
    method_counts = df['imputed_method'].value_counts()
    
    # 定义颜色
    colors = ['#4CAF50', '#2196F3', '#FFC107', '#FF9800', '#9C27B0', '#F44336']
    bars = plt.bar(range(len(method_counts)), method_counts.values, color=colors[:len(method_counts)])
    
    plt.title('各类插补方法在 10万行数据中的使用分布', fontproperties=font_prop, fontsize=16)
    plt.xlabel('插补策略 / 数据类别', fontproperties=font_prop, fontsize=12)
    plt.ylabel('行数', fontproperties=font_prop, fontsize=12)
    plt.xticks(range(len(method_counts)), method_counts.index, rotation=25, fontproperties=font_prop, fontsize=10, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 在柱子上添加具体数值
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 500, int(yval), ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    output_png = '/workspace/demand_imputation/task9_impute_c_to_h_class/imputation_methods_distribution.png'
    plt.savefig(output_png)
    print(f"插补方法分布图已保存至：{output_png}")


if __name__ == "__main__":
    main()
