import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, mean_absolute_error

print("Loading Group 4 Dataset...")
train = pd.read_csv('/workspace/group4_dataset/train_group4.csv')
eval_df = pd.read_csv('/workspace/group4_dataset/eval_group4.csv')

# Feature Sets
# 1. Base features (weather, promo, etc.)
base_features = ['discount', 'holiday_flag', 'activity_flag', 'precpt', 
                 'avg_temperature', 'avg_humidity', 'avg_wind_level']

# 2. All 7 ID features
all_id_features = ['city_id', 'store_id', 'management_group_id', 
                   'first_category_id', 'second_category_id', 
                   'third_category_id', 'product_id']

# 3. Minimal ID features (Drop redundant ones based on hierarchy)
# Since store_id determines city and group, and product_id determines all categories.
minimal_id_features = ['store_id', 'product_id']

# Function to train and evaluate
def evaluate_model(features, name):
    print(f"\n--- Training Proxy Model: {name} ---")
    print(f"Features ({len(features)}): {features}")
    
    # Define categorical features for LightGBM
    cat_features = [f for f in features if f.endswith('_id')]
    
    X_train = train[features]
    y_train = train['sale_amount']
    X_eval = eval_df[features]
    y_eval = eval_df['sale_amount']
    
    # Convert ID columns to 'category' type for LightGBM
    for col in cat_features:
        X_train.loc[:, col] = X_train[col].astype('category')
        X_eval.loc[:, col] = X_eval[col].astype('category')
    
    model = lgb.LGBMRegressor(
        objective='regression',
        n_estimators=100,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1
    )
    
    # Train
    model.fit(
        X_train, y_train,
        eval_set=[(X_eval, y_eval)],
        categorical_feature=cat_features,
        callbacks=[lgb.early_stopping(stopping_rounds=10, verbose=False)]
    )
    
    # Predict
    preds = model.predict(X_eval)
    
    # Metrics
    rmse = np.sqrt(mean_squared_error(y_eval, preds))
    mae = mean_absolute_error(y_eval, preds)
    
    print(f"[{name}] Results:")
    print(f"RMSE: {rmse:.5f}")
    print(f"MAE:  {mae:.5f}")
    
    # Return feature importance
    importance = pd.DataFrame({
        'Feature': features,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    
    return rmse, mae, importance

# Experiment A: Use ALL features
rmse_all, mae_all, imp_all = evaluate_model(base_features + all_id_features, "Model A (All 7 IDs)")

# Experiment B: Drop redundant IDs (Simultaneous Drop)
rmse_min, mae_min, imp_min = evaluate_model(base_features + minimal_id_features, "Model B (Only store_id & product_id)")

print("\n================ SUMMARY ================")
print(f"Model A (14 features) RMSE: {rmse_all:.5f} | MAE: {mae_all:.5f}")
print(f"Model B ( 9 features) RMSE: {rmse_min:.5f} | MAE: {mae_min:.5f}")
diff = (rmse_min - rmse_all) / rmse_all * 100
print(f"RMSE Change: {diff:+.2f}%")

print("\nTop 5 Important Features in Model A:")
print(imp_all.head())

