#!/usr/bin/env python
# -*- coding:utf-8 -*-
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

    # 因为flask的线程隔离机制,新线程因获得真实的app对象,用如下方法
    app = current_app._get_current_object()
    thread = Thread(target=async_send_mail, args=[msg,app])
    thread.start()
