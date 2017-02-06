#!/usr/bin/env python

###############################################################################
## File name:   Wolfram.py
## Author:      BL(02-05-2017)
## Modified by: 
## Description: This python script is used to collect question from client and 
##              push the result to the client.
##
## TODO: install wolfram alpha library
##       communicate from between client and server.

import wolframalpha
import os
import sys
import socket

client = wolframalpha.Client("HXV625-27RGEV674Q"); # add app id;

res = client.query(argv[1]); # question
answer = next(res.results).text

host = 'localhost'
# host = '192.168.1.108'
port = 50000
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
s.send(answer)
s.close()
print (answer) # print out answer

