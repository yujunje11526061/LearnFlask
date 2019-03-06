#!/usr/bin/env python
# -*- coding:utf-8 -*-

from wtforms import Form, StringField, PasswordField, ValidationError
from wtforms.validators import Length, NumberRange, DataRequired, Email

from app.models.user import User

class loginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="电子邮箱不符合规范")])
    password = StringField(validators=[DataRequired(message="密码不能为空"), Length(6, 32, message="密码长度需为6~32个字符")])


class RegisterForm(loginForm):
    '''
    其实例，比如form = RegisterForm()，通过form.data获取字典
    {字段名:字段值}
    源码：
    @property
    def data(self):
        return dict((name, f.data) for name, f in iteritems(self._fields))
    可见每个字段值是存在字段对象的data中的
    要获取form中某个字段的值，可以写成form.data["字段名"]，或写成form.字段名.data
    '''
    # email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="电子邮箱不符合规范")])
    # password = StringField(validators=[DataRequired(message="密码不能为空"), Length(6, 32, message="密码长度需为6~32个字符")])
    nickname = StringField(validators=[DataRequired(message="昵称不能为空"), Length(2, 10, message="昵称需为2~10个字符")])

    def validate_email(self,field):
        '''
        自定义验证器必须以validate_columnName的形式，wtforms会自动帮我们去验证对应的字段，不需要手动加到字段定义时的验证器列表中
        用于验证Email账户是否已经被注册
        :param field:字段对象，通过.data取值
        :return:
        '''
        # ORM下查询语句的写法：<模型类>.query.<过滤方法>.<查询方法>
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("此Email已经存在")

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError("此昵称已被占用")