#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, current_app, request

app = Flask(__name__)



# Flask核心对象 包装成 AppContext 应用上下文 对象
# Request对象 包装成 RequestContext 请求上下文 对象

# 视图函数中flask会自动帮我们实现_request_ctx_stack， _app_ctx_stack的进出栈，request和current_app是两个代理对象，取两个栈顶。视图函数外得手动实现进出栈。
ctx = app.app_context()
ctx.push()
a = current_app
print('```````````````',a)
ctx.pop()
