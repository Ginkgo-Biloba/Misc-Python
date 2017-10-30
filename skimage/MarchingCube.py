# coding = utf-8
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure
from skimage.draw import ellipsoid

# 生成两个相同的椭圆体水平集
ellip_base = ellipsoid(6, 10, 16, levelset=True)
ellip_double = np.concatenate((ellip_base[:-1, ...], ellip_base[2:, ...]), axis=0)

# 使用行进立方获得椭圆体的表面网格
verts, faces = measure.marching_cubes(ellip_double, 0)

# 显示得到的三角测量网格
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# 巧妙的索引：`verts[faces]` 得到三角测量的集合
mesh = Poly3DCollection(verts[faces])
ax.add_collection3d(mesh)

ax.set_xlabel("$x: a = 6$")
ax.set_ylabel("$y: b = 10$")
ax.set_zlabel("$z: c = 16$")

ax.set_xlim(0, 24)  # a = 6 (两个椭圆体，多乘以 2)
ax.set_ylim(0, 20)  # b = 10
ax.set_zlim(0, 32)  # c = 16

plt.tight_layout()
plt.show()