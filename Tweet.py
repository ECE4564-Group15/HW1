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
from tweepy import TweepError
import hashlib
import re
import socket
import pickle
import random
import itertools

reply_user = None
class APIData:
    def __init__(self,CK,CS,AK,AS,user):
        #create the api
        self.auth = OAuthHandler(CK,CS)
        self.auth.set_access_token(AK,AS)
        self.api = API(self.auth)

        self.reply_user = user

#custom listener class
class SFREDStreamListener(StreamListener):

    def set_api_data(self,api_data):
        self.api_data=api_data
    
    #various error tweeting methods
    def invalid_format(self,tweet):
        try:
            self.api_data.api.update_status("@%s Invalid format. Use '@me #server.address:port_\"Question here\"' #"%(self.api_data.reply_user)+str(random.randint(0,10000)))
        except TweepError as e:
            print("Error sending tweet: "+str(e.message))
    
    def invalid_address(self,tweet,reason):
        try:
            self.api_data.api.update_status("@%sInvalid address: "%(self.api_data.reply_user)+reason+' #'+str(random.randint(0,10000)))
        except TweepError as e:
            print("Error sending tweet: "+str(e.message))

    def tweet_error(self,tweet,reason):
        try:
            self.api_data.api.update_status("@%s Error: "%(self.api_data.reply_user)+reason+' #'+str(random.randint(0,10000)))
        except TweepError as e:
            print("Error sending tweet: "+str(e.message))
    
    #This method sends evey element in a given response array
    #expects that each element is a string or can be implicitly converted to a string
    def send_reply(self,response,tweet):
        #valid response?
        if response is not None:
            #this contains the previously send response
            #this allows us to chain together mutliple tweets
            toReply = None
            #loop
            for r in response:
                print("Tweeted: "+r)
                #prepend the @
                r = "@%s %s #" %(self.api_data.reply_user,r) + str(random.randint(0,10000))
                try:
                    #first tweet
                    if toReply is None:
                        toReply = self.api_data.api.update_status(r)
                    #not first
                    else:
                        toReply = self.api_data.api.update_status(r,in_reply_to_status_id = toReply.id)
                except TweepError as e:
                    print("Error sending tweet: "+str(e.message))

    #This method tries to send a question to the server as epcified by the user
    #it then returns the response from the server
    #the response is always valid, but can contain an error message from the server
    def send_question(self,payload,tweet):
        #socket constants
        size = 2048
        s = None
        #init
        response = "Error constructing response"
        try:
            #connect
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((payload[0][0],int(payload[0][1])))
            #create a new tuple and pickle it
            toSend = (payload[2],payload[1],)
            print("Asking: "+str(toSend))
            toSend = pickle.dumps(toSend)
            #send
            s.send(toSend)
            #wait for receive (or not...; look at EOFError)
            response = s.recv(size)
            #unpickle
            response = pickle.loads(response)
            print("Got: "+str(response))
            #text
            answer = response[1]
            #compare hash
            md5 = hashlib.md5()
            md5.update(answer.encode())
            md5_a = md5.hexdigest()
            #if good
            if md5_a == response[0]:
                #split the answer by lines (will tweet line by line)
                response = [s.strip() for s in answer.splitlines()]
                n = 123 #124 because of @user and random int
                #refactor the response list to be <=124 characters per entry
                response = [r[i:i+n] for r in response for i in range(0,len(r),n)]
            #if bad hash for some reason
            else:
                self.tweet_error(tweet,'Error receiving answer from server. Incorrect hash')
        #if given address/port fails to connect
        except socket.error as message:
            self.invalid_address(tweet,message)
        #if the server disconnects before giving us a response
        except EOFError:
            self.tweet_error(tweet,'Error receiving answer from server.')
        #always try to close the connection
        finally:
            if s:
                s.close()
            s.close()
        #always return
        return response 

    #this method deconstructs the received tweet and gets all the juicy bits    
    #this includes: 
    # 1)Server address and port
    # 2)Question to ask
    def parse_tweet(self,tweet):
        #need the text
        text = tweet.text
        #split into @... and data
        data = text.split('#',1)
        #should only be two fields
        if len(data) >= 2:
            #redo data (address and question are seperated by '_'
            data = data[1].split('_',1)
            #again should only be 2
            if len(data) is 2:
                #extract info
                address = data[0]
                #remove '"'
                quest = re.sub('"','',data[1])
                address = address.split(':',1)
                #get an md5 from the question
                md5 = hashlib.md5()
                md5.update(quest.encode())
                md5 = md5.hexdigest()
                #this is the payload
                return (address,quest,md5,)
        #this only returns when there is an error so that the caller can handle that
        return None

    #this is the main tweet handler
    #every time the filter detects that we got a message    
    #this function is called with the detected tweet
    def on_status(self, status):
        #get all of the useful info
        payload = self.parse_tweet(status)
        #error handling
        if payload is None:
            print ("Errror with tweet")
            #tell the user that they are bad
            self.invalid_format(status)
        else:
            #send message and wait for response
            print ("Good tweet")
            print (payload)
            #send the question and get a response from the server specified in the tweet
            response = self.send_question(payload,status)
            self.send_reply(response,status)
        return True

def main():
    #create the 'secret' data
    api_data = APIData("AVoVfyfpBW2ULsVSebtLQEpO9","iUXnIABiyiC11ok9obagtTzg43SHDtBg4pHidj0qsTn2CT3wdb","825049989705560065-I22v2Fgp2HDTTdPt9XZssT2blrL3N3M","eI9uGprtn1Eum42NfqEatPz6ljUQKP6aWLEh7K99ZKTEk","VTNetApps")
    #listener instance
    sl = SFREDStreamListener()
    sl.set_api_data(api_data)
    #we use this all the time
    random.seed()
    #create the stream object
    stream = Stream(auth = api_data.auth, listener=sl)
    #make sure it loooks at the right tweets
    stream.filter(track=['@sfred_bot'])
#start the whole thing
main()
