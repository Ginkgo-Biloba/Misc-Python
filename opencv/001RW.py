import cv2
from matplotlib import pyplot as plt

def cv2Image():
    img = cv2.imread('2.jpg', -1)
    cv2.imshow('image', img)
    k = cv2.waitKey(7000)
    if k == 27: # ESC
        cv2.destroyAllWindows()
    elif k == ord('s'):
        cv2.imwrite('image.png', img)
        cv2.destroyAllWindows()

    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img2, cmap='gray', interpolation='bicubic')
    plt.xticks([]), plt.yticks([]) # 隐藏坐标数值
    plt.show()

def cv2Video():
    cap = cv2.VideoCapture(r"F:\.实验室相关\论文附件\klein_07_ptam_ismar.avi")
    fps = cap.get(cv2.CAP_PROP_FPS) # 4 # 帧率
    fsp = 1000//int(fps)
    while(cap.isOpened()):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', gray)
        if cv2.waitKey(fsp)&0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


# cv2Image()
cv2Video()
