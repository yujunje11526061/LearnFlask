#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask_sqlalchemy import SQLAlchemy # 从flask封装的sqlalchemy中导入SQLAlchemy类
from sqlalchemy import SmallInteger, Column

db = SQLAlchemy()


class Base(db.Model):
    # 每个db.Model的子类都会被SQLAchelmy所记录，故只需建立db和app的绑定即可，在creat_all时会自动为记录的所有模型创建表，如果不希望创建此表，则需要设置该属性，标记为是抽象的。
    __abstract__ = True

    # status 字段定义是否删除了，这是一种软删除形式。，当删除行为发生时，更改为删除状态，但是保留历史记录。物理删除即直接删除数据，这样会丢失历史纪录
    status = Column(SmallInteger, default=1)

    def set_attr(self, form:dict):
        '''
        将提交的表单数据复制到实例对象的同名属性下
        :param form:
        :return:
        '''
        for key, val in form.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, val)