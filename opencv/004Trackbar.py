import cv2
import numpy as np

def nothing(x):
    pass

img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow("image")
# 跟踪条
cv2.createTrackbar("R", "image", 0, 255, nothing)
cv2.createTrackbar("G", "image", 0, 255, nothing)
cv2.createTrackbar("B", "image", 0, 255, nothing)
# ON/OFF
sw = "0: OFF\n1: ON"
cv2.createTrackbar(sw, "image", 0, 1, nothing)

while 1:
    cv2.imshow("image", img)
    k = cv2.waitKey(20)&0xFF
    if k == 27:
        break
    r = cv2.getTrackbarPos("R", "image")
    g = cv2.getTrackbarPos("G", "image")
    b = cv2.getTrackbarPos("B", "image")
    s = cv2.getTrackbarPos(sw, "image")
    if s == 0:
        img[:] = 0
    else:
        img[:] = [b, g, r]

cv2.destroyAllWindows()
