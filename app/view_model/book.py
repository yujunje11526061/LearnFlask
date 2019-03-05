#!/usr/bin/env python
# -*- coding:utf-8 -*-

class BookViewModel:
    '''
    此类用于对API返回的数据加以修改整合，使得isbn搜索和关键字搜索返回得数据具有统一格式
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
            "book": [],
            "total": 0,
            "keyword": key,
        }
        if rawData:
            returnedData["total"] = rawData["total"]
        returnedData["book"] = [cls.__cut_book_data(book) for book in rawData["books"]]
        return returnedData

    @classmethod
    def __cut_book_data(cls, data:dict)->dict:
        '''
        从API获取的原始数据中选择需要的字段
        :param data:
        :return:
        '''
        book = {
            "title":data["title"],
            "publisher":data["publisher"],
            "pages":data["pages"] or "",
            "author":"--".join(data["author"]), # 通过模板渲染的方式得到页面则直接将数据在服务端处理完再填进去比较好。若是前后端分离，则提供列表供客户端去决定需要呈现的方式更好，更灵活。
            "price":data["price"],
            "summary":data["summary"] or "",
            "image":data["image"],
        }
        return book