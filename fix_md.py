import re

with open('/workspace/marketing_features_analysis/Marketing_Features_EDA_Report.md', 'r') as f:
    content = f.read()

old_text = """### 方案 A：业务直觉驱动的“特征交叉相乘”（Feature Crossing）
- **实现方式**：构造新特征 `real_activity_discount = discount * activity_flag`。
- **业务解释性**：
  - 当 `activity_flag = 0`（无活动）时，乘积为 0。
  - 当 `activity_flag = 1`（有活动）时，乘积为真实的折扣率（如 0.8）。"""

new_text = """### 方案 A：业务直觉驱动的“条件特征构造”（Conditional Feature Engineering）
- **实现方式**：绝不能直接相乘！正确的构造公式为 `real_activity_discount = np.where(activity_flag == 1, discount, 1.0)`，即 `discount * activity_flag + 1.0 * (1 - activity_flag)`。
- **业务解释性与避坑**：
  - **直接相乘的灾难**：如果直接相乘，无活动（flag=0）时结果为 0，在折扣语境下 0 代表“免费/0元购”，这会让模型产生极其严重的误判（以为平时没活动的东西都是免费送的）。
  - **正确的逻辑**：当 `activity_flag = 0`（无活动）时，强制该特征等于 **1.0**（代表原价/不打折）。
  - 当 `activity_flag = 1`（有活动）时，取真实的折扣率（如 0.8）。"""

if old_text in content:
    content = content.replace(old_text, new_text)
    with open('/workspace/marketing_features_analysis/Marketing_Features_EDA_Report.md', 'w') as f:
        f.write(content)
    print("Markdown file updated successfully.")
else:
    print("Could not find the text to replace.")
