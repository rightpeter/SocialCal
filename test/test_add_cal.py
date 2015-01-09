#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import util.myTools as myTools
import util.calendar_tools as calendar_tools

def test_add_birthday_to_rightpeter():
    user = myTools.get_user_by_name('Rightpeter')
    birthday_event = {}
    birthday_event['title'] = 'birthday'
    birthday_event['starttime'] = '2015-06-22 00:00:00'
    birthday_event['endtime'] = '2015-06-22 23:59:59'
    birthday_event['allday'] = 1
    res = calendar_tools.add_event_to_user(birthday_event, user)
    print 'res: ', res
    events = calendar_tools.get_event_of_user(user)
    print 'events: ', events

if __name__ == '__main__':
    test_add_birthday_to_rightpeter()
