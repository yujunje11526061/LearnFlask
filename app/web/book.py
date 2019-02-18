#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import request, jsonify

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
    r = YushuBook.search_by_isbn(q) if YushuBook.is_ISBN(q) else YushuBook.search_by_key(q)
    return jsonify(r)

@web.route('/book/search/')
def search2():
    '''
    ?q={}&page={} 方式传参
    request上下文对象的args属性（MultiDict）来获取参数
    :param q: 普通关键字
    :param page:
    :return:
    '''
    q = request.args.get('q')
    page = request.args.get('page')
    r = YushuBook.search_by_isbn(q) if YushuBook.is_ISBN(q) else YushuBook.search_by_key(q)
    return jsonify(r)