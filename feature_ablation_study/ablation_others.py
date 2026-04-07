import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

print("Loading Group 4 Dataset for Comprehensive Single Ablation...")
train = pd.read_csv('/workspace/group4_dataset/train_group4.csv')
eval_df = pd.read_csv('/workspace/group4_dataset/eval_group4.csv')

base_features = ['discount', 'holiday_flag', 'activity_flag', 'precpt', 
                 'avg_temperature', 'avg_humidity', 'avg_wind_level']

all_id_features = ['city_id', 'store_id', 'management_group_id', 
                   'first_category_id', 'second_category_id', 
                   'third_category_id', 'product_id']

# The 5 features we suspect are redundant because store_id & product_id cover them
suspected_redundant = ['management_group_id', 'city_id', 
                       'first_category_id', 'second_category_id', 'third_category_id']

def train_and_eval(drop_cols):
    features = base_features + [f for f in all_id_features if f not in drop_cols]
    cat_features = [f for f in features if f.endswith('_id')]
    
    X_train = train[features].copy()
    y_train = train['sale_amount']
    X_eval = eval_df[features].copy()
    y_eval = eval_df['sale_amount']
    
    for col in cat_features:
        X_train[col] = X_train[col].astype('category')
        X_eval[col] = X_eval[col].astype('category')
        
    model = lgb.LGBMRegressor(
        objective='regression',
        n_estimators=100,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1,
        verbose=-1
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

print("\nTraining Baseline (All 14 Features)...")
rmse_base, mae_base = train_and_eval([])
print(f"Baseline RMSE = {rmse_base:.6f} | MAE = {mae_base:.6f}\n")

print("Testing removal of each suspected redundant feature INDIVIDUALLY:")
print("-" * 65)
print(f"{'Dropped Feature':<25} | {'RMSE':<10} | {'Change (%)':<10}")
print("-" * 65)

for col in suspected_redundant:
    rmse, mae = train_and_eval([col])
    diff_rmse = (rmse - rmse_base) / rmse_base * 100
    print(f"{col:<25} | {rmse:.6f}   | {diff_rmse:+.4f}%")

print("-" * 65)
