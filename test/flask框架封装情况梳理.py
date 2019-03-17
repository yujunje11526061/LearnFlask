#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import request

'''
以线程ID作为key的字典 --> Local --> LocalStack

Flask --> AppContext        对应栈取名_app_ctx_stack
Request --> RequestContext  对应栈取名_request_ctx_stack

AppContext， RequestContext --> LocalStack

_app_ctx_stack.top 得到Appcontext对象，top.app取到核心对象  -->  current_app，current_app._get_current_object()获得真实app对象而非代理对象
_request_ctx_stack.top 得到RequestContext对象，top.request名字 取到对应请求   --> request
session和g类似。

'''