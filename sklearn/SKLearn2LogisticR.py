# coding = utf-8
"""
2.7 逻辑回归 (LogisticRegression)
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/2.md
"""

import numpy as np
import matplotlib.pyplot as plt
plt.style.use("ggplot")

x = np.linspace(-5, 5, 50)
y = 1 / (np.exp(-x) + 1)
# y = np.apply_along_axis(lambda x: 1 / (1 + np.exp(-x)), 0, x)
(fig, ax) = plt.subplots(figsize=(7,5))
ax.plot(x, y)
ax.set_title("Logistic 函数")

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
(x, y) = make_classification(n_samples=1000, n_features=4)
xTrain = x[:-200]; xTest = x[-200:]
yTrain = y[:-200]; yTest = y[-200:]
lr = LogisticRegression()
lr.fit(xTrain, yTrain)
yPredTrain = lr.predict(xTrain)
yPredTest = lr.predict(xTest)

rTrain = (yPredTrain == yTrain).sum() / float(yTrain.shape[0])
print("训练集预测正确的比例：{:f}".format(rTrain))
rTest = (yPredTest == yTest).sum() / float(yTest.shape[0])
print("测试集预测正确的比例：{:f}".format(rTest))




