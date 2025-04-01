# coding = utf-8
"""
1.13 用字典学习分解法分类
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/1.md
"""

import numpy as np
from sklearn import datasets

iris = datasets.load_iris()
x = iris.data
y = iris.target

from sklearn.decomposition import DictionaryLearning
dl = DictionaryLearning(3)
xt1 = dl.fit_transform(x[::2])
# print("===== xt1 =====")
# print(xt1)

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.style.use("ggplot")
cs = np.array(["magenta", "orange", "green"])
fig = plt.figure()
# ax = fig.add_subplot(111, projection="3d")
ax = Axes3D(fig)
ax.set_title("训练集")
ax.scatter(xt1[:, 0], xt1[:, 1], xt1[:, 2], color=cs[y[::2]])
fig.show()

# 用 transform 而不是 fit_transform 来训练

xt2 = dl.transform(x[1::2])
fig = plt.figure()
# ax = fig.add_subplot(111, projection="3d")
ax = Axes3D(fig)
ax.set_title("训练集 2")
ax.scatter(xt2[:, 0], xt2[:, 1], xt2[:, 2], color=cs[y[1::2]])
fig.show()



