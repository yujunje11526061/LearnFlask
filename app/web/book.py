#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint

from app.web.blueprint import web
from config import URLISBN
from httptool import HTTP
from yushubook import YushuBook
from flask import current_app


@web.route('/book/search/<q>/<page>/') # 把视图函数注册到相应蓝图对象
def search(q, page):
    '''
    :param q: 普通关键字
    :param page:
    :return:
    '''
    return YushuBook.search_by_isbn(q) if YushuBook.is_ISBN(q) else YushuBook.search_by_key(q)



