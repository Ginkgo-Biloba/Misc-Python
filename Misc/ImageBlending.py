# coding = utf-8
import numpy as np
import skimage.io as skio
import matplotlib.pyplot as plt

def blendImg(im1, im2, alpha=0.5, beta=None, gamma=0.0):
	"按百分比混合两张图像"
	if beta is None: beta = 1 - alpha
	im1f = im1.astype(np.float32);
	im2f = im2.astype(np.float32)
	im1f *= alpha; im2f *= beta
	im3f = im1f + im2f
	im3f /= im3f.max(); im3f *= 255.0
	im3 = im3f.astype(np.uint8)
	return im3
	

im1File = r"F:\.实验室相关\论文\cave_2-frame_0002.png"
im2File = r"F:\.实验室相关\论文\cave_2-frame_0003.png"


im1 = skio.imread(im1File); im2 = skio.imread(im2File)
im3 = blendImg(im1, im2)
skio.imsave("cave_2-frame_0002-0003.png", im3)

fig, axes = plt.subplots(3, 1)
for (axis, im) in zip(axes, (im1, im2, im3)):
	axis.imshow(im)
	axis.set_xticks([]); axis.set_yticks([])
plt.show()