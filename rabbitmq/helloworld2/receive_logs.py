#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# https://www.rabbitmq.com/tutorials/tutorial-three-python
# 绑定 exchange, 临时exclusive队列, fanout 发给所有队列
# 执行多次 python3 receive_logs.py。所有队列都能收到消息
import os
import sys
import pika


def worker():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # 创建 exchange. fanout类型会发给所有队列
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    # 创建队列. 队列名称是随机生成的. 例如 amq.gen-vX1lknI15GadLbDggvUdwg
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # 绑定 exchange, 队列
    channel.queue_bind(exchange='logs', queue=queue_name)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(f" [x] {body}")

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