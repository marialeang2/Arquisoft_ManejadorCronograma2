#!/usr/bin/env python
import time
import pika
from random import uniform

import json
from sys import path
from os import environ
import django

rabbit_host = '10.128.0.10'
rabbit_user = 'losarquis_user'
rabbit_password = '1234'
exchange = 'cronogramas_pagos'
topic = 'Cronograma'


path.append('reportes/settings.py')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'reportes.settings')
django.setup()

from reportes.logic.logic_cronogramas import cronogramaPagos

while True:
    pagos = cronogramaPagos()
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbit_host, credentials=pika.PlainCredentials(rabbit_user, rabbit_password))
    )
    
    channel = connection.channel()

    # Declarar la cola (asegúrate de que la cola existe)
    channel.queue_declare(queue=queue_name)

    # Publicar el mensaje en la cola
    for p in pagos:
        message = {
        'fecha': p.fecha,
        'concepto': p.nombre,
        }
        channel.basic_publish(exchange=exchange,
                          routing_key=topic,
                            body=message)  # Convertir el mensaje a JSON
    
    print(f"[x] Mensaje enviado: {message}")

    time.sleep(5)

connection.close()

