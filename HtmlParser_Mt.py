# -*- coding: utf-8 -*-
__author__ = 'EasouChen'

'''
    本模块用于处理获取主页中的电影链接，以及处理ajax请求返回的数据
'''

import re,json

class Paser_url(object):

    def htmlPars(self,page_url,content):
        '''
            用于获取电影列表的链接
        :param page_url: 主页
        :param content:  htmlDownloader中返回的数据
        :return: 电影的链接列表
        '''
        if content is None:
            return

        #定义匹配模式并匹配，注意：两个括号，进行了两次匹配。所以返回的列表中，每个元素都有两个子元素
        pattern = re.compile(r'(http://movie.mtime.com/(\d+)/)')
        urls = pattern.findall(content)
        # print urls

        #判断，如果获取成功，则去重，并返回列表
        if urls !=None:
            return list(set(urls))
        else:
            return None



    def paser_json(self,page_url,content):
        '''
            解析AJAX响应返回的信息
        :param page_url: HtmlPars返回的电影链接
        :param content:  ajax返回的信息
        :return: 处理后的数据
        '''

        #抽取 “=” 与 “；”的内容
        pattern = re.compile(r'=(.*?);')
        result = pattern.findall(content)[0]
        # print 'results is ..'
        # print result
        #判断是否有数据
        if result !=None:
            value = json.loads(result)  #将数据变回字典模式
            # print "value is .."
            # print value
            try:
                #获取是否上映状态
                isRelease = value.get('value').get('isRelease')
                print 'isRelease is %s'%isRelease
            except Exception,e:
                print e
                return None

            if isRelease:   #判断是否上映

                if value.get('value').get('hotValue') == None:
                    #已上映影片，调用已上映影片的处理函数，否则，调用未上映影片的处理函数
                    return self._paser_release(page_url,value)
                else:
                    return self._paser_no_release(page_url,value,isRelease=2)
            else:
                return self._paser_no_release(page_url,value)

    def _paser_release(self,page_url,value):
        '''
            已上映影片的处理函数，解析已经上映的影片
        :param page_url:   对应的电影链接
        :param value:   从jason字典中抽取出来的数据
        :return:    处理过的电影信息
        '''
        try:
            isRelease = 1
            #获取需要的信息，并返回
            movieRating = value.get('value').get('movieRating')
            print 'this is ok...'
            boxOffice = value.get('value').get('boxOffice')
            movieTitle = value.get('value').get('movieTitle')

            RPictureFinal = movieRating.get('RPictureFinal')
            RStoryFinal = movieRating.get('RStoryFinal')
            RDirectorFinal = movieRating.get('RDirectorFinal')
            ROtherFinal = movieRating.get('ROtherFinal')
            RatingFinal = movieRating.get('RatingFinal')
            MovieId = movieRating.get('MovieId')
            Usercount = movieRating.get('Usercount')
            AttitudeCount = movieRating.get('AttitudeCount')

            TotalBoxOffice = boxOffice.get('TotalBoxOffice')
            TotalBoxOfficeUnit = boxOffice.get('TotalBoxOfficeUnit')
            TodayBoxOffice = boxOffice.get('TodayBoxOffice')
            TodayBoxOfficeUnit = boxOffice.get('TodayBoxOfficeUnit')
            ShowDays = boxOffice.get('ShowDays')

            try:
                Rank = boxOffice.get('Rank')

            except Exception,e:
                Rank = 0

            return (MovieId,movieTitle,RatingFinal,
                    ROtherFinal,RPictureFinal,RDirectorFinal,
                    RStoryFinal,Usercount,AttitudeCount,
                    TotalBoxOffice+TotalBoxOfficeUnit,
                    TodayBoxOffice+TodayBoxOfficeUnit,
                    Rank,ShowDays,
                    isRelease)
        except Exception,e:
            print e,page_url,value
            return None

    def _paser_no_release(self,page_url,value,isRelease=0):
        '''
            即将上映影片的处理模块，解析即将上映的影片信息
        :param page_url: 对应的模块
        :param value:   jason字典中取出的数据
        :return:    处理后的信息
        '''

        try:
            movieRating = value.get('value').get('movieRating')
            movieTitle = value.get('value').get('movieTitle')
            print 'that is ok ...'
            RPictureFinal = movieRating.get('RPictureFinal')
            RStoryFinal = movieRating.get('RStoryFinal')
            RDirectorFinal = movieRating.get('RDirectorFinal')
            ROtherFinal = movieRating.get('ROtherFinal')
            RatingFinal = movieRating.get('RatingFinal')
            MovieId = movieRating.get('MovieId')
            Usercount = movieRating.get('Usercount')
            AttitudeCount = movieRating.get('AttitudeCount')
            try:
                Rank = value.get('value').get('hotValue').get('Ranking')

            except Exception, e:
                Rank = 0

            return (MovieId, movieTitle, RatingFinal,
                    ROtherFinal, RPictureFinal, RDirectorFinal,
                    RStoryFinal, Usercount, AttitudeCount,
                    u'无',u'无',
                    Rank, 0, isRelease)
        except Exception, e:
            print e, page_url, value
            return None






