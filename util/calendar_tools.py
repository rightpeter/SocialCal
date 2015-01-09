#!/usr/bin/env python
#-*- coding: utf-8 -*-

from model import *
from config import *

def add_event_to_user(event, user):
    CalendarDatabase.execute('''INSERT INTO `calendarTable`(
        hid, title, endtime, allday) VALUE(%s, %s, %s, %s)
        ''' % (user['id'], event['title'], event['starttime'], event['endtime']))
    return True

def get_event_of_user(user):
    events = CalendarDatabase.query('''SELECT * FROM calendarTable WHERE
        hid=%s''' % user['id'])
    return events