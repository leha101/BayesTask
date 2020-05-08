#!/usr/bin/env python

'''
    This is a basic send messages to rabbitmq servrive with pika script
    - for connection used basic default parameters
    - for message body used one o several testing message files msg1.json 
      where file name is provided on command line

    NOTE : Since this is a pure testing script no error detection is implemented

    Usage: ./send.py -f msgN.json (where N denotes number of file)
'''

import argparse
import json
import pika
import re
import sys

from pprint import pprint

###########################################################
############### GLOBAL VARIABLES PART #####################
###########################################################
QUEUENAME = 'emsg'
RABBITMQHOST = 'localhost'

###########################################################
################### FUCTIONS PART #########################
###########################################################

##########################################
#Custom formater for argparse to display #
#better help message                     #
##########################################
class CustomFormatter(
        argparse.RawDescriptionHelpFormatter,
        argparse.ArgumentDefaultsHelpFormatter):
        pass

##########################################
def parseInput():

    ''' Parsing input parameters  '''

    args = sys.argv[1:]

    parser = argparse.ArgumentParser(
                    description = sys.modules[__name__].__doc__,
                    formatter_class = CustomFormatter,
    )

    parser.add_argument("--file", "-f", type=str, required=True, help="Name of message file to process")
    args = parser.parse_args()

    return args.file


##########################################
def sendMsg(msg_file):

    '''Send pika message function '''

    #Open message file and read message to send. Since we know that message files have json format issues
    #need to clear these issues first. Fortunately all known issues are of bad sequal ',}'
    # 1. Remove backspaces from string
    # 2. Remove all white spaces
    # 3. Return space back in date field (format 2020-01-07 14:30:00)
    # 4. Replace bad combination ',}' with '}'
    with open(msg_file,'r') as fh:
        msg = fh.read().replace('\n','')

    msg = msg.replace(' ','')
    msg = re.sub('(\d+-\d+-\d{2})(\d+:\d+:\d+)',r'\1 \2',msg)
    msg = msg.replace(',}','}')

    #Convert message string into json format
    data = json.loads(msg)

    #Covert json object into dictionary
    data = json.dumps(data)

    #Send message to rabbitmq server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQHOST))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUENAME)

    channel.basic_publish(exchange='', routing_key=QUEUENAME, body=data)
    connection.close()

###########################################################
##################### MAIN PART ###########################
###########################################################

mfile = parseInput()
sendMsg(mfile)


