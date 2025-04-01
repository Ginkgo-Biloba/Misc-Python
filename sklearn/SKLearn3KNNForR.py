# coding = utf-8
"""
3.9 将 kNN 用于回归
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/3.md
"""
import numpy as np
from sklearn import datasets
iris = datasets.load_iris()
print(iris.feature_names)
x = iris.data[:, [0, 1]]
y = iris.data[:, 2]

# 使用线性回归做对比
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(x, y)
lrPred = lr.predict(x)
print("lr MSE: {:f}".format(np.power(y - lrPred, 2).mean()))

# 使用 kNN 回归
from sklearn.neighbors import KNeighborsRegressor
knnr = KNeighborsRegressor(n_neighbors=10)
knnr.fit(x, y)
knnrPred = knnr.predict(x)
print("knnr MSE: {:f}".format(np.power(y - knnrPred, 2).mean()))

# 使用最近的 10 个点用于回归
from matplotlib import pyplot as plt
plt.style.use("ggplot")
(fig, ax) = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(7, 7))
ax[0].scatter(x[:, 0], x[:, 1], s=lrPred*10, label="线性回归预测", color="orange")
ax[0].legend()
ax[0].set_title("预测")
ax[1].scatter(x[:, 0], x[:, 1], s=knnrPred*10, label="$k$-NN 回归预测", color="green")
ax[1].legend()
fig.tight_layout()
fig.show()


