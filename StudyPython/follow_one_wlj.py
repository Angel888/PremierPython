import argparse
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
    video = cv2.VideoCapture(0)   # OpenCV打开摄像头
    time.sleep(0.1)

# 否则我们读取一个视频文件
else:
    video = cv2.VideoCapture(args["video"])

first_frame = True  # 标记，是否是第一帧，若在第一帧需要先初始化
selection = None  # 实时跟踪鼠标的跟踪区域
track_window = None  # 要检测的物体所在区域
drag_start = None  # 标记，是否开始拖动鼠标


# 鼠标点击事件回调函数
def on_mouse_clicked(event, x, y, flags, param):
    global selection, track_window, drag_start  # 定义全局变量
    if event == cv2.EVENT_LBUTTONDOWN:  # 鼠标左键按下
        drag_start = (x, y)
        track_window = None
    if drag_start:  # 是否开始拖动鼠标，标记位置
        x_min = min(x, drag_start[0])
        y_min = min(y, drag_start[1])
        x_max = max(x, drag_start[0])
        y_max = max(y, drag_start[1])
        selection = (x_min, y_min, x_max, y_max)
    if event == cv2.EVENT_LBUTTONUP:  # 鼠标左键松开
        drag_start = None
        track_window = selection
        selection = None


if __name__ == '__main__':
    cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("image", on_mouse_clicked)

    # opencv的bgr格式图片转换成rgb格式

    while 1:
        ret, frame = video.read()  # 读入1帧

        if first_frame:  # 如果是第一帧，需要先初始化
            # 窗口中会停在当前帧，用鼠标拖拽一个框来指定区域，随后会跟踪这个目标
            while True:
                img_first = frame.copy()  # 不改变原来的帧，拷贝一个新的出来
                if track_window:  # 实时标出跟踪目标的窗口
                    cv2.rectangle(img_first, (track_window[0], track_window[1]), (track_window[2], track_window[3]),
                                  (0, 255, 0), 1)
                elif selection:  # 跟踪目标的窗口随鼠标拖动实时显示
                    cv2.rectangle(img_first, (selection[0], selection[1]), (selection[2], selection[3]), (0, 255, 0), 1)
                cv2.imshow("image", img_first)
                # 按下回车，退出循环
                if cv2.waitKey(7) == 13:
                    break
            first_frame = False  # 初始化完毕，不再是第一帧了
            tracker.start_track(frame, dlib.rectangle(track_window[0], track_window[1], track_window[2],
                                                      track_window[3]))  # 跟踪第一帧的目标
        else:
            tracker.update(frame)  # 更新，实时跟踪

        target = tracker.get_position()  # 得到目标的位置
        cv2.rectangle(frame, (int(target.left()), int(target.top())),
                      (int(target.right()), int(target.bottom())), (0, 255, 255), 1)  # 用矩形框标注出来
        cv2.imshow("image", frame)
        # 如果按下q键，就退出
        if cv2.waitKey(10) == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
