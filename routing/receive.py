#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: similraface
# @contact: similarface@gmail.com
# @software: PyCharm
# @file: receive.py
# @time: 2022/6/12 10:43 上午
# @desc:
"""
P ------> E(direct_logs)______> error ______> C1
                        \_____> error ______> C2
                        \_____> info  ______> C2
                        \_____> warning ____> C2
                        \_____> debug ______> C2
"""
import sys
from main import Receive

if __name__ == '__main__':
    exchange = "direct_logs"
    exchange_type = "direct"
    severities = sys.argv[1:]
    if not severities:
        sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
        sys.exit(1)
    print(f"severities: ------> {severities}")
    receiver = Receive(url="amqp://guest:guest@localhost:5672/")
    receiver.consume_routing(exchange=exchange, exchange_type=exchange_type,routing_keys=severities)

