#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: similraface
# @contact: similarface@gmail.com
# @software: PyCharm
# @file: receive.py
# @time: 2022/6/12 9:37 上午
# @desc:


from main import Receive

if __name__ == '__main__':
    exchange_name = "logs"
    receiver = Receive(url="amqp://guest:guest@localhost:5672/")
    receiver.subscribe(exchange=exchange_name)
