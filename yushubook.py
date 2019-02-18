#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import current_app
from httptool import HTTP


class YushuBook:

    @classmethod
    def is_ISBN(cls, q:str):
        if len(q)==13 and q.isdigit():
            return True
        short_q = q.replace('-','')
        if '-' in q and len(short_q) == 10 and short_q.isdigit():
            return True
        return False

    @classmethod
    def search_by_isbn(cls,isbn):
        r = HTTP.get(current_app._get_current_object().config['URLISBN'].format(isbn), return_json=True)
        return r

    @classmethod
    def search_by_key(cls, q, count=15, start=0):
        r = HTTP.get(current_app._get_current_object().config['URLKEY'].format(q, count, start), return_json=True)
        return r



