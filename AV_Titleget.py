## 视屏随机抽帧，保存成图片
import cv2
import os
import random,math
import numpy as np

##创建百度应用链接
import SecertKey as SK
import json
import requests
import base64
import urllib.parse

APP_ID = SK.Client('face','App_ID')
API_KEY = SK.Client('face','API_Key')
SECRECT_KEY = SK.Client('face','Secret_Key')

# 获取token
url = 'https://aip.baidubce.com/oauth/2.0/token'
body = {'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': SECRECT_KEY
        }

req = requests.post(url=url, data=body)
token = json.loads(req.content)['access_token']


#获取视频时长
def get_video_duration(cap):
    if cap.isOpened():
        # get方法参数按顺序对应下表（从0开始编号)
        rate = cap.get(5) # 帧速率
        #frame_num =cap.get(7) # 视频文件的帧数
        #duration = frame_num/rate # 帧速率/视频总帧数 是时间，除以60之后单位是分钟
        return rate
    return -1

vPath = r".\Test_Data\SSNI-756.mp4" 

vidcap = cv2.VideoCapture(vPath)
rate=get_video_duration(vidcap) # 总帧数
print(rate)
rs=[]
## 从头3min 2s抽一帧
for i in range(0,180,2):
    rs.append(math.floor(rate)*i)
'''
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
'''

## 对生成的图片进行识别
for root, dirs, files in os.walk('.\\Temp'):
    for file in files:
        image = cv2.imread(root+'\\'+file,cv2.IMREAD_GRAYSCALE)#读取灰度图像
        cnt_array = np.where(image,0,1)
        black_rate=np.sum(cnt_array)/(np.shape(image)[0]*np.shape(image)[1])
        if black_rate>0.6 and black_rate<0.95:
            new_image=image[np.shape(image)[0]-150:np.shape(image)[0],np.shape(image)[1]-300:np.shape(image)[1]]
            cv2.imwrite('.\\Temp\\title.jpg',new_image)
            break

# 获取百度api识别结果
ocr_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=%s'%token
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# 读取图片并进行base64加密
body = base64.b64encode(open('.\\Temp\\title.jpg' ,'rb').read())
# 进行urlencode
data = urllib.parse.urlencode({'image': body})

# post请求
r = requests.post(url=ocr_url, headers=headers, data=data)

# 输出请求结果
print('请求码为: %s' %r.status_code)
res_words = json.loads(r.content)['words_result'][0]['words']
print('识别结果为: %s' % res_words)
