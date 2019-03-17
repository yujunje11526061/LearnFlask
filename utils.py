#!/usr/bin/env python
# -*- coding:utf-8 -*-
from enum import Enum
from threading import Thread
import logging
from traceback import format_exc

from flask import current_app, render_template

from app import mail
from flask_mail import Message


def async_send_mail(msg, app):
    with app.app_context(): # 把实例包装成上下文对象,并用with语句管理上下文实现入展出栈
        try:
            mail.send(msg)
        except:
            logging.error(format_exc())


def send_mail(to, subject, template, **kwargs):
    msg = Message(
            subject=current_app.config["MAIL_SUBJECT_PREFIX"]+subject,
            sender = current_app.config["MAIL_USERNAME"],
            recipients=[to],
            )
    msg.html = render_template(template, **kwargs)

    # 因为flask的线程隔离机制,新线程应获得真实的app对象,用如下方法
    app = current_app._get_current_object()
    thread = Thread(target=async_send_mail, args=[msg,app])
    thread.start()

class PendingStatus(Enum):
    '''
    枚举类中定义的类变量都是枚举变量, 是类的实例对象.
    >>> isinstance(PendingStatus.Redraw, PendingStatus)
    True
    取值的时候都要.value, 但是枚举对象的合理用法就是直接用对象本身,而不是取值.
    实例化时可以给构造函数传枚举类型对应的值得到对应实例, 也可以按类变量的取法取.
    >>> PendingStatus(2)
    <PendingStatus.Success: 2>
    >>> PendingStatus.Reject
    <PendingStatus.Reject: 3>
    '''
    Waiting = 1
    Success = 2
    Reject = 3
    Redraw = 4

    @classmethod
    def pending_str(cls, status:Enum, who:str):
        mapping = {
            cls.Waiting: {
                "requester": "等待对方邮寄",
                "gifter": "等待你邮寄"
            },
            cls.Success: {
                "requester": "对方已邮寄",
                "gifter": "你已邮寄"
            },
            cls.Reject: {
                "requester": "对方已拒绝",
                "gifter": "你已拒绝"
            },
            cls.Redraw: {
                "requester": "你已撤销",
                "gifter": "对方已撤销"
            }
        }
        return mapping[status][who]