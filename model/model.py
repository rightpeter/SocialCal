#!/usr/bin/env python
#encoding=utf-8
# import tornado.database
import torndb

CalendarDatabase = torndb.Connection(
    "127.0.0.1",
    "social_cal",
    "test",
    "woludie",
)
