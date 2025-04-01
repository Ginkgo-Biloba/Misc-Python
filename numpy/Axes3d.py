# coding = utf-8
"""
绘制三维图形
"""

from mpl_toolkits.mplot3d import axes3d
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np

# style.use("ggplot")

# 散点图
fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')
x = [1,2,3,4,5,6,7,8,9,10]
y = [5,6,7,8,2,5,6,3,7,2]
z = [1,2,6,3,2,7,3,3,7,2]
x2 = [-1,-2,-3,-4,-5,-6,-7,-8,-9,-10]
y2 = [-5,-6,-7,-8,-2,-5,-6,-3,-7,-2]
z2 = [1,2,6,3,2,7,3,3,7,2]
ax1.scatter(x, y, z, c='g', marker='o')
ax1.scatter(x2, y2, z2, c ='r', marker='o')
ax1.set_xlabel('$x$')
ax1.set_ylabel('$y$')
ax1.set_zlabel('$z$')
fig.show()

# 条形图
fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')
x3 = [1,2,3,4,5,6,7,8,9,10]
y3 = [5,6,7,8,2,5,6,3,7,2]
z3 = np.zeros(10)
dx = np.ones(10)
dy = np.ones(10)
dz = [1,2,3,4,5,6,7,8,9,10]
ax1.bar3d(x3, y3, z3, dx, dy, dz, color="#CC99AA")
ax1.set_xlabel('$x$')
ax1.set_ylabel('$y$')
ax1.set_zlabel('$z$')
fig.show()

# 线框图
fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')
x, y, z = axes3d.get_test_data()
print(axes3d.__file__)
ax1.plot_wireframe(x,y,z, rstride = 3, cstride = 3)
ax1.set_xlabel('$x$')
ax1.set_ylabel('$y$')
ax1.set_zlabel('$z$')
plt.show()