#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: similraface
# @contact: similarface@gmail.com
# @software: PyCharm
# @file: main.py
# @time: 2022/6/11 9:00 下午
# @desc:
"""

"""
import sys
import time

import pika
from pika.exchange_type import ExchangeType


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


class Sender(BasicPikaClient):
    def declare_queue(self, queue, durable=False, exclusive=False,arguments=None):
        """
        :param queue: 队列名称
        :param durable:设置是否持久化， true 设置队列持久化，持久化会存盘重启后不丢失信息
        :param exclusive:设置是否排他。为 true 则设置队列为排他的。如果一个队列被声明为排
                        他队列，该队列仅对首次声明它的连接可见，并在连接断开时自动删除。这里需要注意
                        三点:排他队列是基于连接( Connection) 可见的，同个连接的不同信道 (Channel)
                        是可以同时访问同一连接创建的排他队列; "首次"是指如果 个连接己经声明了
                        排他队列，其他连接是不允许建立同名的排他队列的，这个与普通队列不同:即使该队
                        列是持久化的，一旦连接关闭或者客户端退出，该排他队列都会被自动删除，这种队列
                        适用于一个客户端同时发送和读取消息的应用场景。
        :param arguments
        :return:
        """
        print(f"定义队列： ({queue})...")
        self.channel.queue_declare(queue=queue, durable=durable, exclusive=exclusive,arguments=arguments)

    def exchange_declare(self, exchange,
                         exchange_type=ExchangeType.direct,
                         passive=False,
                         durable=False,
                         auto_delete=False,
                         internal=False,
                         arguments=None):
        """
        :param exchange: 交换机名称
        :param exchange_type: 默认direct
        :param passive=False 执行声明或仅检查是否存在,
        如果设置为被动，则服务器将在exchange已存在同名，
        如果不存在，则引发错误，如果exchange不存在，
        服务器必须引发通道回复代码404异常（未找到）。
        :param durable=设置是否持久化,
        :param auto_delete=设置是否自动删除,
        :param internal=设置是否内置的,true- 交换机到交换机
        :param arguments=TODO？
        :return:
        """
        self.channel.exchange_declare(exchange,
                                      exchange_type=exchange_type,
                                      passive=passive,
                                      durable=durable,
                                      auto_delete=auto_delete,
                                      internal=internal,
                                      arguments=arguments)

    def send_message(self,
                     exchange,
                     routing_key,
                     body,
                     properties=None):
        """
        :param exchange: 交换机
        :param routing_key: 路由key
        :param body:  消息
        :param properties: 消息的基本属性
        :return:
        """
        # 信道 ----> 交换机---路由key
        self.channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=body,
                              properties=properties)
        print(f"Sent message. Exchange: {exchange}, Routing Key: {routing_key}, Body: {body}")

    def close(self):
        self.channel.close()
        self.connection.close()


class Receive(BasicPikaClient):

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

    def consume_subscribe(self, exchange=None):
        """
        广播方式消费
        :param exchange: 交换机名称
        :return:
        """
        # self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        print(f"queue_name: {queue_name}")
        self.channel.queue_bind(exchange=exchange, queue=queue_name)
        print(' [*] Waiting for logs. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print(" [x] %r" % body)

        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def consume_routing(self,
                        exchange=None,
                        exchange_type=None,
                        routing_keys=None):
        self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        for routing_key in routing_keys:
            self.channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)
        print(' [*] Waiting for logs. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print(" [x] %r:%r" % (method.routing_key, body))

        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def consume_topics(self, exchange, exchange_type, binding_keys=None):
        self.channel.exchange_declare(exchange=exchange,
                                      exchange_type=exchange_type)
        result = self.channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        if not binding_keys:
            sys.stderr.write("binding_keys must be list")
            sys.exit(1)
        for binding_key in binding_keys:
            self.channel.queue_bind(
                exchange=exchange, queue=queue_name, routing_key=binding_key)
        print(' [*] Waiting for logs. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print(" [x] %r:%r" % (method.routing_key, body))

        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        self.channel.start_consuming()

    def close(self):
        self.channel.close()
        self.connection.close()
