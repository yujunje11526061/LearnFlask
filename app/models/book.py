#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy # 从flask封装的sqlalchemy中导入SQLAlchemy类


db = SQLAlchemy()

class book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未名')
    binding = Column(String(20))  # 精装or平装
    publisher = Column(String(50))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))

    # MVC M Model 如果只有数据，等同于数据表，但是模型层会写很多业务逻辑，来操作数据
    # ORM，对象关系映射，通过操作模型来操作数据库