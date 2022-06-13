#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: similraface
# @contact: similarface@gmail.com
# @software: PyCharm
# @file: worker.py
# @time: 2022/6/11 9:21 下午
# @desc:
from workqueues import WorkQueuesReceive

if __name__ == '__main__':

    worker = WorkQueuesReceive(url="amqp://guest:guest@localhost:5672")
    queue_name = "task_queue"
    worker.consume_messages(queue=queue_name)
