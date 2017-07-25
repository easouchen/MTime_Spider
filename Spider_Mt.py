# -*- coding: utf-8 -*-
__author__ = 'EasouChen'

'''
    爬虫项目的主入口
'''

from HtmlDowloader_Mt import HtmlDowloader
from HtmlParser_Mt import Paser_url
from SaveData_Mt import DataOutput
import time


class SpiderMain(object):
    def __init__(self):
        '''
            初始化要用到的各个模块
        '''
        self.downloader = HtmlDowloader()
        self.parser = Paser_url()
        self.output = DataOutput()

    def crawl(self,root_url):
        '''
            爬虫开始模块
        :param root_url:    爬取目标页
        :return:
        '''
        #按照流程，爬取页面信息---获取电影链接列表
        content =self.downloader.htmlDownload(root_url)
        urls = self.parser.htmlPars(root_url,content)

        # 获取列表后，对每个电影进行ajax数据处理
        for url in urls:
            print url
            try:
                #定义时间戳
                t = time.strftime('%Y%m%d%H%M%S3282', time.localtime())
                print t

                #定义ajax请求的链接
                rank_url = 'http://service.library.mtime.com/Movie.api' \
                '?Ajax_CallBack=true' \
                '&Ajax_CallBackType=Mtime.Library.Services' \
                '&Ajax_CallBackMethod=GetMovieOverviewRating' \
                '&Ajax_CrossDomain=1' \
                '&Ajax_RequestUrl=%s' \
                '&t=%s'\
                '&Ajax_CallBackArgument0=%s'%(url[0],t,url[1])
                rank_content = self.downloader.htmlDownload(rank_url)
                print 'rank_content is ...'
                # print rank_content

                #处理请求返回的数据，并写入数据库
                data = self.parser.paser_json(rank_url,rank_content)
                self.output.store_data(data)
            except Exception,e:
                print "Crawl failed"

        self.output.output_end()    #最后别忘了关闭数据库
        print "Crawl finish..."

if __name__ == '__main__':
    #实例化并运行爬虫
    spider = SpiderMain()
    spider.crawl('http://theater.mtime.com/China_Beijing/')

