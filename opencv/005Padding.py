import cv2
import numpy as np
from matplotlib import pyplot as plt

PURPLE = [255, 0, 255]
img = cv2.imread('..\Images\opencv-logo2.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

replicate = cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_REPLICATE)
reflect = cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_REFLECT)
reflect101 = cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_REFLECT_101)
wrap = cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_WRAP)
constant = cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=PURPLE)

plt.subplot(231), plt.imshow(img, 'gray'), plt.title("original")
plt.subplot(232), plt.imshow(replicate, 'gray'), plt.title("replicate")
plt.subplot(233), plt.imshow(reflect, 'gray'), plt.title("reflect")
plt.subplot(234), plt.imshow(reflect101, 'gray'), plt.title("reflect_101")
plt.subplot(235), plt.imshow(wrap, 'gray'), plt.title("wrap")
plt.subplot(236), plt.imshow(constant, 'gray'), plt.title("constant")

plt.show()
