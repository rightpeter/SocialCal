#!/usr/bin/env python
#-*- coding: utf-8 -*-

from model import *
from config import *

RELATION_FRIEND = 1
RELATION_STRANGER = 0
def cal_privilege(privilege_list):
    '''
    privilege_list = [
        friend_content, friend_space, friend_attend, friend_share,
        stranger......,
    ]
    '''
    res = 0
    for i in privilege_list:
        res <<= 1
        res += i
    return res

def get_relation(user, guest, res):
    '''
    res = 1 : Friend
    res = 0 : Stranger
    '''
    return res

def get_privilege(event, privilege):
    if privilege == RELATION_FRIEND:
        return event['privilege'] >> 4
    else:
        return event['privilege'] & 15

def add_event_to_user(event, user):
    CalendarDatabase.execute('''INSERT INTO `calendarTable`(
        hid, title, starttime, endtime, allday, privilege) VALUE(%s, %s, %s,
        %s, %s, %s) ''', user['id'], event['title'], event['starttime'],
            event['endtime'], event['allday'], event['privilege'])
    return True

def get_event_of_user(user):
    events = CalendarDatabase.query('''SELECT id FROM calendarTable WHERE
        hid=%s''' % user['id'])
    return events

def get_event_of_user_to_guest(user, guest, rel):
    relation = get_relation(user, guest, rel) 
    if relation == RELATION_FRIEND:
        pri = 64
        # shown = 128
    elif relation == RELATION_STRANGER:
        pri = 4
        # shown = 8
    else:
        pri = 255
        # shown = 0

    events = CalendarDatabase.query('''SELECT id FROM calendarTable WHERE hid=%s
        and privilege&%s=%s''', user['id'], pri, pri)

    # for event in events:
    #     if event.privilege&shown != shown:
    #         event.title = None
    #     
    #     if relation == RELATION_FRIEND:
    #         event['privilege'] >>= 4
    #     elif relation == RELATION_STRANGER:
    #         event['privilege'] &= 15
    #     else:
    #         event['privilege'] &= 0

    return events
