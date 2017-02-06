#!/usr/bin/env python3.6

###############################################################################
## File name:   Tweet.py
## Author:      BL(02-05-2017)
## Modified by: 
## Description: This python script is used to push the question to server side 
## and request for answers and post the answers as a tweet 
##
## TODO: install tweet
##       communicate from between client and server.

import tweepy
import sys

CONSUMER_KEY = "bPqfYmH4yYQw5ZkUhuSYZIIpd";
CONSUMER_SECRET = "IBsm0SrLSR3uKynCYppo0YDa5tThawD5h4lQ2BNFvlNYS6UhZp";

ACCESS_KEY = "1456947205-4hpgqmfBh92YtMuTL60oIcFVmMVRaWp4NJYQcyA";
ACCESS_SECRET = "IgvVo2Jg6bSN5LjholkZUHkrBnEcfHSKF4TOHNc9X3vxw";

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)
api.update_status(sys.argv[1])

