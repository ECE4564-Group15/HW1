# HW1

## Question to Dr. Plymale

1. @username myself? or given by TA

##TODO

1. The server needs a loop to receive data from client and receive the data from wolfram, when receive data from client, send the contents to wolfram; when receives from wolfram, send data to client and tweet;

2. multi-answer does not implemnt

3. convert to python3.

4. report

5. setup a time this week and next week for all four of us to meet

   This week is for testing on rsp pi in Durham, next week is for validation

before you start to work on this repo,

    git clone https://github.com/ECE4564-Group15/HW1
    cd ./HW1
    chmod +x setup.sh
    sudo ./setup.sh

to install libraries that is needed for this assignment, I recommend you 

to do this in a vm.

## Usage
    
in the first terminal, do
        
    python3 simple_echo_server.py &

in the second terminal

    python client.py <question>
    
    example: python client.py "what is the weather in Blacksburg, Virginia"

or you can use any single script

    python Tweet.py "Hello, world" # this will post something on my tweet
                                   # @lbc0430
    python Wolfram.py "4+5"        # This will get the answer from wolfram
    

## Wolfram Alpha API ID:
APP NAME: Tweet wolframalpha Q&A

APPID: HXV625-27RGEV674Q

USAGE TYPE: Personal/Non-commercial Only


## Tweet API key
Consumer Key (API Key): 

    bPqfYmH4yYQw5ZkUhuSYZIIpd 
Consumer Secret (API Secret): 

    IBsm0SrLSR3uKynCYppo0YDa5tThawD5h4lQ2BNFvlNYS6UhZp

Access Token: 

    1456947205-4hpgqmfBh92YtMuTL60oIcFVmMVRaWp4NJYQcyA

Access Token Secret: 

    IgvVo2Jg6bSN5LjholkZUHkrBnEcfHSKF4TOHNc9X3vxw
