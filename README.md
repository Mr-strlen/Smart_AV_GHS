# Smart_AV_GHS
## 项目背景
22年1月，我从学校被赶回家隔离，但是在家无心学习，于是开始整理自己积攒多年的小电影  
自己以前下载的时候，没有整理小电影的好习惯，日积月累，现在足足有几个T。而且内容繁杂，质量良莠不齐  
想要整理清楚，耗时耗力，每天就对着小电影看，身心俱疲，非常的头疼（我花了一周的时间在上面，淦）  
这遭到了我那生医老铁的嘲讽  
作为一个计算机的学生，理应利用专业知识，为自己开发一个**智能的AV管理系统**

## 基本介绍
目前涉及的功能包括以下几块：  

### 1. 根据给定番号，返回该番号的基本信息
* 这是一个信息刮削的事情，有著名的网站javbus可以进行查询，简单爬虫就可以实现；  
* 同时，由于这里是对本地的小电影番号进行检索，所以不存在高并发的需求
* 默认所有视屏文件均为番号命名

### 2. 按照番号信息，对小电影进行归纳分类 
* 这里我是按照演员分类（存在多人的归为单独一类） 每个演员建立一个文件夹，下属所有为其作品 
* 并且检测视屏分辨率，分辨率过低的进行警报，需要换源  
分辨率检测参考 https://blog.csdn.net/li_ji_an/article/details/104280347

### 3. 自动对视屏进行打分，规避踩雷
由于存在封面杀这种恶劣现象，需要一种智能的打分系统，辅助用户进行规避，目前设计思路如下：
* 在影片中随机抽取10帧画面，并保存
* 对每张图片进行人脸识别，将识别为“亚洲女性”的图像进行头像截取  
可使用Github开源人脸识别项目face_recognition https://github.com/ageitgey/face_recognition  
参考 https://zhuanlan.zhihu.com/p/25025596
* 对截取的图像进行颜值打分，取平均  
颜值打分部分，由于微软小冰的api关闭，使用别人预训练好的模型  
参考链接为 https://github.com/koala9527/face_rank  
百度、腾讯也提供了类似的接口，可以尝试

### 4. 对没有番号或番号错误的视频，获取正确番号
这里是两个问题，1.如何指导番号是对的还是错的，2.如何获取正确的番号
* 可以使用人脸比对，来比对视频中的人和宣传画上的人是否为同一人，可调用百度API实现。
* 大部分AV在开头会有一个黑色背景板的页面，出现标题，右下角会有番号。  
利用定格抽帧，判断黑色背景板，然后截取右下角图片，进行文字识别，即可获得番号。  
此处也可以利用百度文字识别API。

### 5. 允许用户自主修改信息，并保存
* 对女演员进行等级划分（我分为了五档 SSS SS S A B）
* 对作品进行标签补充（例如我最关注的黑丝）
* 对女演员or作品进行辅助说明
  
此部分目前存为了一个excel表格，之后会使用数据库进行管理

### 6. 设计完整的交互系统

## 功能实现
* AV_InfoFind.py  
实现了对指定番号的信息刮削  
参考 https://github.com/johngao01/javbus
* AV_Titleget.py  
实现了对片头标题页面的文字识别，调用百度文字识别API。  
关于API调用的参考：  
https://www.cnblogs.com/jclian91/p/10850272.html  
* BeautyScore.py  
实现了颜值打分，这里是初步的，直接调用百度API实现的结果，之后会做细化。  
参考：  
https://blog.csdn.net/tuoyakan9097/article/details/90415493  
https://www.cnblogs.com/BookMiki/p/9844857.html  
* FaceCompare.py
实现了视频中人物和宣传画上人物的比对，也是直接调用百度人脸比对API。  
参考：  
https://blog.csdn.net/fangye945a/article/details/102512532  

## 其他工具
GHS作为一项刚需，已经有不少前辈完成了相关技术的开发和应用，我只是在大佬们的身后捡贝壳  
这里提供一些工具
### 人脸搜索/比对
* 使用了AI进行人脸识别，主要针对AV女优搜索 https://xslist.org/zh 
* 号称最先进的人脸反向搜索引擎，比较精准，但同一IP每天有搜索10次限制，需翻墙 https://pimeyes.com  
* 新鲜出炉的，使用了AI进行人脸识别，主要针对Pornhub小姐姐搜索 https://pornstarbyface.com/ 
* 老牌以图搜图工具 https://tineye.com 
* Multi-service image search，主要针对动画、游戏、壁纸图片搜索 https://iqdb.org 
* 主要针对Pixiv （pixiv.net）图片搜索 https://saucenao.com
* 主要针对二次元图片搜索 http://www.ascii2d.net
* 主要针对动漫视频截图搜索 https://trace.moe 
### AV信息查询索引
* avmoo和javlibrary是日本知名的在线成人视频库
* javbus为成人影片的磁力链接数据库
### 隔壁大佬的牛逼项目（截止到20220223）
* AVbook系统 8.2k stars  https://github.com/guyueyingmu/avbook
* JAViewer 4.6k stars https://github.com/SplashCodes/JAViewer
* javdst https://github.com/JustMachiavelli/javsdt
* JAVClub 2.7k stars https://github.com/JAVClub/core
* JBusDriver 2.1k stars https://github.com/Ccixyj/JBusDriver
* JavRocket 1.8k stars https://github.com/gentlemansolo/JavRocket
* JavScraper Emby/Jellyfin 的一个日本电影刮削器插件 1.7k stars https://github.com/JavScraper/Emby.Plugins.JavScraper
* AVDC 日本电影元数据刮削器，配合kodi,emby,plex等本地媒体管理工具使用 1.3k stars https://github.com/moyy996/AVDC  
讲真，这个和我最后想实现的东西有点接近
* Gfriends 823 stars 女友头像仓库 https://github.com/xinxin8816/gfriends

## 附录
附上我自己排的颜值分类头尾三部分  
审美这件事萝卜青菜各有所爱，望与大家友好探讨
### T0 SSS 颜值天花板
* 桃谷绘里香
* 枫可怜
* 葵司
* 明日花绮罗
* 桥本有菜
* 相泽南 
* 凉森玲梦
* 河北彩花
* 深田咏美
* 桃乃木香奈 
### T1 SS 好看但差点意思
* Aika
* 大桥未久
* 铃原爱蜜莉
* 高桥圣子
* 三上悠亚 
* 天使萌 
* 明里紬 
* 上原亚衣
* 天海翼
* Rion

### T4 B 不好看，欺骗用户
* 二階堂夢  
* 小野六花
* 白石茉莉奈
* 七泽美亚
