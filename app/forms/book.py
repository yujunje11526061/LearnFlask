#!/usr/bin/env python
# -*- coding:utf-8 -*-

from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange # 导入各种已有的验证器

'''
Form类类似Scrapy的Item类，字段定义也类似, 可以在字段构造函数中通过关键字参数传入各种功能，如添加标签，验证器，过滤器，默认值等
'''

class SearchForm(Form):
    q = StringField(validators = [Length(min = 1, max=30)])
    page = IntegerField(validators = [NumberRange(min=1, max= 99)], default=1)

