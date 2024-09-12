#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# https://www.rabbitmq.com/tutorials/tutorial-two-python
# 先运行两个 worker. 即 python helloworld1.py 两次
# 然后运行 new_task. python3 helloworld1.py First message.
import os
import sys
import time
import pika


def new_task():
    # 建立连接
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # 创建一个 queue
    channel.queue_declare(queue='hello')

    message = ' '.join(sys.argv[1:]) or "Hello World!"
    channel.basic_publish(exchange='', routing_key='hello', body=message)
    print(" [x] Sent {message}")


def worker():
    """
    auto_ack 收到消息会直接 ack
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %s" % body.decode())
        time.sleep(body.count(b'.'))
        print(" [x] Done")

    # 告诉rabbitmq，这个回调要接受 hello 这个 queue 的消息
    channel.basic_consume(queue='hello', auto_ack=True, on_message_callback=callback)

    # 开始消费
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def worker2():
    """
    主动 ack，如果没 ack 宕机了，消息还在
    通过命令查看 sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %s" % body.decode())
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        # 主动确认
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # 不用 auto_ack
    channel.basic_consume(queue='hello', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    try:
        new_task()
        # worker()
        # worker2()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)