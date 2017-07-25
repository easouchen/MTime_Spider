# MTime_Spider
	本项目是一个简单的爬取时光网（北京地区）电影信息的爬虫程序，主要是对AJAX返回的信息作处理，并写入到sqlite3数据库中

##本项目的框架说明
	本项目包含几个py文件，属于爬虫中较为常见的几个处理模块，分别有：
	1 HtmlDownloader_MT.py  负责获取html页面，并返回整个页面的content
	2 HtmlParser_MT.py 		负责处理content的信息，也负责处理ajax返回的数据
	3 SaveData_MT.py 		负责数据写入
	4 Spider_MT.py			程序的主入口

##框架示意图如下
	![](http://i.imgur.com/1AEY0hR.jpg)