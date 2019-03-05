#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

'''
用多蓝图来分文件有点小题大做，蓝图通常用于大型工程分小项目，单个小项目用单蓝图分文件更合适。下面把多个文件导入，并注册到同一蓝图web上
'''
web = Blueprint('web',__name__)

# 不导入则book文件不会被执行，无法完成里面视图函数的在蓝图上的注册
from . import book
from . import main
from . import wish
from . import drift
from . import auth
from . import gift



