## 视屏随机抽帧，保存成图片
import cv2
import os
import random,math

#获取视频时长
def get_video_duration(cap):
    if cap.isOpened():
        # get方法参数按顺序对应下表（从0开始编号)
        #rate = cap.get(5) # 帧速率
        frame_num =cap.get(7) # 视频文件的帧数
        #duration = frame_num/rate # 帧速率/视频总帧数 是时间，除以60之后单位是分钟
        return frame_num
    return -1

vPath = r".\Test_Data\SNIS-704.avi" 
vidcap = cv2.VideoCapture(vPath)
length=get_video_duration(vidcap) # 总帧数
print(length)
frame_num=10
## 从头尾5%-95% 产生10个的随机序列
rs = random.sample(range(math.floor(length*0.05), math.floor(length*0.95)), frame_num)

## 清除缓存
for root, dirs, files in os.walk('.\\Temp'):
    for file in files:
        os.remove(root+'\\'+file)
## 开始生成图片
for i in rs:
    vidcap.set(cv2.CAP_PROP_POS_FRAMES,i)  #设置要获取的帧号
    success,image=vidcap.read()
    cv2.imwrite(f'.\\Temp\\_{i}.jpg', image)     # save frame as JPEG file
    print('Read a new frame: ', success)