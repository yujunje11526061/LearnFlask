#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import Column, String, Integer, SmallInteger

from app.models.base import Base
from utils import PendingStatus


class Drift(Base):
    '''
    没用模型关联了, 存储冗余信息, 各有优缺点
    模型关联, 则数据之间实时性同步性好, 省空间, 但是查询关联数据需要额外查询, 降低数据库性能
    存储冗余信息, 则可以记录历史状态, 保存的是某一时刻的状态快照. 费存储空间, 但是可以减少数据库查询次数
    比如下单价格必然是下单时的价格, 不能随着时间遍, 这时候就应该重复记录价格信息而不是关联到商品
    '''

    id = Column(Integer, primary_key=True)
    # 邮寄信息
    recipient_name = Column(String(20),nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile= Column(String(20),nullable=False)
    # 书籍信息
    isbn = Column(String(13))
    book_title=Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))
    # 请求者信息
    requester_id =Column(Integer)
    requester_nickname = Column(String(20))
    # 赠送者信息
    gifter_id= Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))

    # 记录当前状态, 应该用枚举类型, 一目了然, 而不是直接用状态数字. 枚举类要取值记得取value,但是良好的枚举写法就应该用枚举对象名
    _pending = Column("pending", SmallInteger, default = PendingStatus.Waiting.value)

    @property
    def pending(self):
        '''
        由于字段类型只能是SmallInteger, orm没有枚举类型, 故实际存的时候存数据
        而为了使用清晰明了, 用的时候应该用枚举类型 中间通过属性描述符转换.
        :return:
        '''
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, newStatus):
        self._pending = newStatus.value
