#!/usr/bin/env python3.6

###############################################################################
## File name:   Wolfram.py
## Author:      BL(02-05-2017)
## Modified by: 
## Description: This python script is used to collect question from client and 
##              push the result to the client.
##
## TODO: install wolfram alpha library
##       communicate from between client and server.

import wolframalpha.Client

client = wolframalpha.Client("HXV625-27RGEV674Q"); # add app id;

res = client.query('temperature in Washington,DC on October 3, 2012'); # question
answer = next(res.results).text

print (answer) # print out answer

