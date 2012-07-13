# -*- coding: utf-8 -*-
import webapp2
from google.appengine.api import memcache

from urls import routes
from settings import DEBUG, config
from handler import BaseHandler
from models import Flatpage, Category, Board

def get_flatpage(title):
    q = Flatpage.all()
    res = q.filter('title =', title).get()
    if res:
        return res.content
    return

class IndexPage(BaseHandler):
    def get(self):
        if config['MEMCAHCE_ENABLE']:
            data = memcache.get('IndexPage')
            if data is not None:
                self.response.write(data)
                return
        context = {}
        context['config'] = config
        context['content'] = ''
        if not config['WARNING_PAGE']:
            self.redirect('/main/')
            return
        res = get_flatpage('MOTD')
        if res : context['content'] = res
        data = self.render_to_cahce('index.html', **context)
        memcache.add('IndexPage', data, config['MEMCACHE_EXPIRES'])
        self.response.write(data)
        #self.render_response('index.html', **context)
        
class MainPage(BaseHandler):
    def get(self):
        if config['MEMCAHCE_ENABLE']:
            data = memcache.get('MainPage')
            if data is not None:
                self.response.write(data)
                return
        context = {}
        context['config'] = config
        data = self.render_to_cahce('main.html', **context)
        memcache.add('MainPage', data, config['MEMCACHE_EXPIRES'])
        self.response.write(data)
        #self.render_response('main.html', **context)
        
class MotdPage(BaseHandler):
    def get(self):
        if config['MEMCAHCE_ENABLE']:
            data = memcache.get('MotdPage')
            if data is not None:
                self.response.write(data)
                return
        context = {}
        context['config'] = config
        res = get_flatpage('MOTD')
        if res : context['content'] = res
        data = self.render_to_cahce('main_motd.html', **context)
        memcache.add('MotdPage', data, config['MEMCACHE_EXPIRES'])
        self.response.write(data)
        #self.render_response('main_motd.html', **context)
        
class MenuPage(BaseHandler):
    def get(self):
        if config['MEMCAHCE_ENABLE']:
            data = memcache.get('MenuPage')
            if data is not None:
                self.response.write(data)
                return
        context = {}
        context['config'] = config
        q = Category.all()
        q.filter('enable =', True)
        q.order('order')
        q.fetch(1000)
        context['categorys'] = q
        data = self.render_to_cahce('bbsmenu.html', **context)
        memcache.add('MenuPage', data, config['MEMCACHE_EXPIRES'])
        self.response.write(data)
        #self.render_response('bbsmenu.html', **context)
        
class ClearCachePage(BaseHandler):
    def get(self):
        if config['MEMCAHCE_ENABLE']:
            memcache.delete('IndexPage')
            memcache.delete('MainPage')
            memcache.delete('MotdPage')
            memcache.delete('MenuPage')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('okay!')
      
app = webapp2.WSGIApplication(routes=routes, debug=DEBUG, config=config)