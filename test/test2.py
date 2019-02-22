#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
进程，意义上是分配资源；线程，共享进程资源，意义上是操作共享的资源

werkzeug 的 Local类，__slots__ = ('__storage__', '__ident_func__')，__storage__属性为一个存储信息的字典，key为线程ID，value为info字典。__ident_func__属性为获取线程ID的函数对象。且是一个描述符类，自定义了三个方法。

该类通过巧妙封装，实现了线程隔离，不同线程修改Local类的实例属性时，相互之间不干扰，因为内部为每个线程各自配备了存储信息的字典

LocalStack类，线程隔离的栈结构。在Local上进一步封装，从而不同的线程有各自的栈

为什么要有线程隔离的栈？
因为在flask中都是用同一个变量名去引用相似的一类对象，如request引用Request对象，如何正确区分？
flask通过包装成上下文对象，通过栈的特性，来保证上下文对象的存储和一致性（AppContext对象和RequestContext对象配套）。
线程隔离特性，保证线程之间操作各自的栈而互不干扰。（Request对象因为实例化了多个，所以需要隔离，而核心对象实际上只有一个，隔不隔离没有意义。）
意义在于：能使当前的线程能够正确引用到他自己所创建的对象，而不是引用到其他线程所创建的对象。虽然都叫相同的名字，但是从各自的栈顶取。从而保证不同请求的隔离性。

为什么要用一个栈来存取上下文对象？
实际上多线程模式下，一个请求由一个线程来处理，请求来进栈，处理完出栈，不需要保存多个上下文。但有些情况下，如离线脚本或单元测试时，可能会需要推入多个上下文，故需要一个容器来存取。
'''

import time
from threading import Thread, current_thread

from werkzeug.local import Local, LocalStack

obj = Local()
obj.a = 1
print(f'In {current_thread().name} {obj.__ident_func__()} obj.a is', obj.a)

def manipulate():
    obj.a = 2
    print(f'In {current_thread().name} {obj.__ident_func__()} obj.a is', obj.a)


newThread = Thread(name = 'newThread', target= manipulate)
newThread.start()
time.sleep(1)

print(f'In {current_thread().name} {obj.__ident_func__()} obj.a is', obj.a)


# 线程隔离栈的试验
stk = LocalStack()
stk.push(1)
print(f'In {current_thread().name} {stk._local.__ident_func__()} stk.top is', stk.top)

def manipulateStack():
    print(f'In {current_thread().name} {stk._local.__ident_func__()} stk.top is', stk.top)



newTread2 = Thread(name= 'newThread2', target = manipulateStack)
newTread2.start()
time.sleep(1)

print(f'In {current_thread().name} {stk._local.__ident_func__()} stk.top is', stk.top)