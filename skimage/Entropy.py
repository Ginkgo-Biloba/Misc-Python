# coding = utf-8
import numpy as np
import matplotlib.pyplot as plt
import skimage
from skimage import color, data, filters, morphology

# 物体检测

noiseMask = 28 * np.ones((128,128), dtype=np.uint8)
noiseMask[32:-32, 32:-32] = 30
noise = noiseMask * np.random.random(noiseMask.shape) - 0.5 * noiseMask
noise += 128
img = noise.astype(np.uint8)
etp = filters.rank.entropy(img, morphology.disk(10))
fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(8, 3))
ax0.imshow(noiseMask)
ax0.set_title("原始图像")
ax1.imshow(noise)
ax1.set_title("噪声图像")
ax2.imshow(etp)
ax2.set_title("局部熵")
fig.tight_layout()

# 纹理检测

img = skimage.img_as_ubyte(data.camera())
fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 4), sharex=True, sharey=True, subplot_kw={"adjustable": "box-forced"})
imgs = ax0.imshow(img, cmap=plt.cm.gray)
ax0.set_title("原始图像")
ax0.axis("off")
fig.colorbar(imgs, ax=ax0)
imgs = ax1.imshow(filters.rank.entropy(img, morphology.disk(5)), cmap=plt.cm.gray)
ax1.set_title("局部熵")
ax1.axis("off")
fig.colorbar(imgs, ax=ax1)
fig.tight_layout()
plt.show()
