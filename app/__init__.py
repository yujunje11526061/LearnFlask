#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask
from app.web.blueprint import web


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')  # 源码显示以此函数导入的配置的键必须全大写
    app.config.from_object('app.secure_setting')
    register_blueprint(app, web)
    return app


def register_blueprint(app, blueprint):
    '''
    把蓝图对象注册到flask核心对象
    :param app:
    :param blueprint:
    :return:
    '''
    app.register_blueprint(blueprint)
    return




