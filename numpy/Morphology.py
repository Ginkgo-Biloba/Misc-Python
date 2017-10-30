# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage.morphology as mor

# 用于显示形态学处理的结果
def expandImg(img, value, out=None, size=10):
	if out is None:
		w, h = img.shape
		out = np.zeros((w * size, h * size), dtype=np.uint8)
	tmp = np.repeat(np.repeat(img, size, 0), size, 1)
	out[:, :] = np.where(tmp, value, out)
	out[::size, :] = 0
	out[:, ::size] = 0
	return out

def showImg(*imgs):
	for (idx, img) in enumerate(imgs, 1):
		ax = plt.subplot(1, len(imgs), idx)
		plt.imshow(img, cmap="gray")
		ax.axis("off")
	plt.subplots_adjust(0.02, 0, 0.98, 1, 0.02, 0)
	plt.show()

def dilation(a, struc=None):
	b = mor.binary_dilation(a, struc)
	img = expandImg(a, 255)
	return expandImg(np.logical_xor(a, b), 150, out=img)

def dltDemo():
	a = plt.imread("./morphology-A.png").astype(np.uint8)
	img1 = expandImg(a, 255)
	img2 = dilation(a)
	img3 = dilation(a, [[1, 1, 1], [1, 1, 1], [1, 1, 1]])
	showImg(img1, img2, img3)

def erosion(a, struc=None):
    b = mor.binary_erosion(a, struc)
    img = expandImg(a, 255)
    return expandImg(np.logical_xor(a,b), 100, out=img)

def ersDemo():
	a = plt.imread("./morphology-A.png").astype(np.uint8)
	img1 = expandImg(a, 255)
	img2 = erosion(a)
	img3 = erosion(a, [[1, 1, 1], [1, 1, 1], [1, 1, 1]])
	showImg(img1, img2, img3)

if (__name__ == "__main__"):
	dltDemo()
	ersDemo()