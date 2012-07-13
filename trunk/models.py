# -*- coding: utf-8 -*-
from google.appengine.ext import db

import appengine_admin

KIND_CHOICES = [
    'MOTD',
]

TARGET_CHOICE = [
    'cont',
    '_blank',
    'tag',
]

TAG_CHOICE = [
    'new',
    'beta',
]

class Flatpage(db.Model):
    title = db.StringProperty(required=True, choices=set(KIND_CHOICES))
    content = db.TextProperty(required=True)
    
class Category(db.Model):
    title = db.StringProperty(required=True)
    order = db.IntegerProperty(required=True, default=9999)
    tag = db.StringProperty()
    enable = db.BooleanProperty(required=True, default=True)
    create_time = db.DateTimeProperty(auto_now_add=True)

    def __unicode__(self):
        return self.title
    
    def get_board(self):
        q = Board.all()
        q.filter('category =', self)
        q.filter('enable =', True)
        q.order('order')
        return q.fetch(1000)
    
class Board(db.Model):
    category = db.ReferenceProperty(reference_class=Category)
    title = db.StringProperty(required=True)
    order = db.IntegerProperty(required=True, default=9999)
    target = db.StringProperty(required=True, choices=set(TARGET_CHOICE), default='cont')
    link = db.LinkProperty()
    tag = db.StringProperty(choices=set(TAG_CHOICE))
    enable = db.BooleanProperty(required=True, default=True)
    create_time = db.DateTimeProperty(auto_now_add=True)
    
class FlatpageAdmin(appengine_admin.ModelAdmin):
    model = Flatpage
    listFields = ('title',)
    editFields = ('title', 'content')
    
class CategoryAdmin(appengine_admin.ModelAdmin):
    model = Category
    listFields = ('title', 'order', 'enable', 'create_time')
    editFields = ('title', 'order', 'tag', 'enable')
    readonlyFields = ('create_time',)
        
class BoardAdmin(appengine_admin.ModelAdmin):
    model = Board
    listFields = ('category', 'title', 'order', 'enable', 'create_time')
    editFields = ('category', 'title', 'order', 'target', 'link', 'tag', 'enable')
    readonlyFields = ('create_time',)    
    
appengine_admin.register(FlatpageAdmin, CategoryAdmin, BoardAdmin)