#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime

# from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
# 从flask封装的sqlalchemy中导入SQLAlchemy类，并重命名，目的是为了可以自定义一个同名的子类，从而在子类中增加一些自定义的扩展功能
from sqlalchemy import SmallInteger, Column, Integer
from contextlib import contextmanager

class SQLAlchemy(_SQLAlchemy):
    '''
    自定义一个同名的子类，从而在子类中增加一些自定义的扩展功能, 子类名字不好取，又想按照用父类那样写，故从框架中把父类导入时重命名一下
    '''
    @contextmanager
    def auto_commit(self):
        '''
        为了避免重复写事务操作的代码，用一个上下文管理函数包装下公共代码
        :return:
        '''
        yield
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            # raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        '''
        由于是做软删除，所以记录仍在，只是标记成已删除
        业务中查询是必然是没被删除的条目，故必须有status==1，为了避免每次查询时写这个条件，覆盖框架的filter_by方法
        :param kwargs:
        :return:
        '''
        if "status" not in kwargs:
            kwargs["status"] = 1
        return super().filter_by(**kwargs)

db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    # 每个db.Model的子类都会被SQLAchelmy所记录，故只需建立db和app的绑定即可，在creat_all时会自动为记录的所有模型创建表，如果不希望创建此表，则需要设置该属性，标记为是抽象的。
    __abstract__ = True

    # status 字段定义是否删除了，这是一种软删除形式。，当删除行为发生时，更改为删除状态,status=0，但是保留历史记录。物理删除即直接删除数据，这样会丢失历史纪录
    status = Column(SmallInteger, default=1)
    create_time = Column("create_time", Integer) # 不能在此处设置default，类变量时在类加载时定义的，而每个对象的create_time应该是对象创建时记录，故必须用构造函数

    def __init__(self):
        self.create_time = int(datetime.datetime.now().timestamp())

    def set_attr(self, data:dict):
        '''
        将提交的表单数据复制到实例对象的同名属性下
        :param form:
        :return:
        '''
        for key, val in data.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, val)

    @property
    def create_datetime(self):
        return datetime.datetime.fromtimestamp(self.create_time)