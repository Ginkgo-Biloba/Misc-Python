# coding = utf-8
"""
4.1 使用决策树实现基本的分类
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/4.md
"""
from time import clock
import numpy as np
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier

nFeature = 200
(x, y) = make_classification(n_samples=750, n_features=nFeature, n_informative=5)
idxTrain = np.random.choice([True, False], p=[0.75, 0.25], size=y.shape[0])
nAccuray = list()
xTrain = x[idxTrain]
xTest = x[np.logical_not(idxTrain)]
yTrain = y[idxTrain]
yTest = y[np.logical_not(idxTrain)]
idx = np.arange(1, nFeature + 1)

t1 = clock()
for x in idx:
	dt = DecisionTreeClassifier(max_depth=x)
	dt.fit(xTrain, yTrain)
	yPred = dt.predict(xTest)
	nAccuray.append((yPred == yTest).mean())
t2 = clock()
print("耗时 {:f} 秒".format(t2 - t1))

from matplotlib import pyplot
pyplot.style.use("ggplot")
(fig, ax) = pyplot.subplots(figsize=(7, 5))
ax.plot(idx, nAccuray)
ax.set_xlabel("最大深度")
ax.set_ylabel("正确率 (%)")
ax.set_title("决策树深度的影响")
fig.tight_layout()
fig.show()
