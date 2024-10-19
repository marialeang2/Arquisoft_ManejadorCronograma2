#!/usr/bin/env python
import time
import pika
from random import uniform
from reportes.logic.logic_cronogramas import cronogramaPagos

rabbit_host = '10.128.0.10'
rabbit_user = 'losarquis_user'
rabbit_password = '1234'
exchange = 'cronogramas_pagos'
topic = 'Cronograma'



def publish_message(message):
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbit_host, credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))
    
    channel = connection.channel()

    channel.queue_declare(queue='pagos_queue')
    channel.basic_publish(exchange='',
                          routing_key='pagos_queue',
                          body=message)
    
    print(f"[x] Mensaje enviado: {message}")
    connection.close()