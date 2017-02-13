import socket
from tweepy import *
import hashlib
import pickle

"""Configure Twitter API Oauth keys"""
consumer_key = 'ylUdMSUd7BckqBhESDVO4iWuW'
consumer_secret = '1TRkAWXCC4z654HNzGXaquoUQCvcM8PwhCxOctm3kKwjb7ZiG7'
access_token_key = '2825198773-DVqdSRL1YSPyDJ4jcgcnK6M3aSst232tQXdVKEw'
access_token_secret = '1xQmdiB91kh1Fix75pJb99mHxQuRLLzfHycf2NUYJO8yo'

"""Configure socket connection to server"""
packsize = 1024
#streamSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def serverQuery(message):
    """Helper method for getting the answer from the server
        return the answer string"""
    t = (hashlib.md5(message.encode()).hexdigest(), message)
    print("MD5 sent: ", t[0])
    data = pickle.dumps(t)
    streamSocket.send(data)
    t = pickle.loads(streamSocket.recv(packsize))
    if t[0] != hashlib.md5(t[1].encode()).hexdigest():
        print("Answer tuple MD5 mismatch")
        print("Received: ", t)
        print("Calculated: ", hashlib.md5(t[1]).hexdigest())
    return t[1]


def socketconfig(address):
    """Config socket"""
    global streamSocket
    streamSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:

        streamSocket.connect((address[0], int(address[1])))
    except socket.herror as e:
        print("herror!")
    except socket.gaierror as e:
        print("gaierror!")
    except socket.timeout as e:
        print("timed out!")


class TwitterListener(StreamListener):
    """Subclass of StreamListener"""
    def on_status(self, status):
        """Define what to do when receives a new twitter"""
        try:
            # indices = status.entities['hashtags'][0]['indices']
            # message = status.text[indices[0]+1:].split("_")
            message = status.text.split("#")
            message = message[1].split("_")
            print("Question received: ", status.text)
            socketconfig(message[0].split(":"))
            reply = '@Liyanlii Team_Rookie ' + status.created_at.__str__()[-8:] \
                + '#"' + serverQuery(message[1]) + '"'
            # reply = "'" + reply + "'"
            print("Answer Tweet: ", reply)
            api.update_status(status = reply)
        except TweepError as e:
            print("Something went wrong")
            try:
                print("Tweet received: ", status.text)
                # print("indices: ", indices)
                # print("message: ", message)

            except:
                print("Unable to connect to server")

        finally:
            streamSocket.close()

    def on_connect(self):
        print("Script is now connected to the twitter stream")

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = API(auth)

twitterStream = Stream(auth, TwitterListener())
twitterStream.filter(track=['xianze1996'])

