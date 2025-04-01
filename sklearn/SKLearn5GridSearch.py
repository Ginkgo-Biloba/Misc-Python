# coding = utf-8
"""
5.5 菜鸟的网格搜索
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/5.md
"""
# 我们使用 NumPy 来创建数据集，其中我们知道底层的均值
# 我们会对半个数据集采样，来估计均值，并看看它和底层的均值有多接近
import numpy as np
from matplotlib import pyplot as plt
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
import itertools

criteria = ["gini", "entropy"]
maxFeatures = ["auto", "log2", None]
(x, y) = datasets.make_classification(n_samples=2000, n_features=10)
idxTrain = np.random.binomial(1, 0.5, y.shape).astype(np.bool)
xTrain = x[idxTrain]
xTest = x[np.logical_not(idxTrain)]
yTrain = y[idxTrain]
yTest = y[np.logical_not(idxTrain)]
accuracies = dict()
for (ct, mf) in itertools.product(criteria, maxFeatures):
	dt = DecisionTreeClassifier(criterion=ct, max_features=mf)
	dt.fit(xTrain, yTrain)
	accuracies[(ct, mf)] = (dt.predict(xTest) == yTest).mean()
print("\n========== accuracies ==========")
print(accuracies)

# 画图
plotArray = list()
for mf in maxFeatures:
	m = list()
	for ct in criteria:
		m.append(accuracies[(ct, mf)])
	plotArray.append(m)
(fig, ax) = plt.subplots(figsize=(4, 4))
ax.set_xticklabels(["AAA"] + criteria)
ax.set_yticklabels(["BBB"] + maxFeatures)
cb = ax.matshow(plotArray, vmin=np.min(list(accuracies.values()))-0.1, vmax=np.max(list(accuracies.values()))+0.1, cmap=plt.cm.jet)
fig.colorbar(cb)
fig.tight_layout()
fig.show()

# 5.6 爆破网格搜索
# 我们需要下列步骤来开始：
# 1. 创建一些数据集
# 2. 之后创建LogisticRegression对象，训练我们的模型
# 3. 之后，我们创建搜索对象，GridSearch和RandomizedSearchCV

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
(x, y) = datasets.make_classification(1000, n_features=5)
lr = LogisticRegression(class_weight="balanced")
lr.fit(x, y)
print("\n========== lr ==========")
print(lr)
gridSearchParam = {"penalty": ["l1", "l2"], "C": [1, 2, 3, 4]}
gs = GridSearchCV(lr, gridSearchParam)
gs.fit(x, y)
print("\n========== gs ==========")
print(gs)
print("\n========== gs.cv_results_ ==========")
print(gs.cv_results_)





