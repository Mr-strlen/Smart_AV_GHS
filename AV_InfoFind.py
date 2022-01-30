## 参考 https://github.com/johngao01/javbus
## 给定番号名称，返回基本信息
import lxml.html
import requests
from bs4 import BeautifulSoup
import re
from lxml import etree

AV_code='WAAA-140' #给定番号
response=requests.get('https://www.javbus.com/'+AV_code)

av_info = {}
response.encoding="utf-8"
soup = BeautifulSoup(response.text, 'lxml')
# 获取到的网页信息需要进行解析，使用lxml解析器，其实默认的解析器就是lxml，但是这里会出现警告提示，方便你对其他平台移植
webtitle = str(soup.h3.string)
# print(webtitle)
av_info['avid'] = webtitle.split(" ")[0]
# print(avid)
av_info['avdesc'] = webtitle[len(av_info['avid']) + 1:len(webtitle)]
av_info['product_date'] = re.search(
    r'\d\d\d\d.\d\d.\d\d', response.text).group(0)
if re.search(r'(\d+)分鐘', response.text) is not None:
    av_info['duartion'] = re.search(r'(\d+)分鐘', response.text).group(1)
else:
    av_info['duartion'] = ''

if re.search('導演:<.*">(.*)</a></p>', response.text) is not None:
    av_info['director'] = re.search(
        '導演:<.*">(.*)</a></p>', response.text)[1]
else:
    av_info['director'] = ''
if re.search('系列:<.*">(.*)</a>', response.text) is not None:
    av_info['series'] = re.search('系列:<.*">(.*)</a>', response.text)[1]
else:
    av_info['series'] = ''
av_info['Category'] = re.findall(
    '<input type="checkbox" name="gr_sel".*">(.*)</a>',
    response.text)
if re.search('製作商:<.*">(.*)</a>', response.text) is not None:
    av_info['producer'] = re.search('製作商:<.*">(.*)</a>', response.text)[1]
else:
    av_info['producer'] = ''
if re.search('發行商:<.*">(.*)</a>', response.text) is not None:
    av_info['issuer'] = re.search('發行商:<.*">(.*)</a>', response.text)[1]
else:
    av_info['issuer'] = ''
if re.findall(
        '<a href="https://www.javbus.com/star/.{3,5}">(.{1,8})</a>', response.text) is not None:
    av_info['actors'] = re.findall(
        '<a href="https://www.javbus.com/star/.{3,5}">(.{1,8})</a>',
        response.text)
else:
    av_info['actors'] = ''
gid = re.search(r'var gid = (\d{10,12});', response.text).group(1)
uc = re.search(r'var uc = (\d+);', response.text).group(1)
img = re.search('var img = \'(.*)\';', response.text).group(1)

print(av_info)

