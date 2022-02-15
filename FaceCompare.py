import SecertKey as SK
import json
import base64
import requests
# 1.读取两张图片数据，整合两张图片 json数据
with open("./Temp_/_78165.jpg","rb") as f:
    pic1 = f.read()
with open("./Temp_/test.jpg","rb") as f:
    pic2 = f.read()
image_data = json.dumps([
    {"image": str(base64.b64encode(pic1), "utf-8"),"image_type":"BASE64","face_type":"LIVE","quality_control":"NORMAL","liveness_control":"NONE"},
    {"image": str(base64.b64encode(pic2), "utf-8"),"image_type":"BASE64","face_type":"LIVE","quality_control":"NORMAL","liveness_control":"NONE"}
])
# 2.拼接人脸识别API接口
APP_ID = SK.Client('face','App_ID')
API_KEY = SK.Client('face','API_Key')
SECRECT_KEY = SK.Client('face','Secret_Key')


get_token = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id="+API_KEY+"&client_secret="+SECRECT_KEY
 
API_url = "https://aip.baidubce.com/rest/2.0/face/v3/match?access_token="
 
text = requests.get(get_token).json()
print(text['access_token'])
 
url = API_url + text['access_token']
print(url)
# 3.请求API接口传入json数据，返回图片相似度
response = requests.post(url, image_data).json()
 
print(response)
 
score = response['result']['score']
print("相似度为：{}%".format(score))
if score > 80:
    print("是同一个人")
else:
    print("不是同一个人")
