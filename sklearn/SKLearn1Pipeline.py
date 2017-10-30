# coding = utf-8
"""
1.14 管线命令连接多个方法
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/1.md
"""

import numpy as np
from sklearn import datasets
np.set_printoptions(precision=2, edgeitems=3)

iris = datasets.load_iris()
x = iris.data
y = iris.target
xmask = np.random.binomial(1, 0.25, x.shape).astype(np.bool)
x[xmask] = np.nan
print("===== x =====")
print(x)

# 首先补全 iris.data 的缺失值，然后对补全的数据集用 PCA
# 管线命令会让事情更简单

from sklearn import pipeline, preprocessing, decomposition
pca = decomposition.PCA()
imputer = preprocessing.Imputer()
pl = pipeline.Pipeline([("Imputer", imputer), ("PCA", pca)])
xt = pl.fit_transform(x)
print("===== xt =====")
print(xt)
