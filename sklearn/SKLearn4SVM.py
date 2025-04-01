# coding = utf-8
"""
4.5 使用支持向量机 (SVM) 对数据分类
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/4.md
"""
import numpy as np
from sklearn import datasets
from sklearn.svm import LinearSVC
(x, y) = datasets.make_blobs(n_features=2, centers=2)
lsvc = LinearSVC()
lsvc.fit(x, y)

# 可视化
from itertools import product
db = list() # decisonBoundary = list()
for (xpt, ypt) in product(np.linspace(x[: ,0].min(), x[:, 0].max()), np.linspace(x[:, 1].min(), x[:, 1].max())):
	db.append([xpt, ypt, lsvc.predict([xpt, ypt])])
db = np.array(db)

import matplotlib.pyplot as plt
plt.style.use("ggplot")
cs = np.array(["tomato", "teal"])
(fig, ax) = plt.subplots(figsize=(6, 5))
ax.scatter(x[:, 0], x[:, 1], c=cs[y])
ax.scatter(db[:, 0], db[:, 1], c=cs[db[:, 2].astype(np.int32)], alpha=0.2)
ax.set_title("一个好的可分离数据集")
fig.tight_layout()
fig.show()


# 另一个例子，这次决策边界不是那么清晰
(x, y) = datasets.make_classification(n_features=2, n_classes=2, n_informative=2, n_redundant=0)
lsvc.fit(x, y)
xTest = np.array([[xx, yy] for (xx, yy) in product(np.linspace(x[: ,0].min(), x[:, 0].max()), np.linspace(x[:, 1].min(), x[:, 1].max()))])
xPred = lsvc.predict(xTest)
(fig, ax) = plt.subplots(figsize=(6, 5))
ax.scatter(x[:, 0], x[:, 1], c=cs[y])
ax.scatter(xTest[:, 0], xTest[:, 1], c=cs[xPred], alpha=0.2)
ax.set_title("一个好的可分离数据集")
fig.tight_layout()
fig.show()

# 使用径向基函数的 SVC
from sklearn.svm import SVC
(x, y) = datasets.make_blobs(n_features=2, centers=2)
xTest = np.array([[xx, yy] for (xx, yy) in product(np.linspace(x[: ,0].min(), x[:, 0].max()), np.linspace(x[:, 1].min(), x[:, 1].max()))])
rsvc = SVC(kernel="rbf")
rsvc.fit(x, y)
xPred = rsvc.predict(xTest)
(fig, ax) = plt.subplots(figsize=(6, 5))
ax.scatter(x[:, 0], x[:, 1], c=cs[y])
ax.scatter(xTest[:, 0], xTest[:, 1], c=cs[xPred], alpha=0.2)
ax.set_title("使用径向基函数的 SVM")
fig.tight_layout()
fig.show()

