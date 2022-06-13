#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: similraface
# @contact: similarface@gmail.com
# @software: PyCharm
# @file: server.py
# @time: 2022/6/12 2:57 下午
# @desc:

from main import Server


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


if __name__ == '__main__':
    queue = 'rpc_queue'
    server = Server(url="amqp://guest:guest@localhost:5672")
    server.declare_queue(queue=queue)
    server.publish_server(
        exchange='',
        queue='rpc_queue',
        callback=fib
    )
