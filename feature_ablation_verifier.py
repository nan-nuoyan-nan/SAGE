"""
特征冗余验证专用脚本 (Feature Redundancy Verifier)
目的: 用于自动化验证某些宏观ID特征(如management_group_id, city_id, 一二三级分类ID)的冗余性。
逻辑: 这些特征在本质上是可被更细粒度特征(store_id, product_id)抽象替代的"二级公式"。
      通过大迭代下的LightGBM消融实验，证明它们对模型精度的实际贡献度。
"""

import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import mean_squared_error
from datasets import load_dataset
import warnings
warnings.filterwarnings('ignore')

def run_verification():
    print("1. 加载数据集...")
    dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")
    train_df = dataset['train'].to_pandas()
    eval_df = dataset['eval'].to_pandas()

    # 提取十万级样本（管理区1）作为验证基准
    print("2. 提取十万级样本进行验证...")
    train_g1 = train_df[train_df['management_group_id'] == 1].copy()
    eval_g1 = eval_df[eval_df['management_group_id'] == 1].copy()

    # 目标变量
    target = 'sale_amount'

    # 定义全量特征
    features = [
        'city_id', 'store_id', 'management_group_id', 
        'first_category_id', 'second_category_id', 'third_category_id', 'product_id',
        'discount', 'holiday_flag', 'activity_flag', 
        'precpt', 'avg_temperature', 'avg_humidity', 'avg_wind_level',
        'stock_hour6_22_cnt'
    ]
    
    # 涉嫌冗余的"二级公式"特征列表
    redundant_candidates = [
        'management_group_id', 'city_id', 
        'first_category_id', 'second_category_id', 'third_category_id',
        'precpt', 'avg_humidity', 'avg_wind_level'
    ]

    cat_features = [f for f in features if f.endswith('_id')] + ['holiday_flag', 'activity_flag']

    # 类型转换
    for col in cat_features:
        train_g1[col] = train_g1[col].astype('category')
        eval_g1[col] = eval_g1[col].astype('category')

    # 核心训练评估函数 (大迭代参数)
    def train_model(drop_features=None):
        drop_features = drop_features or []
        current_features = [f for f in features if f not in drop_features]
        current_cats = [f for f in cat_features if f not in drop_features]
        
        model = lgb.LGBMRegressor(
            objective='regression',
            n_estimators=1500,    # 大迭代次数
            learning_rate=0.03,   # 较小学习率，确保充分收敛
            random_state=42,
            n_jobs=-1,
            verbose=-1
        )
        
        model.fit(
            train_g1[current_features], train_g1[target],
            eval_set=[(eval_g1[current_features], eval_g1[target])],
            categorical_feature=current_cats,
            callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=False)]
        )
        
        preds = model.predict(eval_g1[current_features])
        rmse = np.sqrt(mean_squared_error(eval_g1[target], preds))
        return rmse

    print("\n--- 开始训练 Baseline (全量特征) ---")
    base_rmse = train_model()
    print(f"Baseline RMSE: {base_rmse:.6f}")

    print("\n--- 逐一验证涉嫌冗余特征 (Leave-One-Out) ---")
    results = []
    for col in redundant_candidates:
        rmse = train_model([col])
        change = (rmse - base_rmse) / base_rmse * 100
        status = "冗余/噪音 (可安全删除)" if change <= 0 else "有用特征 (保留)"
        results.append({'Dropped_Feature': col, 'RMSE': rmse, 'Change_%': change, 'Status': status})
        print(f"剔除 {col:<20} | RMSE={rmse:.6f} | 变化={change:+.4f}% | 结论: {status}")

    print("\n--- 验证: 一次性剔除所有涉嫌冗余的特征 ---")
    rmse_clean = train_model(redundant_candidates)
    change_clean = (rmse_clean - base_rmse) / base_rmse * 100
    print(f"剔除全部 8 个冗余特征 | RMSE={rmse_clean:.6f} | 变化={change_clean:+.4f}%")
    
    # 保存报告
    res_df = pd.DataFrame(results)
    res_df.to_csv('/workspace/redundancy_verification_report.csv', index=False)
    print("\n[✔] 验证报告已保存至: /workspace/redundancy_verification_report.csv")

if __name__ == "__main__":
    run_verification()
