#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# https://www.rabbitmq.com/tutorials/tutorial-four-python
# 指定 routing_key. info warning error
# 同一个 exchange 和 queue，但不同的 routing_key
#
# 分别执行下面，用不同的 routing_key
# python3 receive_logs_direct.py info warning error
# python3 receive_logs_direct.py error
import os
import pika
import sys

def worker():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # 创建 exchange, type 为 direct
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    # 临时队列
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    severities = sys.argv[1:]
    if not severities:
        sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
        sys.exit(1)

    # 绑定 exchange 到同一个队列，但可以不同的 routing_key
    for severity in severities:
        channel.queue_bind(
            exchange='direct_logs', queue=queue_name, routing_key=severity)

    print(' [*] Waiting for logs. To exit press CTRL+C')


    def callback(ch, method, properties, body):
        print(f" [x] {method.routing_key}:{body}")


    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    try:
        worker()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)