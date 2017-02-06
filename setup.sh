#!/bin/bash
###############################################################################
## Filename: setup.sh
## Author: BL (02-05-2017)
## Description: This script is installing apts taht is needed in hw1
## prerequisite: debian based operating system
##               running under root

set -euo pipefail

apt-get install python3-pip         # install pip
python3 -m pip install tweepy       # tweet lib
python3 -m pip insatll wolframalpha # wolfram alpha lib
