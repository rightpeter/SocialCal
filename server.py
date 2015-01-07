#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado
import torndb

from controller.web import *

class Application(tornado.web.Application):
    handler = [
        ('/', MainHandler),
        ('/signup', SignupHandler)
    ]

