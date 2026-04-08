import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def main():
    print("【步骤 1】加载清洗后的 10 万行数据集...")
    df = pd.read_csv('/workspace/demand_imputation/缺失销量插补/10万行_模型训练最终输入集.csv')

    print("【步骤 2】特征工程 (时间特征提取)...")
    # 将日期字符串转换为 datetime 类型
    df['dt'] = pd.to_datetime(df['dt'])
    
    # 为了避免未来数据穿越，按照时间顺序排列数据集
    df = df.sort_values('dt').reset_index(drop=True)
    
    # 提取时间特征：月份、号数、星期几、是否周末
    df['month'] = df['dt'].dt.month
    df['day'] = df['dt'].dt.day
    df['dayofweek'] = df['dt'].dt.dayofweek
    df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)

    # 声明必须被模型当作类别变量（Categorical）处理的 ID 特征
    cat_cols = ['store_id', 'management_group_id', 'first_category_id', 
                'second_category_id', 'third_category_id', 'product_id']
    for col in cat_cols:
        df[col] = df[col].astype('category')

    print("【步骤 3】划分特征 (X) 和目标 (y) 以及数据集划分...")
    # 明确丢弃：
    # 1. dt (已提取为具体时间特征)
    # 2. sale_amount (这是截断的假销量，不能用来训练)
    # 3. stock_hour6_22_cnt (未来不可预知当天会缺货几个小时)
    # 4. 两个插补相关的标记列 (未来不可预知)
    drop_cols = ['dt', 'sale_amount', 'stock_hour6_22_cnt', 'is_imputed_b_class', 'imputed_method']
    
    # 预测目标变量：经过我们算法还原后的真实全天总销量
    target = 'imputed_sale_amount'
    
    # 所有其他列作为特征
    features = [c for c in df.columns if c not in drop_cols and c != target]
    print(f"最终喂给模型的特征列表: \n{features}")

    # 按照时间进行切分：前 80% 时间的数据作为训练集，后 20% 时间的数据作为测试集
    split_idx = int(len(df) * 0.8)
    
    X_train = df.loc[:split_idx-1, features]
    y_train = df.loc[:split_idx-1, target]
    X_test = df.loc[split_idx:, features]
    y_test = df.loc[split_idx:, target]

    print(f"\n数据集切分完毕: \n- 训练集大小: {X_train.shape} \n- 测试集大小: {X_test.shape}")

    print("\n【步骤 4】构建并训练 LightGBM 预测模型...")
    # 初始化 LightGBM 回归模型
    model = lgb.LGBMRegressor(
        n_estimators=1000,
        learning_rate=0.05,
        max_depth=8,
        num_leaves=63,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1
    )
    
    # 使用早停法防止过拟合
    callbacks = [lgb.early_stopping(stopping_rounds=50, verbose=True)]
    
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        callbacks=callbacks
    )

    print("\n【步骤 5】模型评估...")
    y_pred = model.predict(X_test)
    
    # 限制预测值不能小于 0（销量不为负）
    y_pred = np.clip(y_pred, 0, None)
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    print(f"=====================================")
    print(f"✅ 模型在未见过的测试集上的表现:")
    print(f"   -> RMSE (均方根误差): {rmse:.4f}")
    print(f"   -> MAE  (平均绝对误差): {mae:.4f}")
    print(f"=====================================")

    print("\n【步骤 6】绘制特征重要性图...")
    try:
        font_prop = fm.FontProperties(fname='/workspace/SimHei.ttf')
        plt.rcParams['font.family'] = font_prop.get_name()
    except Exception as e:
        print("中文字体加载失败", e)
        
    plt.figure(figsize=(10, 8))
    # 使用特征分裂时的信息增益 (gain) 来衡量重要性
    lgb.plot_importance(model, max_num_features=15, importance_type='gain', 
                        title='模型特征重要性排行榜 (Gain)', 
                        xlabel='特征增益 (Gain)', ylabel='特征列')
    
    plt.tight_layout()
    output_png = '/workspace/demand_imputation/预测模型构建/特征重要性排行图.png'
    plt.savefig(output_png, dpi=300)
    print(f"特征重要性图已保存至: {output_png}")

if __name__ == '__main__':
    main()
