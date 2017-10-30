# coding=utf-8
import numpy as np
from scipy import ndimage as nimg
import matplotlib.pyplot as plt

def filterDemo():
	""" 热点图 """
	(h, w) = (500, 500)
	xs = list(); ys = list()
	for i in range(100):
		wm = w * np.random.rand()
		hm = h * np.random.rand()
		mean = (wm, hm)
		a = 50 + np.random.randint(50, 200)
		b = 50 + np.random.randint(50, 200)
		c = (a + b) * np.random.normal() * 0.1
		cov = [[a, c], [c, b]]
		count = 200
		(x, y) = np.random.multivariate_normal(mean, cov, size=count).T
		xs.append(x)
		ys.append(y)
	x = np.concatenate(xs); y = np.concatenate(ys)
	hist, junk1, junk2 = np.histogram2d(x, y, bins=(np.arange(0, w), np.arange(0, h)))
	hist = hist.T
	heat = nimg.gaussian_filter(hist, 10.0)
	heatN = plt.Normalize()(heat)
	heatRGB = plt.cm.jet(heatN)
	heatRGB[:, :, -1] = heatN
	plt.imshow(heatRGB)
	plt.show()


if (__name__ == "__main__"):
	filterDemo()

