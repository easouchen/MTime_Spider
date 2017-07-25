# -*- coding: utf-8 -*-
__author__ = 'EasouChen'
'''
    本模块用于处理主页的html
'''

import requests

class HtmlDowloader(object):

    def htmlDownload(self,url,rf=None,data=None):
        '''
            下载链接，并将html转为str，返回
        :param url:主页链接
        :return:
        '''
        if url is None:return
        count = 0                   #用于控制下载失败后，重新下载次数

        #定义header信息，伪装信息
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
        headers = {'User-Agent':user_agent,'Referer':rf,}

        #重试次数为2次
        while count <3:
            try:
              content = requests.get(url,headers = headers,timeout = 3) #设置超时

            #判断是否下载成功，成功则返回html的str格式
              if content.status_code == 200:
                  return content.text
              else:return content.status_code
            except Exception,e:
                print e
                count += 1
