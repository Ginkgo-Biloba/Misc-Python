# coding=utf-8
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter
import numpy as np

x = np.arange(0, 4*np.pi, 0.01)
y = np.sin(x)
plt.figure(figsize=(8,4))
plt.plot(x, y)
ax = plt.gca()

def pi_formatter(x, pos):
	"""
	比较罗嗦地将数值转换为以pi/4为单位的刻度文本
	"""
	eqstr = "$"
	m = int(x / (np.pi / 4))
	n = 4
	if m%2==0: m, n = int(m/2), int(n/2)
	if m%2==0: m, n = int(m/2), int(n/2)
	if m == 0:
		eqstr += "0"
	elif m == 1 and n == 1:
		eqstr += r"\pi"
	elif n == 1:
		eqstr += (str(m) + r"\pi")
	elif m == 1:
		eqstr += (r"\frac{\pi}{" + str(n) + r"}")
	else:
		eqstr += (r"\frac{" + str(m) + r"\pi}{" + str(n) + r"}")
	eqstr += "$"
	return eqstr

# 设置两个坐标轴的范围
plt.ylim(-1.5,1.5)
plt.xlim(0, np.max(x))

# 设置图的底边距
plt.subplots_adjust(bottom = 0.15)

plt.grid() #开启网格

# 主刻度为pi/4
ax.xaxis.set_major_locator( MultipleLocator(np.pi/4) )

# 主刻度文本用pi_formatter函数计算
ax.xaxis.set_major_formatter( FuncFormatter( pi_formatter ) )

# 副刻度为pi/20
ax.xaxis.set_minor_locator( MultipleLocator(np.pi/20) )

# 设置刻度文本的大小
for tick in ax.xaxis.get_major_ticks():
	tick.label1.set_fontsize(16)
plt.show()