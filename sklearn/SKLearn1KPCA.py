# coding = utf-8
"""
1.11 核 PCA 非线性降维
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/1.md
"""

# 准备两个不同的过程 (process) 数据 A B

import numpy as np
_A1Mean = np.array([1, 1])
_A1Cov = np.array([[2, 0.99], [1, 1]])
_A1 = np.random.multivariate_normal(_A1Mean, _A1Cov, 50)
_A2Mean = np.array([5, 5])
_A2Cov = np.array([[2, 0.99], [1, 1]])
_A2 = np.random.multivariate_normal(_A2Mean, _A2Cov, 50)
A = np.vstack((_A1, _A2))

_BMean = np.array([5, 0])
_BCov = np.array([[0.5, -1], [0.9, -0.5]])
B = np.random.multivariate_normal(_BMean, _BCov, 100)

# 显示

from matplotlib import pyplot
pyplot.style.use("ggplot")
(fig, ax) = pyplot.subplots(figsize=(7, 7))
ax.set_title("$A$ and $B$ processes")
ax.scatter(A[:,0], A[:, 1], color="magenta", alpha=0.7)
ax.scatter(B[:,0], B[:, 1], color="blue", alpha=0.7)
fig.show()

# 看起来明显是两个不同的过程数据，但是用一超平面分割它们很难
# 因此，我们用前面介绍带余弦核的核PCA来处理

from sklearn.decomposition import KernelPCA
kpca = KernelPCA(kernel="cosine", n_components=1)
AB = np.vstack((A, B))
ABTrans = kpca.fit_transform(AB)
_AColor = np.array(["magenta"]*A.shape[0])
_BColor = np.array(["blue"]*B.shape[0])
cs = np.hstack((_AColor, _BColor))

# 用 PCA 做对比
from sklearn.decomposition import PCA
pca = PCA(n_components=1)
ABTransPCA = pca.fit_transform(AB)

(fig, ax) = pyplot.subplots(nrows=2, ncols=1, figsize=(7, 7))
fig.subplots_adjust(hspace=0.3)
ax[0].set_title("$A$ 和 $B$ 的 1 维余弦核 PCA")
ax[0].scatter(ABTrans, np.zeros_like(ABTrans), color=cs, alpha=0.7)
ax[1].set_title("$A$ 和 $B$ 的 1 维 PCA")
ax[1].scatter(ABTransPCA, np.zeros_like(ABTransPCA), color=cs, alpha=0.7)
fig.show()

