#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: similraface
# @contact: similarface@gmail.com
# @software: PyCharm
# @file: client.py
# @time: 2022/6/12 2:58 下午
# @desc:
from main import FibonacciRpcClient

if __name__ == '__main__':
    fibonacci_rpc = FibonacciRpcClient(url="amqp://guest:guest@localhost:5672")

    print(" [x] Requesting fib(30)")
    response = fibonacci_rpc.call(2)
    print(" [.] Got %r" % response)
