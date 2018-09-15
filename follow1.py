import cv2
import numpy as np

# 读取视频
cap = cv2.VideoCapture("E:\\Users\\linyi05.INTERNAL\\Documents\\WLJ\\code\\PremierPython\\data\\2.mp4")

# 设置颜色区间
# 白色：0 0 221,180 30 255
# 蓝色：100 43 46,124 255 255
lower_white = np.array([78, 25, 221])
upper_white = np.array([125, 99, 255])

while (cap != 0):
    # 读取视频到frame中，颜色识别方式转换成HSV
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 显示原来的视频
    cv2.namedWindow('frame', cv2.WINDOW_FULLSCREEN)
    cv2.imshow('frame', frame)

    # 提取视频中白色的部分
    mask = cv2.inRange(hsv, lower_white, upper_white)
    cv2.namedWindow('mask', cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Mask', mask)

    # 原视频和提取后的视频做与操作
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.namedWindow('res', cv2.WINDOW_FULLSCREEN)
    cv2.imshow('res', res)

    # q键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
