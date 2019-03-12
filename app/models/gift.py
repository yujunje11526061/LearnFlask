#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import current_app
from flask_login import current_user
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, SmallInteger, desc
from sqlalchemy.orm import relationship

from app.models.base import Base
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
    def get_user_gifts(cls,uid):
        return cls.query.filter_by(uid = uid, launched = False).order_by(desc(cls.create_time)).all()

