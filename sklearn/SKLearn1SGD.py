# coding = utf-8
"""
1.15 用随机梯度下降 (Stochastic Gradient Descent) 处理回归
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/1.md
"""

import numpy as np
from sklearn import datasets
np.set_printoptions(precision=2, edgeitems=3)

# SGD 适合大数据集
(x, y) = datasets.make_regression(1000000)
print("x: {:,} bytes".format(x.nbytes))
train = np.random.binomial(1, 0.75, x.shape[0]).astype(np.bool)
pred = np.logical_not(train)

from sklearn import linear_model
sgd = linear_model.SGDRegressor()
sgd.fit(x[train], y[train])
print(sgd)
yPred = sgd.predict(x[pred])
yError = yPred - y[pred]

from matplotlib import pyplot
pyplot.style.use("ggplot")
(fig, ax) = pyplot.subplots(figsize=(7, 5))
ax.hist(yError, bins=30, label="线性残差", alpha=0.7)
ax.set_title("残差")
ax.legend(loc="best")
fig.tight_layout()
fig.show()

