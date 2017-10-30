# coding = utf-8
"""
3.6 寻找特征空间中的最接近对象
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/3.md
"""
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.metrics import pairwise
(points, labels) = make_blobs()
dist = pairwise.pairwise_distances(points) # N \times N
# 将点按照接近程度排序，比如寻找最接近第 0 个点的点索引
ranks = np.argsort(dist[0])
print("前 5 个点的索引", ranks[:5])
# 拿到真实的点坐标
print("前 5 个点的坐标")
print(points[ranks[:5]])

