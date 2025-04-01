# coding = utf-8
"""
3.5 使用 KMeans 聚类来量化图像
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/3.md
"""
import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt

img = ndimage.imread(r"Butterfly.jpg")
(fig, ax) = plt.subplots(figsize=(5, 6))
ax.imshow(img)
ax.axis("off")
fig.show()

# 拉展像素到一行，然后聚类
(x, y, z) = img.shape
flatImg = img.reshape(x * y, z)

from sklearn import cluster
kMeans = cluster.KMeans(n_clusters=10)
kMeans.fit(flatImg)
centers = kMeans.cluster_centers_
# print(centers)

# 标签关联不关联
labels = kMeans.labels_
(fig, ax) = plt.subplots(figsize=(5, 6))
ax.imshow(centers[labels].reshape(x, y, z))
ax.axis("off")
fig.show()
