#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship

from app.models.base import Base


class Gift(Base):
    id = Column(Integer, primary_key=True)
    # 建立Gift模型和User模型的关联
    user = relationship("User")
    uid = Column(Integer, ForeignKey("user.id")) # 对应上一行的user
    # book = relationship("Book")
    # bid = Column(Integer, ForeignKey("book.id"))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)
