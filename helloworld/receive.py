#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: similraface
# @contact: similarface@gmail.com
# @software: PyCharm
# @file: receive.py
# @time: 2022/6/11 8:23 下午
# @desc:

from helloworld import HelloWorldReceive

if __name__ == '__main__':
    url = 'amqp://guest:guest@localhost:5672'
    receiver = HelloWorldReceive(url=url)
    queue_name = 'hello'
    receiver.consume_messages(queue=queue_name)
