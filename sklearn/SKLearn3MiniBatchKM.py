# coding = utf-8
"""
3.4 使用 MiniBatch KMeans 处理更多数据
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/3.md
"""
from time import clock
from sklearn.datasets import make_blobs
(blobs, labels) = make_blobs(1000000, 3)

from sklearn.cluster import KMeans, MiniBatchKMeans
kmeans = KMeans(n_clusters=3)
minibatch = MiniBatchKMeans(n_clusters=3)

t1 = clock()
kmeans.fit(blobs)
t2 = clock()
print("kmeans.fit: {:f} 秒".format(t2 - t1))

t1 = clock()
minibatch.fit(blobs)
t2 = clock()
print("kmeans.fit: {:f} 秒".format(t2 - t1))

# 形心
print("kmeans.cluster_centers_[0]",kmeans.cluster_centers_[0])
print("minibatch.cluster_centers_[0]", minibatch.cluster_centers_[0])

# 两个聚类的形心间距
from sklearn.metrics import pairwise
print("第 0 个形心间距", pairwise.pairwise_distances(kmeans.cluster_centers_[0], minibatch.cluster_centers_[0]))
print("对角线包含形心的差异", np.diag(pairwise.pairwise_distances(kmeans.cluster_centers_, minibatch.cluster_centers_)))




