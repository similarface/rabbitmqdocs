#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: similraface
# @contact: similarface@gmail.com
# @software: PyCharm
# @file: send.py
# @time: 2022/6/11 9:02 下午
# @desc:
import pika
import random
from rabbitmqdocs import URL
from workqueues import WorkQueuesSender

if __name__ == '__main__':
    queue_name = 'task_queue'
    message = f"Work Queues Send... {random.randint(1,100)}"
    sender = WorkQueuesSender(url=URL)
    sender.declare_queue(queue=queue_name, durable=True)
    sender.send_message(
        exchange='',
        routing_key='task_queue',
        body=message,
        # 持续交付模式
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
    )
    print(" [x] Sent %r" % message)
    sender.close()
