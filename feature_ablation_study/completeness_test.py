import pandas as pd
import numpy as np
import lightgbm as lgb
from datasets import load_dataset
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings('ignore')

print("=== 完备性测试 (Completeness Test) ===")
print("1. 应对局限性1：加载 Management Group 2 的数据 (约 62万行) 进行交叉验证")
dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")
train_df = dataset['train'].to_pandas()
eval_df = dataset['eval'].to_pandas()

train_g2 = train_df[train_df['management_group_id'] == 2].copy()
eval_g2 = eval_df[eval_df['management_group_id'] == 2].copy()
print(f"Group 2 训练集行数: {len(train_g2)}")
print(f"Group 2 测试集行数: {len(eval_g2)}")

print("\n2. 应对局限性3：从序列列表中提取衍生特征")
def extract_seq_features(df):
    # 解析序列
    # hours_stock_status 是一个包含 24 个元素的 list/array
    # 特征A：当天总缺货小时数
    df['total_stockout_hours'] = df['hours_stock_status'].apply(lambda x: sum(x))
    
    # 特征B：首次缺货发生的时间点 (0-23)，如果没有缺货则标记为 24
    def get_first_stockout(arr):
        lst = list(arr)
        return lst.index(1) if 1 in lst else 24
        
    df['first_stockout_hour'] = df['hours_stock_status'].apply(get_first_stockout)
    
    # 日期特征
    df['dt'] = pd.to_datetime(df['dt'])
    df['dayofweek'] = df['dt'].dt.dayofweek
    return df

print("正在提取训练集序列特征...")
train_g2 = extract_seq_features(train_g2)
print("正在提取测试集序列特征...")
eval_g2 = extract_seq_features(eval_g2)

base_features = ['discount', 'holiday_flag', 'activity_flag', 'precpt', 
                 'avg_temperature', 'avg_humidity', 'avg_wind_level', 
                 'stock_hour6_22_cnt', 'dayofweek', 
                 'total_stockout_hours', 'first_stockout_hour'] # 加入了新的序列衍生特征

all_id_features = ['city_id', 'store_id', 'management_group_id', 
                   'first_category_id', 'second_category_id', 
                   'third_category_id', 'product_id']

def run_model(features, name):
    print(f"\n--- 训练 {name} ---")
    cat_features = [f for f in features if f.endswith('_id')] + ['dayofweek', 'holiday_flag', 'activity_flag']
    
    X_train = train_g2[features].copy()
    y_train = train_g2['sale_amount']
    X_eval = eval_g2[features].copy()
    y_eval = eval_g2['sale_amount']

    for col in cat_features:
        if col in X_train.columns:
            X_train[col] = X_train[col].astype('category')
            X_eval[col] = X_eval[col].astype('category')

    # 使用 1500 棵树进行严谨验证
    model = lgb.LGBMRegressor(n_estimators=1500, learning_rate=0.05, random_state=42, n_jobs=-1, verbose=-1)
    
    # 因为 LightGBM 在有些版本会对不存在的 categorical_feature 报错，过滤一下
    valid_cat_features = [c for c in cat_features if c in X_train.columns]
    
    model.fit(X_train, y_train, 
              eval_set=[(X_eval, y_eval)], 
              categorical_feature=valid_cat_features, 
              callbacks=[lgb.early_stopping(stopping_rounds=30, verbose=False)])
    
    preds = model.predict(X_eval)
    rmse = np.sqrt(mean_squared_error(y_eval, preds))
    
    importance = pd.DataFrame({'Feature': features, 'Importance': model.feature_importances_}).sort_values(by='Importance', ascending=False)
    return rmse, importance

# 测试 1: 包含所有特征 (应对交叉验证要求)
rmse_all, imp_all = run_model(base_features + all_id_features, "Model A: 全量特征 (含新的序列衍生特征)")
print(f"Model A RMSE: {rmse_all:.6f}")

# 测试 2: 剔除 5 个冗余 ID，验证在加入了新特征、换了新数据集后，这个规律是否仍然成立
minimal_features = base_features + ['store_id', 'product_id']
rmse_min, imp_min = run_model(minimal_features, "Model B: 剔除 5 个宏观分类 ID")
print(f"Model B RMSE: {rmse_min:.6f}")

change = (rmse_min - rmse_all) / rmse_all * 100
print(f"\n================ 完备性交叉验证结论 ================")
print(f"在新数据集 (Group 2, 62万行) + 加入复杂序列衍生特征后：")
print(f"剔除 5 个冗余特征导致的 RMSE 变化为: {change:+.4f}%")

print("\nModel B 中排名前 8 的重要特征:")
print(imp_min.head(8).to_string(index=False))
