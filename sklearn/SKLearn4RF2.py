# coding = utf-8
"""
4.4 调整随机森林模型
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/4.md
"""
import numpy as np
from sklearn.datasets import make_classification
(x, y) = make_classification(n_samples=10000, n_features=20, n_informative=15, flip_y=0.5, weights=[0.2, 0.8])
idxTrain = np.random.choice([True, False], p=[0.8, 0.2], size=y.shape)
xTrain = x[idxTrain]
xTest = x[np.logical_not(idxTrain)]
yTrain = y[idxTrain]
yTest = y[np.logical_not(idxTrain)]

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(xTrain, yTrain)
yPred = rf.predict(xTest)
print("精度 {:f}".format((yPred == yTest).mean()))

# 使用混淆矩阵
from sklearn.metrics import confusion_matrix
maxFeatureParam = ["auto", "sqrt", "log2", 0.01, 0.5, 0.99]
cfs = dict()
for mf in maxFeatureParam:
	rf = RandomForestClassifier(max_features=mf)
	rf.fit(xTrain, yTrain)
	cfs[mf] = confusion_matrix(yTest, rf.predict(xTest)).ravel()

# 查看混淆矩阵
import itertools
import matplotlib.pyplot as plt
plt.style.use("ggplot")
import pandas as pd
(fig, ax) = plt.subplots(figsize=(6, 5))
cfdf = pd.DataFrame(cfs)
cfdf.plot(kind="bar", ax=ax)
ax.legend(loc="best")
ax.set_title("猜测类别 $i$ 和正确类别 $j$: $(i, j)$")
ax.set_xticklabels([str((i, j)) for (i, j) in list(itertools.product(range(2), range(2)))], rotation="horizontal")
ax.set_xlabel("猜测 / 正确")
ax.set_ylabel("数量")
fig.tight_layout()
fig.show()

# 我们可以从混淆矩阵的迹除以总和来计算准确度
n_estimator_params = range(1, 20)
confusion_matrixes = {}
accuracy = lambda x: np.trace(x) / np.sum(x, dtype=np.float32)
for n_estimator in n_estimator_params:
	rf = RandomForestClassifier(n_estimators=n_estimator)
	rf.fit(xTrain, yTrain)
	curr_cm = confusion_matrix(yTest, rf.predict(xTest))
	confusion_matrixes[n_estimator] = accuracy(curr_cm)
accuracy_series = pd.Series(confusion_matrixes)
(fig, ax) = plt.subplots(figsize=(6, 4))
accuracy_series.plot(kind='bar', ax=ax)
ax.set_xticklabels(ax.get_xticklabels(), rotation="horizontal")
ax.set_ylim(0, 1) # 完整范围
ax.set_ylabel("精度")
ax.set_xlabel("估计器数量")
ax.set_title("使用不同数量估计器时的精度")
fig.tight_layout()
fig.show()

