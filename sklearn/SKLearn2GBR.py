# coding = utf-8
"""
2.9 用梯度提升回归 (Gradient boosting regression, GBR) 从误差中学习
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/2.md
"""
from sklearn.datasets import make_regression
(x, y) = make_regression(1000, 2, noise=20)

# 梯度提升回归
from sklearn.ensemble import GradientBoostingRegressor
gbr = GradientBoostingRegressor()
gbr.fit(x, y)
gbrPred = gbr.predict(x)
gbrRes = gbrPred - y

# 普通线性回归
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(x, y)
lrPred = lr.predict(x)
lrRes = lrPred - y

# 画出误差
from matplotlib import pyplot as plt
plt.style.use("ggplot")
(fig, ax) = plt.subplots(figsize=(7,5))
ax.hist(gbrRes, bins=40, label="梯度提升回归", alpha=0.5)
ax.hist(lrRes, bins=40, label="线性回归", alpha=0.5)
ax.set_title("残差对比")
ax.legend()
fig.tight_layout()
fig.show()

import numpy as np
print("GBR 95% 置信区间", np.percentile(gbrRes, [2.5, 97.5]))
print("LR 95% 置信区间", np.percentile(lrRes, [2.5, 97.5]))

