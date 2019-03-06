#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import current_app

from httptool import HTTP


class YushuBook:
    
    def __init__(self):
        self.total = 0
        self.books = []

    def is_ISBN(self, q: str):
        if len(q) == 13 and q.isdigit():
            return True
        short_q = q.replace('-', '')
        if '-' in q and len(short_q) == 10 and short_q.isdigit():
            return True
        return False

    def search_by_isbn(self, isbn):
        r = HTTP.get(current_app.config['URL_ISBN'].format(isbn), return_json=True)
        self.__fill_single(r)


    def search_by_key(self, q, page=1):
        r = HTTP.get(current_app.config['URL_KEY'].format(q, current_app.config['PER_PAGE'], self.calculate_start(page)), return_json=True)
        self.__fill_collection(r)

    def __fill_single(self,data:dict):
        if data:
            self.total = 1
            self.books = [data]

    def __fill_collection(self,data:dict):
        self.total = data.get("total",0)
        self.books = data.get("books",[])

    def calculate_start(self, page):
        return (page - 1) * current_app.config['PER_PAGE']

    @property
    def first(self):
        return self.books[0] if len(self.books)>0 else None
