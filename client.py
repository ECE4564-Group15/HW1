#!/usr/bin/env python

"""
A simple echo client
"""

import socket
import sys
import os

host = 'localhost'
# host = '192.168.1.108'
port = 50000
size = 1024
cmd = "python Tweet.py @lbc0430"+'#' +host +':' + str(port) +'_' + sys.argv[1]
print(cmd)

os.system(cmd)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
user_input = sys.argv[1]
s.send(user_input)
data = s.recv(size)
s.close()
post = "python Tweet.py " + data
os.system(post)

