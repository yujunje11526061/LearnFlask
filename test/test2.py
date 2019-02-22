#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from threading import Thread

from werkzeug.local import Local

'''
werkzeug Local类，__slots__ = ('__storage__', '__ident_func__')，__storage__属性为一个存储信息的字典，key为线程ID，value为info字典。__ident_func__属性为获取线程ID的函数对象。且是一个描述符类，自定义了三个方法。

该类通过巧妙封装，实现了线程隔离，不同线程修改Local类的实例属性时，相互之间不干扰，因为内部为每个线程各自配备了存储信息的字典
'''


obj = Local()
obj.a = 1
print('In main thread obj.a is', obj.a)

def manipulate():
    obj.a = 2
    print('In newThread obj.a is', obj.a)


newThread = Thread(name = 'newThread', target= manipulate)
newThread.start()
newThread.run()
time.sleep(2)

print('In main thread obj.a is', obj.a)

