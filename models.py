'''
Created on 2011/04/24

@author: glassesfactory
'''

from google.appengine.ext import db

class Status(db.Model):
    status_id = db.IntegerProperty()
    user = db.StringProperty()
    text = db.TextProperty()
    icon_url = db.StringProperty()
    
class RepliedStatus(db.Model):
    status_id = db.IntegerProperty()