#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: similraface
# @contact: similarface@gmail.com
# @software: PyCharm
# @file: sender.py
# @time: 2022/6/12 9:37 上午
# @desc:
import random
from rabbitmqdocs.publishsubscribe.main import Sender

if __name__ == '__main__':
    sender = Sender(url="amqp://guest:guest@localhost:5672/")
    exchange_name = "logs"
    message = f"Work Queues Send... {random.randint(1, 100)}"
    sender.exchange_declare(exchange=exchange_name, exchange_type="fanout")
    sender.send_message(
        exchange=exchange_name, routing_key='', body=message, properties=None
    )
