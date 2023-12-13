import cv2
import pytesseract
import os
import socket
import sys
import struct
import time

# 设置保存文件夹
save_folder = "save"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# 加载视频文件
video_path = "videos/test.mp4"
cap = cv2.VideoCapture(video_path)

# 初始化计时器和标志
start_time = None
delay_flag = False

# 设置帧计数器和动作计数器
frame_interval = 10  # 抽帧间隔，每隔10帧抽取一帧

frame_count = 0  # 计数器，记录读取的帧数
action_count = 0 # 动作计数器，记录存取的帧数

# 循环遍历视频的每一帧 # 改为抽帧
while True:
    # 读取一帧
    ret, frame = cap.read()
    if not ret:
        break
    frame_count += 1

    # 判断是否抽取该帧
    if frame_count % frame_interval == 0:
        # 在这里执行对抽取的帧进行处理的操作
        
        # 划定识别区域
        x = 0
        y = 0
        w = 300
        h = 40
        crop = frame[y:y + h, x:x + w]
        # 使用Tesseract OCR识别文本
        text = pytesseract.image_to_string(crop)
        # print(text)
        # 检查文本是否包含指定的关键字
        if 'yawning' in text.lower():
            action_count += 1
            # 判断是否需要延迟
            if not delay_flag:
                # 如果标志为False，启动计时器
                start_time = time.time()
                delay_flag = True
                # 如果包含关键字，则截取当前帧并保存到文件夹中
                cv2.imwrite('/home/pi/raspberry/recognition_demo/save/yawning{}.jpg'.format(cap.get(cv2.CAP_PROP_POS_FRAMES)),
                            frame)
            else:
                # 如果标志为True，检查时间是否超过五秒钟
                if time.time() - start_time >= 5:
                    # 如果超过五秒钟，重置标志
                    delay_flag = False
                else:
                    continue


# 释放资源
cap.release()

# 输出动作帧的数量
print(f"Found {action_count} action frames.")

host = "192.168.1.110"
port1 = 8888
port2 = 7777

dir_path = 'save'
for filename in os.listdir(dir_path):
    filepath = os.path.join(dir_path, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as file:
            data = file.read(os.path.getsize(filepath))
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((host, port1))
    s2.connect((host, port2))

    s1.send(data)
    str = "tiny:yawning"  # 这里填违法类型
    s2.sendall(str.encode("utf-8"))
    print(f'文件"{filename}"发送成功')
    s1.close()
    s2.close()
    time.sleep(5)

# 设置要清理的文件夹路径
folder_path = 'save'

# 遍历文件夹中的所有文件和子文件夹
for root, dirs, files in os.walk(folder_path):
    for filename in files:
        # 删除文件
        os.remove(os.path.join(root, filename))
