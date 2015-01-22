#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 搜索 CalendarDatabase.execute
# 不是： 是/
from model import *
from config import *
import util.myTools as myTools 
from bson.objectid import ObjectId

RELATION_FRIEND = 1
RELATION_STRANGER = 0
PRIVILEGE_CONTENT = 8
PRIVILEGE_SHOWN = 4
PRIVILEGE_ATTEND = 2
PRIVILEGE_SHARE = 1

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

def get_privilege(event, relation):
    if relation == RELATION_FRIEND:
        return event['privilege'] >> 4
    elif relation == RELATION_STRANGER:
        return event['privilege'] & 15
    else:
        return 0

def add_event_to_user(event, user):
    # cal = {}
    # cal['blabla'] = xxxx
    cal = {}
    cal['name'] = user['name']
    cal['title'] = user['title']
    cal['starttime'] = user['starttime']
    cal['endtime'] = user['endtime']
    cal['allday'] = user['allday']
    cal['privilege'] = user['privilege']
    CalCollection.insert(cal)
    return True

def get_host_of_event(event):
    user = myTools.get_user_by_id(event['hid'])
    return user


def get_event_by_id(eid, guest, rel):
    try:
        event = CalCollection.find_one({'_id': ObjectId(eid)})
    except Exception, e:
        print 'get_event_by_id: ', e
        return {}

    user = get_host_of_event(event)
    relation = get_relation(user, guest, rel) 

    event['guest_privilege'] = get_privilege(event, relation)

    if event.guest_privilege&PRIVILEGE_CONTENT != PRIVILEGE_CONTENT:
        event['title'] = None

    if event.guest_privilege&PRIVILEGE_SHOWN != PRIVILEGE_SHOWN:
        event = {}

    return event

def get_events_of_user(user):
    # find({'name': user['name']})
    events = CalCollection.find({'name': user['name']})
    return events

def get_events_of_user_to_guest(user, guest, rel):
    relation = get_relation(user, guest, rel) 
    if relation == RELATION_FRIEND:
        pri = 64
    elif relation == RELATION_STRANGER:
        pri = 4
    else:
        pri = 255

    # 你疯了么。。。。:vsp 试试
    # hjkl 对应方向， ctrl+w 接 一个方向键就可以跳区域
    # 这样你就能看一边敲一边了。。。来回跳多脑残
    # 你写的不对啊 - -
    # 我不知道对不对，先这么写
    # find({'name': user['name'], 'privilege': pri})
    # 卧槽。。完蛋了。。。这个好像暂时没法写。。。用到位运算了。。。妈蛋。。。
    # QQ
    events = CalCollection.find_one("_id", hid)
    events = CalendarDatabase.query('''SELECT id FROM calendarTable WHERE hid=%s
        and privilege&%s=%s''', user['id'], pri, pri)

    # for event in events:
    #     if event.privilege&shown != shown:
    #         event['title'] = None
    #     
    #     if relation == RELATION_FRIEND:
    #         event['privilege'] >>= 4
    #     elif relation == RELATION_STRANGER:
    #         event['privilege'] &= 15
    #     else:
    #         event['privilege'] &= 0

    return events

def share_a_event(guest, eid, rel):
    try:
        event = CalendarDatabase.query('''SELECT * FROM calendarTable WHERE
            id=%s''', eid)[0]
    except Exception, e:
        print 'in share_a_event: ', e
        return False

    user = get_host_of_event(event)
    relation = get_relation(user, guest, rel)

    event['guest_privilege'] = get_privilege(event, relation)

    if event.guest_privilege&PRIVILEGE_SHARE != PRIVILEGE_SHARE:
        return False
    else:
        res = add_event_to_user(event, guest)
        return res
