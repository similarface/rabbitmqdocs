#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pika


class BasicURLPikaClient:
    def __init__(self, url, ssl=False):
        parameters = pika.URLParameters(url)
        if ssl:
            # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')
            parameters.ssl_options = pika.SSLOptions(context=ssl_context)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()


class BasicPikaClient(BasicURLPikaClient):

    def __init__(self,
                 rabbitmq_broker_host=None,
                 rabbitmq_user=None,
                 rabbitmq_password=None,
                 rabbitmq_broker_port=None,
                 url=None,
                 ssl=False,
                 proto='amqp'):
        if not url:
            # amqp://username:password@host:port/<virtual_host>[?query-string]
            url = f"{proto}://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_broker_host}:{rabbitmq_broker_port}"
        super(BasicPikaClient, self).__init__(url=url, ssl=ssl)


class HelloWorldSender(BasicPikaClient):
    def declare_queue(self, queue_name):
        print(f"定义队列： ({queue_name})...")
        self.channel.queue_declare(queue=queue_name)

    def send_message(self, exchange, routing_key, body):
        # 获取信道
        channel = self.connection.channel()
        # 信道 ----> 交换机---路由key
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=body)
        print(f"Sent message. Exchange: {exchange}, Routing Key: {routing_key}, Body: {body}")

    def close(self):
        self.channel.close()
        self.connection.close()


class HelloWorldReceive(BasicPikaClient):

    def consume_messages(self, queue):
        def callback(ch, method, properties, body):
            print(" [x] 接受 %r" % body)

        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        self.channel.close()
        self.connection.close()
