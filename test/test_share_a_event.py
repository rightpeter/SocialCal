#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import util.myTools as myTools
import util.calendar_tools as calendar_tools

def test_share_a_event():
    user = myTools.get_user_by_name('Rightpeter')
    guest = myTools.get_user_by_name('june_fiend')
    events = calendar_tools.get_event_of_user_to_guest(user, guest, 1)
    for event in evnets:
        print 'id: ', event.id, ' title: ', event.title, ' privilege: ', event.privilege

    eid = raw_input('Input the ID of event: \n')
    res = calendar_tools.share_a_event(

if __name__ == '__main__':
    test_share_a_event()
