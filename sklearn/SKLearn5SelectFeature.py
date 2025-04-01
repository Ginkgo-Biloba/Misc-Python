# coding = utf-8
"""
5.9 特征选取
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/5.md
"""
import numpy as np
from sklearn import datasets
from sklearn import feature_selection

(x, y) = datasets.make_regression(n_samples=1000, n_features=10000)
(f, p) = feature_selection.f_regression(x, y)
print(f[:7])
print(p[:7])
# f 就是和每个线性模型的特征之一相关的 f 分数
# 我们之后可以比较这些特征，并基于这个比较，我们可以筛选特征
# p 是 f 值对应的 p 值。在统计学中，p 值是一个值的概率
# 我们可以看到，许多 p 值都太大了。我们更想让 p 值变小
# 并且选取小于 0.05 的 p 值。这些就是我们用于分析的特征

idx = np.arange(0, x.shape[1])
ftKeep = idx[p < 0.05]
print(ftKeep.shape)

# 另一个选择是使用VarianceThreshold对象
varTh = feature_selection.VarianceThreshold(np.median(np.var(x, axis=1)))
print(varTh.fit_transform(x).shape)

# 绘制 p 值，可以看到筛选和保留那些特征
import matplotlib.pyplot as plt
plt.style.use("ggplot")
(fig, ax) = plt.subplots(figsize=(6, 4))
ax.bar(np.arange(100), p[:100])
ax.set_title("p 值的分布")
fig.tight_layout()
fig.show()


