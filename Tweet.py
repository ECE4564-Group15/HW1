#!/usr/bin/env python3

###############################################################################
## File name:   Tweet.py
## Author:      BL(02-05-2017)
## Modified by: 
## Description: This python script is used to push the question to server side 
## and request for answers and post the answers as a tweet 
##
## TODO: install tweet
##       communicate from between client and server.

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import hashlib
import re

CONSUMER_KEY = "AVoVfyfpBW2ULsVSebtLQEpO9";
CONSUMER_SECRET = "iUXnIABiyiC11ok9obagtTzg43SHDtBg4pHidj0qsTn2CT3wdb";

ACCESS_KEY = "825049989705560065-I22v2Fgp2HDTTdPt9XZssT2blrL3N3M";
ACCESS_SECRET = "eI9uGprtn1Eum42NfqEatPz6ljUQKP6aWLEh7K99ZKTEk";

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = API(auth)

class SFREDStreamListener(StreamListener):

    def invalid_format(self):
            api.update_status("Invalid format. Use '@sfred_bot #server.address:port_\"Question here\"'",in_reply_to_status_id = tweet.in_reply_to_status_id)
        

    def parse_tweet(self,tweet):
        #need the text
        text = tweet.text
        print(text)
        data = text.split('#',1)
        if len(data) >= 2:
            #redo data
            data = data[1].split('_',1)
            if len(data) is 2:
                address = data[0]
                quest = re.sub('"','',data[1])
                address = address.split(':',1)
                md5 = hashlib.md5()
                md5.update(quest.encode())
                md5 = md5.hexdigest()
                return (address,quest,md5,)
        self.invalid_format()    
        return None

    def on_status(self, status):
        payload = self.parse_tweet(status)
        if payload is None:
            #do nothing
            print ("Errror with tweet")
        else:
            #send message and wait for response
            print ("Success")
            print (payload)
        return True

if __name__ == '__main__':
    sl = SFREDStreamListener()

    stream = Stream(auth = auth, listener=sl)

    stream.filter(track=['@sfred_bot'])

