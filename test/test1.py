#!/usr/bin/env python
# -*- coding:utf-8 -*-
def test_context():
    from flask import Flask, current_app, request

    app = Flask(__name__)

    # Flask核心对象 包装成 AppContext 应用上下文 对象
    # Request对象 包装成 RequestContext 请求上下文 对象

    # 视图函数中flask会自动帮我们实现_request_ctx_stack， _app_ctx_stack的进出栈，request和current_app是两个代理对象，取两个栈顶。视图函数外得手动实现进出栈。
    ctx = app.app_context()
    ctx.push()
    a = current_app
    print('```````````````',a,'```````````')
    ctx.pop()

    # 实现了__enter__和__exit__方法的对象（这里是AppContext对象）可以用with语句来管理上下文
    # 在AppContext对象的这两个方法中分别实现了进出栈。
    # as后面的引用指向上下文管理器的__enter__方法返回值，通常会返回self，此处源码也是，从而获得上下文管理器对象
    with app.app_context() as ctx:
        a = current_app
        print('```````````````', a, '```````````')

class MyResource():

    def __enter__(self):
        print('Connect resource')
        return self

    def __exit__(self, exc_type:'异常类型', exc_val:'异常信息', exc_tb:'异常堆栈信息')->bool:
        if exc_tb:
            print(exc_type,'----',exc_val,'----',exc_tb)
        else:
            print('No exception')
        print('Disconnect resource')
        return False # 返回True表明异常已被处理，不再上抛，否则继续抛，不return代表返回None，仍判为False

    def query(self):
        print('Manipulate resource')

def test_with():
    try:
        with MyResource() as resource:
            1/0
            resource.query()
    except Exception as e:
        print(e)

# test_context()
test_with()