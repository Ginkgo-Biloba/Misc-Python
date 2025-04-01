# coding: utf-8

import numpy as np
import cv2
import time

time.clock()
MIN_MATCH_COUNT = 10
img1 = cv2.imread("../Images/box.png") # Query
img2 = cv2.imread("../Images/box_in_scene.png") # Train
print(time.clock())

surf = cv2.xfeatures2d.SURF_create()
kp1, dscp1 = surf.detectAndCompute(img1, None)
kp2, dscp2 = surf.detectAndCompute(img2, None)
print(time.clock())

FLANN_INDEX_KDTREE = 0
indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
searchParams = dict(checks=50)

flann = cv2.FlannBasedMatcher(indexParams, searchParams)

matches = flann.knnMatch(dscp1, dscp2, k=2)

good = list()
for (m, n) in matches:
    if m.distance < 0.7 * n.distance:
        good.append(m)

if len(good) > MIN_MATCH_COUNT:
    queryPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    trainPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    M, mask = cv2.findHomography(queryPts, trainPts, cv2.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()
    h, w, d = img1.shape
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)
    img2 = cv2.polylines(img2, [np.int32(dst)], True, (0, 0, 255), 1, cv2.LINE_AA)
else:
    print("匹配的点数不够", len(good), "<", MIND_MATCH_COUNT)
    matchesMask = None
print(time.clock())

# Finally we draw our inliers (if successfully found the object) or matching keypoints (if failed).
drawParams = dict(matchColor=(255, 0, 0), singlePointColor=None, matchesMask=matchesMask, flags=2)
img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **drawParams)
cv2.imshow("images", img3)
cv2.waitKey(0)
