# -*- coding: utf-8 -*-
from google.appengine.ext import db

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
    name = db.StringProperty(required=True, choices=set(KIND_CHOICES))
    content = db.TextProperty(required=True)
    
class Category(db.Model):
    name = db.StringProperty(required=True)
    order = db.IntegerProperty(required=True, default=9999)
    tag = db.StringProperty()
    enable = db.BooleanProperty(required=True, default=True)
    create_time = db.DateTimeProperty(auto_now_add=True)
    
    def get_board(self):
        q = Board.all()
        q.filter('category =', self)
        q.filter('enable =', True)
        q.order('order')
        return q.fetch(1000)
    
class Board(db.Model):
    category = db.ReferenceProperty(reference_class=Category)
    name = db.StringProperty(required=True)
    order = db.IntegerProperty(required=True, default=9999)
    target = db.StringProperty(required=True, choices=set(TARGET_CHOICE), default='cont')
    link = db.LinkProperty()
    tag = db.StringProperty(choices=set(KIND_CHOICES))
    enable = db.BooleanProperty(required=True, default=True)
    create_time = db.DateTimeProperty(auto_now_add=True)