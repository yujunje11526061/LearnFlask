#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint

web = Blueprint('web',__name__)


@web.route('/book/') # 把视图函数注册到相应蓝图对象
def hello_world():
    return 'Hello World!'
    # return时flask会自动封装成一个response对象。

# http://t.yushu.im/v2/book/isbn/9787501524044