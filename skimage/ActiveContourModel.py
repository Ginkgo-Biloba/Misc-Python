# coding = utf-8
import numpy as np
import matplotlib.pyplot as plt
import scipy
from skimage import color, data, filters, segmentation

# 图片
img = data.astronaut()
img = color.rgb2gray(img)
s = np.linspace(0, 2*np.pi, 400)
x = 220 + 100 * np.cos(s)
y = 100 + 100 * np.sin(s)
init = np.array([x, y]).T
snake = segmentation.active_contour(filters.gaussian(img, 3), init, alpha=0.015, beta=10, gamma=0.001)
fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111)
ax.imshow(img, cmap=plt.cm.gray)
ax.plot(x, y, "--r", lw=2)
ax.plot(snake[:, 0], snake[:, 1], "-g", lw=2)
ax.set_axis_off()
fig.tight_layout()

# 文字
img = data.text()
x = np.linspace(5, 424, 100)
y = np.linspace(136, 50, 100)
init = np.array([x, y]).T
snake = segmentation.active_contour(filters.gaussian(img, 1), init, bc="fixed", alpha=0.1, beta=1.0, w_line=-5, w_edge=0, gamma=0.1)
fig = plt.figure(figsize=(7, 4))
ax = fig.add_subplot(111)
ax.imshow(img, cmap=plt.cm.gray)
ax.plot(x, y, "--r", lw=2)
ax.plot(snake[:, 0], snake[:, 1], "-g", lw=2)
ax.set_axis_off()
fig.tight_layout()

plt.show()
