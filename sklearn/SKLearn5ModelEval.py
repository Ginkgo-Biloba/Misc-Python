# coding = utf-8
"""
5.8 回归模型评估
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/5.md
"""
from functools import partial
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("ggplot")
from sklearn import metrics


def yGen(x, m=2, b=1, e=None, s=10):
	"""
	x: 自变量 Independent variable
	k: 斜率 Slope
	b: 截距 Intercept
	e: 误差 Error，给出随机误差
	"""
	if e is None:
		e_i = 0
	elif e is True:
		e_i = np.random.normal(0, s, x.shape)
	else:
		e_i = e
	return (x * m + b + e_i)

N = 100
xs = np.sort(np.random.rand(N))
xs *= 100
yPred = yGen(x=xs, e=True)
yTruth = yGen(x=xs)
(fig, ax) = plt.subplots(figsize=(6, 5))
ax.scatter(xs, yPred, s=10, c="teal", label=r"$\hat{y}$")
ax.plot(xs, yTruth, color="tomato", label=r"$y$")
ax.set_title("适应和基本的处理图示")
ax.legend(loc="best")
fig.tight_layout()
fig.show()

# 计算残差
e_hat = yPred - yTruth
(fig, ax) = plt.subplots(figsize=(6, 5))
ax.hist(e_hat, bins=30, alpha=0.7)
ax.set_title("残差直方图")
fig.tight_layout()
fig.show()

# 度量标准
print("MSE: {:f}".format(metrics.mean_squared_error(yTruth, yPred)))
print("MAD: {:f}".format(metrics.mean_absolute_error(yTruth, yPred)))
print("MSE: {:f}".format(metrics.r2_score(yTruth, yPred)))



