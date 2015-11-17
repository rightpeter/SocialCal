#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import uuid
from random import choice
# import re
import time
import tornado
import tornado.web
import httplib
import datetime
from model import UserCollection, SaltCollection
# from config import *
import traceback


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("name")

    def get_login_url(self):
        return "/login"


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),


def generate_password(passwd_length, passwd_seed):
    passwd = []
    while len(passwd) < passwd_length:
        passwd.append(choice(passwd_seed))
    return ''.join(passwd)


def get_json(domain, url):
    try:
        httpClient = httplib.HTTPConnection(domain, 8000, timeout=2000)
        httpClient.request('GET', url)

        response = httpClient.getresponse()
        # print response.status
        response.reason
        return response.read()
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
    # return raw_news


def request_info(httprequest):
    print "-----------------------------one request-----------------------------"
    print "method: %s" % httprequest.request.method
    print "uri: %s" % httprequest.request.uri
    print "remote_ip: %s" % httprequest.request.remote_ip
    print "body: %s" % httprequest.request.body
    print "time: %s" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print "-----------------------------one request-----------------------------"
    return False


def insert_a_user(user):
    '''
    user = {
        'email': 'xxx@xx.xx',
        'name': 'xxxx',
        'password': 'xxxx',
        }
    '''
    passwd = user['password']
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(passwd + salt).hexdigest()

    try:
        user['password'] = hashed_password
        UserCollection.insert(user)
        salt_dict = {}
        salt_dict['email'] = user['email']
        salt_dict['salt'] = salt
        SaltCollection.insert(salt_dict)
        return True
    except Exception, e:
        print e
        print traceback.print_exc()
        return False
