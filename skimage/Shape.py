# coding = utf-8
import numpy as np
import matplotlib.pyplot as plt
from skimage import draw

(fig, (ax0, ax1)) = plt.subplots(1, 2, figsize=(10, 6))
img = np.zeros((500, 500, 3), dtype=np.float64)

# 红直线
(rr, cc) = draw.line(120, 123, 20, 40)
img[rr, cc, 0] = 255
# 绿多边形
poly = np.array([(300, 300), (480, 320), (380, 430), (220, 590), (300, 300)])
(rr, cc) = draw.polygon(poly[:, 0], poly[:, 1], img.shape)
img[rr, cc, 1] = 1
# 黄圆
(rr, cc) = draw.circle(200, 200, 100, img.shape)
img[rr, cc, :] = (1, 1, 0)
# 蓝椭圆
(rr, cc) = draw.ellipse(300, 300, 100, 200, img.shape)
img[rr, cc, 2] = 1
# 红圆圈
(rr, cc) = draw.circle_perimeter(120, 400, 15)
img[rr, cc, 0] = 1
# 紫贝塞尔曲线
(rr, cc) = draw.bezier_curve(70, 100, 10, 10, 150, 100, 1)
img[rr, cc, :] = (1, 0, 1)
# 椭圆圈
rr, cc = draw.ellipse_perimeter(120, 400, 60, 20, orientation=np.pi / 4.)
img[rr, cc, :] = (1, 0, 1)
rr, cc = draw.ellipse_perimeter(120, 400, 60, 20, orientation=-np.pi / 4.)
img[rr, cc, :] = (0, 0, 1)
rr, cc = draw.ellipse_perimeter(120, 400, 60, 20, orientation=np.pi / 2.)
img[rr, cc, :] = (1, 1, 1)

ax0.imshow(img, cmap=plt.cm.gray, interpolation="bilinear")
ax0.set_title("未开启抗锯齿")
ax0.set_axis_off()
fig.tight_layout()

img = np.zeros((100, 100), dtype=np.float64)

# 反锯齿直线
(rr, cc, val) = draw.line_aa(12, 12, 20, 50)
img[rr, cc] = val
# 反锯齿圆
(rr, cc, val) = draw.circle_perimeter_aa(60, 40, 30)
img[rr, cc] = val


ax1.imshow(img, cmap=plt.cm.gray, interpolation="bilinear")
ax1.set_title("开启抗锯齿")
ax1.set_axis_off()
fig.tight_layout()

plt.show()

