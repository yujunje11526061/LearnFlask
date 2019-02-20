#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask
from app.web.blueprint import web
from app.models.book import db


def create_app():
    app = Flask(__name__)

    # 导入自定义配置文件，源码显示以此函数导入的配置的键必须全大写
    app.config.from_object('app.config')
    app.config.from_object('app.secure_setting')

    # 注册蓝图
    app.register_blueprint(web)

    # 关联数据库
    db.init_app(app)
    db.create_all(app=app) # 把数据模型映射到数据库

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




