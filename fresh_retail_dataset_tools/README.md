# FreshRetailNet数据集工具文件夹

此文件夹包含所有与FreshRetailNet-50K数据集相关的处理工具和转换文件，统一管理以提高规范性。

## 包含的文件

### 1. 数据集转换脚本
- **`convert_arrow_to_df.py`** - 将Arrow格式数据转换为DataFrame的原始脚本
- **`load_fresh_retail_dataset.py`** - 从Hugging Face加载数据集的主脚本
- **`simple_fresh_retail_to_df.py`** - 简化的数据集加载和转换工具

### 2. 数据集样本文件
- **`fresh_retail_train_1000.csv`** - 训练集前1000行样本
- **`fresh_retail_train_df.csv`** - 训练集DataFrame转换结果
- **`fresh_retail_eval_500.csv`** - 评估集前500行样本
- **`fresh_retail_eval_df.csv`** - 评估集DataFrame转换结果

### 3. 大数据处理工具
- **`safe_bigdata_processing.py`** - 安全处理大数据集的方案（分批次、流式、采样）

## 数据集基本信息

**FreshRetailNet-50K** 是针对生鲜零售场景的专业数据集：
- **训练集**: 450万条记录（~2.38GB）
- **评估集**: 35万条记录（~185.5MB）
- **特征数**: 19个，涵盖时空、商品、销售、库存、营销、天气等维度

## 主要特征

| 类别 | 特征列 | 说明 |
|------|--------|------|
| 时空 | `city_id`, `store_id`, `dt` | 城市、店铺、日期 |
| 商品 | `product_id`, 三级分类ID | 商品标识和分类 |
| 销售 | `sale_amount`, `hours_sale` | 日销售额 + 24小时销售时序 |
| 库存 | `stock_hour6_22_cnt`, `hours_stock_status` | 库存数量 + 24小时库存状态 |
| 营销 | `discount`, `holiday_flag`, `activity_flag` | 折扣、节假日、活动标志 |
| 天气 | `precpt`, `avg_temperature`, `avg_humidity`, `avg_wind_level` | 降水、温度、湿度、风力 |

## 使用建议

1. **小规模测试**：使用样本文件（`*_1000.csv`、`*_500.csv`）进行快速验证
2. **大数据处理**：使用`safe_bigdata_processing.py`避免内存溢出
3. **完整加载**：使用`simple_fresh_retail_to_df.py`加载完整数据集（注意内存）

## 原始数据位置

原始Arrow格式数据位于：
```
FreshRetailNet_cache/Dingdong-Inc___fresh_retail_net-50_k/default/0.0.0/08c1fab7f9257bc73679d415d65d644165d351d4/
```

## 项目关联

此数据集用于"农产品供应链韧性提升——生鲜超市智能决策系统"项目，支持：
- 真实需求恢复（考虑库存限制）
- 未来7天销量预测
- 最优采购量计算
- 动态定价策略

---
**整理时间**: 2026-04-07  
**目的**: 统一管理FreshRetailNet相关文件，提高项目规范性