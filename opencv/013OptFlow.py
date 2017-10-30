# coding: utf-8

import numpy as np
import cv2
import time

def LKDemo(filename="../Images/768x576.avi"):
	cap = cv2.VideoCapture(filename)
	# ShiTomasi 角点检测参数
	ftParams = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
	# LK 光流参数
	lkParams = dict(winSize=(15, 15), maxLevel=3, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
	# 随即颜色
	rdc = np.random.randint(0, 255, (100, 3))
	# 第一帧为输入
	ret, frame = cap.read()
	oldGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	p0 = cv2.goodFeaturesToTrack(oldGray, mask=None, **ftParams)
	#创建遮罩图像，画图
	mask = np.zeros_like(frame)

	while (True):
		start = time.clock()
		k = cv2.waitKey(30) & 0xFF
		if (k == 27): break
		ret, frame = cap.read()
		if not ret: break
		frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# 计算光流
		p1, st, err = cv2.calcOpticalFlowPyrLK(oldGray, frameGray, p0, None, **lkParams)
		# 选择好的点
		goodNew = p1[st == 1]
		goodOld = p0[st == 1]
		# 画轨迹
		for (i, (new, old)) in enumerate(zip(goodNew, goodOld)):
			a, b = new.ravel()
			c, d = old.ravel()
			mask = cv2.line(mask, (a, b), (c, d), rdc[i].tolist(), 1)
			frame = cv2.circle(frame, (a, b), 4, rdc[i].tolist(), -1)
		img = np.where(mask == 0, frame, mask)
		cv2.imshow("frame", img)
		# 更新帧
		oldGray = frameGray
		p0 = goodNew.reshape(-1, 1, 2) 
		print(time.clock() - start, "s")

	cv2.destroyAllWindows()
	cap.release()


def FarnebackDemo(filename="../Images/768x576.avi"):
	cap = cv2.VideoCapture(filename)
	ret, frame1 = cap.read()
	prev = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
	hsv = np.zeros_like(frame1)
	hsv[:, :, 1] = 255

	while (True):
		start = time.clock()
		k = cv2.waitKey(30) & 0xFF
		if (k == 27): break
		ret, frame = cap.read()
		if not ret: break
		curr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		flow = cv2.calcOpticalFlowFarneback(prev, curr, None, 0.7, 3, 15, 3, 5, 1.2, 0)
		mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
		hsv[..., 0] = ang * 180 / np.pi / 2
		hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
		bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
		cv2.imshow("frame", bgr)
		prev = curr
		print(time.clock() - start, "s")

	cv2.destroyAllWindows()
	cap.release()

class LKTrack(object):
	def __init__(self, src="../Images/768x576.avi"):
		self.trackLen = 10
		self.detectInterval = 5
		self.tracks = list()
		self.cam = cv2.VideoCapture(src)
		self.frameIndex = 0
		self.ftParams = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
		self.lkParams = dict(winSize=(15, 15), maxLevel=3, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

	def run(self):
		while (True):
			k = cv2.waitKey(10) & 0xFF
			if (k == 27): break
			ret, frame = self.cam.read()
			if not ret: break
			frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			vis = frame.copy()
			if (len(self.tracks) > 0):
				img0, img1 = self.prevGray, frameGray
				p0 = np.float32([tr[-1] for tr in self.tracks])
				p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **self.lkParams)
				p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **self.lkParams)
				d = abs(p0 - p0r).reshape(-1, 2).max(-1)
				good = (d < 1)
				newTracks = list()
				for (tr, (x, y), goodFlag) in zip(self.tracks, p1.reshape(-1, 2), good):
					if not goodFlag:
						continue
					tr.append((x, y))
					if (len(tr) > self.trackLen):
						del tr[0]
					newTracks.append(tr)
					cv2.circle(vis, (x, y), 2, (0, 0, 255), -1)
				self.tracks = newTracks
				cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (255, 0,0 ))
				# common.draw_str(vis, (20, 20), "track count: {}".format(len(self.tracks)))

			if (self.frameIndex % self.detectInterval == 0):
				mask = np.zeros_like(frameGray)
				mask[:] = 255
				for (x, y) in [np.int32(tr[-1]) for tr in self.tracks]:
					cv2.circle(mask, (x, y), 4, (255, 255, 0), -1)
				p = cv2.goodFeaturesToTrack(frameGray, mask=mask, **self.ftParams)
				if (p is not None):
					for (x, y) in np.float32(p).reshape(-1, 2):
						self.tracks.append([(x, y)])
			
			self.frameIndex += 1
			self.prevGray = frameGray
			cv2.imshow("LK Track", vis)


if (__name__ == "__main__"):
	# LKDemo()
	# FarnebackDemo()
	LKTrack().run()

