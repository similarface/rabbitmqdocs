#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: similraface
# @contact: similarface@gmail.com
# @software: PyCharm
# @file: receive.py
# @time: 2022/6/12 11:26 上午
# @desc:
import sys
from main import Receive

"""
python receive "#"
python receive "kern.*"
python receive "*.critical"
python receive "kern.*" "*.critical"
python receive "kern.critical" "A critical kernel error"
"""
if __name__ == '__main__':
    exchange_name = "topic_logs"
    exchange_type = "topic"
    binding_keys = sys.argv[1:]
    receiver = Receive(url="amqp://guest:guest@localhost:5672")
    receiver.consume_topics(exchange=exchange_name,
                            exchange_type=exchange_type,
                            binding_keys=binding_keys)
