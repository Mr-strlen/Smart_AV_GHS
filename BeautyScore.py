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

vPath = r".\Test_Data\ssni-392.mp4" 
vidcap = cv2.VideoCapture(vPath)
length=get_video_duration(vidcap) # 总帧数
print(length)
frame_num=40
## 从头尾5%-95% 产生20个的随机序列
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
    
 
## 人脸识别+颜值打分
import requests 
import urllib
import base64
import SecertKey as SK
# client_id 为官网获取的AK， client_secret 为官网获取的SK
APP_ID = SK.Client('face','App_ID')
API_KEY = SK.Client('face','API_Key')
SECRECT_KEY = SK.Client('face','Secret_Key')
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+API_KEY+'&client_secret='+SECRECT_KEY
response = requests.get(host)
if response:
    print(response.json())
    
request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

imgPath='./Temp_/_78165.jpg'
f = open(imgPath, 'rb')
image = base64.b64encode(f.read())
imgBase64 = str(image,'utf-8')
image_type = "BASE64"



# params = "{\"image\":\"%s\",\"image_type\":\"BASE64\",\"face_field\":\"faceshape,facetype\"}"%image64
params = {"image": imgBase64, "image_type": "BASE64","face_field":"age,beauty,expression,face_shape,gender"}
# 此处的faceshape和facetype需要自己加上去 更具自己需要的返回值

params = urllib.parse.urlencode(params).encode("utf-8")


access_token = '[24.826cefc0a461083514ca6818849023b3.2592000.1647425813.282335-25608768]'
request_url = request_url + "?access_token=" + access_token

request = urllib.request.urlopen(url=request_url, data=params)   # 发送请求

content = request.read()  # 将返回结果读取出来
print(content)  # 显示返回结果



import urllib, sys
import ssl
import json
import base64
import cv2
result=json.loads(content)['result']
face_list=result['face_list'][0]
location=face_list['location']
age=face_list['age']
beauty=face_list['beauty']
expression=face_list['expression']['type']
gender=face_list['gender']['type']
 
img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
leftTopX=int(location['left'])
leftTopY=int(location['top'])
rightBottomX=int(leftTopX+int(location['width']))
rightBottomY = int(leftTopY + int(location['height']))
cv2.rectangle(img, (leftTopX, leftTopY), (rightBottomX, rightBottomY), (0, 255, 0), 2)
font = cv2.FONT_HERSHEY_SIMPLEX
# 第一个坐标表示起始位置
cv2.putText(img,"age:"+str(age),(0, 20),font, 0.5, (200, 255, 255), 1)
cv2.putText(img, "gender:" + gender, (0, 40), font, 0.5, (200, 255, 255), 1)
cv2.putText(img, "beauty:" + str(beauty), (0, 60), font, 0.5, (200, 255, 255), 1)
cv2.putText(img, "expression:" + str(expression), (0, 80), font, 0.5, (200, 255, 255), 1)
cv2.imshow('image', img)
cv2.imwrite('test.jpg',img)
cv2.waitKey(0)
 
print("end")