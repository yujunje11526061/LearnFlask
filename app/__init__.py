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
    '''
    源码显示init_app方法传入的参数app不作保存，只是临时用一下
    create_all方法底层用到了db的get_app方法，由源码知有三种方式获取，
    1. 作为关键字参数传入
    2. 通过with语句来执行上下文管理器，使得栈中可以取到current_app,
    3. db.app = app，把当前得应用实例作为db得实例属性，把当前数据库实例和应用实例绑定
    '''
    db.init_app(app)
    # 1.
    db.create_all(app=app) # 把数据模型映射到数据库。
    # 2.
    # with app.app_context():
    #     db.create_all()
    # 3.
    # db.app=app
    # db.create_all()
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




