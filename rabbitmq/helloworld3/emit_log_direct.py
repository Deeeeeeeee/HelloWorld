#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# https://www.rabbitmq.com/tutorials/tutorial-four-python
# 指定 routing_key. info warning error
# 同一个 exchange 和 queue，但不同的 routing_key
#
# python3 emit_log_direct.py info 'Hello World!'
# python3 emit_log_direct.py error 'Run. Run. Or it will run for you.'
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 创建 exchange, 类型为 direct
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
# 指定 routing_key 发消息. info warning error
channel.basic_publish(
    exchange='direct_logs', routing_key=severity, body=message)
print(f" [x] Sent {severity}:{message}")
connection.close()