#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
import sys
import time
import pika
import pika.delivery_mode


def new_task():
    # 建立连接
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # 创建一个 queue
    channel.queue_declare(queue='test', durable=True)

    message = ' '.join(sys.argv[1:]) or "Hello World!"
    channel.basic_publish(exchange='', routing_key='test', body=message,
                          properties=pika.BasicProperties(delivery_mode=pika.delivery_mode.DeliveryMode.Persistent))
    print(" [x] Sent {message}")




if __name__ == "__main__":
    try:
        new_task()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)