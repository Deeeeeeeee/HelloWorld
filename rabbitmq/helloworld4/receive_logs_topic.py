#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# https://www.rabbitmq.com/tutorials/tutorial-five-python
# topic. * 匹配一个单词，# 匹配0个或者多个单词
#
# 执行脚本 ./receive_logs_topic.py 1 或者 2
import os
import pika
import sys


def worker():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # 创建 exchange, type 使用 topic
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    # 临时队列
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    binding_keys = sys.argv[1:]
    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
        sys.exit(1)

    # 指定 routing_key 绑定
    for binding_key in binding_keys:
        channel.queue_bind(
            exchange='topic_logs', queue=queue_name, routing_key=binding_key)

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