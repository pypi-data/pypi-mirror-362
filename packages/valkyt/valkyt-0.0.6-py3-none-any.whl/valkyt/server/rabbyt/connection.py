import pika
import json
from loguru import logger

class RabbitMQConnection:
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        port: str,
        virtual_host: str,
        queue: str,
        routing_key: str,
        exchange: str
    ):
        self.queue: str = queue
        self.routing_key: str = routing_key
        self.exchange: str = exchange
        
        credentials = pika.PlainCredentials(
            username,
            password
        )
        parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=virtual_host,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        return self.channel

    def close(self):
        if self.connection:
            self.connection.close()