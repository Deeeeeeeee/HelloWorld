#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 死信交换器
# 这里过期的消息，会自动的发到死信队列中
# https://www.rabbitmq.com/docs/dlx
import os
import sys
import pika
import pika.exchange_type


def new_task():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # 创建死信队列和正常的工作队列
    channel.exchange_declare("exchange.dlx", pika.exchange_type.ExchangeType.direct)
    channel.exchange_declare("exchange.normal", pika.exchange_type.ExchangeType.fanout)

    # 正常的工作队列，绑定死信交换器，并指定死信的 routing key
    # 也设置消息过期时间
    args = {
        "x-dead-letter-exchange": "exchange.dlx",
        "x-dead-letter-routing-key": "dlx.routingkey",
        "x-message-ttl": 5000
    }
    channel.queue_declare("queue.normal", durable=True, arguments=args)
    channel.queue_bind("queue.normal", "exchange.normal", routing_key="")

    # 私信队列，绑定死信交换器，并指定死信的 routing key
    channel.queue_declare("queue.dlx", durable=True)
    channel.queue_bind("queue.dlx", "exchange.dlx", routing_key="dlx.routingkey")

    # 发布消息
    channel.basic_publish("exchange.normal", routing_key="", body="hello world")

    connection.close()


if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        new_task()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)