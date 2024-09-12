#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 过期时间
# 分为消息过期和队列过期
# 
# 消息过期有
# 1. 每条消息过期 x-message-ttl
# 2. 指定消息过期 expiration
#
# 队列过期 x-expires
# https://www.rabbitmq.com/docs/ttl#per-queue-message-ttl
import os
import sys
import pika


def message_ttl_x_arguments():
    """
    x-message-ttl 设置队列消息的过期时间
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # 设置队列消息过期时间。单位：毫秒
    channel.queue_declare(queue='message-ttl-x-arguments',
                          arguments={'x-message-ttl': 5000},
                          durable=True)

    channel.basic_publish(exchange='',
                         routing_key='message-ttl-x-arguments',
                         body='hello world!')
    print(' [x] Sent "hello world!"')

    connection.close()


def expiration():
    """
    expiration 指定消息过期时间
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='message-ttl-expiration',
                          durable=True)

    # 设置单独消息过期时间。单位：毫秒
    channel.basic_publish(exchange='',
                         routing_key='message-ttl-expiration',
                         body='hello world!',
                         properties=pika.BasicProperties(expiration='5000'))

    # 如果设置0，如果没有立即消费，则直接丢弃. 但队列中不会直接抹去，在即将投递的时候判断是否过期
    channel.basic_publish(exchange='',
                         routing_key='message-ttl-expiration',
                         body='hello world!',
                         properties=pika.BasicProperties(expiration='0'))
    print(' [x] Sent "hello world!"')

    connection.close()


def queue_expires():
    """
    x-expires 设置队列的 TTL
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # 队列的过期时间
    channel.queue_declare(queue='queue-ttl-expires',
                          durable=True,
                          arguments={'x-expires': 5000})

    channel.basic_publish(exchange='',
                         routing_key='queue-ttl-expires',
                         body='hello world!')
    print(' [x] Sent "hello world!"')

    connection.close()


if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        if args[0] == '1':
            message_ttl_x_arguments()
        elif args[0] == '2':
            expiration()
        elif args[0] == '3':
            queue_expires()
        else:
            print('Usage: %s worker|new_task' % sys.argv[0])
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)