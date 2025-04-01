# coding = utf-8
import numpy as np
from skimage.transform import (hough_line, hough_line_peaks, probabilistic_hough_line)
from skimage.feature import canny
from skimage import data
import matplotlib.pyplot as plt
from matplotlib import cm

# 构建测试图像
image = np.zeros((100, 100))
idx = np.arange(25, 75)
image[idx[::-1], idx] = 255
image[idx, idx] = 255

# 经典的直线 Hough 变换
h, theta, d = hough_line(image)

fig, axes = plt.subplots(1, 3, figsize=(15, 6),subplot_kw={'adjustable': 'box-forced'})
ax = axes.ravel()

ax[0].imshow(image, cmap=cm.gray)
ax[0].set_title("输入图像")
ax[0].set_axis_off()

ax[1].imshow(np.log(1 + h), extent=[np.rad2deg(theta[-1]), np.rad2deg(theta[0]), d[-1], d[0]],cmap=cm.gray, aspect=1/1.5)
ax[1].set_title("Hough 变换")
ax[1].set_xlabel("角度 (度)")
ax[1].set_ylabel("距离 (像素)")
ax[1].axis("off")

ax[2].imshow(image, cmap=cm.gray)
for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
	y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
	y1 = (dist - image.shape[1] * np.cos(angle)) / np.sin(angle)
	ax[2].plot((0, image.shape[1]), (y0, y1), '-r')
ax[2].set_xlim((0, image.shape[1]))
ax[2].set_ylim((image.shape[0], 0))
ax[2].set_axis_off()
ax[2].set_title("检测的直线")
fig.tight_layout()

# 使用概率 Hough 变换
image = data.camera()
edges = canny(image, 2, 1, 25)
lines = probabilistic_hough_line(edges, threshold=10, line_length=5, line_gap=3)
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=True, sharey=True)
ax = axes.ravel()
ax[0].imshow(image, cmap=cm.gray)
ax[0].set_title("输入图像")
ax[1].imshow(edges, cmap=cm.gray)
ax[1].set_title("Canny 边缘")
ax[2].imshow(edges * 0)
for line in lines:
	p0, p1 = line
	ax[2].plot((p0[0], p1[0]), (p0[1], p1[1]))
ax[2].set_xlim((0, image.shape[1]))
ax[2].set_ylim((image.shape[0], 0))
ax[2].set_title("概率 Hough 变换")
for a in ax:
	a.set_axis_off()
	a.set_adjustable('box-forced')
fig.tight_layout()

plt.show()