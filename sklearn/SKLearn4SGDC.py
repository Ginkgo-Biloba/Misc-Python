# coding = utf-8
"""
4.9 使用随机梯度下降来分类
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/4.md
"""
from sklearn.datasets import make_classification
from sklearn.linear_model import SGDClassifier
(x, y) = make_classification()
sgdc = SGDClassifier()
sgdc.fit(x, y)
print(sgdc)



