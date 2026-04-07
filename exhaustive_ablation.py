import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import mean_squared_error
from datasets import load_dataset
import warnings
warnings.filterwarnings('ignore')

print("1. Loading dataset from Hugging Face...")
dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")
train_df = dataset['train'].to_pandas()
eval_df = dataset['eval'].to_pandas()

print("2. Extracting Management Group 1 (~100k rows) for exhaustive LOO ablation...")
train_g1 = train_df[train_df['management_group_id'] == 1].copy()
eval_g1 = eval_df[eval_df['management_group_id'] == 1].copy()

# Feature Engineering for 'dt' -> 'dayofweek' (0-6)
train_g1['dt'] = pd.to_datetime(train_g1['dt'])
eval_g1['dt'] = pd.to_datetime(eval_g1['dt'])
train_g1['dayofweek'] = train_g1['dt'].dt.dayofweek
eval_g1['dayofweek'] = eval_g1['dt'].dt.dayofweek

# Target
target = 'sale_amount'

# Exclude target, 'dt' (parsed), 'hours_sale' (list), 'hours_stock_status' (list)
# We include 'stock_hour6_22_cnt' and the new 'dayofweek'
features = [
    'city_id', 'store_id', 'management_group_id', 
    'first_category_id', 'second_category_id', 'third_category_id', 'product_id',
    'discount', 'holiday_flag', 'activity_flag', 
    'precpt', 'avg_temperature', 'avg_humidity', 'avg_wind_level',
    'stock_hour6_22_cnt', 'dayofweek'
]

cat_features = [f for f in features if f.endswith('_id')] + ['dayofweek', 'holiday_flag', 'activity_flag']

# Convert types
for col in cat_features:
    train_g1[col] = train_g1[col].astype('category')
    eval_g1[col] = eval_g1[col].astype('category')

def run_lgbm(drop_col=None):
    current_features = [f for f in features if f != drop_col]
    current_cats = [f for f in cat_features if f != drop_col]
    
    model = lgb.LGBMRegressor(
        objective='regression',
        n_estimators=1000,
        learning_rate=0.05,
        random_state=42,
        n_jobs=-1,
        verbose=-1
    )
    
    model.fit(
        train_g1[current_features], train_g1[target],
        eval_set=[(eval_g1[current_features], eval_g1[target])],
        categorical_feature=current_cats,
        callbacks=[lgb.early_stopping(stopping_rounds=30, verbose=False)]
    )
    
    preds = model.predict(eval_g1[current_features])
    return np.sqrt(mean_squared_error(eval_g1[target], preds))

print("\n--- Training Baseline (ALL Features) ---")
base_rmse = run_lgbm(None)
print(f"Baseline RMSE: {base_rmse:.6f}\n")

print("--- Starting Leave-One-Out (LOO) Ablation Study ---")
results = []
for col in features:
    rmse = run_lgbm(col)
    change = (rmse - base_rmse) / base_rmse * 100
    results.append({'Dropped_Feature': col, 'RMSE': rmse, 'Change_%': change})
    print(f"Dropped {col:<20} | RMSE={rmse:.6f} | Change={change:+.4f}%")

res_df = pd.DataFrame(results).sort_values('Change_%', ascending=False)
res_df.to_csv('/workspace/exhaustive_ablation_results.csv', index=False)

print("\n================ FINAL RANKING ================")
print("If Change% > 0: Feature is USEFUL (dropping it hurts model)")
print("If Change% < 0: Feature is REDUNDANT/NOISY (dropping it helps model)\n")
print(res_df.to_string(index=False))
