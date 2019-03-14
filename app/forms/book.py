#!/usr/bin/env python
# -*- coding:utf-8 -*-

from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp  # 导入各种已有的验证器

'''
Form类类似Scrapy的Item类，字段定义也类似, 可以在字段构造函数中通过关键字参数传入各种功能，如添加标签，验证器，过滤器，默认值等
'''

class SearchForm(Form):
    '''
    定义search视图函数接收到的表单应有的形式
    '''
    q = StringField(validators = [DataRequired(), Length(min = 1, max=30)])
    page = IntegerField(validators = [NumberRange(min=1, max= 99)], default=1)

class DriftForm(Form):

    recipient_name = StringField(validators = [DataRequired(),Length(min=2,max=20, message="收件人姓名必须在2~20个字符之间")])
    message = StringField()
    address = StringField(validators = [DataRequired(), Length(min=10, message= "地址太简略了,写得再详细些吧")])
    mobile = StringField(validators=[DataRequired(), Regexp("^1[0-9]{10}$", 0, message = '请输入正确的手机号')])

