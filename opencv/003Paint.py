import cv2
import numpy as np
import random

drawing = False # 鼠标按下时为 True
mode = True # True 画矩形。按 m 画曲线
ix = iy = -1
b = g = r = 0

# 鼠标回调函数
def drawCircle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        b = random.randint(0,255)
        g = random.randint(0,255)
        r = random.randint(0,255)
        cv2.circle(img, (x,y), 100, (b,g,r), 1)

def draw2(event, x, y, flags, param):
    global ix, iy, drawing, mode, b, g, r
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix = x
        iy = y
        b = random.randint(0,255)
        g = random.randint(0,255)
        r = random.randint(0,255)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            if mode:
                cv2.rectangle(img, (ix, iy), (x, y), (b, g, r), 2)
            else:
                cv2.circle(img, (x, y), 5, (b, g, r), 1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            pass
        else:
            pass

# 创建空图像、窗口，绑定函数
img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw2)

while 1:
    cv2.imshow('image', img)
    key = cv2.waitKey(20)&0xFF
    if  key == 27:
        break
    elif key == ord('c'):
        img.fill(10)
    elif key == ord('m'):
        mode = not mode
cv2.destroyAllWindows()
