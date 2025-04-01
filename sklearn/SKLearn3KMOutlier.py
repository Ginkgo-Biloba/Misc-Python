# coding = utf-8
"""
3.8 将 KMeans 用于离群点检测
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/3.md
"""
# 生成 100 个点的单个数据块，然后识别 5 个离形心最远的点
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
(x, labels) = make_blobs(100, centers=1)
kms = KMeans(n_clusters=1)
kms.fit(x)

# 识别 5 个最远的点
dist = kms.transform(x)
sortedIdx = np.argsort(dist.ravel())[::-1][:5]
# 移除这些点
nx = np.delete(x, sortedIdx, axis=0)
# 形心位置变化了
nkms = KMeans(n_clusters=1)
nkms.fit(nx)

from matplotlib import pyplot as plt
plt.style.use("ggplot")
(fig, ax) = plt.subplots(figsize=(6, 5))
ax.scatter(x[:, 0], x[:, 1], s=10, label="点")
ax.scatter(kms.cluster_centers_[:, 0], kms.cluster_centers_[:, 1], label="形心", s=50, alpha=0.7)
ax.scatter(x[sortedIdx][:, 0], x[sortedIdx][:, 1], label="极值", s=100, alpha=0.7)
ax.scatter(nkms.cluster_centers_[:, 0], nkms.cluster_centers_[:, 1], label="新的形心", s=50, alpha=0.7)
ax.set_title("单点簇集")
ax.legend(loc="best")
fig.tight_layout()
fig.show()
plt.show()

