# coding = utf-8
"""
2.1 线性回归 (Linear Regression)
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/2.md
"""
from sklearn import datasets
boston = datasets.load_boston()

# 建立线性回归模型
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
# 传入自变量和因变量
lr.fit(boston.data, boston.target)
print(lr)
# LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
# 评估模型和残差 (Residuals)
pred = lr.predict(boston.data)
res = boston.target - pred

# 均方误差 (Mean Squared Error，MSE)
# 平均绝对误差 (Mean Absolute Deviation，MAD)
import numpy as np
mad = np.mean(np.abs(res))
mse = np.mean(res * res)
print("平均平方误差 {:f}".format(mad))
print("平均绝对误差 {:f}".format(mse))

# 画出残差
from matplotlib import pyplot as plt
plt.style.use("ggplot")
(fig, ax) = plt.subplots(nrows=2, figsize=(8, 6))
idx = np.arange(pred.shape[0])
ax[0].plot(idx, pred, lw=1, label="预测值")
ax[0].plot(idx, boston.target, lw=1, label="实际值")
ax[0].plot(idx, res, lw=1, label="残差")
ax[0].legend(loc="best")
ax[0].set_title("预测值、实际值、残差")
ax[1].hist(res, bins=40, label="线性回归残差")
ax[1].set_title("残差直方图")
ax[1].legend(loc="best")
fig.tight_layout()
fig.show()

# 分位数概率分布 (Quantile-Quantile, Q-Q) 图
from scipy.stats import probplot
(fig, ax) = plt.subplots(figsize=(7, 5))
probplot(res, plot=ax)
ax.set_title("Probability Plot")
fig.tight_layout()
fig.show()
