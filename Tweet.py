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
import socket
import pickle
import random

CONSUMER_KEY = "AVoVfyfpBW2ULsVSebtLQEpO9";
CONSUMER_SECRET = "iUXnIABiyiC11ok9obagtTzg43SHDtBg4pHidj0qsTn2CT3wdb";

ACCESS_KEY = "825049989705560065-I22v2Fgp2HDTTdPt9XZssT2blrL3N3M";
ACCESS_SECRET = "eI9uGprtn1Eum42NfqEatPz6ljUQKP6aWLEh7K99ZKTEk";

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = API(auth)

reply_user = "VTNetApps"

class SFREDStreamListener(StreamListener):

    def invalid_format(self,tweet):
            api.update_status("@%s Invalid format. Use '@me #server.address:port_\"Question here\"'"%(reply_user)+str(random.randint(0,1000)),in_reply_to_status_id = tweet.in_reply_to_status_id)
    
    def invalid_address(self,tweet,reason):
            api.update_status("@%sInvalid address: "%(reply_user)+reason+str(random.randint(0,1000)),in_reply_to_status_id = tweet.in_reply_to_status_id)

    def tweet_error(self,tweet,reason):
            api.update_status("@%s Error: "%(reply_user)+reason+str(random.randint(0,1000)),in_reply_to_status_id = tweet.in_reply_to_status_id)
    
    def send_reply(self,response,tweet):
        if response is not None:
            toReply = None
            for r in response:
                print("Tweeted: "+r)
                r = "@%s %s" %(reply_user,r)
                if toReply is None:
                    toReply = api.update_status(r)
                else:
                    toReply = api.update_status(r,in_reply_to_status_id = toReply.id)

    def send_question(self,payload,tweet):
        size = 2048
        s = None
        response = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((payload[0][0],int(payload[0][1])))

            #create a new tuple and pickle it
            toSend = (payload[2],payload[1],)
            print("Asking: "+str(toSend))
            toSend = pickle.dumps(toSend)
            s.send(toSend)
            response = s.recv(size)
            #unpickle
            response = pickle.loads(response)
            print("Got: "+str(response))
            answer = response[1]
            #compare hash
            md5 = hashlib.md5()
            md5.update(answer.encode())
            md5_a = md5.hexdigest()
            if md5_a == response[0]:
                #split the answer
                response = [s.strip() for s in answer.splitlines()]
            else:
                self.tweet_error(tweet,'Error receiving answer from server. Incorrect hash')
        except socket.error as message:
            self.invalid_address(tweet,message)
        except EOFError:
            self.tweet_error(tweet,'Error receiving answer from server.')
        finally:
            if s:
                s.close()
            s.close()
        return response 

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
        self.invalid_format(tweet)    
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
            response = self.send_question(payload,status)
            self.send_reply(response,status)
        return True

def main():
    sl = SFREDStreamListener()
    random.seed()
    stream = Stream(auth = auth, listener=sl)

    stream.filter(track=['@sfred_bot'])
main()
