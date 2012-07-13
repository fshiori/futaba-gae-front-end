# -*- coding: utf-8 -*-
import webapp2

routes = [
    (r'/', 'main.IndexPage'),
    (r'/main/', 'main.MainPage'),
    (r'/mainmenu/', 'main.MotdPage'),
    (r'/bbsmenu/', 'main.MenuPage'),
]