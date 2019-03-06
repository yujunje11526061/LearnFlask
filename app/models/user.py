#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import login_manager
from app.models.base import Base


class User(Base, UserMixin):
    '''
    Base基类中定义了模型类的通用方法
    UserMixin类来自flask_login插件，该插件用于管理用户登录(如设置cookie，视图函数访问权限控制)。
    login_user函数调用user对象的get_id方法来设置cookie，具体方法定义在UserMixin类中，自动取用id属性(主键)。继承该类可以不用自己写该插件所必需的一些方法。
    倘若我们不叫id叫idx，则需要覆写get_id方法。
    '''
    # __tablename__ = "user1"
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True, nullable=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    _password = Column(String(128), name="password", nullable=False) # 把密码定位私有变量，但是表中名字仍未password

    # 通过公开的方法来操作私有变量，并用装饰为属性描述符，这样就可以直接用父类中的set_attr方法，通过遍历字典实现表单数据到用户实例属性的复制
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password:str):
        '''
        通过方法来才操作属性，能够进行数据预处理，如加密。
        还可以通过在该描述符属性中限制写操作（不设置写功能，或者返回错误提示），使之成为只读。
        :param raw_password:
        :return:
        '''
        self._password = generate_password_hash(raw_password)

    def check_password(self,raw_password:str):
        return check_password_hash(self.password, raw_password)

@login_manager.user_loader
def get_user(uid):
    # 根据主键获得user对象，不需要filter_by
    return User.query.get(int(uid))