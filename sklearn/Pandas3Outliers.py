# coding = utf-8
"""
3 Pandas 离群点
"""

import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("ggplot")

# 从日期创建 DataFrame 作为索引
States = ["NY", "NY", "NY", "NY", "FL", "FL", "GA", "GA", "FL", "FL"]
data = [1.0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
idx = pd.date_range("20120101", periods=10, freq="MS")
df1 = pd.DataFrame(data, index=idx, columns=["Revenue"])
df1["State"] = States
# 创建第二个 DataFrame
data2 = [10.0, 10.0, 9, 9, 8, 8, 7, 7, 6, 6]
idx2 = pd.date_range("20130101", periods=10, freq="MS")
df2 = pd.DataFrame(data2, index=idx2, columns=["Revenue"])
df2["State"] = States
# 合并 DataFrame
df = pd.concat([df1, df2])
df = df.to_period("M")
df.Revenue.plot.bar(lw=1)

# 方法 1
newdf1 = df.copy()
newdf1["x-Mean"] = abs(newdf1["Revenue"] - newdf1["Revenue"].mean())
newdf1["1.96*std"] = 1.96 * newdf1["Revenue"].std()
newdf1["Outlier"] = abs(newdf1["Revenue"] - newdf1["Revenue"].mean()) > 1.96 * newdf1["Revenue"].std()

# 方法 2
# 按照项目分组
newdf2 = df.copy()
State = newdf2.groupby('State')
newdf2['Outlier'] = State.transform(lambda x: abs(x-x.mean()) > 1.96*x.std())

# 方法 3
# 按照项目分组
newdf2 = df.copy()
State = newdf2.groupby('State')
def s(group):
    group['x-Mean'] = abs(group['Revenue'] - group['Revenue'].mean())
    group['1.96*std'] = 1.96*group['Revenue'].std()
    group['Outlier'] = abs(group['Revenue'] - group['Revenue'].mean()) > 1.96*group['Revenue'].std()
    return group
newdf3 = State.apply(s)

# 假设不是高斯分布（如果你绘制它，你会觉得不像）
newdf4 = df.copy()
State = newdf4.groupby('State')
newdf4['Lower'] = State['Revenue'].transform(lambda x: x.quantile(q=.25) - (1.5*(x.quantile(q=.75)-x.quantile(q=.25))))
newdf4['Upper'] = State['Revenue'].transform(lambda x: x.quantile(q=.75) + (1.5*(x.quantile(q=.75)-x.quantile(q=.25))))
newdf4['Outlier'] = (newdf4['Revenue'] < newdf4['Lower']) | (newdf4['Revenue'] > newdf4['Upper'])

