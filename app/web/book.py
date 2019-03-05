#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from flask import request, jsonify, make_response
from app.forms.book import SearchForm
from app.view_model.book import BookCollection
from app.web.blueprint import web
from yushubook import YushuBook


@web.route('/book/search/<q>/<page>/')  # 把视图函数注册到相应蓝图对象
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
    # 以参数构建表单对象
    form = SearchForm(request.args)
    # 表单数据合法性验证
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        yushu_book = YushuBook() # 封装了获取原始数据的过程及得到的原始数据
        books = BookCollection() # 封装了
        isbn_or_key = yushu_book.is_ISBN(q)

        if isbn_or_key:
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_key(q, page)

        books.fill(yushu_book,q)
        # return jsonify(books.__dict__)
        # flask提供的jsonify只能序列化字典，此处BookCollection对象包括其内聚的BookViewModel对象无法被序列化
        # 故使用原生的json.dumps来序列化books，通过default参数自定义序列化策略，ensure_ascii=False参数使可以显示中文
        return json.dumps(books, default= lambda x:x.__dict__, ensure_ascii=False)

    else:
        return jsonify(form.errors)
