# -*- coding: utf-8 -*-
import webapp2

from urls import routes
from settings import DEBUG, config
from handler import BaseHandler
from models import Flatpage, Category, Board

def _debug_flatpage():
    flatpage = Flatpage(name='MOTD', content='123')
    flatpage.put()
    category = Category(name='Test')
    category.put()
    board = Board(category=category, name='Test', link='http://www.yahoo.com.tw')
    board.put()

def get_flatpage(title):
    q = Flatpage.all()
    res = q.filter('title =', title).get()
    if res:
        return res.content
    return

class IndexPage(BaseHandler):
    def get(self):
        #_debug_flatpage()
        context = {}
        context['config'] = config
        context['content'] = ''
        if not config['WARNING_PAGE']:
            self.redirect('/main/')
            return
        res = get_flatpage('MOTD')
        if res : context['content'] = res
        self.render_response('index.html', **context)
        
class MainPage(BaseHandler):
    def get(self):
        context = {}
        context['config'] = config
        self.render_response('main.html', **context)
        
class MotdPage(BaseHandler):
    def get(self):
        context = {}
        context['config'] = config
        res = get_flatpage('MOTD')
        if res : context['content'] = res
        self.render_response('main_motd.html', **context)
        
class MenuPage(BaseHandler):
    def get(self):
        context = {}
        context['config'] = config
        q = Category.all()
        q.filter('enable =', True)
        q.order('order')
        q.fetch(1000)
        context['categorys'] = q
        self.render_response('bbsmenu.html', **context)
        
app = webapp2.WSGIApplication(routes=routes, debug=DEBUG, config=config)