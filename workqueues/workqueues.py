#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: similraface
# @contact: similarface@gmail.com
# @software: PyCharm
# @file: workqueues.py
# @time: 2022/6/11 9:00 下午
# @desc:
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import time

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


class WorkQueuesSender(BasicPikaClient):
    def declare_queue(self, queue, durable=False):
        """
        :param queue: 队列名称
        :param durable:设置是否持久化， true 设置队列持久化，持久化会存盘重启后不丢失信息
        :return:
        """
        print(f"定义队列： ({queue})...")
        self.channel.queue_declare(queue=queue, durable=durable)

    def send_message(self, exchange, routing_key, body, properties=None):
        """
        :param exchange: 交换机
        :param routing_key: 路由key
        :param body:  消息
        :param properties: 消息的基本属性
        :return:
        """
        # 获取信道
        channel = self.connection.channel()
        # 信道 ----> 交换机---路由key
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=body,
                              properties=properties)
        print(f"Sent message. Exchange: {exchange}, Routing Key: {routing_key}, Body: {body}")

    def close(self):
        self.channel.close()
        self.connection.close()


class WorkQueuesReceive(BasicPikaClient):

    def consume_messages(self, queue):
        self.channel.queue_declare(queue=queue, durable=True)

        def callback(ch, method, properties, body):
            """
            :param ch:  BlockingChannel
            :param method: spec.Basic.Deliver
            :param properties: spec.BasicProperties
            :param body:
            :return:
            """
            print(" [x] 接受 %r" % body)
            time.sleep(body.count(b'.'))
            print(" [X] Done")
            # basic_ack确认一条或多条消息
            # delivery_tag是消息投递序号，每个channel对应一个(long类型)，从1开始到9223372036854775807范围，在手动消息确认时可以对指定delivery_tag的消息进行ack、nack、reject等操作。
            # method.delivery_tag 会+1递增【队列】
            ch.basic_ack(delivery_tag=method.delivery_tag)

        # channel.basicQos(1)指该消费者在接收到队列里的消息但没有返回确认结果之前,
        # 队列不会将新的消息分发给该消费者。队列中没有被消费的消息不会被删除，还是存在于队列中。
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue, on_message_callback=callback)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        self.channel.close()
        self.connection.close()
