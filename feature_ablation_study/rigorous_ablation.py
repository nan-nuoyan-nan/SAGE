import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
from datasets import load_dataset
import time
import warnings
warnings.filterwarnings('ignore')

print("1. Loading dataset from Hugging Face...")
dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")
train_df = dataset['train'].to_pandas()
eval_df = dataset['eval'].to_pandas()

print("2. Extracting Management Group 5 (approx 1 Million rows)...")
train_g5 = train_df[train_df['management_group_id'] == 5].copy()
eval_g5 = eval_df[eval_df['management_group_id'] == 5].copy()
print(f"   Train rows: {len(train_g5):,}")
print(f"   Eval rows:  {len(eval_g5):,}")

base_features = ['discount', 'holiday_flag', 'activity_flag', 'precpt', 
                 'avg_temperature', 'avg_humidity', 'avg_wind_level']

all_id_features = ['city_id', 'store_id', 'management_group_id', 
                   'first_category_id', 'second_category_id', 
                   'third_category_id', 'product_id']

def train_eval(features, name):
    print(f"\n--- Training {name} ---")
    print(f"Features ({len(features)}): {features}")
    cat_features = [f for f in features if f.endswith('_id')]
    
    X_train = train_g5[features].copy()
    y_train = train_g5['sale_amount']
    X_eval = eval_g5[features].copy()
    y_eval = eval_g5['sale_amount']

    for col in cat_features:
        X_train[col] = X_train[col].astype('category')
        X_eval[col] = X_eval[col].astype('category')

    # RIGOROUS SETUP: 1500 trees, 0.03 learning rate, 50 early stopping
    model = lgb.LGBMRegressor(
        objective='regression',
        n_estimators=1500,
        learning_rate=0.03,
        random_state=42,
        n_jobs=-1,
        verbose=-1
    )
    
    start_time = time.time()
    model.fit(
        X_train, y_train,
        eval_set=[(X_eval, y_eval)],
        categorical_feature=cat_features,
        callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=False)]
    )
    train_time = time.time() - start_time
    
    preds = model.predict(X_eval)
    rmse = np.sqrt(mean_squared_error(y_eval, preds))
    mae = mean_absolute_error(y_eval, preds)
    
    print(f"[{name}] Finished in {train_time:.1f}s. Best iteration: {model.best_iteration_}")
    print(f"RMSE: {rmse:.6f} | MAE: {mae:.6f}")
    return rmse, mae

# Exp 1: Baseline (All 14 Features)
rmse_all, mae_all = train_eval(base_features + all_id_features, "Model A: Baseline (All 14 Features)")

# Exp 2: Drop ONLY management_group_id
features_drop_group = base_features + [f for f in all_id_features if f != 'management_group_id']
rmse_group, mae_group = train_eval(features_drop_group, "Model B: Drop ONLY management_group_id")

# Exp 3: Drop ALL 5 redundant features (Keep only store_id and product_id)
features_minimal = base_features + ['store_id', 'product_id']
rmse_min, mae_min = train_eval(features_minimal, "Model C: Drop ALL 5 Redundant Features")

print("\n" + "="*50)
print(" RIGOROUS ABLATION STUDY RESULTS (1M ROWS, 1500 TREES)")
print("="*50)
print(f"1. Baseline (14 features):      RMSE = {rmse_all:.6f}")
print(f"2. Drop management_group_id:    RMSE = {rmse_group:.6f} (Change: {(rmse_group-rmse_all)/rmse_all*100:+.4f}%)")
print(f"3. Drop ALL 5 redundant IDs:    RMSE = {rmse_min:.6f} (Change: {(rmse_min-rmse_all)/rmse_all*100:+.4f}%)")

