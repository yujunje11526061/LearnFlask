#!/usr/bin/env python
# -*- coding:utf-8 -*-

from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, Email


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="电子邮箱不符合规范")])
    password = StringField(validators=[DataRequired(message="密码不能为空"), Length(6, 32, message="密码长度需为6~32个字符")])
    nickname = StringField(validators=[DataRequired(message="昵称不能为空"), Length(2, 10, message="昵称需为2~10个字符")])
