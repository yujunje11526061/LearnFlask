#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import request, jsonify, make_response
from app.forms.book import SearchForm
from app.web.blueprint import web
from yushubook import YushuBook


@web.route('/book/search/<q>/<page>/') # 把视图函数注册到相应蓝图对象
def search(q, page):
    '''
    :param q: 普通关键字
    :param page:
    :return:
    jsonify()函数可将字典封装成response对象
    '''
    r = YushuBook.search_by_isbn(q) if YushuBook.is_ISBN(q) else YushuBook.search_by_key(q)
    return jsonify(r)

# @web.route('/book/search/')
# def search2():
#     '''
#     ?q={}&page={} 方式传参
#     request上下文对象的args属性（MultiDict）来获取参数
#     :param q: 普通关键字
#     :param page:
#     :return:
#     '''
#     q = request.args.get('q')
#     page = request.args.get('page')
#     r = YushuBook.search_by_isbn(q) if YushuBook.is_ISBN(q) else YushuBook.search_by_key(q)
#     return jsonify(r)

@web.route('/book/search/')
def search2():
    '''
    ?q={}&page={} 方式传参
    request上下文对象的args属性（MultiDict）来获取参数
    WTForms插件来进行参数验证
    :param q: 普通关键字
    :param page:
    :return:
    '''
    form = SearchForm(request.args)
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        r = YushuBook.search_by_isbn(q) if YushuBook.is_ISBN(q) else YushuBook.search_by_key(q)
        return jsonify(r)
    return jsonify(form.errors)