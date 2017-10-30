# coding = utf-8
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d as conv2
from skimage import color, data, restoration

astro = color.rgb2gray(data.astronaut())

psf = np.ones((5, 5)) / 25
# 卷积并添加噪声
astro_noisy = conv2(astro, psf, 'same')
astro_noisy += (np.random.poisson(lam=25, size=astro.shape) - 10) / 255.

# 用 Richardson-Lucy 算法修复
deconvolved_RL = restoration.richardson_lucy(astro_noisy, psf, iterations=30)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(8, 5))
plt.gray()

for a in ax:
       a.axis('off')

ax[0].imshow(astro)
ax[0].set_title('原始图像')

ax[1].imshow(astro_noisy)
ax[1].set_title('带噪声图像')

ax[2].imshow(deconvolved_RL, vmin=astro_noisy.min(), vmax=astro_noisy.max())
ax[2].set_title('用 Richardson-Lucy 方法修复')


fig.subplots_adjust(wspace=0.02, hspace=0.2,
                    top=0.95, bottom=0.05, left=0, right=1)
plt.show()
