import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

print("Loading Group 4 Dataset...")
train = pd.read_csv('/workspace/group4_dataset/train_group4.csv')
eval_df = pd.read_csv('/workspace/group4_dataset/eval_group4.csv')

base_features = ['discount', 'holiday_flag', 'activity_flag', 'precpt', 
                 'avg_temperature', 'avg_humidity', 'avg_wind_level']

all_id_features = ['city_id', 'store_id', 'management_group_id', 
                   'first_category_id', 'second_category_id', 
                   'third_category_id', 'product_id']

# 1. 全部 14 个特征
features_all = base_features + all_id_features

# 2. 仅仅剔除 management_group_id (13 个特征)
features_drop_group = base_features + [f for f in all_id_features if f != 'management_group_id']

def evaluate_model(features, name):
    cat_features = [f for f in features if f.endswith('_id')]
    
    # 必须要用 copy，避免 SettingWithCopyWarning
    X_train = train[features].copy()
    y_train = train['sale_amount']
    X_eval = eval_df[features].copy()
    y_eval = eval_df['sale_amount']
    
    # 将 ID 列转为 category 格式供 LightGBM 使用
    for col in cat_features:
        X_train[col] = X_train[col].astype('category')
        X_eval[col] = X_eval[col].astype('category')
        
    model = lgb.LGBMRegressor(
        objective='regression',
        n_estimators=100,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1,
        verbose=-1 # 关闭刷屏输出
    )
    
    model.fit(
        X_train, y_train,
        eval_set=[(X_eval, y_eval)],
        categorical_feature=cat_features,
        callbacks=[lgb.early_stopping(stopping_rounds=10, verbose=False)]
    )
    
    preds = model.predict(X_eval)
    rmse = np.sqrt(mean_squared_error(y_eval, preds))
    mae = mean_absolute_error(y_eval, preds)
    
    return rmse, mae

print("\nTraining Model A (All 14 Features)...")
rmse_all, mae_all = evaluate_model(features_all, "Model A")

print("Training Model C (Drop ONLY management_group_id)...")
rmse_drop, mae_drop = evaluate_model(features_drop_group, "Model C")

print("\n================ SINGLE ABLATION STUDY ================")
print(f"Model A (14 features): RMSE = {rmse_all:.6f} | MAE = {mae_all:.6f}")
print(f"Model C (13 features): RMSE = {rmse_drop:.6f} | MAE = {mae_drop:.6f}")

diff_rmse = (rmse_drop - rmse_all) / rmse_all * 100
print(f"RMSE 精度变化: {diff_rmse:+.4f}%")

