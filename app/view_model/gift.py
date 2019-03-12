#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app.view_model.book import BookViewModel


class MyGifts():

    def __init__(self, my_gifts_list, wish_count_list):
        self.__my_gifts_list = my_gifts_list
        self.__wish_count_list = wish_count_list
        self.gifts = self.__parse() # 通过调用,赋值的形式可以明确知道实例属性在那里被修改了,当类很复杂时应该这样写. 直接在方法中修改实例属性容易找不到哪里发生了改动

    def __parse(self):
        temp_list = []
        for gift in self.__my_gifts_list:
            count = self.__match(gift)
            thisGiftInfo = dict(
                id=gift.id,
                wishes_count=count,
                book=BookViewModel(gift.book)
            )
            temp_list.append(thisGiftInfo)
        return temp_list

    def __match(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn==wish_count["isbn"]:
                count = wish_count["count"]
                break
        return count