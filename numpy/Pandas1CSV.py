# coding = utf-8
"""
(1) Pandas 读写 csv 文件
From: https://github.com/wizardforcel/pandas-official-tutorials-zh/blob/master/3.1.md
"""
import pandas as pd
from matplotlib import pyplot as plt
plt.style.use("bmh")

# 创建数据

# 5 个婴儿名称和数量 (1980 年)
_names = ['Bob','Jessica','Mary','John','Mel']
_births = [968, 155, 77, 578, 973]
babyDataSet = list(zip(_names, _births))
df = pd.DataFrame(data=babyDataSet, columns=["Names", "Births"])
# print("\n===== df ====="); print(df)

# 读写文件
# df.to_csv("birth1980.csv", index=False, header=False)
# 数据并没有标题，设置 header 为 None 或者指定 names
# df = pd.read_csv("birth1980.csv", header=None)
# df = pd.read_csv("birth1980.csv", names=["Names", "Births"])

#寻找最受欢迎的名称
dfSorted = df.sort_values(["Births"], ascending=False)
# print("\n=== dfSorted ====="); print(dfSorted)
maxName = dfSorted["Names"].head(1).values[0]
maxValue = dfSorted["Births"].head(1).values[0]
text = str(maxName) + ": " + str(maxValue)
ax = df["Births"].plot.bar()
ax.set_xticks(pd.np.arange(5))
ax.set_xticklabels(df["Names"].values, rotation="horizontal")
ax.annotate(text, xy=(1, maxValue), xytext=(-75, -10), xycoords=("axes fraction", "data"), textcoords="offset pixels")
ax.set_title("流行的名字")
ax.figure.show()
