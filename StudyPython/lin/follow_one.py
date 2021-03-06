# -*- coding: utf-8 -*-
# author： Emily
# 知乎回答： https://www.zhihu.com/question/26493945/answer/156025576
# 参考: https://blog.csdn.net/hongbin_xu/article/details/78359663
# dlib安装： https://blog.csdn.net/wjzhangcsu/article/details/72600689
# Anaconda 安装： https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/
# Anaconda 使用： https://www.jianshu.com/p/eaee1fadc1e9
import argparse
import sys
import time
import dlib
import cv2

tracker = dlib.correlation_tracker()  # 导入correlation_tracker()类

# 创建参数解析器并解析参数
ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', help='path to the videofile')
args = vars(ap.parse_args())
# 如果video参数为None，那么从摄像头读取数据
if args.get("video", None) is None:
    cap = cv2.VideoCapture(0)   # OpenCV打开摄像头
    time.sleep(0.25)

# 否则我们读取一个视频文件
else:
    cap = cv2.VideoCapture(args["video"])

start_flag = True  # 标记，是否是第一帧，若在第一帧需要先初始化
selection = None  # 实时跟踪鼠标的跟踪区域
track_window = None  # 要检测的物体所在区域
drag_start = None  # 标记，是否开始拖动鼠标


# 鼠标点击事件回调函数
def onMouseClicked(event, x, y, flags, param):
    global selection, track_window, drag_start  # 定义全局变量
    if event == cv2.EVENT_LBUTTONDOWN:  # 鼠标左键按下
        drag_start = (x, y)
        track_window = None
    if drag_start:  # 是否开始拖动鼠标，记录鼠标位置
        xMin = min(x, drag_start[0])
        yMin = min(y, drag_start[1])
        xMax = max(x, drag_start[0])
        yMax = max(y, drag_start[1])
        selection = (xMin, yMin, xMax, yMax)
    if event == cv2.EVENT_LBUTTONUP:  # 鼠标左键松开
        drag_start = None
        track_window = selection
        selection = None


if __name__ == '__main__':
    cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("image", onMouseClicked)

    # opencv的bgr格式图片转换成rgb格式
    # b, g, r = cv2.split(frame)
    # frame2 = cv2.merge([r, g, b])

    while (1):
        ret, frame = cap.read()  # 从摄像头读入1帧

        if start_flag == True:  # 如果是第一帧，需要先初始化
            # 这里是初始化，窗口中会停在当前帧，用鼠标拖拽一个框来指定区域，随后会跟踪这个目标；我们需要先找到目标才能跟踪不是吗？
            while True:
                img_first = frame.copy()  # 不改变原来的帧，拷贝一个新的出来
                if track_window:  # 跟踪目标的窗口画出来了，就实时标出来
                    cv2.rectangle(img_first, (track_window[0], track_window[1]), (track_window[2], track_window[3]),
                                  (0, 0, 255), 1)
                elif selection:  # 跟踪目标的窗口随鼠标拖动实时显示
                    cv2.rectangle(img_first, (selection[0], selection[1]), (selection[2], selection[3]), (0, 0, 255), 1)
                cv2.imshow("image", img_first)
                # 按下回车，退出循环
                if cv2.waitKey(5) == 13:
                    break
            start_flag = False  # 初始化完毕，不再是第一帧了
            tracker.start_track(frame, dlib.rectangle(track_window[0], track_window[1], track_window[2],
                                                      track_window[3]))  # 跟踪目标，目标就是选定目标窗口中的
        else:
            tracker.update(frame)  # 更新，实时跟踪

        box_predict = tracker.get_position()  # 得到目标的位置
        cv2.rectangle(frame, (int(box_predict.left()), int(box_predict.top())),
                      (int(box_predict.right()), int(box_predict.bottom())), (0, 255, 255), 1)  # 用矩形框标注出来
        cv2.imshow("image", frame)
        # 如果按下ESC键，就退出
        if cv2.waitKey(10) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
