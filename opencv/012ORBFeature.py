# coding=utf-8

import numpy as np
import cv2
import pylab as pl


def ORBDemo(filename="../Images/building.jpg"):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
	orb = cv2.ORB_create()
	kp = orb.detect(img, None) # 用 ORB 找关键点
	kp, dscp = orb.compute(img, kp) # 计算描述子

	img2 = cv2.drawKeypoints(img, kp, None, color=(200, 150, 100))
	pl.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB), cmap="gray");
	pl.show()
	# cv2.imwrite("orb.jpg", img2)

def ORBBF(filenames=["../Images/box.png", "../Images/box_in_scene.png"]):
	img1 = cv2.imread(filenames[0], cv2.IMREAD_GRAYSCALE) # Query
	img2 = cv2.imread(filenames[1], cv2.IMREAD_GRAYSCALE) # Train
	orb = cv2.ORB_create()
	kp1, dscp1 = orb.detectAndCompute(img1, None)
	kp2, dscp2 = orb.detectAndCompute(img2, None)
	# 暴力匹配
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
	matches = bf.match(dscp1, dscp2)
	matches = sorted(matches, key=lambda x: x.distance)
	# 画前 20 个匹配
	img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:20], img1, flags=2)
	pl.figure(1); pl.imshow(img3); pl.show()

def ORBFLANN(filenames=["../Images/box.png", "../Images/box_in_scene.png"]):
	""" ORB 不能有距离比检验 失败"""
	img1 = cv2.imread(filenames[0], cv2.IMREAD_GRAYSCALE) # Query
	img2 = cv2.imread(filenames[1], cv2.IMREAD_GRAYSCALE) # Train
	orb = cv2.ORB_create()
	kp1, dscp1 = orb.detectAndCompute(img1, None)
	kp2, dscp2 = orb.detectAndCompute(img2, None)
	
	FLANN_INDEX_KDTREE = 0
	indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
	searchParams = dict(chech=50) # 或者空字典使用默认值
	flann = cv2.FlannBasedMatcher(indexParams, searchParams)
	matches = flann.knnMatch(dscp1, dscp2, k=2)

	# 创建遮罩，只画好的匹配
	mask = [[0, 0] for i in range(len(matches))]
	# 距离比检验
	for (i, (m, n)) in enumerate(matches):
		if m.distance < 0.7 * n.distance:
			mask[i] = [1, 0]

	drawParams = dict(matchColor=(0, 0, 255), singlePointColor=(255, 0, 0), matchMask=mask, flags=0)
	img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, img1, **drawParams)
	cv2.imshow("ORB FLANN", img3)

	img3 = np.zeros(img1.shape)
	img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, img3, flags=2)
	pl.figure(1); pl.imshow(img3); pl.show()


if (__name__ == "__main__"):
	ORBFLANN()
