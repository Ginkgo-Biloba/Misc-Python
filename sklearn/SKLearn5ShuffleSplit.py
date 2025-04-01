# coding = utf-8
"""
5.3 使用 ShuffleSplit 交叉验证
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/5.md
"""
# 我们使用 NumPy 来创建数据集，其中我们知道底层的均值
# 我们会对半个数据集采样，来估计均值，并看看它和底层的均值有多接近
import numpy as np
from matplotlib import pyplot as plt
plt.style.use("ggplot")

tLoc = 1000
tScale = 10
n = 1000
x = np.random.normal(tLoc, tScale, n)
(fig, ax) = plt.subplots(figsize=(6, 4))
ax.hist(x, histtype="bar", alpha=0.7)
ax.set_title("数据集直方图")
fig.tight_layout()
fig.show()

# 截取前一半数据集，并计算均值
xholdout = x[:n//2]
xfitting = x[n//2:]
estMean = xfitting.mean()
(fig, ax) = plt.subplots(figsize=(6, 4))
ax.vlines(tLoc, 0, 1, color="teal", label="真实平均值")
ax.vlines(estMean, 0, 1, color="orange", label="估计平均值")
ax.set_xlim(tLoc-1, tLoc+1)
ax.legend(loc="best")
ax.set_title("数据集直方图")
fig.tight_layout()
fig.show()

# 使用 ShuffleSplit 在多个相似的数据集上拟合估计值
from sklearn.cross_validation import ShuffleSplit
ss = ShuffleSplit(xfitting.shape[0])
pMean = list()
for (t, _) in ss:
	pMean.append(xfitting[t].mean())
se = np.mean(pMean)
(fig, ax) = plt.subplots(figsize=(6, 4))
ax.vlines(tLoc, 0, 1, color="teal", alpha=1, label="真实平均值")
ax.vlines(estMean, 0, 1, color="orange", alpha=1, label="估计平均值")
ax.vlines(se, 0, 1, color="crimson", alpha=1, label="随机分割估计")
ax.set_xlim(tLoc-1, tLoc+1)
ax.legend(loc="best")
ax.set_title("数据集直方图")
fig.tight_layout()
fig.show()


