#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: similraface
# @contact: similarface@gmail.com
# @software: PyCharm
# @file: receive.py
# @time: 2022/6/12 8:43 下午
# @desc:
import json

from main import Receive

if __name__ == '__main__':
    receiver = Receive(url="amqp://guest:guest@localhost:5672")
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

    receiver.channel.exchange_declare(exchange=exchange_dlx,
                                      durable=True,
                                      exchange_type="direct"
                                      )
    result = receiver.channel.queue_declare(queue=quenue_normal, durable=False)

    receiver.channel.queue_bind(exchange=exchange_dlx,
                                queue=quenue_dlx,
                                routing_key=dead_letter_routing_key)


    def callback(ch, method, properties, body):
        data = json.loads(body.decode())

        ch.basic_ack(delivery_tag=method.delivery_tag)


    receiver.channel.basic_consume(quenue_dlx, callback, auto_ack=False)

    receiver.channel.start_consuming()
