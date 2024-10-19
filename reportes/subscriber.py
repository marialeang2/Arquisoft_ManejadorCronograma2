import json
import pika
from sys import path
from os import environ
import django

rabbit_host = 'host'
rabbit_user = 'losarquis_user'
rabbit_password = '1234'
exchange = 'cronogramas_pagos'
topics = ['Cronograma.#']


#path.append('monitoring/settings.py')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoring.settings')
django.setup()



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
    #payload = json.loads(body.decode('utf8').replace("'", '"'))
    #topic = method.routing_key.split('.')
    #variable = get_variable(topic[2])
    #create_measurement_object(
    #    variable, payload['value'], payload['unit'], topic[0] + topic[1])
    #if variable.name == 'Temperature':
    #    check_alarm(payload['value'])
    #print("Measurement :%r" % (str(payload)))
    print(f"[x] Recibido {body}")

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()