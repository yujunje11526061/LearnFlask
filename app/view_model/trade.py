#!/usr/bin/env python
# -*- coding:utf-8 -*-

class TradeInfo():

    def __init__(self, goods):
        self.trades = [self._parse_single(good) for good in goods]
        self.total = len(self.trades)

    def _parse_single(self, single: "礼物或心愿"):
        return dict(
            user_name=single.user.nickname,
            create_time=single.create_datetime,
            id=single.id
        )
