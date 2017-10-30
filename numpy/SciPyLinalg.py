# coding=utf-8
import numpy as np
from numpy.lib.stride_tricks import as_strided
from scipy import linalg
import matplotlib.pyplot as plt

#plt.rcParams["font.sans-serif"] = ["mlkb"] #用来正常显示中文标签
#plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

def makeData(M, N, noiseScale):
	np.random.seed(1)
	x = np.random.standard_normal(M)
	h = np.random.standard_normal(N)
	y = np.convolve(x, h)
	yn = y + np.random.standard_normal(len(y)) * noiseScale * np.max(y)
	return (x, yn, h)

def solveh(x, y, N):
	X = as_strided(x, shape=(len(x) - N + 1, N), strides=(x.itemsize, x.itemsize))
	Y = y[N-1:len(x)]
	h = linalg.lstsq(X, Y)
	return h[0][:: -1]

def testLstSq():
	(x, yn, h) = makeData(1000, 100, 0.4)
	H = solveh(x, yn, 120)
	H2 = solveh(x, yn, 80)
	(fig, (ax1, ax2)) = plt.subplots(2, 1, figsize=(7, 5))
	ax1.plot(h, linewidth=2, label=u"实际的系统参数")
	ax1.plot(H, linewidth=2, label=u"最小二乘解", alpha=0.7)
	ax1.legend(loc="best", ncol=2)
	ax1.set_xlim(0, len(H))
	ax2.plot(h, linewidth=2, label=u"实际的系统参数")
	ax2.plot(H2, linewidth=2, label=u"最小二乘解", alpha=0.7)
	ax2.legend(loc="best", ncol=2)
	ax2.set_xlim(0, len(H))
	fig.show()

def composite(U, sigma, Vh, n):
	return np.dot(U[:, :n], sigma[:n, np.newaxis] * Vh[:n, :])

def testSVD(imgFile):
	(r, g, b) = np.rollaxis(plt.imread(imgFile), 2).astype(float)
	img = 0.2989 * r + 0.5870 * g + 0.1140 * b
	print(u"图像大小 (行列):", img.shape)
	(U, sigma, Vh) = linalg.svd(img)
	(fig1, ax1) = plt.subplots()
	ax1.semilogy(sigma, lw=1, label=u"$\\Sigma$")
	ax1.legend()
	print("U, simga, Vh:")
	# 组合
	print(U.shape, sigma.shape, Vh.shape)
	img20 = composite(U, sigma, Vh, 20)
	img50 = composite(U, sigma, Vh, 50)
	img200 = composite(U, sigma, Vh, 200)
	(fig2, axs2) = plt.subplots(1, 4, figsize=(10, 4))
	fig2.subplots_adjust(wspace=0.2)
	for ax2, _img in zip(axs2, (img, img20, img50, img200)):
		ax2.imshow(_img, cmap="gray")
		ax2.axis("off")
	plt.show()

if (__name__ == "__main__"):
	# testLstSq()
	testSVD(r"..\Images\melting.jpg")
