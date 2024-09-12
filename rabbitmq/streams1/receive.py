#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Stream 只能添加日志，可以重复读，直到过期
# https://www.rabbitmq.com/docs/streams
import os
import sys
import pika


STREAM_NAME = "hello-python-stream"
# 5GB
STREAM_RETENTION = 5000000000


def worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # x-queue-type 指定队列为 stream
    # x-max-length-bytes 限制队列大小，后续无法修改
    args = {
        "x-queue-type": "stream",
        "x-max-length-bytes": STREAM_RETENTION
    }
    channel.queue_declare(STREAM_NAME, durable=True, arguments=args)

    def callback(ch, method, properties, body):
        print(f"Received {body}")
        ch.basic_ack(delivery_tag=method.delivery_tag, multiple=False)

    # QoS 必须指定
    channel.basic_qos(prefetch_count=100)
    # 指定偏移量. first, last, next, 具体的offset, 时间戳, interval
    args1 = {"x-stream-offset": "first"}
    channel.basic_consume(STREAM_NAME, callback, auto_ack=False, arguments=args1)

    print("Waiting for messages...")
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