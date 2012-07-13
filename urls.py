# -*- coding: utf-8 -*-
import webapp2

import appengine_admin

routes = [
    (r'/', 'main.IndexPage'),
    (r'/main/', 'main.MainPage'),
    (r'/mainmenu/', 'main.MotdPage'),
    (r'/bbsmenu/', 'main.MenuPage'),
    (r'^(/admin)(.*)$', appengine_admin.Admin),
]

