import cv2
import numpy as np

im = cv2.imread(r"..\Images\opencv-logo2.jpg")
imhsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
# 设置阈值
lBlue = np.array([110, 220, 200])
uBlue = np.array([130, 255, 255])
# 阈值化图像
mask = cv2.inRange(imhsv, lBlue, uBlue)
# 应用遮罩
res = cv2.bitwise_and(im, im, mask=mask)

cv2.imshow('im', im)
cv2.imshow('mask', mask)
cv2.imshow('res', res)

cv2.waitKey(0)
cv2.destroyAllWindows()

print(mask.shape)
