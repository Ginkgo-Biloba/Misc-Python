# coding = utf-8
"""
3.1 KMeans 聚类
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/3.md
"""
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
(blobs, classes) = make_blobs(500, centers=3)
kmeans = KMeans(n_clusters=3)
kmeans.fit(blobs)
print("===== kmeans =====")
print(kmeans)
print("===== kmeans.cluster_centers_ =====")
print(kmeans.cluster_centers_)

import numpy as np
import matplotlib.pyplot as plt
plt.style.use("ggplot")
(fig, ax) = plt.subplots(figsize=(6, 5))
cs = np.array(["magenta", "blue", "green"])
for i in range(3):
	p = blobs[classes == i]
	ax.scatter(p[:, 0], p[:, 1], s=10, label="Cluster {}".format(i), color=cs[i], alpha=0.7)
ax.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], marker="*", s=200, color="orange", label="Centers")
ax.set_title("Blobs")
ax.legend(loc="best")
fig.tight_layout()
fig.show()

# 轮廓距离
from sklearn import metrics
slt = metrics.silhouette_samples(blobs, kmeans.labels_)
print("===== np.column_stack((classes[:5], slt[:5])) =====")
print(np.column_stack((classes[:5], slt[:5])))
print("轮廓系数的均值", slt.mean())
(fig, ax) = plt.subplots(figsize=(6, 5))
ax.hist(slt, bins=40, alpha=0.7)
ax.set_title("轮廓距离采样直方图")
fig.tight_layout()
fig.show()

# 训练多个簇的模型，看看平均得分
(blobs, classes) = make_blobs(500, centers=10)
sltAvg = list()
for k in range(2, 50):
	kmeans = KMeans(n_clusters=k).fit(blobs)
	sltAvg.append(metrics.silhouette_score(blobs, kmeans.labels_))
(fig, ax) = plt.subplots(figsize=(6, 5))
ax.plot(sltAvg)
fig.tight_layout()
fig.show()

