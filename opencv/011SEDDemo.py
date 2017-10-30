# coding: utf-8

import numpy as np
import cv2
import matplotlib.pyplot as plt

im = cv2.imread("../Images/fruits.jpg")
im = (im / 255.0).astype(np.float32)
sed = cv2.ximgproc.createStructuredEdgeDetection("../../Flow/model.yml")
edge = sed.detectEdges(im)
cv2.imshow("edge", edge)
cv2.waitKey(7000)
