#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Stream 只能添加日志，可以重复读，直到过期
import pika


STREAM_NAME = "hello-python-stream"
# 5GB
STREAM_RETENTION = 5000000000


def new_task():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # x-queue-type 指定队列为 stream
    # x-max-length-bytes 限制队列大小，后续无法修改
    args = {
        "x-queue-type": "stream",
        "x-max-length-bytes": STREAM_RETENTION
    }
    channel.queue_declare(STREAM_NAME, durable=True, arguments=args)

    channel.basic_publish("", routing_key=STREAM_NAME, body=b"Hello World!",
                          properties=pika.BasicProperties(headers={"x-stream-filter-value": "california"}))

    connection.close()


if __name__ == "__main__":
    new_task()