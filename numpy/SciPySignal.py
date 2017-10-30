# coding = utf-8
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

"""
remez 是一种迭代算法，它能够找到一个 n 阶多项式，使得在指定的区间中此多项式和指定函数之间的最大误差最小化。
remez 返回经过 remez 算法最优化之后的 FIR 滤波器的系数。此系数和用 firwin 所设计的结果一样是对称的。当 numtaps 为偶数时，所设计的滤波器对于取样频率/2 的响应为 0，因此无法设计出长度为偶数的高通滤波器。
"""
def remezDemo():
	for l in [11, 31, 51, 101, 201]:
		b = signal.remez(l, (0, 0.18, 0.2, 0.5), (0.01, 1))
		(w, h) = signal.freqz(b, 1)
		plt.plot(w/2/np.pi, 20*np.log10(np.abs(h)), label="${}$".format(l))
	plt.legend()
	plt.xlabel(u"正规化频率（周期 / 取样）")
	plt.ylabel(u"幅值 (dB)")
	plt.title(u"remez 设计高通滤波器\n滤波器长度和频率响应的关系")
	plt.show()


"""
下面的程序绘制 6、7 阶巴特沃斯低通滤波器的 S 复平面上的极点
程序中，使用 butter 函数设计巴特沃斯滤波器，缺省情况下它设计的是数字滤波器，为了设计模拟滤波器，需要传递关键字参数 analog=True。
获得传递函数的 b 和 a 的系数之后，通过 tf2zpk 函数将它们转换为零点和极点：
"""
def butterDemo():
	plt.figure(figsize=(5,5))
	(b, a) = signal.butter(6, 1.0, analog=True)
	(z, p, k) = signal.tf2zpk(b, a)
	plt.plot(np.real(p), np.imag(p), "^", label=u"6 阶巴特沃斯极点")
	(b, a) = signal.butter(7, 1.0, analog=True)
	(z, p, k) = signal.tf2zpk(b, a)
	plt.plot(np.real(p), np.imag(p), "s", label=u"7 阶巴特沃斯极点")
	plt.axis("equal")
	plt.legend(loc="center right")
	plt.show()


"""
双线性变换实际上是 s 复平面和 z 复平面上的点的映射变换，它将 s 复平面上的竖线变换成 z 复平面上的圆，而 s 复平面上的 Y 轴对应于z 复平面上的单位圆。
"""
def bilinearDemo():
	fig = plt.figure(figsize=(7,3))
	axs = plt.subplot(121)
	axz = plt.subplot(122)
	for x in np.arange(-3, 4, 1):
		s = x + 1j * np.linspace(-100, 100, 20000)
		z = (2 + s) / (2 - s) # 将 s 复平面映射到 z 复平面，假设采样周期 T = 1
		axs.plot(np.real(s), np.imag(s), label=u"$x={}$".format(x))
		axz.plot(np.real(z), np.imag(z), label=u"$x={}$".format(x))
	axs.set_xlim(-4, 4); axs.legend()
	axz.axis("equal")
	axz.set_ylim(-3, 3); axz.legend()
	plt.show()

# remezDemo()
# butterDemo()
bilinearDemo()
