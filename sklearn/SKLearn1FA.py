# coding = utf-8
"""
1.10 因子分析 (分解) 降维
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/1.md
"""

# 准备数据

from sklearn import datasets
iris = datasets.load_iris()
x = iris.data
print(x)

# 只使用前 2 个因子用于显示

from sklearn import decomposition
fa = decomposition.FactorAnalysis(n_components=2)
xf = fa.fit_transform(x)
print("xp.shape:", xf.shape)

from matplotlib import pyplot
pyplot.style.use("ggplot")
(fig, ax) = pyplot.subplots(figsize=(7, 7))
ax.scatter(xf[:,0], xf[:, 1], c=iris.target)
ax.set_title("鸢尾花数据集 iris FA 的前 2 个因子")
print(fa.components_)

