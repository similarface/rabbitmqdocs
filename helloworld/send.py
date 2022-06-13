#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: similraface
# @contact: similarface@gmail.com
# @software: PyCharm
# @file: receive.py
# @time: 2022/6/11 8:23 下午
# @desc:

from helloworld import HelloWorldSender

if __name__ == '__main__':
    url = "amqp://guest:guest@localhost:5672/"
    sender = HelloWorldSender(url=url)
    queue_name = "hello"
    sender.declare_queue(queue_name)
    sender.send_message(exchange='', routing_key='hello', body='hello world!')
    sender.close()
