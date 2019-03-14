#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import login_manager
from app.models.base import Base, db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from utils import PendingStatus
from yushubook import YushuBook


class User(Base, UserMixin):
    '''
    Base基类中定义了模型类的通用方法
    UserMixin类来自flask_login插件，该插件用于管理用户登录(如设置cookie，视图函数访问权限控制)。
    login_user函数调用user对象的get_id方法来设置cookie，具体方法定义在UserMixin类中，自动取用id属性(主键)。继承该类可以不用自己写该插件所必需的一些方法。
    倘若我们不叫id叫idx，则需要覆写get_id方法。

    相关业务逻辑都通过方法写在模型层, 控制层(视图函数)中只写对方法的调用来实现业务逻辑,实现对逻辑细节的封装
    方法名字应能看出业务内容,使得调用方代码能清洗明了.
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

    def generate_token(self, expiredTime = 600):
        # 用itsdangerous库生成token
        # 用密钥生成一个序列化器
        s = Serializer(current_app.config["SECRET_KEY"], expiredTime)
        # 把相关信息组成的字典加密序列化得到token, 得到的是字节码(ASCII码也是utf-8的一部分).用utf-8解码
        token = s.dumps({"id":self.id}).decode("utf-8")
        return token

    @classmethod
    def reset_password(cls,token, newPassword):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            id = s.loads(token.encode("utf-8")).get("id")
        except: # token过期或者是篡改的,则itsdangerous库会抛出异常
            return False
        with db.auto_commit():
            user = cls.query.get(id) # 主键查询可以直接用get
            if user:
                user.password = newPassword
            else:
                return False
        return True

    def change_password(self,  newPassword):
        with db.auto_commit():
            # 数据库的改操作,可以直接改了提交. 插入才需要add进会话
            self.password = newPassword
        return True



    def check_password(self,raw_password:str):
        return check_password_hash(self.password, raw_password)

    @property
    def baseInfo(self):
        return dict(
            nickname = self.nickname,
            send_receive = str(self.send_counter)+"/"+str(self.receive_counter),
            beans =  self.beans,
            email = self.email,
        )

    def can_save_to_gift_list(self, isbn):
        yushu_book = YushuBook()
        if not yushu_book.is_ISBN(isbn):
            return False
        yushu_book.search_by_isbn(isbn)
        if yushu_book.first is None:
            return False
        # 同样的书不能在正想要的时候还想送
        wishing =  Wish.query.filter_by(uid = self.id, isbn = isbn, acquired = False).first()
        # 未送出去前，不能重复添加多本同样的书。
        gifting = Gift.query.filter_by(uid= self.id, isbn = isbn, launched = False).first()
        if wishing is None and gifting is None:
            return True
        else:
            return False

    def can_save_to_wish_list(self, isbn):
        yushu_book = YushuBook()
        if not yushu_book.is_ISBN(isbn):
            return False
        yushu_book.search_by_isbn(isbn)
        if yushu_book.first is None:
            return False
        # 同样的书不能正在送的时候还有想要
        gifting =  Gift.query.filter_by(uid = self.id, isbn = isbn, launched = False).first()
        # 还没收到时，不能重复添加多本同样的书。
        wishing = Wish.query.filter_by(uid= self.id, isbn = isbn, acquired = False).first()
        if wishing is None and gifting is None:
            return True
        else:
            return False

    def can_send_drift(self):
        if self.beans<1:
            return False
        success_gifts_count = Gift.query.filter_by(id=self.id, launched = True).count()
        success_drifts_count = Drift.query.filter_by(requester_id=self.id, pending = PendingStatus.Success).count()
        return success_drifts_count//2 <= success_gifts_count

    @property
    def summary(self):
        return dict(
            nickname = self.nickname,
            beans = self.beans,
            email = self.email,
            send_receive = str(self.send_counter)+ "/" + str(self.receive_counter)
        )



@login_manager.user_loader
def get_user(uid):
    # 根据主键id获得user对象，get写比较方便. 必须是整数
    return User.query.get(int(uid))