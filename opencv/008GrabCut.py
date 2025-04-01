# coding=utf-8

import numpy as np
import cv2
from matplotlib import pyplot as plt

def gc1():
	img = cv2.imread("11.jpg", cv2.IMREAD_COLOR)
	mask = np.zeros(img.shape[:2], np.uint8)
	# img.shape -> (480, 640, 3)
	bgdModel = np.zeros((1, 65), np.float64)
	fgdModel = np.zeros((1, 65), np.float64)
	rect = (80, 180, 65, 65)

	cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 12, cv2.GC_INIT_WITH_RECT)

	mask2 = np.where((mask==2)|(mask==0), 0, 1).astype("uint8")
	img2 = img * mask2[:,:,np.newaxis]
	cv2.imwrite("FolwS.png", img2)

	plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
	plt.colorbar()
	plt.show()

def gc2():
	plt.figure(1)
	img = cv2.imread("../Images/DSC01266.JPG", cv2.IMREAD_COLOR)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
	h, s, v = cv2.split(hsv)
	vMin, vMax, vMinIdx, vMaxIdx = cv2.minMaxLoc(v)
	v = (np.uint8)(255 * (v - vMin) / (vMax - vMin))
	hsv = cv2.merge([h,s,v])
	img2 = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)


	plt.subplot(2,3,1); plt.imshow(img, "gray")
	plt.title("Image"); plt.xticks([]); plt.yticks([])
	plt.subplot(2,3,2); plt.imshow(img2, "gray")
	plt.title("Image Edited"); plt.xticks([]); plt.yticks([])
	plt.subplot(2,3,4); plt.imshow(h, "gray");
	plt.title("Hue"); plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,5); plt.imshow(s, "gray")
	plt.title("Saturation"); plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,6); plt.imshow(v, "gray")
	plt.title("Value"); plt.xticks([]), plt.yticks([])
	plt.show()


if __name__ == "__main__":
	gc1()
