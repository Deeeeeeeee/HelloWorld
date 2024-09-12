#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# https://www.rabbitmq.com/tutorials/tutorial-two-python
# 持久化，主动ack，公平分发
import pika
import sys

if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # 持久化. 原来不是持久化的队列，现在变成持久化会报错
    channel.queue_declare(queue='task_queue', durable=True)

    message = ' '.join(sys.argv[1:]) or "Hello World!"
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent
        ))
    print(f" [x] Sent {message}")
    connection.close()