# coding = utf-8
"""
4.6 使用多类分类来归纳
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/4.md
"""
import numpy as np
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
(x, y) = datasets.make_classification(n_samples=10000, n_classes=3, n_informative=3)
dt = DecisionTreeClassifier()
dt.fit(x, y)
print(dt.predict(x))

# 转向多类分类器的案例中
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
mlr = OneVsRestClassifier(LogisticRegression())
mlr.fit(x, y)
print(mlr.predict(x))





