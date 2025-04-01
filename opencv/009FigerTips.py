import cv2
import numpy as np

def skinExtract(img):
	ycbcr = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
	[y, cb, cr] = cv2.split(ycbcr)
	skin = np.zeros((img.shape[:2]), np.uint8)

	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			# 肤色大致范围
			if(138 <= cr[x, y] and cr[x, y] <=170 and 100 <= cb[x, y] and cb[x, y] <= 127):
				skin[x, y] = 255
			else:
				skin[x, y] = 0
	
	# 膨胀去除空洞，腐蚀消除突起
	skin = cv2.dilate(skin, np.ones((15, 15), np.uint8))
	skin = cv2.erode(skin, np.ones((15, 15), np.uint8))
	return skin

if __name__ == "__main__":
	im = cv2.imread("../Images/hand.jpg", cv2.IMREAD_COLOR)
	if (im.shape[0] == 0):
		print("没有图片 hand.jpg")
		exit(1)
	im = cv2.GaussianBlur(im, (3, 3), 1)
	skin = skinExtract(im)
	im2 = im; # 后面显示
	cv2.imshow("skin", skin)

	im, contours, hierarchy = cv2.findContours(skin, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
	# 找到最大的轮廓
	index = 0
	maxArea = 0.0
	for i in range(len(contours)):
		area = cv2.contourArea(contours[i])
		if (area > maxArea):
			maxArea = area
			index = i
	# 计算矩，找重心
	print ("maxArea:", maxArea)
	mo = cv2.moments(skin, True)
	center = (int(mo["m10"] / mo["m00"]), int(mo["m01"] / mo["m00"]))
	cv2.circle(im2, center, 8, (0, 0, 255), -1)
	
	# 寻找指尖
	cou = contours[index][0]
	maxM = 0
	count = 0
	notice = 0
	fingerTips = list()
	for i in range(20, len(cou) - 20, 2):
		q = cou[i - 20]; p = cou[i]; r = cou[i + 20]
		pqx = p[0] - q[0]; pqy = p[1] - q[1]
		prx = p[0] - r[0]; pry = p[1] - r[1]
		dot = pqx * pqy + prx + pry
		if (dot < -20 or dot > 20):
			cross = pqx * pry - prx* pqy
			if cross > 0:
				fingerTips.append(p)
				cv2.circle(im2, tuple(p), 5, (255, 0, 0), cv2.FILLED)
				cv2.line(im2, center, p, (255, 0, 0), 2)

	skin = cv2.drawContours(skin, contours[index], 0, (0, 255, 255))
	cv2.imshow("contours", skin)
	cv2.imshow("show", im2)
	while (cv2.waitKey() & 0xFF != ord('q')):
		pass

	# return fingerTips
	# 失败
