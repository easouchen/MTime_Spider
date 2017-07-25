# -*- coding: utf-8 -*-
__author__ = 'EasouChen'

'''
    存储数据模块，用于将数据存入sqlite3数据库
'''

import sqlite3

class DataOutput(object):

    def __init__(self):
        '''
            初始化时，链接数据库并创建表格。
            同时初始一个空表格，用于缓存数据
        '''
        self.cx = sqlite3.connect('MTime.db')
        self.create_table('MTime')
        self.datas = []

    def create_table(self,table_name):
        '''
            创建数据表
        :param table_name:  表名
        :return:
        '''
        values = '''
        id integer primary key ,
        MovieId integer,
        MovieTitle varchar(40) NOT NULL,
        RatingFinal REAL NOT NULL DEFAULT 0.0,
        ROtherFinal REAL NOT NULL DEFAULT 0.0,
        RPictureFinal REAL NOT NULL DEFAULT 0.0,
        RDirectorFinal REAL NOT NULL DEFAULT 0.0,
        RStoryFinal REAL NOT NULL DEFAULT 0.0,
        Usercount integer NOT NULL DEFAULT 0,
        AttitudeCount integer NOT NULL DEFAULT 0,
        TotalBoxoffice varchar(20) NOT NULL,
        TodayBoxoffice varchar(20) NOT NULL,
        Rank integer NOT NULL DEFAULT 0,
        ShowDays integer NOT NULL DEFAULT 0,
        isRelease integer NOT NULL
        '''
        self.cx.execute('CREATE TABLE IF NOT EXISTS %s(%s) '%(table_name,values))

    def store_data(self,data):
        '''
            缓存数据
        :param data:    HtmlParser 处理后的电影对应数据
        :return:
        '''
        if data is None:
            return
        #每个电影对应的数据集合，作为列表中的一个元素，增添到列表中
        self.datas.append(data)

        #如果列表条数大于10，则写入数据库中
        if len(self.datas)>10:
            self.output_db('MTime')

    def output_db(self,table_name):
        '''
            数据写入数据库函数
        :param table_name: 目标表格名称
        :return:
        '''
        #写入数据
        for data in self.datas:
            print 'data is ...'
            # print data
            self.cx.execute("INSERT INTO %s (MovieId,MovieTitle,RatingFinal,"
                    "ROtherFinal,RPictureFinal,RDirectorFinal,"
                    "RStoryFinal,Usercount,AttitudeCount,"
                    "TotalBoxoffice,TodayBoxoffice,"
                    "Rank,ShowDays,isRelease) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                    ""%table_name,data )
            self.datas.remove(data)     #本条数据写入完成后，将其从列表中删除，以免重复写入
        self.cx.commit()    #写完后，提交

    def output_end(self):
        '''
            数据写入完成后关闭数据库
        :return:
        '''
        #如果列表中剩余的0<数据<10，调用写入函数
        if len(self.datas)>0:
            self.output_db('MTime')
        self.cx.close() #写入完毕后，关闭数据库

