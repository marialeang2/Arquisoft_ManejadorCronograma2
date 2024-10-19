#!/usr/bin/env python
import time
import pika
from random import uniform
from reportes.logic.logic_cronogramas import cronogramaPagos
import json
from sys import path
from os import environ
import django

rabbit_host = '10.128.0.10'
rabbit_user = 'losarquis_user'
rabbit_password = '1234'
exchange = 'cronogramas_pagos'
topic = 'Cronograma'
queue_name = 'pagos_queue'
queue_name = 'pagos_queue'

path.append('reportes/settings.py')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'reportes.settings')
django.setup()

def publish_message(correo, responsable, fecha, concepto):
    # Crear el mensaje en formato JSON
    message = {
        'correo': correo,
        'responsable': responsable,
        'fecha': fecha,
        'concepto': concepto,
    }
    
    # Conectar a RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbit_host, credentials=pika.PlainCredentials(rabbit_user, rabbit_password))
    )
    
    channel = connection.channel()

    # Declarar la cola (asegúrate de que la cola existe)
    channel.queue_declare(queue=queue_name)

    # Publicar el mensaje en la cola
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=json.dumps(message))  # Convertir el mensaje a JSON
    
    print(f"[x] Mensaje enviado: {message}")
    connection.close()

