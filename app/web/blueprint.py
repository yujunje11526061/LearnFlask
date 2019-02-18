#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint

'''
用多蓝图来分文件有点小题大做，蓝图通常用于大型工程分小项目，单个小项目用单蓝图分文件更合适。
'''
web = Blueprint('web',__name__)