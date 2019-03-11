#!/usr/bin/env python
# -*- coding:utf-8 -*-



# http://t.yushu.im/v2/book/isbn/9787501524044
URL_ISBN = 'http://t.yushu.im/v2/book/isbn/{}'
URL_KEY = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'
PER_PAGE = 15

# config默认配置为True，导致jsonify得到的数据在浏览器上无法显示中文
# 或用json.dumps(mydict, ensure_ascii = False)
# 对于安装了JSONView插件的谷歌浏览器不影响吗，会自动呈现合适的形式。
JSON_AS_ASCII = False
BEAN_GIVEN_BY_SYSTEM_PER_BOOK = 0.5