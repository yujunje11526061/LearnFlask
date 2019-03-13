#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app.view_model.book import BookViewModel


class MyWishes():
    '''
    和MyGifts类可以封装成一个类.
    '''

    def __init__(self, my_wishes_list, gift_count_list):
        self.__my_wishes_list = my_wishes_list
        self.__gift_count_list = gift_count_list
        self.wishes = self.__parse() # 通过调用,赋值的形式可以明确知道实例属性在那里被修改了,当类很复杂时应该这样写. 直接在方法中修改实例属性容易找不到哪里发生了改动

    def __parse(self):
        temp_list = []
        for wish in self.__my_wishes_list:
            count = self.__match(wish)
            thisWishInfo = dict(
                id=wish.id,
                gifts_count=count,
                book=BookViewModel(wish.book)
            )
            temp_list.append(thisWishInfo)
        return temp_list

    def __match(self, wish):
        count = 0
        for gift_count in self.__gift_count_list:
            if wish.isbn==gift_count["isbn"]:
                count = gift_count["count"]
                break
        return count