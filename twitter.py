# -*- coding: utf-8 -*-
'''
Created on 2011/04/24

@author: glassesfactory
'''

"""
なんか色々参考にしたよ
"""

from google.appengine.ext.webapp import util
import random
import yaml
import re

import tweepy
import config
from models import Status, RepliedStatus

ptn = re.compile('^\@%s\s(.+)$' % 'boorin_bot')

class BotCore(object):
    def __init__(self):
        self.api = self.getAPI()
        
    def get(self):
        searchWords = [u'はっしゅたぐでもキーワードでも何でも入れて']
        tweets = self.search(searchWords)
        tweets = self.filter(tweets)
        for tweet in tweets:
            self.put(tweet)
    
    def update(self, somekey =''):
        """
        statusから抜き出してついーと
        """
        """適当"""
        stasu = Status.all().order('status_id').fetch(1)
        self.post(status)
    
    def search(self,keywords):
        results =[]
        for key in keywords:
            results += self.api.search(key.encode('utf-8'))
        return sorted(set(results),key=results.index)
    
    def post(self, status = ''):
        file = open('messages.yaml').read()
        data = yaml.load(file)
        msgs = data['messages']
        key = random.randint(0, len(msgs)-1)
        self.api.update_status(msgs[key])
        
    def reply(self):
        file = open('replys.yaml').read()
        data = yaml.load(file)
        msgs = data['replys']
        status_id = 0
        mentions = self.api.mentions()
        if len(mentions) > 0:
            mention_cache = RepliedStatus.all().order('-status_id').fetch(1)
            if len(mention_cache) > 0:
                status_id = mention_cache[0].status_id
            else:
                status_id = mentions[len(mentions)-1].id
            print status_id
            for tweet in tweepy.Cursor(self.api.mentions, since_id = status_id).items(3):
                msg = '@' + tweet.author.screen_name + msgs[random.randint(0, len(msgs)-1)]
                self.api.update_status(msg)
                reply = RepliedStatus()
                reply.status_id = tweet.id
                reply.put()
    
    def put(self, status):
        s = Status()
        s.status_id = status.id;
        s.user = status.from_user
        s.text = status.text
        s.icon_url = status.profile_image_url
        s.put()
        
    def filter(self, posts):
        results = []
        for p in posts:
            if(not self._isCached(p)):
                results.append(p)
        return results
        
    def _isCached(self,status):
        q = Status.all()
        q.filter('status_id =',status.id)
        print q.count() > 0
        return q.count() > 0
    
    def getAPI(self):
        auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.SECRET_KEY)
        auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_VERIFIER)
        return tweepy.API(auth)
        