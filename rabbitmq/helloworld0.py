#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 单个生产者，单个消费者
# https://www.rabbitmq.com/tutorials/tutorial-one-python
import os
import sys
import pika

def send_hello():
    # 建立连接
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # 创建一个 queue
    channel.queue_declare(queue='hello')

    # 不能直接发到 queue，需要通过一个 exchange，空字符串的 exchange 表示默认的 exchange
    # 默认的 exchange 能够直接将消息发送到 queue，但需要指定 routing_key
    # routing_key 为 queue 的名字
    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
    print(" [x] Sent 'Hello World!'")

    # 关闭连接。网络缓存 flushed
    connection.close()


def recv_hello():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    # 接收消息需要回调函数
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    # 告诉rabbitmq，这个回调要接受 hello 这个 queue 的消息
    channel.basic_consume(queue='hello', auto_ack=True, on_message_callback=callback)

    # 开始消费
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        send_hello()
        # recv_hello()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)