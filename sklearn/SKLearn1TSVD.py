# coding = utf-8
"""
1.12 截断奇异值分解降维
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/1.md
截断奇异值分解 (Truncated singular value decomposition, TSVD) 是一种矩阵因式分解技术，将矩阵 M 分解成 U、\Sigma 和 V。
它与 PCA 很像，只是 SVD 分解是在数据矩阵上进行，而 PCA 是在数据的协方差矩阵上进行。
"""

# 用 iris 数据集
from sklearn import datasets
iris = datasets.load_iris()
x = iris.data
y = iris.target
print(x)

# 分解
from sklearn.decomposition import TruncatedSVD
tsvd = TruncatedSVD(n_components=2)
xTrans = tsvd.fit_transform(x)
print(xTrans)

# 结果
from matplotlib import pyplot
pyplot.style.use("ggplot")
(fig, ax) = pyplot.subplots()
ax.scatter(xTrans[:,0], xTrans[:, 1], c=y, alpha=0.7)
ax.set_title("截断奇异值分解：2 维")
