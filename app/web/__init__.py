#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint, render_template

'''
用多蓝图来分文件有点小题大做，蓝图通常用于大型工程分小项目，单个小项目用单蓝图分文件更合适。下面把多个文件导入，并注册到同一蓝图web上
'''

web = Blueprint('web',__name__)

@web.app_errorhandler(404)
def not_found(e):
    '''
    AOP 面向切面编程, 把所有404异常看成是一个切面, 监听捕获这个切面,并对其处理.
    此函数通过装饰器,监听任何404异常,自动调用本函数处理. 可在本函数下定制404异常时得行为.
    :param e:
    :return:
    '''
    return render_template("404.html"), 404

# 不导入则book文件不会被执行，无法完成里面视图函数的在蓝图上的注册
# 找不到对象,通常是由于没导入或者循环导入的问题.
# 原则:实际运行时同一项目文件只会被导入一次. 从模块导入对象本质上还是进入模块然后按顺序执行代码,直到碰到所要导入的对象,然后合并命名空间
# 如果把以下导入语句移到web实例化之前,则在程序启动时,在app的__init__里导入了一次本文件, 然后在未实例化web之前就导入以下文件, 就会进入相应文件
# 由于在以下文件中又试图从该文件导入web, 因为已经被app的__init__里导入过了,所以不会再导入, 此时在该明明空间中又没有web,就会报错找不到web
# 放到下面,则在以下文件中视图导入web时web已经存在了
# 碰到此类循环导入的问题, 通常通过调整语句顺序可以解决, 如在需要用的时候再导入
# 复杂项目的入口文件不宜实例化对象, 如app, 因为当别的文件需要用到该对象而从入口文件导入时, 由于最初运行时实例化了一个, 导入时又实例化了一个,导致最终运行的app和注册视图函数(蓝图)的app不是同一个.

from . import book
from . import main
from . import wish
from . import drift
from . import auth
from . import gift


