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

#main loop of the server
#accepts connections and handles them
def serverLoop(s,size,wolf):
    #LOOP
    while 1:
        #connection
        client = None
        res = ""
        try:
            #conenct and get the data
            client, address = s.accept()
            data = client.recv(size)
            #if good data
            if data:
                #try to look at data
                data = pickle.loads(data)
                print(data)
                #data is in format (md5,q)
                #check to make sure the sent hash is good
                question = data[1]
                md5_q = hashlib.md5()
                md5_q.update(question.encode())
                md5_q = md5_q.hexdigest()
                #check
                if md5_q == data[0]:
                    #good, ask q
                    print("Good md5")
                    try:
                        #ask question
                        res = wolf.query(question)
                        res = next(res.results).text
                    #if there is some problem with wolfram then we need to let the client know
                    except Exception:
                        res = "Error answering the question. Please try again in a few minutes."
                    finally:
                        print(res)
                else:
                    print("Bad md5")
                    res = "Error answering the question. Please try again in a few minutes."
                #compute the hash to send back
                md5_a = hashlib.md5()
                md5_a.update(res.encode())
                md5_a = md5_a.hexdigest()
                #create the tuple to send
                answer = (md5_a,res)
                print(answer)
                #pickle
                answer = pickle.dumps(answer)
                #send
                client.send(answer)
        except socket.error:
            print("Socket error :(.")
        #always disconnect and close
        finally:
            if client:
                client.close()            
#main function
#settup and calls the main loop
def main():
    #connect to service
    client = wolframalpha.Client("AHJ6PV-E7ULX75PHV") # add app id;
    #socket constants
    host = 'localhost'
    port = 9005
    size = 2048
    backlog = 1
    s = None
    #attempt to connect
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
    #if all is good then start the loop
    else:
        serverLoop(s,size,client)
main()
