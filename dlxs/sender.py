#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: similraface
# @contact: similarface@gmail.com
# @software: PyCharm
# @file: sender.py
# @time: 2022/6/12 7:18 下午
# @desc:

"""
Producer ---> exchange.normal+fanout---> quenue.normal
                                                      \_dlx__> exchange.dlx+direct--->quene.dlx
"""
import json
import time

import pika

from main import Sender

if __name__ == '__main__':
    sender = Sender(url="amqp://guest:guest@localhost:5672")

    # 正常交换机
    exchange_normal = "exchange_normal"
    # 正常队列
    quenue_normal = "quenue_normal"
    # 正常路由
    routing_key = "routing_normal"

    # 死信交换机
    exchange_dlx = "exchange.dlx"
    # 死信队列
    quenue_dlx = "dead_letter_queue"
    dead_letter_routing_key = "dead_letter_routing_key_a"

    arguments = {
        "x-message-ttl": 5000,
        "x-dead-letter-exchange": exchange_dlx,
        "x-dead-letter-routing-key": dead_letter_routing_key
    }

    sender.channel.confirm_delivery()

    sender.channel.exchange_declare(exchange=exchange_normal, durable=True, exchange_type="direct")
    result = sender.channel.queue_declare(queue=quenue_normal, durable=False, arguments=arguments)
    sender.channel.queue_bind(exchange=exchange_normal, queue=quenue_normal, routing_key=routing_key)

    for i in range(10):
        message = json.dumps({"OrderId": i})
        sender.channel.basic_publish(exchange=exchange_normal,
                                     routing_key=routing_key,
                                     body=message,
                                     properties=pika.BasicProperties(delivery_mode=2)
                                     )
        print(message)
        time.sleep(1.5)
    sender.close()
