import cv2
import numpy

img = numpy.zeros((512,512,3), numpy.uint8)
img = cv2.line(img, (0,0), (500,400), (255,0,0), 2)
img = cv2.rectangle(img, (384,0), (510,128), (0,255,0), 2)
img = cv2.circle(img, (447,65), 63, (0,0,255), -1)
img = cv2.ellipse(img, (256,256), (100,50), 0, 0, 270, (255,255,0), 1)

pts = numpy.array([[10,5],[20,30],[70,20],[50,10]], numpy.int32)
pts = pts.reshape((-1,1,2))
img = cv2.polylines(img, [pts], True, (0,255,255))

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, 'OpenCV', (80,480), font, 3, (255,0,255), 2, cv2.LINE_AA)

cv2.imshow('img', img)
