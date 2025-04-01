# coding = utf-8
"""
1.9 主成分分析降维
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/1.md
"""

# 准备数据

from sklearn import datasets
iris = datasets.load_iris()
x = iris.data
print(x)

# 处理

from sklearn import decomposition
pca = decomposition.PCA()
print(pca)

xpca = pca.fit_transform(x)
print(xpca)
print("pca.explained_variance_ratio_:",pca.explained_variance_ratio_)

# 只转换前 2 维用于显示

from matplotlib import pyplot
pyplot.style.use("ggplot")
pca = decomposition.PCA(n_components=2)
xp = pca.fit_transform(x)
print("xp.shape:", xp.shape)
(fig, ax) = pyplot.subplots(figsize=(7, 7))
ax.scatter(xp[:,0], xp[:, 1], c=iris.target)
ax.set_title("鸢尾花数据集 iris PCA 的前 2 维分量")
print("pca.explained_variance_ratio_:",pca.explained_variance_ratio_)

