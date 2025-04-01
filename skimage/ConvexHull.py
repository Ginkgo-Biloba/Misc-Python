# coding = utf-8
"""
凸包是包围图像中白色像素的最小（面积？周长？）凸多边形
"""

import numpy as np
import matplotlib.pyplot as plt
from skimage import color, data, util, filters, morphology

# 反转颜色，物体必须为白色
img = 255 - data.horse()[:, :, 1]
chull = morphology.convex_hull_image(img)
blend = util.img_as_float(chull)
blend[np.where(img > 0)] = 2
fig, ax = plt.subplots()
ax.imshow(blend, interpolation="bilinear")
ax.set_title("图像和凸包")
ax.set_axis_off()
plt.show()