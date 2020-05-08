import daemon
import json
import lockfile
import logging
import os
import pika
import pytz
import signal
import sys
import time

from lockfile import LockFile

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "challengetask.settings")

import django
django.setup()

from django.db import transaction
from dataholder.models import (
    Match,
    Score,
    Team, 
)

from pprint import pprint

########################################################
############### CLASS DEFEINITIONS #####################
########################################################
class PikaConsumer():

    #Class variables
    lockfile = "/var/run/pikad"
    logfile = "/tmp/pikad.log"
    pikadlog = "pikadlog"

    ############################################
    def __init__(self):

        #Interrupt termination signals to permit lock cleanup
        signal.signal(signal.SIGINT, self.sig_handler)
        signal.signal(signal.SIGTERM, self.sig_handler)

        self.host = 'rabbitmq'

    ############################################
    def sig_handler(self,signum, frame):

        #If we abort execution we need to clean up lock file prior to exiting

        if PikaConsumer.lock.is_locked():        
            PikaConsumer.lock.release()
            PikaConsumer.logger.info("Cleaning up lock and exiting ...")

        #Now after cleanup we can exit
        sys.exit()

    #################################################
    ############# Utility functions #################
    #################################################

    ##################################################
    @classmethod
    def set_loglevel(cls):

        ''' Set loglevel to control output verboseness '''

        loglevel = os.getenv('LOGLEVEL')
    
        #Set log verbose level default level is INFO
        if not loglevel:
            loglevel = 'INFO'

        #Based on loglevel variable set logger verbose level
        if loglevel == 'ERROR':
            return logging.ERROR

        if loglevel == 'WARNING':
            return logging.WARNING

        if loglevel == 'DEBUG':
            return logging.DEBUG

        # Retrun default loglevel INFO
        return logging.INFO


    ##################################################
    @classmethod
    def init_logging(cls):

        ''' Initialize logging '''

        #Set log verbose level. Default is INFO
        loglevel = cls.set_loglevel()

        #logging initialization process
        logger = logging.getLogger(PikaConsumer.pikadlog)
        logger.setLevel(loglevel)

        #Log messages format
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s',datefmt='%Y-%m-%d %H-%M-%S')
        
        lh = logging.FileHandler(PikaConsumer.logfile)
        lh.setFormatter(formatter)

        logger.addHandler(lh)
        logger.info('Logging initialized')

        #set logger handler as class variable to use in message logging
        cls.logger = logger

    #################################################
    ####### pika consumer related functions #########
    #################################################
    
    ##################################################
    @transaction.atomic
    def uploadData2DB(self, msg):
        
        ''' Upload received message into database  '''

        ###There are three tables we need to upload###
    
        #According to demo messages tournument part can be of two types
        #dictionary with id and name or simple name string. Check for type
        #and prcess results acrdingly
        if type(msg['data']['tournament']) == type(dict()):
            tid = msg['data']['tournament'].get('id',None)
            tname = msg['data']['tournament'].get('name', msg['data']['tournament']['name'])
        else:
            tid = None
            tname = msg['data']['tournament']

        #Updating Score table if needed
        score_obj = Score.objects.get_or_create(
            score1=msg['data']['scores'][0]['score'], 
            score2=msg['data']['scores'][1]['score'], 
            winner1=msg['data']['scores'][0]['winner'], 
            winner2=msg['data']['scores'][1]['winner'],
        )[0]

        #Updating Team table if needed
        team1_obj = Team.objects.get_or_create(team_id=msg['data']['teams'][0]['id'],team_name=msg['data']['teams'][0]['name'])[0]
        team2_obj = Team.objects.get_or_create(team_id=msg['data']['teams'][1]['id'],team_name=msg['data']['teams'][1]['name'])[0]

        #Updating Match table if needed
        match_obj = Match.objects.get_or_create(
            id=msg['data']['id'],
            title=msg['data']['title'],
            date_start=msg['data']['date_start_text'],
            url=msg['data']['url'],
            state=msg['data']['state'],
            bestof=msg['data']['bestof'],
            tournament_id=tid,
            tournament_name=tname,
            score=score_obj,
            team1=team1_obj,
            team2=team2_obj
        )        

        PikaConsumer.logger.info("uploadData2DB : Uploading DB with %s" % json.dumps(msg))

        #Test printout
        pprint(msg['data'])

    ##################################################
    def callback(self, ch, method, properties, body):

        ''' Callback function where message is pulled '''

        PikaConsumer.logger.info("Callback : retriving message")

        body = json.loads(body)
        PikaConsumer.logger.info("Run : message : %s" % json.dumps(body))

        #send message for db upload
        self.uploadData2DB(body)

    ##################################################
    def run(self):

        ''' Run function where listen process is initalized '''

        PikaConsumer.logger.info("Run : Initializing consumer")

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        channel = connection.channel()
        channel.queue_declare(queue='emsg')
        channel.basic_consume(queue='emsg', on_message_callback=self.callback, auto_ack=True)
        channel.start_consuming()

    ##################################################
    def start(self):

        ''' Start point for pika consumer run '''

        #Initialize logging
        PikaConsumer.init_logging() 
        PikaConsumer.logger.info("start : Initializing logging")

        #Intitialize locking
        PikaConsumer.lock = LockFile(PikaConsumer.lockfile)
        if PikaConsumer.lock.is_locked():
            PikaConsumer.logger.error("start : Locked by another instance")
            print("Instance is locked by %s" %  PikaConsumer.lockfile)
            return 

        PikaConsumer.lock.acquire()
        PikaConsumer.logger.info("start : Instance locked")

        #Daemonize process
        context = daemon.DaemonContext()
        consumer = PikaConsumer()

        with context:
            consumer.run()

        #We are not suppose to get here since pika enters listen loop
        PikaConsumer.lock.release()
        PikaConsumer.logger.info("start : Instance unlocked")


#############################################################
##################### MAIN PART #############################
#############################################################
if __name__ == "__main__":

    consumer = PikaConsumer()
    consumer.start() 
