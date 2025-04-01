# coding: utf-8

import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

def flow2img(flow, BGR=True):
	x, y = flow[..., 0], flow[..., 1]
	hsv = np.zeros((flow.shape[0], flow.shape[1], 3), dtype = np.uint8)
	ma, an = cv2.cartToPolar(x, y, angleInDegrees=True)
	hsv[..., 0] = (an / 2).astype(np.uint8)
	hsv[..., 1] = (cv2.normalize(ma, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)).astype(np.uint8)
	hsv[..., 2] = 255
	if BGR:
		img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
	else:
		img = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
	return img

startT = time.clock()
im1 = cv2.imread("../../Middlebury/TrainImages/Dimetrodon_10.png")
im2 = cv2.imread("../../Middlebury/TrainImages/Dimetrodon_11.png")
gray1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

methods = ["Farneback", "SpareToDense PyrLK", "Dual TV-L1",
	"DIS Flow", "Simple Flow", "PCA Flow",
	"Deep Flow"]
flows = list()

flowFB = cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.6, 3, 25, 7, 5, 1.2, cv2.OPTFLOW_FARNEBACK_GAUSSIAN)
flows.append(flow2img(flowFB, False))

flowSTD = cv2.optflow.calcOpticalFlowSparseToDense(gray1, gray2, grid_step=5, sigma=0.5)
flows.append(flow2img(flowSTD, False))

dtvl1 = cv2.createOptFlow_DualTVL1()
flowDTVL1 = dtvl1.calc(gray1, gray2, None)
flows.append(flow2img(flowDTVL1, False))

dis = cv2.optflow.createOptFlow_DIS()
flowDIS = dis.calc(gray1, gray2, None)
flows.append(flow2img(flowDIS, False))

flowSF = cv2.optflow.calcOpticalFlowSF(im1, im2, 3, 5, 5)
flows.append(flow2img(flowSF, False))

pcaF = cv2.optflow.createOptFlow_PCAFlow()
flowPCA = pcaF.calc(gray1, gray2, None)
flows.append(flow2img(flowPCA, False))

startT = time.clock()
deepF = cv2.optflow.createOptFlow_DeepFlow()
flowDeep = deepF.calc(gray1, gray2, None)
flows.append(flow2img(flowDeep, False))
endT = time.clock()
print(endT - startT, "s")
cv2.optflow.writeOpticalFlow("dp.flo", flowDeep)

fig, axes = plt.subplots((len(flows) + 2) // 3, 3)
for i in range(axes.size):
	ax = axes.item(i)
	if (i < len(flows)):
		ax.imshow(flows[i])
		ax.set_title(methods[i])
	ax.axis("off")

plt.show()