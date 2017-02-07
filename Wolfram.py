#!/usr/bin/env python3

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
import socket
import sys
import pickle
import hashlib

def serverLoop(s,size,wolf):
    while 1:
        #get the data
        client, address = s.accept()
        data = client.recv(size)
        if data:
            data = pickle.loads(data)
            print(data)
            #data is in format (md5,q)
            question = data[1]
            md5_q = hashlib.md5()
            md5_q.update(question.encode())
            md5_q = md5_q.hexdigest()
            if md5_q == data[0]:
                #good, ask q
                print("Good md5")
                res = wolf.query(question)
                res = next(res.results).text
                print(res)
            else:
                print("Bad md5")
                res = "Error answering the question. Sorry"    

            md5_a = hashlib.md5()
            md5_a.update(res.encode())
            md5_a = md5_a.hexdigest()
            answer = (md5_a,res)
            print(md5_a + ' : ' + res)
            print(answer)
            answer = pickle.dumps(answer)
            client.send(answer)            
        client.close()

def main():
    client = wolframalpha.Client("AHJ6PV-E7ULX75PHV") # add app id;
    host = 'localhost'
    port = 9005
    size = 2048
    backlog = 1
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        s.bind((host,port))
        s.listen(backlog) 
    except socket.error as message:
        if s:
            s.close()
            print ("Could not open socket: " + str(message))
            sys.exit(1)

    serverLoop(s,size,client)
main()
