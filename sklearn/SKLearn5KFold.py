# coding = utf-8
"""
5.3 5.4 分层的 k-fold
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/5.md
"""
# 我们使用 NumPy 来创建数据集，其中我们知道底层的均值
# 我们会对半个数据集采样，来估计均值，并看看它和底层的均值有多接近
import numpy as np
from matplotlib import pyplot as plt
plt.style.use("ggplot")
from sklearn.datasets import make_classification
(x, y) = make_classification(n_samples=1000, weights=[1/11])
print(y.mean()) # 大约 90% 多的样本都是 1

# 创建分层 k-fold 对象，并通过每个折叠来迭代
from sklearn import cross_validation as CV
nf = 50
sk = CV.StratifiedKFold(y, n_folds=nf)
ss = CV.ShuffleSplit(n=y.shape[0], n_iter=nf)
sky = list()
ssy = list()

for ((kTrain, kTest), (sTrain, sTest)) in zip(sk, ss):
	sky.append(y[kTrain].mean())
	ssy.append(y[sTrain].mean())

# 画出每个折叠上的比例
(fig, ax) = plt.subplots(figsize=(6, 4))
idx = np.arange(nf)
ax.plot(idx, sky, label="StratifiedKFolds")
ax.plot(idx, ssy, label="ShuffleSplit")
ax.legend(loc="best")
ax.set_title("比较分类属性")
fig.tight_layout()
fig.show()







