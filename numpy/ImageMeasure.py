# coding=utf-8
import numpy as np
from scipy.ndimage import morphology as mor
from scipy.ndimage import measurements as msm
import matplotlib.pyplot as plt

squares = plt.imread("./Rect-Rcg.jpg")
squares = (squares < 200).astype(np.uint8)
sqrdt = mor.distance_transform_cdt(squares)
print(u"各种距离值", np.unique(sqrdt))
# plt.imshow(sqrdt, cmap="jet")
sqrCore = (sqrdt > 8).astype(np.uint8)
# plt.imshow(sqrCore, cmap="gray")

def randomPalette(labels, count, seed=1):
	np.random.seed(seed)
	palette = np.random.rand(count + 1, 3)
	palette[0, :] = 0
	return palette[labels]

(labels, count) = msm.label(sqrCore)
# (h, w) = labels.shape
# ctrs = np.array(msm.center_of_mass(labels, labels, index=range(1, count + 1)), np.int)
# plt.imshow(randomPalette(labels, count))
# (ctry, ctrx) = ctrs.T
# plt.plot(ctrx, ctry, "o", color="white")
# plt.xlim(0, w); plt.ylim(h, 0)

index = mor.distance_transform_cdt(1 - sqrCore, return_distances=False, return_indices=True)
nearLabels = labels[index[0], index[1]]
mask = (squares - sqrCore).astype(bool)
labels2 = labels.copy()
labels2[mask] = nearLabels[mask]
plt.imshow(randomPalette(labels2, count))
# marks = labels.copy()
# marks[squares == 0] = count + 1
# import cv2
# cv2.watershed(cv2.cvtColor((squares).astype(np.uint8), cv2.COLOR_GRAY2BGR), marks)
# marks[(marks == -1) | (marks == count + 1)] = 0
# plt.imshow(randomPalette(marks, count))

plt.show()
