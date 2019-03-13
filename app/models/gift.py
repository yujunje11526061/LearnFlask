#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import current_app
from flask_login import current_user
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, SmallInteger, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from yushubook import YushuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    # 建立Gift模型和User模型的关联
    user = relationship("User")
    uid = Column(Integer, ForeignKey("user.id")) # 对应上一行的user
    # book = relationship("Book")
    # bid = Column(Integer, ForeignKey("book.id"))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False) # False代表还未送出去

    @classmethod
    def recent(cls):
        # 复杂SQL的编写，链式调用。类似pyquery中封装的的css选择器
        # 主体query
        # 一系列过滤条件, 每次都返回新的query
        # 查询条件如first(), all(), 才会执行真正的SQL查询
        return Gift.query.filter_by(launched = False).\
                group_by(Gift.isbn).\
                order_by(desc(Gift.create_time)).\
                limit(current_app.config["BOOK_NUMBER_IN_HOMEPAGE"]).\
                all()

    @property
    def book(self):
        '''
        :return:礼物所对应的书籍信息
        '''
        yushu_book = YushuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_all_gifts(cls, isbn_list):
        '''
        根据传入的一组isbn,查询wish表中,每个isbn对应的记录数量
        利用session来查询, filter语句相比filter_by语句更灵活, 写的是条件表达式,而filter_by写的是关键字参数
        利用mysql 的 in 功能
        利用func.count (sqlalchemy库的func对象封装了MySQL的汇总函数) 和group_by结合进行分组统计
        :param isbn_list:
        :return: 一组数量, dict(isbn=isbn,数量=数量)构成的列表
        '''
        # SELECT COUNT(id), isbn
        # FROM gift
        # WHERE acquired=0 AND isbn IN isbn_list AND status = 1
        # GROUP BY isbn;
        count_list = db.session.query(func.count(cls.id), cls.isbn).\
                        filter(cls.launched==False,cls.isbn.in_(isbn_list), cls.status==1).\
                        group_by(cls.isbn).all()
        # count_list是一个二元祖组成的列表, 返回元祖列表需要调用方了解细节,不友好,故转化成字典列表,也可以用namedtuple
        return [dict(count=count, isbn= isbn) for count, isbn in count_list]

    @classmethod
    def get_user_gifts(cls,uid):
        return cls.query.filter_by(uid = uid, launched = False).order_by(desc(cls.create_time)).all()

