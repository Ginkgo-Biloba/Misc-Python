# coding = utf-8
"""
pandas csv 文件读写
"""
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import time

plt.style.use("ggplot")

# 读取显示
csvFile = r"comptagevelo2012.csv"
df = pd.read_csv(csvFile, encoding="utf-8", parse_dates=["Date"], dayfirst=True, index_col="Date")
df.drop(df.columns[0], axis=1, inplace=True)
fig, ax = plt.subplots(figsize=(10,6))
fig.suptitle(csvFile)
df.plot(ax=ax, linewidth=1)
# df.plot(ax=ax, subplots=True, sharex = True, linewidth=1)

# 看看 Berri 一周每天的骑车的情况
secCol = "Berri1"
berri1 = df[[secCol]]
berri1.insert(len(berri1.columns), "Weekday", berri1.index.weekday)
# berri1["Weekday"] = berri1.index.weekday
weekDayCnt = berri1.groupby("Weekday").aggregate(np.sum)
weekDayCnt.index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
fig, ax = plt.subplots(figsize=(6,4))
weekDayCnt.plot(ax=ax, kind="bar")
ax.set_title(secCol)
fig.tight_layout()
