import json
import pika

from loguru import logger
from .connection import RabbitMQConnection

class Rabbyt(RabbitMQConnection):
    def send(self, data: dict):
        channel = self.connect()

        channel.exchange_declare(
            exchange=self.exchange, 
            exchange_type='direct', 
            durable=True
        )
        channel.queue_declare(queue=self.queue, durable=True)
        channel.queue_bind(
            exchange=self.exchange,
            queue=self.queue,
            routing_key=self.routing_key
        )

        body = json.dumps(data)
        channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.routing_key,
            body=body,
            properties=pika.BasicProperties(delivery_mode=2)
        )

        logger.info(f"Message send to RabbitMQ: {body}")