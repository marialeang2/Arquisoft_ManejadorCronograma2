import json
import pika
from sys import path
from os import environ
import django

rabbit_host = '10.128.0.10'
rabbit_user = 'losarquis_user'
rabbit_password = '1234'
exchange = 'cronogramas_pagos'
topics = ['Cronograma.#']


path.append('reportes/settings.py')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'reportes.settings')
django.setup()

from generarreportes.services import send_email

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbit_host, credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))
channel = connection.channel()

channel.exchange_declare(exchange=exchange, exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

for topic in topics:
    channel.queue_bind(
        exchange=exchange, queue=queue_name, routing_key=topic)

print('> Esperando pagos. To exit press CTRL+C')


def callback(ch, method, properties, body):
    message = json.loads(body.decode('utf8').replace("'", '"'))
    receptor = message['correo']
    responsable = message['responsable']
    fecha = message['fecha']
    concepto = message['mensaje']
    send_email(receptor, responsable, fecha, concepto)
    print(f"[x] Recibido {message}")

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()