#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import current_app

from httptool import HTTP


class YushuBook:

    @classmethod
    def is_ISBN(cls, q: str):
        if len(q) == 13 and q.isdigit():
            return True
        short_q = q.replace('-', '')
        if '-' in q and len(short_q) == 10 and short_q.isdigit():
            return True
        return False

    @classmethod
    def search_by_isbn(cls, isbn):
        r = HTTP.get(current_app.config['URL_ISBN'].format(isbn), return_json=True)
        return r

    @classmethod
    def search_by_key(cls, q, page=1):
        r = HTTP.get(current_app.config['URL_KEY'].format(q, current_app.config['PER_PAGE'], cls.calculate_start(page)), return_json=True)
        return r

    @classmethod
    def calculate_start(cls, page):
        return (page - 1) * current_app.config['PER_PAGE']
