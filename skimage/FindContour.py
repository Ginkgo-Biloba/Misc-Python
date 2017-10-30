# coding = utf-8
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure

# 构建测试数据
(x, y) = np.ogrid[-np.pi:np.pi:100j, -np.pi:np.pi:100j]
r = np.sin(np.exp((np.sin(x)**3 + np.cos(y)**2)))

# 发现值为 0.6 的轮廓 (等高线)
contours = measure.find_contours(r, 0.6)

# 显示图像并画轮廓
fig, ax = plt.subplots()
ax.imshow(r, interpolation="bilinear", cmap=plt.cm.gray)
for (n, contours) in enumerate(contours):
	ax.plot(contours[:, 1], contours[:, 0], linewidth=2)
ax.axis("off")
ax.set_xticks([])
ax.set_yticks([])
plt.show()


