# coding = utf-8
"""
2.3 用岭回归 (Ridge Regression) 弥补线性回归的不足
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/2.md
"""

# 建一个有 3 个自变量的数据集，但是其秩为 2
# 因此 3 个自变量中有 2 个自变量存在相关性
from sklearn.datasets import make_regression
(rdata, rtarget) = make_regression(n_samples=2000, n_features=3, effective_rank=2, noise=10)

# 首先使用普通的线性回归拟合

import numpy as np
from sklearn.linear_model import LinearRegression
lr = LinearRegression()

def fit2Regression(lr, data, target):
	nBootstraps = 1000
	coef = np.ones((nBootstraps, 3))
	subSampleSize = np.int(0.75 * data.shape[0])
	idxSample = np.arange(0, data.shape[0])
	for i in range(nBootstraps):
		idx = np.random.choice(idxSample, size=subSampleSize)
		subX = data[idx]
		subY = target[idx]
		lr.fit(subX, subY)
		coef[i][0] = lr.coef_[0]
		coef[i][1] = lr.coef_[1]
		coef[i][2] = lr.coef_[2]
	from matplotlib import pyplot as plt
	plt.style.use("ggplot")
	(fig, axes) = plt.subplots(nrows=3, sharex=True, figsize=(7, 5))
	for (i, ax) in enumerate(axes):
		ax.hist(coef[:, i], bins=20, alpha=0.7)
		ax.set_title("第 {} 个系数".format(i))
	fig.tight_layout()
	return coef

coefL = fit2Regression(lr, rdata, rtarget)

# 再使用岭回归拟合，对比结果

from sklearn.linear_model import Ridge
ridge = Ridge()
coefR = fit2Regression(ridge, rdata, rtarget)

print("线性回归方差 {!r}".format(np.var(coefL, axis=0)))
print("岭回归方差 {!r}".format(np.var(coefR, axis=0)))










