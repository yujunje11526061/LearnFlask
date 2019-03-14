#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app.models.drift import Drift
from utils import PendingStatus


class DriftViewModel:
    def __init__(self, drift:"Drift模型", current_user_id):
        self.data = self.__parse(drift, current_user_id)

    def __parse(self, drift,current_user_id):
        you_are = self.requester_or_gifter(drift, current_user_id)
        status_str = PendingStatus.pending_str(drift.pending, you_are)
        data = dict(
            you_are = you_are,
            drift_id = drift.id,
            book_title = drift.book_title,
            book_author = drift.book_author,
            book_img = drift.book_img,
            date = drift.create_datetime.strftime("%Y-%m-%d"),
            message = drift.message,
            address = drift.address,
            recipient_name = drift.recipient_name,
            mobile = drift.mobile,
            status = drift.pending,
            operator = drift.requester_nickname if you_are !="requester" else drift.gifter_nickname,
            status_str = status_str
        )
        return data

    def requester_or_gifter(self, drift, current_user_id):
        if current_user_id == drift.requester_id:
            you_are = "requester"
        else:
            you_are = "gifter"
        return you_are

class DriftCollection:
    def __init__(self, drifts:"Drift模型列表", current_user_id):
        self.data = self.__parse(drifts, current_user_id)

    def __parse(self, drifts, current_user_id):
        temp = []
        for drift in drifts:
            temp.append(DriftViewModel(drift, current_user_id).data)
        return temp