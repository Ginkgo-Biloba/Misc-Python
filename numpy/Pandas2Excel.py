# coding = utf-8
"""
(2) 读写 Excel 文件
From: https://github.com/wizardforcel/pandas-official-tutorials-zh/blob/master/3.3.md
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("ggplot")

# 设置种子
np.random.seed(111)

# 生成测试数据的函数
def CreateDataSet(Number=1):
	Output = list()
	for i in range(Number):
		# 创建按周（周一）的数据范围
		rng = pd.date_range(start='2009-01-01', end='2012-12-31', freq='W-MON')
		# 创建随机数据
		data = np.random.randint(low=25,high=1000,size=len(rng))
		# 状态池
		status = np.array([1,2,3], dtype=np.int32)
		# 创建状态的随机列表
		random_status = status[np.random.randint(low=0, high=len(status), size=len(rng), dtype=np.int32)]
		# 州池
		states = np.array(['GA','FL','fl','NY','NJ','TX'], dtype=np.str)
		# 创建州的随机列表
		random_states = states[np.random.randint(low=0, high=len(states), size=len(rng))]
		Output.extend(zip(random_states, random_status, data, rng))
	return Output

# 创建一些数据
dataset = CreateDataSet(4)
df = pd.DataFrame(data=dataset, columns=['State','Status','CustomerCount','StatusDate'])
df = df.set_index("StatusDate")

# 读写 Excel。算了，没装 xlrd xlwt
# df.to_excel(__file__.replace("py", "xlsx"), index=False)
# df = pd.read_excel(__file__.replace("py", "xlsx"), 0, index_col="StatusDate")

"""
此部分尝试清理要分析的数据
	1. 确保 State 列全部大写
	2. 仅选择帐户状态等于 1 的记录
	3. 在 State 列中合并 NJ 和 NY 为 NY
	4. 删除任何异常值（数据集中的任何奇怪结果）
"""

# 清理 State 列，转换为大写
df['State'] = df.State.apply(lambda x: x.upper())
# 仅仅抓取 Status == 1 的值
dfMask = (df.Status == 1)
df = df[dfMask]
# 将 NJ 变为 NY
dfMask = (df.State == 'NJ')
df['State'][dfMask] = 'NY'
# 查看 CustomerCount
# df.CustomerCount.plot(figsize=(10, 7), kind="line")
df.CustomerCount.plot.line(figsize=(10, 7))
sortdf = df[df.State == "NY"].sort_index(axis=0)












