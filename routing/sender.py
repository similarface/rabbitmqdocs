#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: similraface
# @contact: similarface@gmail.com
# @software: PyCharm
# @file: sneder.py
# @time: 2022/6/12 10:43 上午
# @desc:
import random

from main import Sender

"""
P ------> E(direct_logs)______> error ______> C1
                        \_____> error ______> C2
                        \_____> info  ______> C2
                        \_____> warning ____> C2
                        \_____> debug ______> C2
"""
if __name__ == '__main__':
    messages = {"debug": "debug log",
                "error": "error log",
                "info": "info log",
                "warning": "warning log"}
    severity = random.choice(list(messages.keys()))
    message = messages[severity]

    sender = Sender(url="amqp://guest:guest@localhost:5672/")
    sender.send_message(
        exchange="direct_logs",
        routing_key=severity,
        body=message,
        properties=None
    )
    print(" [x] Sent %r:%r" % (severity, message))
    sender.close()
