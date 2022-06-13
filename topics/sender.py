#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: similraface
# @contact: similarface@gmail.com
# @software: PyCharm
# @file: sender.py
# @time: 2022/6/12 11:22 上午
# @desc:
import sys
import random
from main import Sender

""""
kern.critical
kern.A
A.critical
A.B

"""
if __name__ == '__main__':
    messages = {"kern.critical": "kern.critical message",
                "kern.A": "kern.A message",
                "A.critical": "A.critical message",
                "A.B": "A.B message", }
    severity = random.choice(list(messages.keys()))
    message = messages[severity]

    exchange_name = 'topic_logs'
    exchange_type = 'topic'

    routing_key = severity
    sender = Sender(url="amqp://guest:guest@localhost:5672")
    sender.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
    sender.send_message(
        exchange=exchange_name,
        routing_key=routing_key,
        body=message
    )
    print(" [x] Sent %r:%r" % (routing_key, message))
    sender.close()
