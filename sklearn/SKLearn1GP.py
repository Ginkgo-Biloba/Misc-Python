# coding = utf-8
"""
1.15 用正态随机过程 (Gaussian process) 处理回归
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/1.md
"""

import numpy as np
from sklearn import datasets
np.set_printoptions(precision=2, edgeitems=3)

boston = datasets.load_boston()
x = boston.data
y = boston.target
# 选取一些作为训练集
mask = np.random.binomial(1, 0.75, y.shape).astype(np.bool)
nmask = np.logical_not(mask)


from sklearn import gaussian_process
gp = gaussian_process.GaussianProcess()
# 训练
gp.fit(x[mask], y[mask])
print(gp)
# 预测
(yPred, MSE) = gp.predict(x[nmask], eval_MSE=True)
yTruth = y[nmask]
yError = yPred - yTruth
idx = np.arange(yPred.shape[0])

from matplotlib import pyplot
pyplot.style.use("ggplot")
(fig, ax) = pyplot.subplots(nrows=3, figsize=(8, 6))
ax[0].plot(idx, yPred, label="预测值")
ax[0].plot(idx, yTruth, label="实际值")
ax[0].set_title("预测值和真实值")
ax[0].legend(loc="best")
ax[1].plot(idx, yError)
ax[1].set_title("预测残差")
ax[2].hist(yError, bins=30)
ax[2].set_title("残差直方图")
fig.tight_layout()
# fig.add_subplot(hspace=0.1)
fig.show()

# 画出 MSE，代表估计的不准确性
(fig, ax) = pyplot.subplots(figsize=(6, 4))
# ax.plot(idx, yPred, color="r")
ax.errorbar(idx, yPred, yerr=MSE)
ax.set_title("预测值和误差段")
fig.show()

# 换个回归函数和 theta 参数

gp2 = gaussian_process.GaussianProcess(regr="linear", theta0=0.5)
gp2.fit(x[mask], y[mask])
print(gp2)
yPred2 = gp2.predict(x[nmask])
yError2 = yPred2 - yTruth
(fig, ax) = pyplot.subplots(figsize=(6, 4))
ax.hist(yError, label="原始的残差", bins=30, alpha=0.5)
ax.hist(yError2, label="线性相关的残差", bins=30, alpha=0.5)
ax.legend(loc="best")
ax.set_title("残差")
fig.show()

print(np.abs(yError).mean())
print(np.abs(yError2).mean())

