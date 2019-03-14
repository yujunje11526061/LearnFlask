#!/usr/bin/env python
# -*- coding:utf-8 -*-
from yushubook import YushuBook


class BookViewModel():
    '''
    设计理念:
    定义单本书所需要的字段,把单本书拎出来处理,可以对其添加相应方法, 相比于直接在书籍集合类中以字典代表单本书,更易扩展.
    实例属性全部列出来也一目了然容易阅读.
    '''
    def __init__(self, book:dict):
        self.title = book.get("title", 0)
        self.publisher =  book.get("publisher", "")
        self.pubdate = book.get("pubdate","")
        self.pages = book.get("pages", "")
        self.author =  "--".join(
            book.get("author", []))
        self.price = book.get("price", "")
        self.binding = book.get("binding","")
        self.summary = book.get("summary", "").replace("\\n","\n")
        self.image = book.get("image", "")
        self.isbn = book.get("isbn", "")

    @property
    def into(self):
        intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
        return "/".join(intros)

class BookCollection():
    '''
    定义多本书构成的信息
    '''
    def __init__(self):
        self.total = 0
        self.keyword = ''
        self.books = []

    def fill(self,yushu_book:YushuBook,keyword:str):
        '''
        此方法用于讲API中获取的原始数据进行清洗整合
        :param yushu_book:该对象封装了从API获取的原始数据
        :param key:
        :return:
        '''
        self.keyword = keyword
        self.total = yushu_book.total
        # self.books = [BookViewModel(book).__dict__ for book in yushu_book.books]
        self.books = [BookViewModel(book) for book in yushu_book.books]

@DeprecationWarning
class _BookViewModel:
    '''
    此类用于对API返回的数据加以修改整合，使得isbn搜索和关键字搜索返回得数据具有统一格式

    不具备面向对象的特征，用BookViewModel和BookCollection重构
    '''

    @classmethod
    def package_single(cls, rawData:dict, key:str)->dict:
        '''
        isbn搜索得到的数据最多一个，此函数处理
        :param rawData:
        :param key:
        :return:
        '''
        returnedData = {
            "book" : [],
            "total" : 0,
            "keyword" : key,
        }
        if rawData:
            returnedData["total"] = 1
        returnedData["book"].append(cls.__cut_book_data(rawData))
        return returnedData

    @classmethod
    def package_collection(cls, rawData:dict, key:str)->dict:
        '''
        关键字搜索得到的数据是一个列表，此函数处理
        :param rawData:
        :param key:
        :return:
        '''
        returnedData = {
            "books": [],
            "total": 0,
            "keyword": key,
        }
        if rawData:
            returnedData["total"] = rawData["total"]
        returnedData["books"] = [cls.__cut_book_data(book) for book in rawData["books"]]
        return returnedData

    @classmethod
    def __cut_book_data(cls, data:dict)->dict:
        '''
        从API获取的原始数据中选择需要的字段
        :param data:
        :return:
        '''
        book = {
            "title":data.get("title",0),
            "publisher":data.get("publisher",""),
            "pages":data.get("pages",""),
            "author":"--".join(data.get("author",[])), # 通过模板渲染的方式得到页面则直接将数据在服务端处理完再填进去比较好。若是前后端分离，则提供列表供客户端去决定需要呈现的方式更好，更灵活。
            "price":data.get("price",""),
            "summary":data.get("summary", ""),
            "image":data.get("image",""),
        }
        return book