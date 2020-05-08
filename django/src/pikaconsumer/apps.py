from django.apps import AppConfig
from pikaconsumer.pconsumer import PikaConsumer

class PikaconsumerConfig(AppConfig):
    name = 'pikaconsumer'

    def ready(self):
        #Start pika consumer but only once
        consumer = PikaConsumer()
        consumer.start()

