from django.core.management.base import BaseCommand
import time
import pika
from reportes.logic.logic_cronogramas import cronogramaPagos

class Command(BaseCommand):
    help = 'Runs the RabbitMQ producer'

    def handle(self, *args, **kwargs):
        rabbit_host = '10.128.0.10'
        rabbit_user = 'losarquis_user'
        rabbit_password = '1234'
        exchange = 'cronogramas_pagos'
        topic = 'Cronograma'

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbit_host, credentials=pika.PlainCredentials(rabbit_user, rabbit_password))
        )
        
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, exchange_type='topic')
        self.stdout.write(self.style.SUCCESS('> Sending measurements. To exit press CTRL+C'))

        while True:
            pagos = cronogramaPagos()
            
            for p in pagos:
                message = "{'mensaje': %r, 'correo': %r, 'fecha': %r,'responsable': '%r'}" % (p.nombre, p.responsableF.correo, p.fecha, p.responsableF.nombre)
                channel.basic_publish(exchange=exchange, routing_key=topic, body=message)
                self.stdout.write(f"[x] Mensaje enviado: {message}")

            time.sleep(15)
