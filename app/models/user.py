#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash

from app.models.base import Base


class User(Base):
    # __tablename__ = "user1"
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    _password = Column(name="password") # 把密码定位私有变量，但是表中名字仍未password

    # 通过公开的方法来操作私有变量，并用装饰为属性描述符，这样就可以直接用父类中的set_attr方法，通过遍历字典实现表单数据到用户实例属性的复制
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        '''
        通过方法来才操作属性，能够进行数据预处理，如加密。
        还可以通过在该描述符属性中限制写操作（不设置写功能，或者返回错误提示），使之成为只读。
        :param raw_password:
        :return:
        '''
        self._password = generate_password_hash(raw_password)