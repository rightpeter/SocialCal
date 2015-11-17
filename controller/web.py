#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado
import util.myTools as myTools

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello Social Calendar!')

class SignupHandler(myTools.BaseHandler):
    def get(self):
        user = myTools.get_current_user(self)
        #if self.get_secure_cookie('guest'):
        #    user['name'] = self.get_secure_cookie('guest')
        #    user['id'] = myTools.get_id_by_name(user['name'])
        #    guest = self.get_secure_cookie('guest')
        #elif self.get_current_user():
        #    user['name'] = self.get_current_user()
        #    user['id'] = myTools.get_id_by_name(user['name'])
        login_state = self.get_cookie('login')
        print 'sign up get!'
        self.render('signup.html', user=user, url='/', login_state=login_state)

    def post(self):
        myTools.request_info()
        user = {}
        user['email'] = self.get_argument('email')
        user['name'] = self.get_argument('name')
        user['password'] = self.get_argument('password')
        re_password = self.get_argument('repassword')

        try:
            if self.get_argument('is_subscribed'):
                user['subscribed'] = 1
        except:
            user['subscribed'] = 0

        if user['password'] == re_password:
            if myTools.is_email_exist(user['email']) and not myTools.is_name_exist(user['name']):
                if myTools.insert_a_user(user):
                    myTools.send_check_email(user['email'])
                    print 'befor myTools.login!'
                    if myTools.login(user['email'], user['password']):
                        print 'after myTools.login!'
                        self.set_secure_cookie('guest', user['name'])
                        self.redirect('/signup')
        self.write('Signup Failed!')

class testHandler(tornado.web.RequestHandler):
    def get(self, openId):
        print 'self.request: ', self.request

    def post(self, openId):
        print 'self.request: ', self.request
