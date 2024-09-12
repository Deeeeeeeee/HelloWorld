#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# https://www.rabbitmq.com/tutorials/tutorial-five-python
# topic. * 匹配一个单词，# 匹配0个或者多个单词
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 创建 exchange, type 使用 topic
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
# 指定 routing_key 去发送
channel.basic_publish(
    exchange='topic_logs', routing_key=routing_key, body=message)
print(f" [x] Sent {routing_key}:{message}")
connection.close()