import cv2
import numpy as np

im1 = cv2.imread(r"..\Images\2.jpg")
im2 = cv2.imread(r"..\Images\opencv-logo2.jpg")

height, width, channels = im2.shape
roi = im1[0:height, 0:width] # 左上角

# 创建遮罩
im2gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(im2gray, 200, 255, cv2.THRESH_BINARY_INV)
mask_inv = cv2.bitwise_not(mask)

im1_bg = cv2.bitwise_and(roi, roi, mask = mask_inv)
im2_fg = cv2.bitwise_and(im2, im2, mask = mask)

dst = cv2.add(im1_bg, im2_fg)
im1[0:height, 0:width] = dst

cv2.imshow('res', im1)
cv2.waitKey(2000)
cv2.destroyAllWindows()
