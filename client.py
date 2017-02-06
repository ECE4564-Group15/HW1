#!/usr/bin/env python3.6

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
os.system('python Tweet.py @username#hostname:port_question')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
user_input = sys.argv[1]
s.send(user_input)
data = s.recv(size)
s.close()
os.system('python Tweet.py $data' )
